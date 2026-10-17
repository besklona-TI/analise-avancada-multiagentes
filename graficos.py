from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter


PASTA = Path(__file__).resolve().parent
ARQUIVO_ENTRADA = PASTA / "papelaria_limpa.csv"


def formatar_reais(valor: float) -> str:
    """Formata um número no padrão monetário brasileiro."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def criar_grafico_vendas(
    totais: pd.Series,
    dimensao: str,
    titulo: str,
    arquivo_saida: str,
) -> None:
    fig, ax = plt.subplots(figsize=(9, 5.5))
    barras = ax.bar(totais.index.astype(str), totais.values, color="#4C78A8")

    ax.set_title(titulo)
    ax.set_xlabel(dimensao)
    ax.set_ylabel("Valor vendido (R$)")
    ax.set_ylim(bottom=0)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda valor, _: formatar_reais(valor)))
    ax.bar_label(
        barras,
        labels=[formatar_reais(valor) for valor in totais.values],
        padding=4,
        fontsize=9,
    )
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(PASTA / arquivo_saida, dpi=160, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    dados = pd.read_csv(ARQUIVO_ENTRADA, encoding="utf-8-sig")
    dados["valor_venda"] = pd.to_numeric(dados["valor_venda"], errors="raise")

    total_categoria = dados.groupby("categoria")["valor_venda"].sum().sort_values(
        ascending=False
    )
    total_cidade = dados.groupby("cidade")["valor_venda"].sum().sort_values(
        ascending=False
    )

    criar_grafico_vendas(
        total_categoria,
        dimensao="Categoria",
        titulo="Valor total vendido por categoria",
        arquivo_saida="categorias.png",
    )
    criar_grafico_vendas(
        total_cidade,
        dimensao="Cidade",
        titulo="Valor total vendido por cidade",
        arquivo_saida="cidades.png",
    )

    print("Totais vendidos por categoria:")
    print(total_categoria.to_string())
    print("\nTotais vendidos por cidade:")
    print(total_cidade.to_string())
    print("\nGráficos salvos em categorias.png e cidades.png.")


if __name__ == "__main__":
    main()
