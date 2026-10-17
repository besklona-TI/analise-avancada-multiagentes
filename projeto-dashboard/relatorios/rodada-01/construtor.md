# Relatório do Construtor — rodada 01

## Versão examinada

Sem commit Git disponível neste ambiente. Identificação pelos hashes SHA-256 dos arquivos ao final da preparação e execução dos testes:

| Arquivo | SHA-256 |
|---|---|
| Entrada `papelaria_limpa.csv` | `36D3A6607C75D6A3E22146469F43D3BFD4DAE85B0D60C99019A510F723F84D2B` |
| `preparar_dados.py` | `7966B4B1D4D4ED88127D36AE6349340524FEF2E6EC8AC31C66099E1EF1A66360` |
| `site/dados/vendas.json` | `0CC873CE9C6E13A6F9DC1D4653C2EE22B5B444E471B07CEBB98EAAF86A66D694` |
| `site/index.html` | `6174FE56134C3033AFF8D43BAA25131CB1442F8AF3571105E1585AF759BED0F0` |
| `site/styles.css` | `798CBA32A0F799509894AEF929FF6B72FF65BCDDC99E4C862EFE0CC3B7A5A24F` |
| `site/app.js` | `0EEADF0CDF52C899554DDA0408B1D4DC3591B9CC17125709C50CEE687D569887` |
| `ANALISE.md` | `2427E3EBA2CBC02AA0D5F3FF7154DE09C19E0B099672002BBFAEA1147DF24FA3` |
| `README.md` | `D2595CA4D45EBC2751D86844BCD995FBD3198C77373DEE24BA67F028026ABB64` |
| `tests/test_dashboard.py` | `703A6E3A01580AF58F4EC07814FCAC2839A87D321F0F15E3EA8B5B84DAB6A74E` |

## O que foi construído e conferido

- Preparação reproduzível em `projeto-dashboard/preparar_dados.py`, usando Python e pandas do ambiente `.venv`. Ela lê somente `papelaria_limpa.csv`, valida esquema, ausências, duplicatas, tipos e a identidade `valor_venda = quantidade × preco_unitario`, preserva a fonte e gera `site/dados/vendas.json`.
- Dashboard estático em `site/`, com indicadores de valor vendido, número de vendas e ticket médio; gráficos de barras por categoria e cidade; tabela; filtros sincronizados de cidade e categoria; botão de limpeza; mensagem sem resultados; moeda em reais e layout adaptável a computador e celular. Os controles são nativos e acessíveis por teclado.
- `ANALISE.md` descreve o grão (uma linha por venda), definições dos indicadores, regras de tratamento já aplicadas na fonte limpa e limitações, incluindo que valor vendido não é lucro. `README.md` contém os comandos de preparação, testes e servidor HTTP local, e identifica `site/` como publicável em hospedagem estática.

## Comandos, resultados e evidências

Executados de `projeto-dashboard/`:

- `..\.venv\Scripts\python.exe preparar_dados.py` — **passou**: 180 vendas e total vendido de R$ 20.059,00. Evidência em `site/dados/vendas.json`.
- `..\.venv\Scripts\python.exe -m unittest discover -s tests -v` — suíte terminou com **7 aprovados e 1 ignorado**. Passaram verificações de integridade das fontes, esquema, valores ausentes, duplicatas, regras de limpeza, exemplo conhecido, totais/agrupamentos independentes, correspondência do JSON, resposta HTTP dos arquivos locais e sintaxe JavaScript. Log disponível no resultado desta execução no terminal.
- No recálculo independente da suíte: 548 unidades; ticket médio R$ 111,438888… (apresentado como R$ 111,44); Acessórios R$ 10.517,00, Livros R$ 7.438,00 e Papelaria R$ 2.104,00; Campinas R$ 8.578,00, Santos R$ 6.937,50 e Sorocaba R$ 4.543,50. Os dois agrupamentos somam R$ 20.059,00.
- Testes HTTP obtiveram status 200 para a página e seus recursos locais; `node --check site/app.js` passou dentro da suíte.
- Integridade original: os testes confirmaram que `vendas_papelaria.csv` e `papelaria_limpa.csv` mantêm seus hashes esperados. Nenhum arquivo fora de `projeto-dashboard/` foi editado nesta execução.
- Skills aplicadas ao trabalho: `explore-data` para considerar grão, tipos e qualidade; `data-visualization` para comparar dimensões com barras legíveis; `validate-data` para conferir totais, agrupamentos e ressalvas.

## Problemas e encaminhamento

- O teste real de interação no navegador ficou **PENDENTE**: Playwright não está instalado no ambiente (`importlib.util.find_spec('playwright')` retornou `False`), por isso o unittest marcou esse teste como ignorado. O teste cobre filtros isolados e combinados, seleção vazia, limpeza, teclado e larguras desktop/mobile quando executado com Playwright/Chromium.
- Não há ferramenta de subagentes disponível nesta execução. Assim, o trabalho foi feito somente no papel Construtor; Tester e Revisor independentes não foram simulados nem aprovados. Encaminhar a versão e esta pendência para o Tester e, após os testes, para o Revisor.

## Status

**APROVADO — etapa de construção e checagens básicas do Construtor.** Interação automatizada em navegador, Tester e Revisor: **PENDENTES**; este relatório não representa aprovação conjunta/final do projeto.
