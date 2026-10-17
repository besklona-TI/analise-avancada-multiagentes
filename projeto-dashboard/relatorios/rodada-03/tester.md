# Relatório do Tester — rodada 03

## Versão examinada

Sem commit Git disponível. Conferi a versão informada em `relatorios/rodada-03/construtor.md`; os hashes do produto e das fontes coincidem com os registrados pelo Construtor. Ampliei somente `tests/test_tester_audit.py`, para confrontar cada célula da tabela com o JSON preparado e conferir legibilidade básica dos rótulos em três tamanhos de tela.

| Arquivo | SHA-256 |
|---|---|
| `vendas_papelaria.csv` | `BF95B7609E30EB7E3E6A30CFC16E43D9FB5BDFC48A410E49148CCEB92E2494FF` |
| `papelaria_limpa.csv` | `36D3A6607C75D6A3E22146469F43D3BFD4DAE85B0D60C99019A510F723F84D2B` |
| `preparar_dados.py` | `A3C4D476BFCA1DE6A451C72214E790D9C56353993CE92441E80190E09D532BB5` |
| `ANALISE.md` | `546CB0930BE3C0F53A2A9AB4A3128417613E1DEE3DDDF756B717305BA14695B2` |
| `README.md` | `52C2EC130DE9AADC6023C504DD84F84BF2C9B1BDABB318FD0C0ACC6953E20E0B` |
| `site/index.html` | `6174FE56134C3033AFF8D43BAA25131CB1442F8AF3571105E1585AF759BED0F0` |
| `site/styles.css` | `798CBA32A0F799509894AEF929FF6B72FF65BCDDC99E4C862EFE0CC3B7A5A24F` |
| `site/app.js` | `4EDDED09DC4B110EDD8FE8D2EA4070C25FF3F4BF2E7EF294AEE23F91A062D781` |
| `site/dados/vendas.json` | `0CC873CE9C6E13A6F9DC1D4653C2EE22B5B444E471B07CEBB98EAAF86A66D694` |
| `tests/test_dashboard.py` | `331237CB3007F642E0A06D54DBA11240FF2064516F58BA8F9F643FFFB8DCB6B8` |
| `tests/test_tester_audit.py` (após ampliação) | `B6F1CBB3A8B85AA34BA10EE3D944F36E95FFF42ABA1DE5D02BEBFA65B6B4858D` |
| `tests/README.md` | `7CF2EACB72112CD99DB319A841A089270921DEF79FA62D1F3D0C671E9C07F453` |
| `relatorios/rodada-03/construtor.md` | `B7CCCA07D8E93CD7AC01FD5C32E2F108EB4312C853B27DD80659E207B22748FB` |

## Cobertura e resultados

- Fontes: os hashes conferem; o original tem 182 linhas e duas cópias exatas excedentes, e a fonte limpa tem 180 linhas, sem duplicatas nem IDs repetidos. Conferi colunas, tipos, datas, valores ausentes, campos textuais vazios, categorias, os quatro pagamentos `Não informado` e a reconstrução independente das regras documentadas da fonte limpa a partir do original. O teste confirma que os CSVs permanecem inalterados.
- JSON: 180 registros reconciliados com a fonte linha a linha, incluindo tipos, campos, IDs e valores. Os totais e agrupamentos foram recalculados diretamente com `Decimal`, sem importar a lógica de preparação do Construtor.
- Cálculos: exemplo conhecido `2×10 + 3×4 = 32`, 2 vendas e ticket médio 16; na base, total de R$ 20.059,00, 180 vendas, 548 unidades e ticket médio exato de R$ 20.059,00 ÷ 180. Por categoria: Acessórios R$ 10.517,00, Livros R$ 7.438,00 e Papelaria R$ 2.104,00. Por cidade: Campinas R$ 8.578,00, Santos R$ 6.937,50 e Sorocaba R$ 4.543,50. Os dois agrupamentos conciliam com o total.
- Dashboard em Chromium: os três indicadores e os valores agrupados dos dois gráficos foram comparados com recálculos independentes. A tabela foi conferida registro a registro em todos os nove campos, incluindo datas e formatação de quantidade e moeda.
- Interações: cada opção de categoria e cidade foi testada isoladamente; filtros combinados, seleção sem correspondência e botão de limpar foram exercitados. No estado vazio, foram conferidos mensagem, linhas e gráficos vazios, tabela ocultada, KPIs sem divisão por zero e ausência de `NaN`/`Infinity`. Limpar restaurou a visão completa.
- Navegador e acessibilidade: Chromium carregou página, CSS, JavaScript e JSON por HTTP com status 200; não houve respostas com erro nem erros de console/página. O teste de teclado alcançou e alterou filtro por teclas. Em 1280×900, 390×844 e 320×740 não houve overflow horizontal; filtros e rótulos ficaram visíveis, opacos e com tamanho calculado de pelo menos 11 px.
- JavaScript: `node --check` passou. Revisei também os comandos documentados no README e a indicação de `site/` como pasta publicável.

## Comandos e evidências

Executados no PowerShell com o diretório atual em `projeto-dashboard/`:

```powershell
$env:PYTHONPATH = 'C:\Users\IADADOS\AppData\Local\Temp\opencode\tester-playwright'
$env:PLAYWRIGHT_BROWSERS_PATH = 'C:\Users\IADADOS\AppData\Local\Temp\opencode\tester-browsers'
..\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

A suíte completa foi executada antes e depois da ampliação do teste de tabela. Na execução final: **11 testes passaram, 0 falharam e 0 foram ignorados**, em 13,628 s. Chromium/Playwright foram efetivamente utilizados; os logs de HTTP da execução mostram status 200 para `/`, `/styles.css`, `/app.js` e `/dados/vendas.json`. A saída integral foi capturada no terminal desta rodada.

Os hashes foram obtidos com `Get-FileHash -Algorithm SHA256`. O teste ampliado está em `tests/test_tester_audit.py`; não alterei produto, relatório do Construtor nem CSVs.

## Problemas, encaminhamento e pendências

- Não reproduzi falhas de dados, cálculo, dashboard, filtros, acessibilidade de teclado, responsividade ou carregamento. Nenhum bug foi encaminhado ao Construtor.
- A primeira execução da suíte passou antes da alteração do teste; após ampliar a comparação de todas as células e verificações de rótulos, executei novamente a suíte completa e obtive o resultado final acima.
- Testes obrigatórios não executados: **nenhum**. Verificações pendentes: **nenhuma** nesta etapa.
- A aprovação conjunta e a revisão independente permanecem com a coordenação e o Revisor.

## Status

**APROVADO — etapa do Tester para os hashes listados nesta rodada.** Todos os testes obrigatórios foram executados, inclusive interação real em Chromium; a suíte final passou sem falhas ou skips.
