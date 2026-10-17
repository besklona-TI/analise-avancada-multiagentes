"use strict";

const money = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });
const integer = new Intl.NumberFormat("pt-BR", { maximumFractionDigits: 0 });
const state = { rows: [] };

const elements = {
  category: document.getElementById("filter-category"),
  city: document.getElementById("filter-city"),
  clear: document.getElementById("clear-filters"),
  total: document.getElementById("kpi-total"),
  count: document.getElementById("kpi-count"),
  average: document.getElementById("kpi-average"),
  summary: document.getElementById("filter-summary"),
  chartCategory: document.getElementById("chart-category"),
  chartCity: document.getElementById("chart-city"),
  tableRows: document.getElementById("sales-rows"),
  tableCount: document.getElementById("table-count"),
  empty: document.getElementById("empty-message"),
  tableWrap: document.getElementById("table-wrap"),
  error: document.getElementById("load-error"),
};

function formatDate(value) {
  const [year, month, day] = value.split("-");
  return `${day}/${month}/${year}`;
}

function cents(value) {
  return Math.round(value * 100);
}

function fillFilter(select, values, allLabel) {
  for (const value of values) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    select.append(option);
  }
  select.options[0].textContent = allLabel;
}

function selectedRows() {
  const category = elements.category.value;
  const city = elements.city.value;
  return state.rows.filter((row) =>
    (!category || row.categoria === category) && (!city || row.cidade === city)
  );
}

function aggregate(rows, column) {
  const totals = new Map();
  for (const row of rows) {
    const label = column === "categoria" ? row.categoria : row.cidade;
    totals.set(label, (totals.get(label) || 0) + cents(row.valor_venda));
  }
  return [...totals.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], "pt-BR"));
}

function renderChart(container, rows, column) {
  container.replaceChildren();
  const values = aggregate(rows, column);
  if (values.length === 0) {
    container.setAttribute("aria-label", "Gráfico sem dados para os filtros selecionados.");
    const message = document.createElement("p");
    message.className = "chart-empty";
    message.textContent = "Sem dados para exibir.";
    container.append(message);
    return;
  }

  const maximum = Math.max(...values.map((entry) => entry[1]));
  const dimension = column === "categoria" ? "categoria" : "cidade";
  container.setAttribute("aria-label", `Valor vendido por ${dimension}: ${values.map(([label, value]) => `${label}, ${money.format(value / 100)}`).join("; ")}. Escala iniciada em zero.`);
  for (const [label, value] of values) {
    const row = document.createElement("div");
    row.className = "bar-row";
    const name = document.createElement("span");
    name.className = "bar-label";
    name.textContent = label;
    const track = document.createElement("span");
    track.className = "bar-track";
    const fill = document.createElement("span");
    fill.className = "bar-fill";
    fill.style.width = `${maximum > 0 ? (value / maximum) * 100 : 0}%`;
    track.append(fill);
    const amount = document.createElement("span");
    amount.className = "bar-value";
    amount.textContent = money.format(value / 100);
    row.append(name, track, amount);
    container.append(row);
  }
  const scale = document.createElement("div");
  scale.className = "chart-scale";
  const zero = document.createElement("span");
  zero.textContent = money.format(0);
  const maximumLabel = document.createElement("span");
  maximumLabel.textContent = money.format(maximum / 100);
  scale.append(zero, maximumLabel);
  container.append(scale);
}

function addCell(row, value, className = "") {
  const cell = document.createElement("td");
  cell.textContent = value;
  if (className) cell.className = className;
  row.append(cell);
}

function renderTable(rows) {
  elements.tableRows.replaceChildren();
  const fragment = document.createDocumentFragment();
  for (const sale of rows) {
    const row = document.createElement("tr");
    addCell(row, formatDate(sale.data));
    addCell(row, sale.id_venda);
    addCell(row, sale.cidade);
    addCell(row, sale.categoria);
    addCell(row, sale.produto);
    addCell(row, integer.format(sale.quantidade), "numeric");
    addCell(row, money.format(sale.preco_unitario), "numeric");
    addCell(row, sale.forma_pagamento);
    addCell(row, money.format(sale.valor_venda), "numeric");
    fragment.append(row);
  }
  elements.tableRows.append(fragment);
  elements.empty.hidden = rows.length !== 0;
  elements.tableWrap.hidden = rows.length === 0;
  elements.tableCount.textContent = `${integer.format(rows.length)} ${rows.length === 1 ? "venda" : "vendas"}`;
}

function render() {
  const rows = selectedRows();
  const totalCents = rows.reduce((sum, row) => sum + cents(row.valor_venda), 0);
  const total = totalCents / 100;
  elements.total.textContent = money.format(total);
  elements.count.textContent = integer.format(rows.length);
  elements.average.textContent = money.format(rows.length ? totalCents / rows.length / 100 : 0);
  elements.summary.textContent = `${integer.format(rows.length)} de ${integer.format(state.rows.length)} vendas exibidas.`;
  renderChart(elements.chartCategory, rows, "categoria");
  renderChart(elements.chartCity, rows, "cidade");
  renderTable(rows);
}

async function start() {
  try {
    const response = await fetch("dados/vendas.json");
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const rows = await response.json();
    if (!Array.isArray(rows)) throw new Error("Formato de dados inválido");
    state.rows = rows;
    fillFilter(elements.category, [...new Set(rows.map((row) => row.categoria))].sort((a, b) => a.localeCompare(b, "pt-BR")), "Todas as categorias");
    fillFilter(elements.city, [...new Set(rows.map((row) => row.cidade))].sort((a, b) => a.localeCompare(b, "pt-BR")), "Todas as cidades");
    elements.category.addEventListener("change", render);
    elements.city.addEventListener("change", render);
    elements.clear.addEventListener("click", () => {
      elements.category.value = "";
      elements.city.value = "";
      render();
      elements.category.focus();
    });
    render();
  } catch (error) {
    console.error("Falha ao carregar os dados do dashboard:", error);
    elements.error.hidden = false;
  }
}

start();
