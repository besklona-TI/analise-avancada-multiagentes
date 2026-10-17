# Dashboard de vendas da papelaria

Projeto estático que prepara os dados de `papelaria_limpa.csv` com Python e pandas e os apresenta em um dashboard interativo. Cada linha corresponde a uma venda; os indicadores e as limitações estão explicados em [ANALISE.md](ANALISE.md).

No PowerShell, abra o terminal nesta pasta (`projeto-dashboard`). Os comandos abaixo usam o Python do ambiente `.venv` quando ele existe; sem esse ambiente, usam o `python` disponível no Windows (que precisa ter pandas instalado):

```powershell
if (Test-Path -LiteralPath '..\.venv\Scripts\python.exe') { ..\.venv\Scripts\python.exe preparar_dados.py } else { python preparar_dados.py }
if (Test-Path -LiteralPath '..\.venv\Scripts\python.exe') { ..\.venv\Scripts\python.exe -m unittest discover -s tests -v } else { python -m unittest discover -s tests -v }
python -m http.server 8000 --directory site
```

Abra `http://localhost:8000` no navegador. Para encerrar o servidor, pressione `Ctrl+C` no terminal. A pasta `site/` contém HTML, CSS, JavaScript e dados e é a pasta publicável em uma hospedagem estática. Para refazer os dados depois de atualizar a fonte, execute novamente o primeiro comando. A preparação valida a cópia limpa sem alterar `papelaria_limpa.csv`.
