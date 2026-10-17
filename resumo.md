# Tratamento de vendas_papelaria.csv

## Perfil inicial
- Linhas: **182**; colunas: **8**.
- Granularidade informada: uma linha por venda; `id_venda` identifica a venda.
- Colunas: `id_venda`, `data`, `cidade`, `categoria`, `produto`, `quantidade`, `preco_unitario`, `forma_pagamento`.
- Período registrado: 2026-01-01 a 2026-03-31.

## Problemas encontrados
- **2 duplicatas exatas** (uma repetição extra para cada uma das vendas `V0010` e `V0020`). As linhas não idênticas com o mesmo identificador não foram removidas; neste arquivo, as repetições de ID eram cópias exatas.
- **6 linhas** com espaços no início e/ou no fim de `cidade`.
- **3 linhas** com a categoria `acessórios` em minúsculas, em vez do padrão `Acessórios`.
- **4 valores vazios** em `forma_pagamento`.
- Quantidades (1 a 5) e preços unitários (3,5 a 95) estavam preenchidos e eram positivos; não foram observados valores inválidos nesses campos.

## Tratamento aplicado
- O original foi preservado; os ajustes foram gravados em `papelaria_limpa.csv`.
- Removidas somente as **2 linhas de duplicata exata**, comparando todas as colunas originais. A cópia limpa contém **180 linhas** e **9 colunas**, incluindo a coluna calculada.
- Removidos espaços periféricos de `cidade`.
- Categorias padronizadas para `Livros`, `Papelaria` e `Acessórios` (incluindo normalização de maiúsculas/minúsculas).
- Valores vazios ou compostos apenas por espaços em `forma_pagamento` substituídos por `Não informado`.
- Adicionada `valor_venda`, calculada como `quantidade × preco_unitario`, usando precisão decimal.

## Conferência da cópia limpa
- Categorias: `Acessórios`: 65, `Livros`: 54, `Papelaria`: 61.
- Pagamentos `Não informado`: 4.
- Soma de `valor_venda`: 20059.0.
