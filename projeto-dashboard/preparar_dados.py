"""Valida papelaria_limpa.csv e gera o JSON consumido pelo site estático."""

from __future__ import annotations

import json
import math
from decimal import Decimal
from pathlib import Path

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parent
SOURCE_FILE = PROJECT_DIR.parent / "papelaria_limpa.csv"
OUTPUT_FILE = PROJECT_DIR / "site" / "dados" / "vendas.json"

EXPECTED_COLUMNS = [
    "id_venda",
    "data",
    "cidade",
    "categoria",
    "produto",
    "quantidade",
    "preco_unitario",
    "forma_pagamento",
    "valor_venda",
]
TEXT_COLUMNS = [
    "id_venda",
    "cidade",
    "categoria",
    "produto",
    "forma_pagamento",
]
NUMERIC_COLUMNS = ("quantidade", "preco_unitario", "valor_venda")


def prepare() -> int:
    """Validate the confirmed cleaned input and write the static site data."""
    if not SOURCE_FILE.is_file():
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {SOURCE_FILE}")

    # Preserve identifiers and labels as text instead of relying on inference.
    frame = pd.read_csv(
        SOURCE_FILE,
        encoding="utf-8",
        dtype={column: "string" for column in TEXT_COLUMNS},
    )
    if list(frame.columns) != EXPECTED_COLUMNS:
        raise ValueError(
            "Colunas inesperadas em papelaria_limpa.csv. "
            f"Esperadas: {EXPECTED_COLUMNS}; recebidas: {list(frame.columns)}"
        )
    if frame.empty:
        raise ValueError("A fonte não contém linhas de venda.")
    if frame.isna().any().any():
        missing = frame.columns[frame.isna().any()].tolist()
        raise ValueError(f"Há valores ausentes na fonte limpa: {missing}")
    blank_text = [
        column
        for column in TEXT_COLUMNS
        if frame[column].str.strip().eq("").any()
    ]
    if blank_text:
        raise ValueError(f"Há campos de texto vazios na fonte limpa: {blank_text}")
    if frame["id_venda"].duplicated().any():
        raise ValueError("id_venda deve identificar cada linha/venda desta fonte.")
    if frame.duplicated().any():
        raise ValueError("A fonte limpa contém linhas completamente duplicadas.")

    frame["data"] = pd.to_datetime(frame["data"], format="%Y-%m-%d", errors="raise")
    for column in NUMERIC_COLUMNS:
        frame[column] = pd.to_numeric(frame[column], errors="raise")
        if not frame[column].map(math.isfinite).all():
            raise ValueError(f"A coluna {column} contém valor não finito.")
    if (frame["quantidade"] <= 0).any() or (frame["quantidade"] % 1 != 0).any():
        raise ValueError("Quantidade deve ser um número inteiro positivo.")
    if (frame["preco_unitario"] <= 0).any() or (frame["valor_venda"] <= 0).any():
        raise ValueError("Preço unitário e valor da venda devem ser positivos.")

    # Confere o campo calculado previamente, sem reescrever nem alterar a fonte.
    for row in frame[["quantidade", "preco_unitario", "valor_venda"]].itertuples(
        index=False, name=None
    ):
        quantity, unit_price, sale_value = row
        expected = Decimal(str(int(quantity))) * Decimal(str(unit_price))
        if expected != Decimal(str(sale_value)):
            raise ValueError(
                "valor_venda diferente de quantidade × preco_unitario "
                f"(esperado {expected}, recebido {sale_value})."
            )

    # O formato ISO mantém datas portáveis; os demais campos preservam os valores.
    output_records = []
    for record in frame.to_dict(orient="records"):
        record["data"] = record["data"].strftime("%Y-%m-%d")
        record["quantidade"] = int(record["quantidade"])
        record["preco_unitario"] = float(record["preco_unitario"])
        record["valor_venda"] = float(record["valor_venda"])
        output_records.append(record)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", encoding="utf-8", newline="\n") as output:
        json.dump(output_records, output, ensure_ascii=False, indent=2, allow_nan=False)
        output.write("\n")

    total = sum(Decimal(str(record["valor_venda"])) for record in output_records)
    units = sum(record["quantidade"] for record in output_records)
    print(f"Preparação concluída: {len(output_records)} vendas.")
    print(f"Total vendido: R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    print(f"Unidades vendidas: {units}")
    print("Totais por categoria:")
    for label, amount in sorted(
        _totals_by(output_records, "categoria").items(), key=lambda item: item[1], reverse=True
    ):
        print(f"  {label}: R$ {amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    print("Totais por cidade:")
    for label, amount in sorted(
        _totals_by(output_records, "cidade").items(), key=lambda item: item[1], reverse=True
    ):
        print(f"  {label}: R$ {amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    print(f"Arquivo gerado: {OUTPUT_FILE}")
    return len(output_records)


def _totals_by(records: list[dict], column: str) -> dict[str, Decimal]:
    totals: dict[str, Decimal] = {}
    for record in records:
        label = record[column]
        totals[label] = totals.get(label, Decimal("0")) + Decimal(str(record["valor_venda"]))
    return totals


if __name__ == "__main__":
    prepare()
