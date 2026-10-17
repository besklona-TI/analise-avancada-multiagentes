# Relatório final — Dashboard de vendas da papelaria

## Status conjunto: **APROVADO**

Construtor, Tester e Revisor aprovaram a mesma versão do produto na rodada 03. A preparação foi reproduzida pela coordenação, e a suíte integral passou novamente. Não há pendências obrigatórias.

## Versão final

Não há repositório Git neste ambiente. Os hashes SHA-256 do produto conferidos nas três etapas estão registrados em `relatorios/rodada-03/`. As fontes e os arquivos de resultados anteriores foram preservados:

| Arquivo | SHA-256 |
|---|---|
| `papelaria_limpa.csv` (entrada confirmada) | `36D3A6607C75D6A3E22146469F43D3BFD4DAE85B0D60C99019A510F723F84D2B` |
| `preparar_dados.py` | `A3C4D476BFCA1DE6A451C72214E790D9C56353993CE92441E80190E09D532BB5` |
| `ANALISE.md` | `546CB0930BE3C0F53A2A9AB4A3128417613E1DEE3DDDF756B717305BA14695B2` |
| `README.md` | `52C2EC130DE9AADC6023C504DD84F84BF2C9B1BDABB318FD0C0ACC6953E20E0B` |
| `site/index.html` | `6174FE56134C3033AFF8D43BAA25131CB1442F8AF3571105E1585AF759BED0F0` |
| `site/styles.css` | `798CBA32A0F799509894AEF929FF6B72FF65BCDDC99E4C862EFE0CC3B7A5A24F` |
| `site/app.js` | `4EDDED09DC4B110EDD8FE8D2EA4070C25FF3F4BF2E7EF294AEE23F91A062D781` |
| `site/dados/vendas.json` | `0CC873CE9C6E13A6F9DC1D4653C2EE22B5B444E471B07CEBB98EAAF86A66D694` |
| `tests/test_dashboard.py` | `331237CB3007F642E0A06D54DBA11240FF2064516F58BA8F9F643FFFB8DCB6B8` |
| `tests/test_tester_audit.py` | `B6F1CBB3A8B85AA34BA10EE3D944F36E95FFF42ABA1DE5D02BEBFA65B6B4858D` |

Os hashes do CSV original (`vendas_papelaria.csv`), do CSV limpo e dos arquivos da análise anterior (`resumo.md`, `verificacao.md`, `categorias.png` e `cidades.png`) constam nos relatórios da rodada 03 e não mudaram.

## Entrega e resultados

- A fonte escolhida tem 180 linhas e 180 vendas identificadas, de 01/01/2026 a 31/03/2026. Cada linha representa uma venda de produto. O original preservado continha duas cópias exatas excedentes, já removidas na etapa anterior; a preparação deste dashboard não exclui linhas nem altera CSVs.
- O dashboard mostra **R$ 20.059,00** em valor vendido, **180 vendas**, **548 unidades** e ticket médio apresentado como **R$ 111,44**. Valor vendido não é lucro.
- Os gráficos comparam valor vendido por categoria e cidade. Tabela e indicadores acompanham os dois filtros, com ação para limpá-los e mensagem para seleção sem resultados.
- `ANALISE.md` explica grão, campos, regras, métricas e limitações. `README.md` traz comandos para preparar, testar e servir localmente. `site/` é a pasta publicável em hospedagem estática.
- As skills `explore-data`, `data-visualization` e `validate-data` foram carregadas e usadas conforme as orientações do projeto.

### Verificação final executada pela coordenação

No PowerShell, na pasta `projeto-dashboard`:

```powershell
..\.venv\Scripts\python.exe preparar_dados.py
$env:PYTHONPATH = 'C:\Users\IADADOS\AppData\Local\Temp\opencode\tester-playwright'
$env:PLAYWRIGHT_BROWSERS_PATH = 'C:\Users\IADADOS\AppData\Local\Temp\opencode\tester-browsers'
..\.venv\Scripts\python.exe -m unittest discover -s tests -v
node --check site\app.js
```

Resultados: preparação com 180 vendas, total de R$ 20.059,00 e 548 unidades; **11 testes passaram, 0 falharam, 0 ignorados**; sintaxe JavaScript aprovada. Playwright/Chromium executou os testes de interface, incluindo HTTP, erros JavaScript, filtros isolados/combinados/vazios, limpar, teclado e viewports de 1280×900, 390×844 e 320×740. Construtor, Tester e Revisor também registraram suas evidências nos respectivos relatórios.

## Relatórios por rodada

- `relatorios/rodada-01/` e `relatorios/rodada-02/`: histórico preservado.
- `relatorios/rodada-03/construtor.md`: produto e preparação, **APROVADO**.
- `relatorios/rodada-03/tester.md`: testes independentes e interação no navegador, **APROVADO**.
- `relatorios/rodada-03/revisor.md`: revisão independente da mesma versão, **APROVADO**.

## Como abrir no Windows

1. Abra a pasta `projeto-dashboard` no VS Code.
2. No terminal PowerShell dessa pasta, execute:

   ```powershell
   python -m http.server 8000 --directory site
   ```

3. Acesse `http://localhost:8000` no navegador. Para encerrar o servidor, pressione `Ctrl+C` no terminal.

Para reproduzir a preparação e os testes, use os comandos do `README.md`. Os testes de interface requerem Playwright e Chromium; a configuração utilizada nesta rodada está documentada em `relatorios/rodada-03/tester.md`.
