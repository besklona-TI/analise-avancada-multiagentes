# Sobre os dados e os cálculos

## Fonte e significado das linhas

O dashboard usa exclusivamente `papelaria_limpa.csv`, a cópia tratada da etapa anterior. Cada linha representa uma venda de um produto; `id_venda` identifica essa venda. A fonte contém 180 linhas e 180 identificadores únicos, de 1º de janeiro a 31 de março de 2026. A data é calendário (sem horário ou fuso). As categorias são Acessórios, Livros e Papelaria; as cidades são Campinas, Santos e Sorocaba.

| Campo | Significado e tipo esperado |
|---|---|
| `id_venda` | Identificador textual único de cada venda/linha. |
| `data` | Data da venda no formato `AAAA-MM-DD`. |
| `cidade`, `categoria`, `produto`, `forma_pagamento` | Rótulos textuais; `Não informado` é um valor de pagamento preservado da limpeza anterior. |
| `quantidade` | Número inteiro positivo de unidades vendidas naquela venda. |
| `preco_unitario` | Preço por unidade, em reais. |
| `valor_venda` | Valor calculado para a linha, em reais: `quantidade × preco_unitario`. |

## Regras já aplicadas na fonte limpa

O arquivo de entrada desta etapa já traz o tratamento documentado em `resumo.md`: foram retiradas apenas duas cópias exatas da fonte original, espaços periféricos de cidade foram removidos, categorias foram padronizadas, quatro formas de pagamento vazias foram classificadas como `Não informado` e `valor_venda` foi calculado como quantidade × preço unitário. Esta etapa não relê o original, não elimina linhas e não modifica `papelaria_limpa.csv`. O script valida essas premissas e gera uma cópia JSON para o site.

## Indicadores

- **Valor total vendido:** soma de `valor_venda` das linhas visíveis após os filtros. É valor vendido calculado por quantidade × preço unitário; não é lucro.
- **Quantidade de vendas:** número de linhas/vendas da fonte que passam pelos filtros. Não é a soma de unidades.
- **Ticket médio:** valor total vendido dividido pela quantidade de vendas. Sem vendas, é apresentado como R$ 0,00 para evitar divisão por zero.
- **Unidades:** o campo `quantidade` é a quantidade de itens naquela linha; a soma geral conhecida é 548. Não é usada como quantidade de vendas.

Os dois gráficos somam `valor_venda` por categoria e por cidade, respeitando os mesmos filtros dos indicadores e da tabela. As barras começam em zero; os rótulos numéricos acompanham as barras e a tabela fornece uma alternativa detalhada. Sem registros após os filtros, os três indicadores exibem zero, os gráficos mostram que não há dados e a tabela informa o resultado vazio.

## Valores recalculados para a fonte completa

O script lê todas as 180 linhas sem remover ou modificar registros, confere colunas, ausências, IDs, duplicatas e `valor_venda`, e grava o JSON usado pelo site. Os recálculos da fonte confirmam **R$ 20.059,00** em vendas, **180 vendas**, **548 unidades** e ticket médio de **R$ 111,44** (R$ 20.059,00 ÷ 180). Por categoria: Acessórios **R$ 10.517,00**, Livros **R$ 7.438,00**, Papelaria **R$ 2.104,00**. Por cidade: Campinas **R$ 8.578,00**, Santos **R$ 6.937,50**, Sorocaba **R$ 4.543,50**. Os dois agrupamentos somam o total geral.

## Limitações

- A análise descreve somente as vendas presentes nessa fonte e nesse período; não representa necessariamente todas as operações do negócio.
- Não há custos, despesas, devoluções ou descontos para calcular lucro ou margem.
- Quatro vendas têm forma de pagamento `Não informado`; essa informação foi preservada como categoria, sem inferência.
- O dashboard é estático e carrega seu JSON local; atualizações exigem executar novamente a preparação e publicar os arquivos atualizados da pasta `site/`.
