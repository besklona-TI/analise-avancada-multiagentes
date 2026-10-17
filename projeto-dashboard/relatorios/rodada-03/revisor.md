# Relatório do Revisor — rodada 03

## Versão examinada

Não há repositório Git. Conferi os hashes SHA-256 declarados pelo Construtor e pelo Tester contra os arquivos presentes. Os hashes de fontes e produto coincidem em ambos os relatórios e com esta inspeção; o Tester atualizou apenas `tests/test_tester_audit.py` em relação à lista do Construtor.

| Arquivo | SHA-256 verificado |
|---|---|
| `vendas_papelaria.csv` | `BF95B7609E30EB7E3E6A30CFC16E43D9FB5BDFC48A410E49148CCEB92E2494FF` |
| `papelaria_limpa.csv` | `36D3A6607C75D6A3E22146469F43D3BFD4DAE85B0D60C99019A510F723F84D2B` |
| `resumo.md` (etapa anterior) | `DF19D5B7069B11A133762F95DB2EB6748DCFCAD36C288B23B2F9730DC714F096` |
| `verificacao.md` (etapa anterior) | `103A45DD75589CD27B202FB3DF735EB645E83A0FAD484D5F12207A5F4FC6BFC6` |
| `categorias.png` (etapa anterior) | `58C81057DBF6DA8EBDC441D1769CA4F3CDA014231588F633E108B41657D6EFC4` |
| `cidades.png` (etapa anterior) | `8E45D54232995A8BD7115CB2F004754036A4AB2B093D6785A3598EEF0CB3A3C5` |
| `projeto-dashboard/preparar_dados.py` | `A3C4D476BFCA1DE6A451C72214E790D9C56353993CE92441E80190E09D532BB5` |
| `projeto-dashboard/ANALISE.md` | `546CB0930BE3C0F53A2A9AB4A3128417613E1DEE3DDDF756B717305BA14695B2` |
| `projeto-dashboard/README.md` | `52C2EC130DE9AADC6023C504DD84F84BF2C9B1BDABB318FD0C0ACC6953E20E0B` |
| `projeto-dashboard/site/index.html` | `6174FE56134C3033AFF8D43BAA25131CB1442F8AF3571105E1585AF759BED0F0` |
| `projeto-dashboard/site/styles.css` | `798CBA32A0F799509894AEF929FF6B72FF65BCDDC99E4C862EFE0CC3B7A5A24F` |
| `projeto-dashboard/site/app.js` | `4EDDED09DC4B110EDD8FE8D2EA4070C25FF3F4BF2E7EF294AEE23F91A062D781` |
| `projeto-dashboard/site/dados/vendas.json` | `0CC873CE9C6E13A6F9DC1D4653C2EE22B5B444E471B07CEBB98EAAF86A66D694` |
| `projeto-dashboard/tests/test_dashboard.py` | `331237CB3007F642E0A06D54DBA11240FF2064516F58BA8F9F643FFFB8DCB6B8` |
| `projeto-dashboard/tests/test_tester_audit.py` | `B6F1CBB3A8B85AA34BA10EE3D944F36E95FFF42ABA1DE5D02BEBFA65B6B4858D` |
| `projeto-dashboard/tests/README.md` | `7CF2EACB72112CD99DB319A841A089270921DEF79FA62D1F3D0C671E9C07F453` |

Relatórios examinados: `relatorios/rodada-03/construtor.md` (SHA-256 `B7CCCA07D8E93CD7AC01FD5C32E2F108EB4312C853B27DD80659E207B22748FB`) e `relatorios/rodada-03/tester.md` (SHA-256 `50004833708056ED6E015D5D8B21E264F963FFD13B5F531ABAD2F846C66DB774`). Os hashes do produto declarados por esses relatórios coincidem com a versão acima; assim, as aprovações relatadas pelo Construtor e Tester referem-se aos mesmos arquivos de produto.

## Escopo da revisão

Li os relatórios de Construtor e Tester; `preparar_dados.py`, `ANALISE.md`, `README.md`, HTML, CSS, JavaScript, JSON preparado, ambos os módulos de teste e README dos testes. Conferi também `resumo.md`, `verificacao.md` e hashes dos CSVs, gráficos e resultados anteriores preservados. Recalculei os resultados diretamente da fonte limpa e do JSON, examinei regras de negócio e agregações, interface, teclado, layout responsivo e cobertura dos testes. Não alterei arquivos de produto ou testes.

## Conferências, comandos e evidências

### Identidade e preservação

```powershell
$paths = @('..\vendas_papelaria.csv','..\papelaria_limpa.csv','..\resumo.md','..\verificacao.md','..\categorias.png','..\cidades.png','preparar_dados.py','ANALISE.md','README.md','site\index.html','site\styles.css','site\app.js','site\dados\vendas.json','tests\test_dashboard.py','tests\test_tester_audit.py','tests\README.md','relatorios\rodada-03\construtor.md','relatorios\rodada-03\tester.md'); Get-FileHash -Algorithm SHA256 -LiteralPath $paths
```

Resultado: todos os hashes declarados para fontes, resultados anteriores e produto conferem. Os hashes do Construtor e Tester para fonte e produto são iguais. O CSV original e `papelaria_limpa.csv` continuam preservados.

### Recalculo independente

```powershell
..\.venv\Scripts\python.exe -c "import csv,json; from collections import defaultdict; from decimal import Decimal; from pathlib import Path; src=list(csv.DictReader(Path('..\\papelaria_limpa.csv').open(encoding='utf-8-sig',newline=''))); data=json.loads(Path('site/dados/vendas.json').read_text(encoding='utf-8')); cats=defaultdict(Decimal); cities=defaultdict(Decimal); [cats.__setitem__(r['categoria'],cats[r['categoria']]+Decimal(r['valor_venda'])) for r in src]; [cities.__setitem__(r['cidade'],cities[r['cidade']]+Decimal(r['valor_venda'])) for r in src]; total=sum((Decimal(r['valor_venda']) for r in src),Decimal(0)); units=sum(int(r['quantidade']) for r in src); assert len(src)==len(data)==180 and total==sum((Decimal(str(r['valor_venda'])) for r in data),Decimal(0)); assert cats['Acess'+chr(243)+'rios']==Decimal('10517') and cats['Livros']==Decimal('7438') and cats['Papelaria']==Decimal('2104.0'); assert cities['Campinas']==Decimal('8578') and cities['Santos']==Decimal('6937.5') and cities['Sorocaba']==Decimal('4543.5'); print('total=',total,'vendas=',len(src),'unidades=',units,'ticket=',total/len(src)); print('categorias=',dict(cats)); print('cidades=',dict(cities))"
```

Resultado: 180 linhas na fonte e no JSON, **R$ 20.059,00**, **180 vendas**, **548 unidades** e ticket médio exato de `20059 / 180` (apresentação: **R$ 111,44**). Categorias: Acessórios R$ 10.517,00; Livros R$ 7.438,00; Papelaria R$ 2.104,00. Cidades: Campinas R$ 8.578,00; Santos R$ 6.937,50; Sorocaba R$ 4.543,50. Ambas as partições somam o total. O pequeno caso conhecido está no teste independente: `2 × 10 + 3 × 4 = 32`, 2 vendas e ticket 16.

Confirmei também a coerência com a metodologia documentada: o original tem 182 linhas e as duas cópias exatas excedentes removidas já na etapa anterior; a fonte limpa usada agora tem 180 IDs únicos, sem duplicatas completas, sem ausências, preserva os quatro pagamentos `Não informado` e calcula `valor_venda` como quantidade × preço. A preparação valida a fonte e gera JSON; não altera o CSV. A contagem de vendas é o número de linhas, não a soma das unidades. O dashboard nomeia o indicador como valor vendido e declara que não é lucro.

### Suíte obrigatória e reprodução

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONPATH = 'C:\Users\IADADOS\AppData\Local\Temp\opencode\tester-playwright'
$env:PLAYWRIGHT_BROWSERS_PATH = 'C:\Users\IADADOS\AppData\Local\Temp\opencode\tester-browsers'
..\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Resultado desta revisão: **11 testes passaram, 0 falharam, 0 ignorados**, em 13,070 s. Chromium foi executado via Playwright. Os logs mostram `200` para `/`, `/styles.css`, `/app.js` e `/dados/vendas.json`; os erros de navegador foram verificados pelos testes. Evidência reproduzível: `tests/test_dashboard.py`, `tests/test_tester_audit.py` e saída acima.

```powershell
node --check site\app.js
```

Resultado: sintaxe JavaScript aprovada (também exercitada pela suíte).

### Análise dos testes, produto e UX

- A cobertura dos dados compara hashes das duas fontes, colunas, tipos, ausências, duplicatas, regra documentada de limpeza, tipos e valores do JSON, cálculos independentes por `Decimal` e caso conhecido. A reconciliação da tabela verifica todas as nove células por venda. Os testes conferem KPIs e agregações de ambos os gráficos contra cálculos derivados dos dados preparados.
- Os filtros de categoria e cidade são exercitados isoladamente para suas opções, em combinação, sem resultados e ao limpar. O teste verifica atualização dos componentes, mensagem de estado vazio, ausência de `NaN`/`Infinity` e restauração da visão completa. Não encontrei divisão por zero: o ticket é definido como zero quando não há linhas.
- HTML semântico inclui títulos e cabeçalhos de tabela associados, labels nos selects, botão nativo, link para pular ao conteúdo, nomes acessíveis, `aria-live`/`role=status` e alternativa tabular aos gráficos. O teclado alcança e altera os filtros; limpar devolve o foco ao primeiro filtro. As cores não são o único meio de distinguir os grupos, pois rótulos e valores estão presentes.
- A folha de estilos reorganiza os filtros, cartões e gráficos em telas estreitas. O teste mede ausência de overflow e visibilidade dos controles em 320, 390 e 1280 pixels; foi executado no Chromium nesta revisão. Textos, botões e áreas de seleção permanecem legíveis/utilizáveis nos viewports examinados.
- O README principal contém comandos reais para preparar os dados, executar testes e abrir servidor HTTP local; identifica `site/` como a pasta publicável. `tests/README.md` explica a dependência de Playwright/Chromium e corretamente classifica os testes de navegador ignorados como **PENDENTES**.
- Não executei teste com leitor de tela nem medi contraste por ferramenta automatizada; isso não era critério obrigatório explicitado pela suíte e não observei defeito visual/semântico bloqueador na inspeção. A cobertura obrigatória de teclado, rótulos e responsividade foi exercitada.

## Problemas e encaminhamento

Não encontrei divergência metodológica, erro de cálculo, defeito reproduzível no dashboard, descumprimento de documentação ou lacuna de cobertura obrigatória. **Nenhum encaminhamento necessário ao Tester ou ao Construtor.** Não criei `FINAL.md` nem editei relatórios de outros agentes.

O coordenador executou sessões reais e separadas para Construtor, Tester e Revisor via ferramenta de tarefa. Esta revisão corresponde à sessão designada de Revisor; os relatórios de Construtor e Tester foram comparados com os arquivos, e seus resultados foram conferidos por recálculos e execução próprios.

Pendências da revisão: **nenhuma**. Os testes obrigatórios foram executados; nenhum teste ficou ignorado.

## Status

**APROVADO — revisão da versão identificada pelos hashes desta rodada 03.** Produto e testes aprovados pelos relatórios examinados referem-se à mesma versão de produto, os cálculos foram verificados independentemente e os 11 testes passaram nesta execução. Este status aprova a revisão; a consolidação final e o status conjunto permanecem com a coordenação.
