"""Independent data-contract and rendered-dashboard audit by the Tester."""

from __future__ import annotations

import csv
import hashlib
import json
import threading
import unittest
from collections import defaultdict
from decimal import Decimal
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = PROJECT_DIR.parent
SOURCE = REPO_DIR / "papelaria_limpa.csv"
ORIGINAL = REPO_DIR / "vendas_papelaria.csv"
SITE_DIR = PROJECT_DIR / "site"
DATA_FILE = SITE_DIR / "dados" / "vendas.json"
EXPECTED_COLUMNS = [
    "id_venda", "data", "cidade", "categoria", "produto", "quantidade",
    "preco_unitario", "forma_pagamento", "valor_venda",
]
EXPECTED_SOURCE_SHA256 = "36d3a6607c75d6a3e22146469f43d3bfd4dae85b0d60c99019a510f723f84d2b"
EXPECTED_ORIGINAL_SHA256 = "bf95b7609e30eb7e3e6a30cfc16e43d9fb5bdfc48a410e49148cceb92e2494ff"


def currency(value: Decimal, page: Any) -> str:
    return page.evaluate(
        "value => new Intl.NumberFormat('pt-BR', {style:'currency',currency:'BRL'}).format(value)",
        float(value),
    )


def integer(value: int, page: Any) -> str:
    return page.evaluate(
        "value => new Intl.NumberFormat('pt-BR', {maximumFractionDigits:0}).format(value)",
        value,
    )


def grouped_totals(rows: list[dict[str, Any]], column: str) -> dict[str, Decimal]:
    result: defaultdict[str, Decimal] = defaultdict(Decimal)
    for row in rows:
        result[str(row[column])] += Decimal(str(row["valor_venda"]))
    return dict(result)


class IndependentInputAuditTests(unittest.TestCase):
    def test_csv_hash_schema_types_missing_values_and_duplicate_policy(self) -> None:
        self.assertEqual(EXPECTED_SOURCE_SHA256, hashlib.sha256(SOURCE.read_bytes()).hexdigest())
        self.assertEqual(EXPECTED_ORIGINAL_SHA256, hashlib.sha256(ORIGINAL.read_bytes()).hexdigest())

        source = pd.read_csv(SOURCE, encoding="utf-8")
        self.assertEqual(EXPECTED_COLUMNS, list(source.columns))
        self.assertEqual((180, 9), source.shape)
        self.assertEqual(0, int(source.isna().sum().sum()))
        self.assertEqual("int64", str(source["quantidade"].dtype))
        self.assertEqual("float64", str(source["preco_unitario"].dtype))
        self.assertEqual("float64", str(source["valor_venda"].dtype))
        for column in set(EXPECTED_COLUMNS) - {"quantidade", "preco_unitario", "valor_venda"}:
            self.assertTrue(pd.api.types.is_string_dtype(source[column].dtype), column)
        self.assertFalse(source["id_venda"].duplicated().any())
        self.assertFalse(source.duplicated().any())

        with ORIGINAL.open("r", encoding="utf-8-sig", newline="") as stream:
            original_rows = list(csv.DictReader(stream))
        original_duplicates = len(original_rows) - len(
            {tuple(row[column] for column in original_rows[0]) for row in original_rows}
        )
        self.assertEqual(182, len(original_rows))
        self.assertEqual(2, original_duplicates)
        self.assertEqual(180, len(source))  # documented clean source omits only exact copies

    def test_json_prepared_values_reconcile_independently_to_source(self) -> None:
        with SOURCE.open("r", encoding="utf-8-sig", newline="") as stream:
            source_rows = list(csv.DictReader(stream))
        prepared = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        self.assertEqual(len(source_rows), len(prepared))
        self.assertEqual(
            [row["id_venda"] for row in source_rows],
            [row["id_venda"] for row in prepared],
        )
        for source_row, actual in zip(source_rows, prepared, strict=True):
            self.assertEqual(EXPECTED_COLUMNS, list(actual))
            self.assertIsInstance(actual["id_venda"], str)
            self.assertIsInstance(actual["quantidade"], int)
            self.assertIsInstance(actual["preco_unitario"], (int, float))
            self.assertIsInstance(actual["valor_venda"], (int, float))
            for column in set(EXPECTED_COLUMNS) - {"quantidade", "preco_unitario", "valor_venda"}:
                self.assertEqual(source_row[column], actual[column], (actual["id_venda"], column))
            self.assertEqual(int(source_row["quantidade"]), actual["quantidade"])
            self.assertEqual(Decimal(source_row["preco_unitario"]), Decimal(str(actual["preco_unitario"])))
            self.assertEqual(Decimal(source_row["valor_venda"]), Decimal(str(actual["valor_venda"])))


class RenderedDashboardAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        try:
            from playwright.sync_api import sync_playwright  # noqa: F401
        except ImportError as exc:
            raise unittest.SkipTest(f"PENDENTE: Playwright indisponível: {exc}")
        handler = lambda *args, **kwargs: SimpleHTTPRequestHandler(
            *args, directory=str(SITE_DIR), **kwargs
        )
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls) -> None:
        if hasattr(cls, "server"):
            cls.server.shutdown()
            cls.server.server_close()
            cls.server_thread.join(timeout=3)

    def test_kpis_charts_table_filters_empty_state_keyboard_and_viewports(self) -> None:
        from playwright.sync_api import sync_playwright

        all_rows = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        page_errors: list[str] = []
        failed_responses: list[str] = []
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            page.on("pageerror", lambda error: page_errors.append(str(error)))
            page.on(
                "console",
                lambda message: page_errors.append(message.text) if message.type == "error" else None,
            )
            page.on("response", lambda response: failed_responses.append(response.url) if response.status >= 400 else None)
            page.goto(self.base_url + "/", wait_until="networkidle")

            def check_rendered(rows: list[dict[str, Any]]) -> None:
                total = sum((Decimal(str(row["valor_venda"])) for row in rows), Decimal("0"))
                count = len(rows)
                average = total / count if count else Decimal("0")
                self.assertEqual(currency(total, page), page.locator("#kpi-total").inner_text())
                self.assertEqual(f"{count:,}".replace(",", "."), page.locator("#kpi-count").inner_text())
                self.assertEqual(currency(average, page), page.locator("#kpi-average").inner_text())

                for selector, column in (("#chart-category", "categoria"), ("#chart-city", "cidade")):
                    expected = grouped_totals(rows, column)
                    actual = {}
                    for item in page.locator(f"{selector} .bar-row").all():
                        label = item.locator(".bar-label").inner_text()
                        label_amount = item.locator(".bar-value").inner_text()
                        self.assertIn(label, expected)
                        self.assertEqual(currency(expected[label], page), label_amount)
                        actual[label] = expected[label]
                    self.assertEqual(expected, actual)

                displayed_rows = page.locator("#sales-rows tr").all()
                self.assertEqual(len(rows), len(displayed_rows))
                for sale, displayed in zip(rows, displayed_rows, strict=True):
                    year, month, day = str(sale["data"]).split("-")
                    expected_cells = [
                        f"{day}/{month}/{year}",
                        str(sale["id_venda"]),
                        str(sale["cidade"]),
                        str(sale["categoria"]),
                        str(sale["produto"]),
                        integer(int(sale["quantidade"]), page),
                        currency(Decimal(str(sale["preco_unitario"])), page),
                        str(sale["forma_pagamento"]),
                        currency(Decimal(str(sale["valor_venda"])), page),
                    ]
                    self.assertEqual(
                        expected_cells,
                        displayed.locator("td").all_text_contents(),
                        f"Tabela divergente para id_venda={sale['id_venda']}",
                    )
                if not rows:
                    self.assertTrue(page.locator("#empty-message").is_visible())
                    self.assertFalse(page.locator("#table-wrap").is_visible())
                else:
                    self.assertFalse(page.locator("#empty-message").is_visible())
                self.assertNotRegex(page.locator("body").inner_text(), r"\bNaN\b|\bInfinity\b")

            check_rendered(all_rows)
            categories = sorted({row["categoria"] for row in all_rows})
            cities = sorted({row["cidade"] for row in all_rows})
            for category in categories:
                page.locator("#filter-category").select_option(label=category)
                check_rendered([row for row in all_rows if row["categoria"] == category])
            page.locator("#clear-filters").click()
            for city in cities:
                page.locator("#filter-city").select_option(label=city)
                check_rendered([row for row in all_rows if row["cidade"] == city])
            page.locator("#clear-filters").click()

            sample = all_rows[0]
            page.locator("#filter-category").select_option(label=sample["categoria"])
            page.locator("#filter-city").select_option(label=sample["cidade"])
            check_rendered([
                row for row in all_rows
                if row["categoria"] == sample["categoria"] and row["cidade"] == sample["cidade"]
            ])
            page.locator("#clear-filters").click()
            check_rendered(all_rows)

            page.locator("#filter-category").evaluate(
                "element => { element.add(new Option('Sem resultado','__sem_resultado__')); element.value='__sem_resultado__'; element.dispatchEvent(new Event('change',{bubbles:true})); }"
            )
            check_rendered([])
            self.assertTrue(page.locator("#chart-category .chart-empty").is_visible())
            self.assertTrue(page.locator("#chart-city .chart-empty").is_visible())
            page.locator("#clear-filters").click()
            check_rendered(all_rows)

            page.keyboard.press("Home")
            page.keyboard.press("Tab")
            self.assertIn(page.evaluate("document.activeElement.tagName"), {"A", "BUTTON", "SELECT"})
            page.locator("#filter-category").focus()
            page.locator("#filter-category").press("ArrowDown")
            page.locator("#filter-category").press("Enter")
            check_rendered([row for row in all_rows if row["categoria"] == categories[0]])

            for width, height in ((1280, 900), (390, 844), (320, 740)):
                page.set_viewport_size({"width": width, "height": height})
                self.assertLessEqual(
                    page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth"),
                    1,
                    f"Overflow horizontal em {width}px",
                )
                self.assertTrue(page.get_by_label("Filtrar por categoria").is_visible())
                self.assertTrue(page.get_by_label("Filtrar por cidade").is_visible())
                for selector in ("#filters-title", ".filter-controls label span", ".kpi-label", ".bar-label", ".bar-value"):
                    label = page.locator(selector).first
                    self.assertTrue(label.is_visible(), f"Rótulo ausente em {width}px: {selector}")
                    style = label.evaluate(
                        "element => ({fontSize: parseFloat(getComputedStyle(element).fontSize), "
                        "color: getComputedStyle(element).color, opacity: getComputedStyle(element).opacity})"
                    )
                    self.assertGreaterEqual(style["fontSize"], 11, f"Rótulo pequeno em {width}px: {selector}")
                    self.assertNotEqual("rgba(0, 0, 0, 0)", style["color"])
                    self.assertGreater(float(style["opacity"]), 0)
            browser.close()

        self.assertEqual([], failed_responses)
        self.assertEqual([], page_errors)


if __name__ == "__main__":
    unittest.main(verbosity=2)
