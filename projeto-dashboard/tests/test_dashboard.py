"""Testes de contrato para o dashboard de papelaria.

Execute em projeto-dashboard com:
    python -m unittest discover -s tests -v

Os testes recalculam os resultados sem importar o código de preparação do
construtor. A parte de browser usa Playwright quando instalado e disponível;
sem navegador, fica explicitamente marcada como ignorada (pendente).
"""

from __future__ import annotations

import csv
import hashlib
import html.parser
import json
import re
import shutil
import subprocess
import threading
import unittest
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import date
from decimal import Decimal
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


PROJECT_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = PROJECT_DIR.parent
SOURCE = REPO_DIR / "papelaria_limpa.csv"
ORIGINAL = REPO_DIR / "vendas_papelaria.csv"
SITE_DIR = PROJECT_DIR / "site"
INDEX = SITE_DIR / "index.html"

# Fingerprints registrados antes da construção do dashboard: qualquer mudança
# no original ou na fonte limpa deve ser investigada, não aceita silenciosamente.
EXPECTED_SHA256 = {
    "vendas_papelaria.csv": "bf95b7609e30eb7e3e6a30cfc16e43d9fb5bdfc48a410e49148cceb92e2494ff",
    "papelaria_limpa.csv": "36d3a6607c75d6a3e22146469f43d3bfd4dae85b0d60c99019a510f723f84d2b",
}

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
ORIGINAL_COLUMNS = EXPECTED_COLUMNS[:-1]
CANONICAL_CATEGORIES = {"Acessórios", "Livros", "Papelaria"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def exact_duplicate_count(rows: list[dict[str, str]]) -> int:
    """Count excess identical records, independent of pandas/drop_duplicates."""
    fingerprints = [tuple(row[column] for column in row) for row in rows]
    return len(fingerprints) - len(set(fingerprints))


def expected_cleaned_rows() -> list[dict[str, str]]:
    """Reconstruct the documented cleaning rules directly from the original."""
    original = read_csv(ORIGINAL)
    unique_rows: list[dict[str, str]] = []
    seen: set[tuple[str, ...]] = set()
    for row in original:
        fingerprint = tuple(row[column] for column in ORIGINAL_COLUMNS)
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        cleaned = {column: row[column] for column in ORIGINAL_COLUMNS}
        cleaned["cidade"] = cleaned["cidade"].strip()
        category = cleaned["categoria"].strip().casefold()
        cleaned["categoria"] = {
            "acessórios": "Acessórios",
            "livros": "Livros",
            "papelaria": "Papelaria",
        }[category]
        cleaned["forma_pagamento"] = cleaned["forma_pagamento"].strip() or "Não informado"
        cleaned["valor_venda"] = str(
            Decimal(cleaned["quantidade"]) * Decimal(cleaned["preco_unitario"])
        )
        unique_rows.append(cleaned)
    return unique_rows


def records_from_json(value: Any) -> list[dict[str, Any]] | None:
    """Accept common static-data JSON shapes without assuming builder internals."""
    if isinstance(value, list) and all(isinstance(item, dict) for item in value):
        return value
    if isinstance(value, dict):
        for key in ("vendas", "dados", "data", "rows", "records", "registros"):
            candidate = value.get(key)
            if isinstance(candidate, list) and all(isinstance(item, dict) for item in candidate):
                return candidate
    return None


def locate_prepared_records() -> tuple[Path, list[dict[str, Any]]]:
    """Find the prepared tabular asset, allowing CSV or JSON formats."""
    candidates: list[tuple[Path, list[dict[str, Any]]]] = []
    for path in PROJECT_DIR.rglob("*"):
        if not path.is_file() or "tests" in path.parts or "relatorios" in path.parts:
            continue
        if "node_modules" in path.parts or path.name.startswith("."):
            continue
        try:
            if path.suffix.lower() == ".csv":
                rows = read_csv(path)
                if rows and set(EXPECTED_COLUMNS).issubset(rows[0]):
                    candidates.append((path, rows))
            elif path.suffix.lower() == ".json":
                data = json.loads(path.read_text(encoding="utf-8"))
                rows = records_from_json(data)
                if rows and set(EXPECTED_COLUMNS).issubset(rows[0]):
                    candidates.append((path, rows))
        except (OSError, UnicodeError, json.JSONDecodeError, csv.Error):
            continue
    if not candidates:
        raise FileNotFoundError(
            "Não foi encontrado CSV/JSON preparado com os campos da fonte limpa "
            "em projeto-dashboard/."
        )
    if len(candidates) > 1:
        paths = ", ".join(str(path.relative_to(PROJECT_DIR)) for path, _ in candidates)
        raise AssertionError(f"Mais de um arquivo de dados tabulares candidato: {paths}")
    return candidates[0]


def to_decimal(value: Any) -> Decimal:
    return Decimal(str(value).replace(",", "."))


def canonical_row(row: dict[str, Any]) -> tuple[Any, ...]:
    normalized: list[Any] = []
    for column in EXPECTED_COLUMNS:
        value = row[column]
        if column == "quantidade":
            normalized.append(int(value))
        elif column in {"preco_unitario", "valor_venda"}:
            normalized.append(to_decimal(value).normalize())
        else:
            normalized.append(str(value))
    return tuple(normalized)


class SourceAndDataTests(unittest.TestCase):
    def test_original_and_confirmed_source_are_unchanged(self) -> None:
        for path in (ORIGINAL, SOURCE):
            self.assertTrue(path.is_file(), f"Fonte ausente: {path}")
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(EXPECTED_SHA256[path.name], digest, f"Fonte alterada: {path.name}")

    def test_source_columns_types_missing_values_and_duplicates(self) -> None:
        original = read_csv(ORIGINAL)
        source = read_csv(SOURCE)
        self.assertEqual(ORIGINAL_COLUMNS, list(original[0]))
        self.assertEqual(EXPECTED_COLUMNS, list(source[0]))
        self.assertEqual(182, len(original))
        self.assertEqual(180, len(source))
        self.assertEqual(2, exact_duplicate_count(original))
        self.assertEqual(0, exact_duplicate_count(source))
        self.assertEqual(180, len({row["id_venda"] for row in source}))
        self.assertTrue(all(row[column].strip() for row in source for column in EXPECTED_COLUMNS))
        self.assertEqual(CANONICAL_CATEGORIES, {row["categoria"] for row in source})
        self.assertEqual(4, sum(row["forma_pagamento"] == "Não informado" for row in source))
        for row in source:
            self.assertRegex(row["data"], r"^\d{4}-\d{2}-\d{2}$")
            quantity = int(row["quantidade"])
            price = Decimal(row["preco_unitario"])
            sale_value = Decimal(row["valor_venda"])
            self.assertGreater(quantity, 0)
            self.assertGreater(price, 0)
            self.assertEqual(Decimal(quantity) * price, sale_value, row["id_venda"])

    def test_clean_source_matches_documented_rules_from_original(self) -> None:
        actual = read_csv(SOURCE)
        expected = expected_cleaned_rows()
        self.assertEqual(180, len(expected))
        self.assertEqual(
            Counter(canonical_row(row) for row in expected),
            Counter(canonical_row(row) for row in actual),
        )

    def test_independent_known_example_and_source_totals(self) -> None:
        # Exemplo pequeno calculado à mão: duas linhas de venda no valor de
        # 2×10=20 e 3×4=12 totalizam 32; 2 vendas e ticket médio 16.
        tiny_example = [(2, Decimal("10")), (3, Decimal("4"))]
        example_total = sum((qty * price for qty, price in tiny_example), Decimal("0"))
        self.assertEqual(Decimal("32"), example_total)
        self.assertEqual(2, len(tiny_example))
        self.assertEqual(Decimal("16"), example_total / len(tiny_example))

        rows = read_csv(SOURCE)
        total = sum((Decimal(row["valor_venda"]) for row in rows), Decimal("0"))
        quantity = sum(int(row["quantidade"]) for row in rows)
        by_category: defaultdict[str, Decimal] = defaultdict(Decimal)
        by_city: defaultdict[str, Decimal] = defaultdict(Decimal)
        for row in rows:
            by_category[row["categoria"]] += Decimal(row["valor_venda"])
            by_city[row["cidade"]] += Decimal(row["valor_venda"])
        self.assertEqual(Decimal("20059.0"), total)
        self.assertEqual(548, quantity)
        self.assertEqual(Decimal("111.4388888888888888888888889"), total / len(rows))
        self.assertEqual(
            {"Acessórios": Decimal("10517"), "Livros": Decimal("7438"), "Papelaria": Decimal("2104.0")},
            dict(by_category),
        )
        self.assertEqual(
            {"Campinas": Decimal("8578.0"), "Santos": Decimal("6937.5"), "Sorocaba": Decimal("4543.5")},
            dict(by_city),
        )
        self.assertEqual(total, sum(by_category.values(), Decimal("0")))
        self.assertEqual(total, sum(by_city.values(), Decimal("0")))

    def test_prepared_data_matches_confirmed_source_and_independent_aggregates(self) -> None:
        prepared_path, prepared = locate_prepared_records()
        source = read_csv(SOURCE)
        self.assertIn(prepared_path.suffix.lower(), {".csv", ".json"})
        self.assertEqual(180, len(prepared), str(prepared_path))
        self.assertEqual(set(EXPECTED_COLUMNS), set(prepared[0]))
        self.assertEqual(0, exact_duplicate_count(prepared))
        self.assertEqual(180, len({str(row["id_venda"]) for row in prepared}))
        for row in prepared:
            self.assertTrue(all(str(row[column]).strip() for column in EXPECTED_COLUMNS))
            date.fromisoformat(str(row["data"]))
            quantity = int(row["quantidade"])
            price = to_decimal(row["preco_unitario"])
            sale_value = to_decimal(row["valor_venda"])
            self.assertGreater(quantity, 0)
            self.assertGreater(price, 0)
            self.assertEqual(Decimal(quantity) * price, sale_value)
        self.assertEqual(Counter(canonical_row(row) for row in source), Counter(canonical_row(row) for row in prepared))

        total = sum((to_decimal(row["valor_venda"]) for row in prepared), Decimal("0"))
        count = len(prepared)
        by_category: defaultdict[str, Decimal] = defaultdict(Decimal)
        by_city: defaultdict[str, Decimal] = defaultdict(Decimal)
        for row in prepared:
            by_category[str(row["categoria"])] += to_decimal(row["valor_venda"])
            by_city[str(row["cidade"])] += to_decimal(row["valor_venda"])
        self.assertEqual(Decimal("20059"), total)
        self.assertEqual(180, count)
        self.assertEqual(Decimal("20059") / 180, total / count)
        self.assertEqual(Decimal("20059"), sum(by_category.values(), Decimal("0")))
        self.assertEqual(Decimal("20059"), sum(by_city.values(), Decimal("0")))


class LocalHTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not INDEX.is_file():
            raise FileNotFoundError(f"Site ainda não entregue: {INDEX}")
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

    def test_index_and_all_local_html_assets_load_over_http(self) -> None:
        with urllib.request.urlopen(self.base_url + "/", timeout=5) as response:
            self.assertEqual(200, response.status)
            self.assertIn("text/html", response.headers.get_content_type())
            page = response.read().decode("utf-8")
        self.assertTrue(page.strip())

        parser = AssetParser()
        parser.feed(page)
        local_assets = set()
        for ref in parser.references:
            parsed = urllib.parse.urlparse(ref)
            if parsed.scheme or parsed.netloc or ref.startswith(("#", "data:")):
                continue
            local_assets.add(urllib.parse.urljoin(self.base_url + "/", ref))
        for url in sorted(local_assets):
            with self.subTest(asset=url), urllib.request.urlopen(url, timeout=5) as response:
                self.assertEqual(200, response.status)
                self.assertGreater(len(response.read()), 0)

    def test_javascript_files_pass_node_syntax_check(self) -> None:
        node = shutil.which("node")
        self.assertIsNotNone(node, "Node.js é necessário para validar a sintaxe dos scripts.")
        scripts = list(SITE_DIR.rglob("*.js"))
        self.assertTrue(scripts, "Nenhum arquivo JavaScript encontrado no site.")
        for script in scripts:
            result = subprocess.run([node, "--check", str(script)], capture_output=True, text=True)
            self.assertEqual(0, result.returncode, f"{script}:\n{result.stdout}\n{result.stderr}")


class AssetParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        for key in ("src", "href"):
            if values.get(key):
                self.references.append(str(values[key]))


class BrowserInteractionTests(unittest.TestCase):
    """Real-browser smoke/interaction checks; skipped explicitly if unavailable."""

    def test_dashboard_filters_empty_state_clear_and_responsive_keyboard(self) -> None:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            self.skipTest("PENDENTE: pacote Python Playwright não instalado.")

        if not INDEX.is_file():
            self.fail(f"Site ainda não entregue: {INDEX}")
        with sync_playwright() as playwright:
            try:
                browser = playwright.chromium.launch(headless=True)
            except Exception as exc:  # browser binary may not be installed in this machine
                self.skipTest(f"PENDENTE: navegador Playwright indisponível ({exc}).")
            handler = lambda *args, **kwargs: SimpleHTTPRequestHandler(
                *args, directory=str(SITE_DIR), **kwargs
            )
            server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
            server_thread = threading.Thread(target=server.serve_forever, daemon=True)
            server_thread.start()
            self.addCleanup(server.server_close)
            self.addCleanup(server_thread.join, 3)
            self.addCleanup(server.shutdown)
            base_url = f"http://127.0.0.1:{server.server_port}"
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            page_errors: list[str] = []
            page.on("pageerror", lambda error: page_errors.append(str(error)))
            page.on(
                "console",
                lambda message: page_errors.append(message.text) if message.type == "error" else None,
            )
            page.goto(base_url + "/", wait_until="networkidle")

            selects = page.locator("select")
            self.assertGreaterEqual(selects.count(), 2, "Esperados dois filtros nativos acessíveis por teclado.")
            table = page.locator("table")
            self.assertGreaterEqual(table.count(), 1, "Tabela de vendas não encontrada.")
            reset = page.get_by_role("button", name=re.compile(r"limpar", re.IGNORECASE))
            self.assertEqual(1, reset.count(), "Botão Limpar filtros não encontrado por nome acessível.")

            def visible_data_row_count() -> int:
                count = 0
                for row in page.locator("table tbody tr").all():
                    if not row.is_visible():
                        continue
                    if re.search(r"sem resultado|nenhum|não encontrado|nenhuma venda", row.inner_text(), re.I):
                        continue
                    count += 1
                return count

            initial_rows = visible_data_row_count()
            self.assertGreater(initial_rows, 0)
            initial_text = page.locator("body").inner_text()
            real_choices: list[str] = []

            # Cada filtro precisa mudar o resultado, e limpar precisa restaurá-lo.
            for index in range(2):
                select = selects.nth(index)
                options = select.locator("option")
                choice = None
                for option_index in range(options.count()):
                    option = options.nth(option_index)
                    value = option.get_attribute("value")
                    if value and value.strip():
                        choice = value
                        break
                self.assertIsNotNone(choice, f"Filtro {index + 1} não oferece opções selecionáveis.")
                real_choices.append(str(choice))
                select.select_option(choice)
                page.wait_for_timeout(100)
                self.assertNotEqual(initial_text, page.locator("body").inner_text())
                self.assertLessEqual(visible_data_row_count(), initial_rows)
                reset.click()
                self.assertEqual(initial_rows, visible_data_row_count())

            selects.nth(0).select_option(real_choices[0])
            selects.nth(1).select_option(real_choices[1])
            page.wait_for_timeout(100)
            self.assertLess(visible_data_row_count(), initial_rows, "Filtros combinados não reduziram a tabela.")
            self.assertNotEqual(initial_text, page.locator("body").inner_text())
            reset.click()
            self.assertEqual(initial_rows, visible_data_row_count())

            # Aplicar uma opção sentinela via DOM exercita a seleção sem
            # resultados mesmo quando todas as combinações reais têm vendas.
            selects.nth(0).evaluate(
                "element => { element.add(new Option('Sem correspondência', '__valor_de_teste_sem_correspondencia__')); "
                "element.value = '__valor_de_teste_sem_correspondencia__'; "
                "element.dispatchEvent(new Event('change', { bubbles: true })); }"
            )
            page.wait_for_timeout(100)
            self.assertEqual(0, visible_data_row_count())
            body = page.locator("body").inner_text()
            self.assertRegex(body, re.compile(r"sem resultado|nenhum|não encontrado|nenhuma venda", re.I))
            self.assertNotRegex(body, re.compile(r"\bNaN\b|\bInfinity\b", re.I))
            reset.click()
            self.assertEqual(initial_rows, visible_data_row_count())

            # Teclado: chegar aos filtros por Tab; layout desktop e mobile sem
            # overflow horizontal da página.
            page.keyboard.press("Home")
            page.keyboard.press("Tab")
            focused = page.evaluate("document.activeElement.tagName")
            self.assertIn(focused, {"SELECT", "BUTTON", "A", "INPUT"}, "Controle não alcançável por teclado.")
            selects.nth(0).focus()
            selects.nth(0).press("ArrowDown")
            selects.nth(0).press("Enter")
            self.assertNotEqual(initial_text, page.locator("body").inner_text())
            reset.click()
            for width, height in ((1280, 900), (390, 844)):
                page.set_viewport_size({"width": width, "height": height})
                page.wait_for_timeout(100)
                dimensions = page.evaluate(
                    "({client: document.documentElement.clientWidth, scroll: document.documentElement.scrollWidth})"
                )
                self.assertLessEqual(
                    dimensions["scroll"], dimensions["client"] + 1,
                    f"Overflow horizontal em viewport {width}px: {dimensions}",
                )
                self.assertTrue(selects.nth(0).is_visible())
                self.assertTrue(selects.nth(1).is_visible())

            self.assertEqual([], page_errors, f"Erros JavaScript no navegador: {page_errors}")
            final_text = page.locator("body").inner_text()
            self.assertNotRegex(final_text, re.compile(r"\bNaN\b|\bInfinity\b", re.I))


if __name__ == "__main__":
    unittest.main(verbosity=2)
