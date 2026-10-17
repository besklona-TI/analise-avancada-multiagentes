# Análise avançada multiagentes

Repositório com as skills de exploração, visualização e validação de dados, fluxos de trabalho e um dashboard estático de vendas de papelaria.

## Conteúdo

- [`AGENTS.md`](AGENTS.md): orientações e fluxo de trabalho dos agentes Construtor, Tester e Revisor.
- [Skills](.opencode/skills/): `explore-data`, `data-visualization` e `validate-data`.
- [Projeto do dashboard](projeto-dashboard/README.md): preparação, testes e instruções para abrir o site.
- [Relatórios](projeto-dashboard/relatorios/FINAL.md): status final e histórico das rodadas, somente em Markdown.
- [GitHub Actions](.github/workflows/dashboard-ci.yml): testes automatizados em push e pull request.

Os arquivos `.venv/`, `node_modules/`, caches Python e saídas não Markdown na pasta de relatórios são ignorados pelo Git. As fontes CSV permanecem incluídas para reproduzir a análise.

## Rodar localmente

Abra `projeto-dashboard/` no VS Code e siga os comandos do [README do dashboard](projeto-dashboard/README.md). A pasta `projeto-dashboard/site/` é publicável como site estático.
