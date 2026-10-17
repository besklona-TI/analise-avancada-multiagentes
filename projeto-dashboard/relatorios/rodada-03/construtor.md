# Relatório do Construtor — rodada 03

## Versão examinada

Não há repositório Git. A versão é identificada pelos hashes SHA-256 dos arquivos da fonte, dos resultados anteriores preservados e do produto:

| Arquivo | SHA-256 |
|---|---|
| `vendas_papelaria.csv` (original preservado) | `BF95B7609E30EB7E3E6A30CFC16E43D9FB5BDFC48A410E49148CCEB92E2494FF` |
| `papelaria_limpa.csv` (entrada confirmada, preservada) | `36D3A6607C75D6A3E22146469F43D3BFD4DAE85B0D60C99019A510F723F84D2B` |
| `resumo.md` (etapa anterior, preservado) | `DF19D5B7069B11A133762F95DB2EB6748DCFCAD36C288B23B2F9730DC714F096` |
| `verificacao.md` (etapa anterior, preservado) | `103A45DD75589CD27B202FB3DF735EB645E83A0FAD484D5F12207A5F4FC6BFC6` |
| `categorias.png` (etapa anterior, preservado) | `58C81057DBF6DA8EBDC441D1769CA4F3CDA014231588F633E108B41657D6EFC4` |
| `cidades.png` (etapa anterior, preservado) | `8E45D54232995A8BD7115CB2F004754036A4AB2B093D6785A3598EEF0CB3A3C5` |
| `projeto-dashboard/preparar_dados.py` | `A3C4D476BFCA1DE6A451C72214E790D9C56353993CE92441E80190E09D532BB5` |
| `projeto-dashboard/ANALISE.md` | `546CB0930BE3C0F53A2A9AB4A3128417613E1DEE3DDDF756B717305BA14695B2` |
| `projeto-dashboard/README.md` | `52C2EC130DE9AADC6023C504DD84F84BF2C9B1BDABB318FD0C0ACC6953E20E0B` |
| `projeto-dashboard/site/index.html` | `6174FE56134C3033AFF8D43BAA25131CB1442F8AF3571105E1585AF759BED0F0` |
| `projeto-dashboard/site/styles.css` | `798CBA32A0F799509894AEF929FF6B72FF65BCDDC99E4C862EFE0CC3B7A5A24F` |
| `projeto-dashboard/site/app.js` | `4EDDED09DC4B110EDD8FE8D2EA4070C25FF3F4BF2E7EF294AEE23F91A062D781` |
| `projeto-dashboard/site/dados/vendas.json` | `0CC873CE9C6E13A6F9DC1D4653C2EE22B5B444E471B07CEBB98EAAF86A66D694` |

## Avaliação e alterações do produto

- A implementação já continha os três indicadores, gráficos por categoria e cidade, tabela, filtros por colunas existentes, atualização conjunta, limpeza de filtros, estado sem resultados, suporte a teclado e layout responsivo. Mantive essa estrutura e os nomes das colunas da fonte.
- Fortaleci `preparar_dados.py`: IDs e rótulos são lidos como texto; além de esquema, campos ausentes, IDs e linhas duplicadas, agora são verificados textos vazios, números finitos, quantidades inteiras e positivas, preço/valor positivos e igualdade exata de `valor_venda` a quantidade × preço. O script não elimina linhas nem reescreve o CSV limpo; gera somente `site/dados/vendas.json` e imprime totais de controle.
- O JavaScript agrega valores em centavos inteiros para evitar resíduos de soma de ponto flutuante. Indicadores, gráficos e tabela continuam derivados da mesma seleção de linhas.
- Ampliei `ANALISE.md` com dicionário de campos, tipos, grão, período, regras herdadas, significado das métricas, valores recalculados e limitações. O ticket médio é R$ 111,44 após arredondamento de apresentação; internamente, R$ 20.059,00 ÷ 180 = R$ 111,438888… . Valor vendido não é lucro.
- Atualizei `README.md` para usar `.venv/Scripts/python.exe` quando encontrado, com alternativa pelo `python` do Windows, e comandos de preparação, `unittest` e servidor HTTP. Identifica `site/` como pasta publicável em hospedagem estática.
- Não alterei testes, relatórios de outros agentes, CSVs ou artefatos da etapa anterior. O JSON gerado continua com 180 linhas de venda.

## Recalculo e conferência dos dados

A inspeção independente com pandas confirmou 180 linhas, 9 colunas, nenhuma célula ausente, nenhum ID repetido e nenhuma linha completamente duplicada. A fonte vai de 2026-01-01 a 2026-03-31. Recalculei as somas do CSV e do JSON preparado com `Decimal`:

- Total vendido: **R$ 20.059,00**; quantidade de vendas: **180**; unidades: **548**; ticket médio exato: **R$ 20.059,00 ÷ 180**.
- Categorias: Acessórios **R$ 10.517,00**; Livros **R$ 7.438,00**; Papelaria **R$ 2.104,00**. Soma: R$ 20.059,00.
- Cidades: Campinas **R$ 8.578,00**; Santos **R$ 6.937,50**; Sorocaba **R$ 4.543,50**. Soma: R$ 20.059,00.
- Os resultados coincidem com os valores de referência e com `verificacao.md`.

## Comandos executados, resultados e evidências

Executados no PowerShell com o diretório atual em `projeto-dashboard/`:

```powershell
..\.venv\Scripts\python.exe preparar_dados.py
```

Resultado: 180 vendas; R$ 20.059,00 vendidos; 548 unidades; agregações por categoria e cidade iguais aos valores acima. Evidência: `site/dados/vendas.json` e saída da preparação.

Recálculo independente e sintaxe JavaScript:

```powershell
..\.venv\Scripts\python.exe -c "import json; from decimal import Decimal; import pandas as pd; csv=pd.read_csv('..\\papelaria_limpa.csv',encoding='utf-8'); data=json.load(open('site/dados/vendas.json',encoding='utf-8')); assert len(data)==len(csv)==180; total=sum(Decimal(str(r['valor_venda'])) for r in data); assert total==Decimal('20059.0'); assert sum(r['quantidade'] for r in data)==548; print(total, total/len(data))"
node --check site\app.js
```

Resultado: soma e contagem confirmadas contra a fonte; `node --check` terminou sem erros.

Suíte completa, com o pacote Playwright e os navegadores temporários já usados pela rodada anterior:

```powershell
$env:PYTHONPATH = 'C:\Users\IADADOS\AppData\Local\Temp\opencode\tester-playwright'
$env:PLAYWRIGHT_BROWSERS_PATH = 'C:\Users\IADADOS\AppData\Local\Temp\opencode\tester-browsers'
..\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Resultado: **11 testes passaram, 0 falharam, 0 ignorados**, em 9,184 s. Os testes de navegador carregaram HTML, CSS, JavaScript e JSON por HTTP com respostas 200; verificaram os dados renderizados, interações de filtros (inclusive combinação e seleção vazia), limpar filtros, teclado e viewports. Evidência reproduzível: suíte existente em `tests/`; saída completa da execução no terminal desta rodada. Sem as duas variáveis de ambiente, Playwright não está instalado diretamente no `.venv` e dois testes de interface ficam PENDENTES (execução preliminar: 8 passaram e 2 foram ignorados); com o ambiente temporário disponível, a execução integral foi aprovada.

Preservação verificada com `Get-FileHash -Algorithm SHA256` nos arquivos de entrada e nos resultados da etapa anterior. Seus hashes permanecem os registrados nesta versão e o teste `test_original_and_confirmed_source_are_unchanged` passou.

## Problemas e encaminhamento

- Não encontrei divergência nos totais ou defeito funcional depois das correções. Não há falha de produto para encaminhar.
- **Tester:** considerar os hashes desta rodada como a nova versão do produto e registrar/revisar a execução integral acima no ciclo de testes. Os testes e relatórios do Tester não foram editados pelo Construtor.
- **Revisor:** revisar esta versão após a confirmação do Tester, conforme o ciclo do projeto. Esta atividade não constitui revisão independente.
- Testes de interface: **não pendentes nesta execução**, pois Chromium foi executado por Playwright e os testes correspondentes passaram. A execução sem configurar o pacote temporário deixa esses dois testes pendentes, conforme registrado.
- A aprovação conjunta e o relatório final pertencem à coordenação; este arquivo não declara aprovação global do projeto.

## Status

**APROVADO — entrega do Construtor na rodada 03.** Os requisitos de produto foram conferidos, os valores foram recalculados e a suíte integral, incluindo interação real em navegador, passou nesta versão. A aprovação independente do Tester, a revisão do Revisor e a consolidação final permanecem com os respectivos responsáveis.
