# Relatório do Tester — rodada 01

## Versão examinada

Não há repositório Git disponível. A versão do produto permaneceu a mesma versão entregue pelo Construtor; os hashes SHA-256 abaixo confirmam identidade. Alterei somente os testes: retirei a dependência indevida da ordem de execução e acrescentei `tests/test_tester_audit.py` para conferir tipos e correspondência renderizada.

| Arquivo | SHA-256 |
|---|---|
| `papelaria_limpa.csv` | `36D3A6607C75D6A3E22146469F43D3BFD4DAE85B0D60C99019A510F723F84D2B` |
| `vendas_papelaria.csv` | `BF95B7609E30EB7E3E6A30CFC16E43D9FB5BDFC48A410E49148CCEB92E2494FF` |
| `preparar_dados.py` | `7966B4B1D4D4ED88127D36AE6349340524FEF2E6EC8AC31C66099E1EF1A66360` |
| `site/dados/vendas.json` | `0CC873CE9C6E13A6F9DC1D4653C2EE22B5B444E471B07CEBB98EAAF86A66D694` |
| `site/index.html` | `6174FE56134C3033AFF8D43BAA25131CB1442F8AF3571105E1585AF759BED0F0` |
| `site/styles.css` | `798CBA32A0F799509894AEF929FF6B72FF65BCDDC99E4C862EFE0CC3B7A5A24F` |
| `site/app.js` | `0EEADF0CDF52C899554DDA0408B1D4DC3591B9CC17125709C50CEE687D569887` |
| `ANALISE.md` | `2427E3EBA2CBC02AA0D5F3FF7154DE09C19E0B099672002BBFAEA1147DF24FA3` |
| `README.md` | `D2595CA4D45EBC2751D86844BCD995FBD3198C77373DEE24BA67F028026ABB64` |
| `tests/test_dashboard.py` (auditada/corrigida) | `331237CB3007F642E0A06D54DBA11240FF2064516F58BA8F9F643FFFB8DCB6B8` |
| `tests/test_tester_audit.py` (adicionada) | `269431D4BD250459B3FC7E45094DA7F417E31320B3D0AAEF91701B05F336A040` |

## Escopo e resultado

- Confirmei hashes imutáveis do CSV original e da fonte escolhida. A fonte limpa tem 180 linhas e nove colunas na ordem documentada, sem ausências; os tipos inferidos pelo pandas são texto para identificadores/categorias/dimensões, `int64` para `quantidade` e `float64` para preços e valores. `id_venda` é único. A fonte original tem 182 linhas e duas cópias exatas excedentes; a limpa tem 180 registros sem duplicatas, consistente com a regra documentada.
- Comparei as regras de limpeza da fonte com reconstrução independente a partir do original. Recalculei total, contagem, unidades, ticket e agrupamentos, além do exemplo manual `2×10 + 3×4 = 32`, duas vendas e ticket 16. Resultado observado: R$ 20.059,00, 180 vendas, 548 unidades e ticket de R$ 111,44; categorias e cidades reconciliam com o total.
- Conferi o JSON preparado linha a linha com o CSV, inclusive tipos JSON. Em Chromium, comparei KPIs, valores por grupo nos dois gráficos e IDs/linhas da tabela com recálculos independentes. Repeti a comparação após cada filtro de categoria e cidade, filtros combinados, seleção vazia e limpeza.
- Testei resposta HTTP de HTML, CSS, JavaScript e JSON; sintaxe JavaScript; erros de console/página e respostas HTTP com falha. Testei seleção por teclado e apresentação/visibilidade dos filtros em 1280×900, 390×844 e 320×740, sem overflow horizontal. Estado vazio não exibiu NaN/Infinity e apresentou KPIs zero e gráficos/tabela vazios.

## Comandos e evidências

Ambiente: `.venv/Scripts/python.exe` (Python 3.14.7), pandas e Node.js disponíveis. Chrome e Edge estavam instalados. Playwright não estava instalado inicialmente; instalei Playwright 1.64.0 em `C:\Users\IADADOS\AppData\Local\Temp\opencode\tester-playwright` e Chromium em `C:\Users\IADADOS\AppData\Local\Temp\opencode\tester-browsers`, sem alterar dependências do projeto.

Comando final da suíte completa, executado em `projeto-dashboard/` após as correções nos testes:

```powershell
$env:PYTHONPATH = 'C:\Users\IADADOS\AppData\Local\Temp\opencode\tester-playwright'
$env:PLAYWRIGHT_BROWSERS_PATH = 'C:\Users\IADADOS\AppData\Local\Temp\opencode\tester-browsers'
..\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Resultado final: **11 testes passaram, 0 falharam, 0 ignorados**, em 9,242 s. O log da execução consta no terminal desta rodada. O módulo independente que verifica a renderização e os dados é `tests/test_tester_audit.py`.

Durante a primeira execução com navegador, a suíte revelou defeitos nos próprios testes, não no dashboard: o teste vazio tentava selecionar valor que não existia como opção do `<select>`; o teste de interação dependia da ordem das classes do `unittest`; e a limpeza duplicada do navegador ocorria depois de o Playwright fechar. Corrigi os dois testes para torná-los efetivos e independentes; a suíte final completa passou. Antes de instalar Playwright, a suíte marcou o navegador como ignorado; esse resultado inicial não foi contado como aprovação.

## Problemas e encaminhamento

- Nenhum defeito de produto reproduzido; nenhuma correção encaminhada ao Construtor.
- Correções de teste realizadas somente em `tests/test_dashboard.py`; teste de auditoria independente acrescentado em `tests/test_tester_audit.py`.
- Não há evidência de execução independente do Revisor nesta rodada; a revisão dessa função permanece pendente do fluxo de coordenação.

## Status

**APROVADO — etapa do Tester para a versão hashada acima.** Todos os testes obrigatórios executáveis, inclusive interação em navegador real, foram executados e passaram. Aprovação conjunta/final do projeto continua **PENDENTE** da revisão independente e da consolidação do coordenador.
