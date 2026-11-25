# sql-do-zero-br

![CI](https://github.com/arthurpenedo/sql-do-zero-br/actions/workflows/ci.yml/badge.svg)

70 exercícios de SQL sobre **vagas reais de tecnologia**, com correção automática em DuckDB. Zero instalação de banco, zero custo.

## O problema

SQL aparece em 87 das 214 vagas do conjunto de dados (41%) e é pedido em 50% das vagas de nível júnior do
[radar-skills-br](https://github.com/arthurpenedo/radar-skills-br). Praticar com tabelas de "funcionários e departamentos"
é chato; aqui as perguntas são as de quem procura emprego: qual skill mais cai em vaga júnior? qual empresa mais contrata?

## O que faz

- 70 exercícios em 11 níveis (os novos: **janelas**: ROW_NUMBER, RANK, LAG, soma acumulada; **correlacionada**: subconsulta correlacionada, EXISTS e NOT EXISTS; antes: **nulos**: IS NULL, COALESCE, auto-junção; **união**: UNION e UNION ALL): **básico** (SELECT, WHERE, ORDER BY), **agrupar** (GROUP BY, HAVING),
  **junção** (JOIN, LEFT JOIN), **avançado** (CASE, CTE, funções de janela), **datas** (intervalos,
  `strftime`, média móvel) e **subconsultas** (IN, EXISTS, correlacionadas).
- Página estática com os enunciados e o gabarito escondido (`sql-do-zero demo`), publicada pelo `pagina.yml`. Tem filtro por nível feito só com CSS (sem JavaScript).
- Duas tabelas: `vagas` (214 linhas) e `vaga_skill` (uma linha por vaga e skill), dados públicos do radar em 19/10/2026.
- Corretor: roda a sua consulta e o gabarito, compara colunas, linhas e valores e diz **onde** diferiu.
  Se o exercício não pede ordem, a ordem das linhas não conta.
- Só aceita `SELECT`/`WITH`: `DROP`, `DELETE` e vários comandos na mesma consulta são barrados.

## Como rodar

```bash
pip install -e ".[dev]"
sql-do-zero listar            # os 70 exercícios
sql-do-zero niveis            # os 10 níveis, com contagem e números
sql-do-zero ver 6             # enunciado e dica
sql-do-zero corrigir 6 minha.sql
# corrige uma pasta inteira (arquivos 01.sql, 7-top.sql...) e conta as tentativas
sql-do-zero corrigir --todos respostas/ --tentativas progresso.json
sql-do-zero gabarito 6        # só depois de tentar
sql-do-zero progresso progresso.json   # acertos, pendentes e média de tentativas por nível
sql-do-zero medir             # confere que os 70 gabaritos se corrigem sozinhos
sql-do-zero demo              # gera site/index.html (enunciados, gabarito escondido)
```

### Os 10 níveis (`sql-do-zero niveis` imprime o mesmo)

| Nível | Exercícios | Números |
|---|---|---|
| básico | 5 | 1, 2, 3, 4, 5 |
| agrupar | 8 | 6, 7, 8, 9, 10, 31, 32, 45 |
| junção | 6 | 11, 12, 13, 14, 15, 33 |
| avançado | 8 | 16, 17, 18, 19, 20, 34, 35, 36 |
| datas | 10 | 21, 22, 23, 24, 30, 37, 38, 46, 47, 48 |
| subconsultas | 8 | 25, 26, 27, 28, 29, 39, 40, 44 |
| nulos | 3 | 41, 42, 43 |
| união | 2 | 49, 50 |
| janelas | 5 | 51, 52, 53, 54, 55 |
| correlacionada | 5 | 56, 57, 58, 59, 60 |
| agregação filtrada | 10 | 61, 62, 63, 64, 65, 66, 67, 68, 69, 70 |

### Exemplo do `progresso`

Para testar sem resolver nada, use o arquivo pronto: `sql-do-zero progresso dados/progresso-exemplo.json` (4 resolvidos, 1 pendente).

Com um `progresso.json` em que o 1 e o 6 foram resolvidos e o 12 ainda não:

```text
2/70 exercícios resolvidos
  básico        1/5
  agrupar       1/7
  junção        0/6
  avançado      0/8
  datas         0/7
  subconsultas  0/7
Média de tentativas até acertar: 2.0
Próximo a tentar: 2, 3, 4, 5, 7
```

## Números medidos

- 70/70 gabaritos corrigem como corretos (`sql-do-zero medir`); 103 testes passando, rodando no CI (Python 3.11 e 3.13).
- Dados: 214 vagas, 129 empresas, 69 remotas (32,2%).

## Limites

- Os dados são uma foto de 19/10/2026; as respostas dos gabaritos mudam se você trocar os CSVs em `dados/`.
- O corretor compara resultados, não o jeito de escrever: duas consultas diferentes que dão a mesma tabela valem.
- Bloqueio de comandos por palavra: é uma trava didática, não uma barreira de segurança. Os dados são cópias em memória.

## Licença

MIT.
