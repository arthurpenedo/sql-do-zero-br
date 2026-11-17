# sql-do-zero-br

![CI](https://github.com/arthurpenedo/sql-do-zero-br/actions/workflows/ci.yml/badge.svg)

20 exercícios de SQL sobre **vagas reais de tecnologia**, com correção automática em DuckDB. Zero instalação de banco, zero custo.

## O problema

SQL aparece em 87 das 214 vagas do conjunto de dados (41%) e é pedido em 50% das vagas de nível júnior do
[radar-skills-br](https://github.com/arthurpenedo/radar-skills-br). Praticar com tabelas de "funcionários e departamentos"
é chato; aqui as perguntas são as de quem procura emprego: qual skill mais cai em vaga júnior? qual empresa mais contrata?

## O que faz

- 20 exercícios em 4 níveis: **básico** (SELECT, WHERE, ORDER BY), **agrupar** (GROUP BY, HAVING),
  **junção** (JOIN, LEFT JOIN) e **avançado** (CASE, CTE, funções de janela).
- Duas tabelas: `vagas` (214 linhas) e `vaga_skill` (uma linha por vaga e skill), dados públicos do radar em 19/10/2026.
- Corretor: roda a sua consulta e o gabarito, compara colunas, linhas e valores e diz **onde** diferiu.
  Se o exercício não pede ordem, a ordem das linhas não conta.
- Só aceita `SELECT`/`WITH`: `DROP`, `DELETE` e vários comandos na mesma consulta são barrados.

## Como rodar

```bash
pip install -e ".[dev]"
sql-do-zero listar            # os 20 exercícios
sql-do-zero ver 6             # enunciado e dica
sql-do-zero corrigir 6 minha.sql
sql-do-zero gabarito 6        # só depois de tentar
sql-do-zero medir             # confere que os 20 gabaritos se corrigem sozinhos
```

## Números medidos

- 20/20 gabaritos corrigem como corretos (`sql-do-zero medir`); 32 testes passando, rodando no CI (Python 3.11 e 3.13).
- Dados: 214 vagas, 129 empresas, 69 remotas (32,2%).

## Limites

- Os dados são uma foto de 19/10/2026; as respostas dos gabaritos mudam se você trocar os CSVs em `dados/`.
- O corretor compara resultados, não o jeito de escrever: duas consultas diferentes que dão a mesma tabela valem.
- Bloqueio de comandos por palavra: é uma trava didática, não uma barreira de segurança. Os dados são cópias em memória.

## Licença

MIT.
