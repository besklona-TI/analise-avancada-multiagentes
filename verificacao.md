# Verificação da análise de papelaria

## Escopo e método
Foram lidos localmente `vendas_papelaria.csv`, `papelaria_limpa.csv`, `resumo.md` e `graficos.py`. Os recálculos foram executados com `.venv/Scripts/python.exe`, usando aritmética decimal para `quantidade × preco_unitario` e pandas para reproduzir as agregações do código dos gráficos. A skill `validate-data` não está disponível neste ambiente; a verificação foi feita diretamente nos arquivos, sem integrações externas.

## Reconciliação de vendas
- Original: **182 linhas** e **180 identificadores de venda distintos**.
- O original contém **2 duplicatas exatas**. Somar as 182 linhas sem deduplicar dá R$ 20.066,00 e 550 unidades, incluindo essas repetições.
- Após deduplicar as linhas exatas do original: **180 vendas**, total recalculado de **R$ 20.059,00** e **548 unidades**.
- Cópia limpa: **180 linhas**, **180 vendas identificadas**, total da coluna `valor_venda` de **R$ 20.059,00** e **548 unidades**.
- `valor_venda` foi recalculado em cada linha limpa como `quantidade × preco_unitario`: **0 divergências**.

Assim, a quantidade de vendas da cópia limpa é **180**. As **548 unidades** são a soma das quantidades vendidas por item, uma medida diferente da contagem de vendas.

## Conferência das agregações
A soma abaixo foi refeita a partir de `papelaria_limpa.csv` e sua coluna `valor_venda`:

### Total por categoria
- Acessórios: **R$ 10.517,00**
- Livros: **R$ 7.438,00**
- Papelaria: **R$ 2.104,00**

**Soma das categorias: R$ 20.059,00**, igual ao total geral recalculado de **R$ 20.059,00**.

### Total por cidade
- Campinas: **R$ 8.578,00**
- Santos: **R$ 6.937,50**
- Sorocaba: **R$ 4.543,50**

A soma por cidade também é **R$ 20.059,00**, igual ao total geral.

## Código dos gráficos e conclusões
- `graficos.py` aponta para o arquivo local `papelaria_limpa.csv`, usa `valor_venda` e agrupa por `categoria` e `cidade`; não lê o original para produzir os gráficos.
- O código define o limite inferior do eixo vertical como zero, formata os valores como reais e intitula os gráficos como valor vendido.
- Os totais e as ordenações descritos anteriormente para categorias e cidades conferem com os recálculos. **Não encontrei erro numérico nas conclusões anteriores.**
- O valor de **R$ 20.066,00** corresponde à soma bruta do original com as duplicatas incluídas; para vendas sem duplicação, o total correto é **R$ 20.059,00**. Valor vendido é receita bruta calculada a partir de quantidade e preço unitário, **não lucro**.
