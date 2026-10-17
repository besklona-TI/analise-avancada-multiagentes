# Testes do dashboard

Com o terminal do PowerShell aberto em `projeto-dashboard/`, execute a suíte completa:

```powershell
..\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Os testes verificam hashes e preservação dos CSVs, esquema, tipos, ausências e duplicatas conforme as regras documentadas; comparam a fonte limpa e o JSON preparado; e recalculam totais, agrupamentos e um exemplo pequeno conhecido de forma independente. No Chromium, comparam os três KPIs, os valores agrupados dos dois gráficos e as linhas da tabela com os dados preparados. Também exercitam cada filtro isolado, filtros combinados, estado sem resultados, botão de limpar, teclado, ausência de `NaN`/`Infinity` e viewports desktop e mobile. A suíte ainda verifica HTTP, carregamento dos assets, erros do navegador e sintaxe JavaScript com `node --check`.

Para habilitar os testes de interação real, instale Playwright e Chromium uma vez no mesmo ambiente Python:

```powershell
..\.venv\Scripts\python.exe -m pip install playwright
..\.venv\Scripts\python.exe -m playwright install chromium
```

Execute novamente o primeiro comando após instalar. Se Playwright ou Chromium estiver indisponível, o teste de navegador aparece como ignorado e fica **PENDENTE**; isso não equivale a aprovação da cobertura de interface.
