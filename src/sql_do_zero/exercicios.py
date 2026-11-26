"""Os 90 exercícios. Cada um tem enunciado, dica e a consulta de gabarito.

Tabelas: `vagas(id, titulo, empresa, cidade, uf, modelo, nivel, publicada, fonte, url)`
e `vaga_skill(id, skill)` (`id` aponta para `vagas.id`).
`ordenado=True` quer dizer que a ordem das linhas também conta na correção.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Exercicio:
    numero: int
    nivel: str
    titulo: str
    enunciado: str
    dica: str
    gabarito: str
    ordenado: bool = False


EXERCICIOS: list[Exercicio] = [
    Exercicio(1, "básico", "Contar as vagas",
              "Quantas vagas existem na tabela `vagas`? Devolva uma coluna.",
              "COUNT(*)",
              "SELECT COUNT(*) FROM vagas"),
    Exercicio(2, "básico", "Vagas de estágio",
              "Liste `titulo` e `empresa` das vagas com `nivel` igual a 'estágio'.",
              "WHERE nivel = '...'",
              "SELECT titulo, empresa FROM vagas WHERE nivel = 'estágio'"),
    Exercicio(3, "básico", "Vagas remotas em ordem",
              "Liste `titulo` das vagas remotas, em ordem alfabética.",
              "ORDER BY titulo",
              "SELECT titulo FROM vagas WHERE modelo = 'remoto' ORDER BY titulo", True),
    Exercicio(4, "básico", "Empresas diferentes",
              "Quantas empresas diferentes têm vaga?",
              "COUNT(DISTINCT ...)",
              "SELECT COUNT(DISTINCT empresa) FROM vagas"),
    Exercicio(5, "básico", "Vagas com IA no título",
              "Liste `titulo` das vagas cujo título contém 'IA' ou 'Inteligência Artificial' "
              "(ignore maiúsculas e minúsculas só na segunda forma; 'IA' com letras maiúsculas).",
              "LIKE e ILIKE; cuidado: 'IA' também aparece dentro de outras palavras, "
              "então use ' IA ' com espaços ou compare com a palavra inteira.",
              "SELECT titulo FROM vagas WHERE titulo LIKE '% IA %' OR titulo LIKE '% IA' "
              "OR titulo ILIKE '%inteligência artificial%'"),
    Exercicio(6, "agrupar", "Vagas por nível",
              "Conte as vagas por `nivel`, da maior contagem para a menor. Colunas: `nivel`, `total`.",
              "GROUP BY e ORDER BY ... DESC",
              "SELECT nivel, COUNT(*) AS total FROM vagas GROUP BY nivel ORDER BY total DESC, nivel",
              True),
    Exercicio(7, "agrupar", "Vagas por modelo",
              "Conte as vagas por `modelo` (remoto, híbrido, presencial). Colunas: `modelo`, `total`.",
              "GROUP BY",
              "SELECT modelo, COUNT(*) AS total FROM vagas GROUP BY modelo"),
    Exercicio(8, "agrupar", "Empresas que mais contratam",
              "Liste as 5 empresas com mais vagas. Colunas: `empresa`, `total`. "
              "Desempate por nome da empresa.",
              "ORDER BY total DESC, empresa e LIMIT 5",
              "SELECT empresa, COUNT(*) AS total FROM vagas GROUP BY empresa "
              "ORDER BY total DESC, empresa LIMIT 5", True),
    Exercicio(9, "agrupar", "Empresas com 3 vagas ou mais",
              "Liste as empresas com 3 vagas ou mais. Colunas: `empresa`, `total`.",
              "HAVING filtra depois do GROUP BY",
              "SELECT empresa, COUNT(*) AS total FROM vagas GROUP BY empresa HAVING COUNT(*) >= 3"),
    Exercicio(10, "agrupar", "Vagas por dia",
              "Conte as vagas por data de `publicada`, da data mais recente para a mais antiga. "
              "Colunas: `publicada`, `total`.",
              "GROUP BY publicada",
              "SELECT publicada, COUNT(*) AS total FROM vagas GROUP BY publicada "
              "ORDER BY publicada DESC", True),
    Exercicio(11, "junção", "Skills da vaga 1",
              "Liste as skills da vaga de `id` 1, em ordem alfabética. Coluna: `skill`.",
              "tabela vaga_skill",
              "SELECT skill FROM vaga_skill WHERE id = 1 ORDER BY skill", True),
    Exercicio(12, "junção", "Vagas que pedem SQL",
              "Liste `titulo` e `empresa` das vagas que pedem a skill 'SQL'.",
              "JOIN vagas v ON v.id = s.id",
              "SELECT v.titulo, v.empresa FROM vagas v JOIN vaga_skill s ON s.id = v.id "
              "WHERE s.skill = 'SQL'"),
    Exercicio(13, "junção", "Skills mais pedidas",
              "As 10 skills mais pedidas. Colunas: `skill`, `total`. Desempate por nome da skill.",
              "GROUP BY skill",
              "SELECT skill, COUNT(*) AS total FROM vaga_skill GROUP BY skill "
              "ORDER BY total DESC, skill LIMIT 10", True),
    Exercicio(14, "junção", "SQL no nível júnior",
              "Quantas vagas de nível 'júnior/trainee' pedem SQL? Devolva uma coluna.",
              "JOIN e dois filtros no WHERE",
              "SELECT COUNT(*) FROM vagas v JOIN vaga_skill s ON s.id = v.id "
              "WHERE v.nivel = 'júnior/trainee' AND s.skill = 'SQL'"),
    Exercicio(15, "junção", "Vagas sem nenhuma skill",
              "Liste o `id` das vagas que não têm nenhuma skill registrada.",
              "LEFT JOIN ... WHERE s.id IS NULL (ou NOT EXISTS)",
              "SELECT v.id FROM vagas v LEFT JOIN vaga_skill s ON s.id = v.id WHERE s.id IS NULL"),
    Exercicio(16, "avançado", "Quantidade de skills por vaga",
              "Para cada vaga que tem skills, devolva `id` e `qtd` de skills, das vagas com "
              "mais skills para as com menos (desempate por `id`). Só as 5 primeiras.",
              "GROUP BY id, LIMIT",
              "SELECT id, COUNT(*) AS qtd FROM vaga_skill GROUP BY id ORDER BY qtd DESC, id LIMIT 5",
              True),
    Exercicio(17, "avançado", "Percentual de vagas remotas",
              "Qual o percentual de vagas remotas, com 1 casa decimal? Uma coluna chamada `pct`.",
              "AVG(CASE WHEN ... THEN 1.0 ELSE 0 END) e ROUND",
              "SELECT ROUND(100.0 * AVG(CASE WHEN modelo = 'remoto' THEN 1 ELSE 0 END), 1) AS pct "
              "FROM vagas"),
    Exercicio(18, "avançado", "Quem pede SQL e Python juntos",
              "Quantas vagas pedem SQL **e** Python ao mesmo tempo? Uma coluna.",
              "duas vezes o JOIN, ou GROUP BY id HAVING com SUM(CASE ...)",
              "SELECT COUNT(*) FROM (SELECT id FROM vaga_skill WHERE skill IN ('SQL', 'Python') "
              "GROUP BY id HAVING COUNT(DISTINCT skill) = 2)"),
    Exercicio(19, "avançado", "Skill mais pedida em cada nível",
              "Para cada `nivel`, qual é a skill mais pedida? Colunas: `nivel`, `skill`, `total`. "
              "Se empatar, fica a primeira em ordem alfabética.",
              "ROW_NUMBER() OVER (PARTITION BY nivel ORDER BY total DESC, skill)",
              "WITH c AS (SELECT v.nivel, s.skill, COUNT(*) AS total FROM vagas v "
              "JOIN vaga_skill s ON s.id = v.id GROUP BY v.nivel, s.skill), "
              "r AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY nivel ORDER BY total DESC, skill) AS pos "
              "FROM c) SELECT nivel, skill, total FROM r WHERE pos = 1"),
    Exercicio(20, "avançado", "Acumulado por dia",
              "Vagas publicadas por dia e o acumulado até o dia. Colunas: `publicada`, `total`, "
              "`acumulado`, em ordem de data.",
              "SUM(total) OVER (ORDER BY publicada)",
              "WITH d AS (SELECT publicada, COUNT(*) AS total FROM vagas GROUP BY publicada) "
              "SELECT publicada, total, CAST(SUM(total) OVER (ORDER BY publicada) AS BIGINT) AS acumulado "
              "FROM d ORDER BY publicada", True),
    Exercicio(21, "datas", "Última semana",
              "Quantas vagas foram publicadas nos 7 dias que terminam na data mais recente da tabela "
              "(inclusive)? Uma coluna.",
              "MAX(publicada) - INTERVAL 6 DAY",
              "SELECT COUNT(*) FROM vagas WHERE publicada >= (SELECT MAX(publicada) FROM vagas) - INTERVAL 6 DAY"),
    Exercicio(22, "datas", "Vagas por mês",
              "Quantas vagas por mês? Colunas: `mes` (texto AAAA-MM) e `total`, em ordem de mês.",
              "strftime(publicada, '%Y-%m')",
              "SELECT strftime(publicada, '%Y-%m') AS mes, COUNT(*) AS total FROM vagas "
              "GROUP BY mes ORDER BY mes", True),
    Exercicio(23, "datas", "Dia da semana mais cheio",
              "Em qual dia da semana (nome em inglês, como `dayname` devolve) saem mais vagas? "
              "Colunas: `dia` e `total`. Uma linha; se empatar, o primeiro em ordem alfabética.",
              "dayname(publicada), ORDER BY total DESC, dia LIMIT 1",
              "SELECT dayname(publicada) AS dia, COUNT(*) AS total FROM vagas "
              "GROUP BY dia ORDER BY total DESC, dia LIMIT 1", True),
    Exercicio(24, "datas", "Vagas do primeiro dia",
              "Liste `titulo` das vagas publicadas na data mais antiga da tabela, em ordem alfabética.",
              "subconsulta com MIN(publicada)",
              "SELECT titulo FROM vagas WHERE publicada = (SELECT MIN(publicada) FROM vagas) "
              "ORDER BY titulo", True),
    Exercicio(25, "subconsultas", "Empresas acima da média",
              "Quais empresas têm mais vagas que a média de vagas por empresa? Colunas: `empresa`, "
              "`total`; mais vagas primeiro, empate por nome.",
              "HAVING COUNT(*) > (SELECT AVG(n) FROM (...))",
              "SELECT empresa, COUNT(*) AS total FROM vagas GROUP BY empresa "
              "HAVING COUNT(*) > (SELECT AVG(n) FROM (SELECT COUNT(*) AS n FROM vagas GROUP BY empresa)) "
              "ORDER BY total DESC, empresa", True),
    Exercicio(26, "subconsultas", "Vagas sem skill",
              "Quantas vagas não têm nenhuma linha em `vaga_skill`? Uma coluna.",
              "NOT IN (SELECT id FROM vaga_skill)",
              "SELECT COUNT(*) FROM vagas WHERE id NOT IN (SELECT id FROM vaga_skill)"),
    Exercicio(27, "subconsultas", "Mais skills que a média",
              "Liste `titulo` e `empresa` das vagas com mais skills que a média de skills por vaga "
              "(considere só vagas que têm skill).",
              "subconsulta correlacionada e outra com COUNT(*) / COUNT(DISTINCT id)",
              "SELECT titulo, empresa FROM vagas v WHERE (SELECT COUNT(*) FROM vaga_skill s WHERE s.id = v.id) "
              "> (SELECT COUNT(*) * 1.0 / COUNT(DISTINCT id) FROM vaga_skill)"),
    Exercicio(28, "subconsultas", "Top 3 skills das vagas remotas",
              "As 3 skills mais pedidas nas vagas remotas. Colunas: `skill`, `total`; maior primeiro, "
              "empate por nome.",
              "WHERE id IN (SELECT id FROM vagas WHERE ...)",
              "SELECT skill, COUNT(*) AS total FROM vaga_skill "
              "WHERE id IN (SELECT id FROM vagas WHERE modelo = 'remoto') "
              "GROUP BY skill ORDER BY total DESC, skill LIMIT 3", True),
    Exercicio(29, "subconsultas", "SQL sem Python",
              "Quantas vagas pedem SQL mas **não** pedem Python? Uma coluna.",
              "EXISTS e NOT EXISTS",
              "SELECT COUNT(*) FROM vagas v WHERE EXISTS (SELECT 1 FROM vaga_skill s "
              "WHERE s.id = v.id AND s.skill = 'SQL') AND NOT EXISTS (SELECT 1 FROM vaga_skill s "
              "WHERE s.id = v.id AND s.skill = 'Python')"),
    Exercicio(30, "datas", "Média móvel de 3 dias",
              "Vagas por dia e a média das últimas 3 datas (a atual e as 2 anteriores), com 1 casa "
              "decimal. Colunas: `publicada`, `total`, `media3`, em ordem de data.",
              "AVG(total) OVER (ORDER BY publicada ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)",
              "WITH d AS (SELECT publicada, COUNT(*) AS total FROM vagas GROUP BY publicada) "
              "SELECT publicada, total, ROUND(AVG(total) OVER (ORDER BY publicada "
              "ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 1) AS media3 FROM d ORDER BY publicada", True),
    Exercicio(31, "agrupar", "Vagas por nível",
              "Quantas vagas há em cada `nivel`? Colunas: `nivel`, `total`; mais vagas primeiro, empate por nível.",
              "GROUP BY nivel",
              "SELECT nivel, COUNT(*) AS total FROM vagas GROUP BY nivel ORDER BY total DESC, nivel", True),
    Exercicio(32, "agrupar", "Skills de vagas júnior",
              "As 5 skills mais pedidas nas vagas de nível 'júnior/trainee'. Colunas: `skill`, `total`; "
              "maior primeiro, empate por nome.",
              "JOIN entre vagas e vaga_skill, filtrando nivel",
              "SELECT s.skill, COUNT(*) AS total FROM vaga_skill s JOIN vagas v ON v.id = s.id "
              "WHERE v.nivel = 'júnior/trainee' GROUP BY s.skill ORDER BY total DESC, s.skill LIMIT 5", True),
    Exercicio(33, "junção", "Vagas sem nenhuma skill",
              "Liste `titulo` das vagas que não têm linha em `vaga_skill`, em ordem alfabética. Use LEFT JOIN.",
              "LEFT JOIN ... WHERE s.id IS NULL",
              "SELECT v.titulo FROM vagas v LEFT JOIN vaga_skill s ON s.id = v.id "
              "WHERE s.id IS NULL ORDER BY v.titulo", True),
    Exercicio(34, "avançado", "Percentual de remotas",
              "Qual a porcentagem de vagas remotas, com 1 casa decimal? Uma coluna chamada `pct`.",
              "AVG(CASE WHEN ... THEN 1.0 ELSE 0 END) * 100",
              "SELECT ROUND(AVG(CASE WHEN modelo = 'remoto' THEN 1.0 ELSE 0 END) * 100, 1) AS pct FROM vagas"),
    Exercicio(35, "avançado", "Ranking de empresas",
              "Posição de cada empresa por número de vagas (empates com a mesma posição, sem pular números). "
              "Colunas: `empresa`, `total`, `posicao`; ordem por posição e nome. Só as 10 primeiras linhas.",
              "DENSE_RANK() OVER (ORDER BY COUNT(*) DESC)",
              "SELECT empresa, COUNT(*) AS total, DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS posicao "
              "FROM vagas GROUP BY empresa ORDER BY posicao, empresa LIMIT 10", True),
    Exercicio(36, "avançado", "Skill mais pedida por modelo",
              "Para cada `modelo` (remoto, híbrido, presencial), a skill mais pedida. Colunas: `modelo`, "
              "`skill`, `total`; ordem por modelo. Empate: vence a skill de menor nome.",
              "ROW_NUMBER() OVER (PARTITION BY modelo ORDER BY total DESC, skill)",
              "WITH c AS (SELECT v.modelo, s.skill, COUNT(*) AS total FROM vagas v JOIN vaga_skill s "
              "ON s.id = v.id GROUP BY v.modelo, s.skill), r AS (SELECT *, ROW_NUMBER() OVER "
              "(PARTITION BY modelo ORDER BY total DESC, skill) AS n FROM c) "
              "SELECT modelo, skill, total FROM r WHERE n = 1 ORDER BY modelo", True),
    Exercicio(37, "datas", "Vagas por semana",
              "Quantas vagas por semana (`strftime(publicada, '%Y-%W')`)? Colunas: `semana`, `total`, "
              "em ordem de semana.",
              "strftime(publicada, '%Y-%W')",
              "SELECT strftime(publicada, '%Y-%W') AS semana, COUNT(*) AS total "
              "FROM vagas GROUP BY semana ORDER BY semana", True),
    Exercicio(38, "datas", "Acumulado de vagas",
              "Vagas por dia e o total acumulado até aquele dia. Colunas: `publicada`, `total`, `acumulado`, "
              "em ordem de data.",
              "SUM(total) OVER (ORDER BY publicada)",
              "WITH d AS (SELECT publicada, COUNT(*) AS total FROM vagas GROUP BY publicada) "
              "SELECT publicada, total, CAST(SUM(total) OVER (ORDER BY publicada) AS INTEGER) AS acumulado "
              "FROM d ORDER BY publicada", True),
    Exercicio(39, "subconsultas", "Empresas só com vaga sênior",
              "Liste `empresa` das empresas em que TODAS as vagas são de nível 'sênior+', em ordem alfabética.",
              "GROUP BY empresa HAVING MIN(nivel) = MAX(nivel) ou NOT EXISTS",
              "SELECT empresa FROM vagas GROUP BY empresa "
              "HAVING SUM(CASE WHEN nivel = 'sênior+' THEN 0 ELSE 1 END) = 0 ORDER BY empresa", True),
    Exercicio(40, "subconsultas", "Pedem Python e SQL juntos",
              "Quantas vagas pedem Python **e** SQL ao mesmo tempo? Uma coluna.",
              "INTERSECT ou dois EXISTS",
              "SELECT COUNT(*) FROM (SELECT id FROM vaga_skill WHERE skill = 'Python' "
              "INTERSECT SELECT id FROM vaga_skill WHERE skill = 'SQL')"),
    Exercicio(41, "nulos", "Vagas sem cidade",
              "Quantas vagas têm `cidade` vazia (NULL)? Uma coluna.",
              "IS NULL (não use = NULL)",
              "SELECT COUNT(*) FROM vagas WHERE cidade IS NULL"),
    Exercicio(42, "nulos", "Cidade ou 'Remoto'",
              "Liste `empresa` e o local da vaga: a `cidade`, ou 'Remoto' quando não houver cidade. "
              "Colunas: `empresa`, `local`; só vagas com id até 12, em ordem de id.",
              "COALESCE(cidade, 'Remoto')",
              "SELECT empresa, COALESCE(cidade, 'Remoto') AS local FROM vagas WHERE id <= 12 ORDER BY id", True),
    Exercicio(43, "nulos", "Vagas sem nenhuma skill",
              "Liste `id` das vagas que não têm nenhuma linha em `vaga_skill`, em ordem de id.",
              "LEFT JOIN ... WHERE s.id IS NULL (ou NOT EXISTS)",
              "SELECT v.id FROM vagas v LEFT JOIN vaga_skill s ON s.id = v.id "
              "WHERE s.id IS NULL ORDER BY v.id", True),
    Exercicio(44, "subconsultas", "Mesma empresa, mesma cidade",
              "Quantos pares diferentes de vagas (a, b com a.id < b.id) são da mesma empresa e da mesma "
              "cidade? Uma coluna. (NULL não é igual a NULL: vagas sem cidade não formam par.)",
              "JOIN da tabela com ela mesma",
              "SELECT COUNT(*) FROM vagas a JOIN vagas b ON a.empresa = b.empresa AND a.cidade = b.cidade "
              "AND a.id < b.id"),
    Exercicio(45, "agrupar", "Skills por vaga",
              "Quantas skills a vaga média tem? Considere só vagas com ao menos uma skill; arredonde a "
              "1 casa. Coluna: `media`.",
              "COUNT(*) / COUNT(DISTINCT id)",
              "SELECT ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT id), 1) AS media FROM vaga_skill"),
    Exercicio(46, "datas", "Vagas de outubro",
              "Quantas vagas foram publicadas em outubro de 2026? Uma coluna.",
              "intervalo: >= '2026-10-01' e < '2026-11-01'",
              "SELECT COUNT(*) FROM vagas WHERE publicada >= '2026-10-01' AND publicada < '2026-11-01'"),
    Exercicio(47, "datas", "A vaga mais recente",
              "Qual é a data da vaga publicada mais recentemente? Coluna: `ultima`.",
              "MAX funciona com datas",
              "SELECT MAX(publicada) AS ultima FROM vagas"),
    Exercicio(48, "datas", "Vagas por mês",
              "Quantas vagas foram publicadas em cada mês? Colunas: `mes` (texto AAAA-MM) e `total`; "
              "em ordem de mês.",
              "strftime(CAST(publicada AS DATE), '%Y-%m')",
              "SELECT strftime(CAST(publicada AS DATE), '%Y-%m') AS mes, COUNT(*) AS total "
              "FROM vagas GROUP BY mes ORDER BY mes", True),
    Exercicio(49, "união", "Empresas em São Paulo ou remotas",
              "Quantas empresas diferentes têm vaga na cidade de 'São Paulo' ou no modelo 'remoto'? "
              "Uma coluna.",
              "UNION tira as repetidas",
              "SELECT COUNT(*) FROM (SELECT empresa FROM vagas WHERE cidade = 'São Paulo' "
              "UNION SELECT empresa FROM vagas WHERE modelo = 'remoto')"),
    Exercicio(50, "união", "UNION ou UNION ALL?",
              "Com as mesmas duas listas do exercício 49, quantas linhas a mais o UNION ALL devolve do que "
              "o UNION? Coluna: `repetidas`.",
              "UNION ALL mantém as repetidas",
              "SELECT (SELECT COUNT(*) FROM (SELECT empresa FROM vagas WHERE cidade = 'São Paulo' "
              "UNION ALL SELECT empresa FROM vagas WHERE modelo = 'remoto')) - "
              "(SELECT COUNT(*) FROM (SELECT empresa FROM vagas WHERE cidade = 'São Paulo' "
              "UNION SELECT empresa FROM vagas WHERE modelo = 'remoto')) AS repetidas"),
    Exercicio(51, "janelas", "Ranking de empresas",
              "Conte as vagas por empresa e numere as empresas da que tem mais vagas para a que tem menos, "
              "desempate por nome. Colunas: `empresa`, `total`, `posicao`; só as 5 primeiras posições.",
              "ROW_NUMBER() OVER (ORDER BY total DESC, empresa)",
              "SELECT empresa, total, posicao FROM (SELECT empresa, COUNT(*) AS total, "
              "ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC, empresa) AS posicao FROM vagas GROUP BY empresa) "
              "WHERE posicao <= 5 ORDER BY posicao", True),
    Exercicio(52, "janelas", "Vaga mais recente de cada empresa",
              "Para cada empresa com 3 vagas ou mais, devolva o `titulo` da vaga publicada mais recentemente "
              "(desempate por menor `id`). Colunas: `empresa`, `titulo`; ordem por empresa.",
              "ROW_NUMBER() OVER (PARTITION BY empresa ORDER BY publicada DESC, id)",
              "SELECT empresa, titulo FROM (SELECT empresa, titulo, "
              "ROW_NUMBER() OVER (PARTITION BY empresa ORDER BY publicada DESC, id) AS r, "
              "COUNT(*) OVER (PARTITION BY empresa) AS n FROM vagas) WHERE r = 1 AND n >= 3 "
              "ORDER BY empresa", True),
    Exercicio(53, "janelas", "Total acumulado por dia",
              "Quantas vagas foram publicadas por dia e quanto isso soma até aquele dia? "
              "Colunas: `dia`, `total`, `acumulado`; em ordem de dia.",
              "SUM(COUNT(*)) OVER (ORDER BY publicada)",
              "SELECT publicada AS dia, COUNT(*) AS total, "
              "SUM(COUNT(*)) OVER (ORDER BY publicada) AS acumulado "
              "FROM vagas GROUP BY publicada ORDER BY publicada", True),
    Exercicio(54, "janelas", "Skills por posição empatada",
              "Conte as vagas de cada skill e dê a `posicao` com RANK (empates dividem a mesma posição). "
              "Colunas: `skill`, `total`, `posicao`; só posição 3 ou melhor; ordem por posição e skill.",
              "RANK() OVER (ORDER BY COUNT(*) DESC)",
              "SELECT skill, total, posicao FROM (SELECT skill, COUNT(*) AS total, "
              "RANK() OVER (ORDER BY COUNT(*) DESC) AS posicao FROM vaga_skill GROUP BY skill) "
              "WHERE posicao <= 3 ORDER BY posicao, skill", True),
    Exercicio(55, "janelas", "Comparar com a vaga anterior",
              "Para as vagas publicadas em '2026-10-19', devolva `id` e `anterior`: o `id` da vaga logo antes "
              "(menor `id`) entre as mesmas vagas, ou NULL na primeira. Ordem por `id`.",
              "LAG(id) OVER (ORDER BY id), e o filtro vem antes da janela",
              "SELECT id, LAG(id) OVER (ORDER BY id) AS anterior FROM vagas "
              "WHERE publicada = '2026-10-19' ORDER BY id", True),
    Exercicio(56, "correlacionada", "Vagas com mais skills que a média",
              "Liste `id` das vagas que têm mais skills do que a média de skills por vaga (considere só "
              "vagas com ao menos uma skill). Ordem por `id`.",
              "subconsulta com AVG sobre uma contagem",
              "SELECT id FROM vaga_skill GROUP BY id HAVING COUNT(*) > "
              "(SELECT AVG(n) FROM (SELECT COUNT(*) AS n FROM vaga_skill GROUP BY id)) ORDER BY id", True),
    Exercicio(57, "correlacionada", "Vagas mais novas que a média da empresa",
              "Liste `id` das vagas publicadas depois da data média de publicação da própria "
              "empresa. Use `CAST(publicada AS DATE)` e compare com `AVG(epoch(...))`. Ordem por `id`.",
              "subconsulta correlacionada: WHERE v2.empresa = v.empresa",
              "SELECT v.id FROM vagas v WHERE epoch(CAST(v.publicada AS DATE)) > "
              "(SELECT AVG(epoch(CAST(v2.publicada AS DATE))) FROM vagas v2 WHERE v2.empresa = v.empresa) "
              "ORDER BY v.id", True),
    Exercicio(58, "correlacionada", "Vagas que pedem Python",
              "Quantas vagas têm a skill 'Python'? Resolva com EXISTS, não com JOIN. Uma coluna.",
              "WHERE EXISTS (SELECT 1 FROM vaga_skill s WHERE s.id = v.id AND ...)",
              "SELECT COUNT(*) FROM vagas v WHERE EXISTS "
              "(SELECT 1 FROM vaga_skill s WHERE s.id = v.id AND s.skill = 'Python')"),
    Exercicio(59, "correlacionada", "Vagas sem SQL nem Python",
              "Quantas vagas NÃO têm a skill 'SQL' nem a skill 'Python'? Resolva com NOT EXISTS. Uma coluna.",
              "NOT EXISTS com skill IN ('SQL', 'Python')",
              "SELECT COUNT(*) FROM vagas v WHERE NOT EXISTS "
              "(SELECT 1 FROM vaga_skill s WHERE s.id = v.id AND s.skill IN ('SQL', 'Python'))"),
    Exercicio(60, "correlacionada", "A primeira vaga de cada empresa",
              "Liste `id` da vaga de menor `id` de cada empresa, sem usar janela: use uma subconsulta "
              "correlacionada com MIN. Ordem por `id`.",
              "WHERE id = (SELECT MIN(id) FROM vagas v2 WHERE v2.empresa = v.empresa)",
              "SELECT v.id FROM vagas v WHERE v.id = "
              "(SELECT MIN(v2.id) FROM vagas v2 WHERE v2.empresa = v.empresa) ORDER BY v.id", True),
    Exercicio(61, "agregação filtrada", "Remotas e híbridas numa linha",
              "Numa única consulta, devolva duas colunas: quantas vagas são `remoto` e quantas são `híbrido`.",
              "COUNT(*) FILTER (WHERE ...)",
              "SELECT COUNT(*) FILTER (WHERE modelo = 'remoto'), "
              "COUNT(*) FILTER (WHERE modelo = 'híbrido') FROM vagas"),
    Exercicio(62, "agregação filtrada", "Empresas com 3 ou mais vagas",
              "Liste `empresa` e a quantidade de vagas das empresas com 3 ou mais vagas. "
              "Ordem: mais vagas primeiro, depois `empresa`.",
              "GROUP BY empresa HAVING COUNT(*) >= 3",
              "SELECT empresa, COUNT(*) FROM vagas GROUP BY empresa HAVING COUNT(*) >= 3 "
              "ORDER BY 2 DESC, empresa", True),
    Exercicio(63, "agregação filtrada", "Remotas por nível",
              "Para cada `nivel`, devolva o nível e quantas vagas remotas ele tem, usando FILTER. "
              "Ordem por `nivel`.",
              "COUNT(*) FILTER (WHERE modelo = 'remoto') com GROUP BY nivel",
              "SELECT nivel, COUNT(*) FILTER (WHERE modelo = 'remoto') FROM vagas GROUP BY nivel "
              "ORDER BY nivel", True),
    Exercicio(64, "agregação filtrada", "Skills raras",
              "Liste as `skill` que aparecem em no máximo 5 vagas. Ordem alfabética.",
              "GROUP BY skill HAVING COUNT(*) <= 5",
              "SELECT skill FROM vaga_skill GROUP BY skill HAVING COUNT(*) <= 5 ORDER BY skill", True),
    Exercicio(65, "agregação filtrada", "Estados sem vaga remota",
              "Liste os `uf` (ignore nulos) que têm vagas presenciais mas nenhuma vaga remota. "
              "Ordem alfabética.",
              "HAVING COUNT(*) FILTER (WHERE ...) = 0 e COUNT(*) FILTER (WHERE ...) > 0",
              "SELECT uf FROM vagas WHERE uf IS NOT NULL GROUP BY uf "
              "HAVING COUNT(*) FILTER (WHERE modelo = 'remoto') = 0 "
              "AND COUNT(*) FILTER (WHERE modelo = 'presencial') > 0 ORDER BY uf", True),
    Exercicio(66, "agregação filtrada", "Empresas que misturam modelos",
              "Liste `empresa` das empresas que publicaram vagas em 2 ou mais `modelo` diferentes. "
              "Ordem alfabética.",
              "HAVING COUNT(DISTINCT modelo) >= 2",
              "SELECT empresa FROM vagas GROUP BY empresa HAVING COUNT(DISTINCT modelo) >= 2 "
              "ORDER BY empresa", True),
    Exercicio(67, "agregação filtrada", "Skill mais comum por nível",
              "Para o nível `estágio`, liste `skill` e quantas vagas de estágio pedem a skill, só as que "
              "aparecem em 2 ou mais vagas. Ordem: mais vagas primeiro, depois `skill`.",
              "JOIN vagas com vaga_skill, WHERE nivel = 'estágio', HAVING COUNT(*) >= 2",
              "SELECT s.skill, COUNT(*) FROM vagas v JOIN vaga_skill s ON s.id = v.id "
              "WHERE v.nivel = 'estágio' GROUP BY s.skill HAVING COUNT(*) >= 2 "
              "ORDER BY 2 DESC, s.skill", True),
    Exercicio(68, "agregação filtrada", "Média de skills por modelo",
              "Para cada `modelo`, devolva o modelo e a média de skills por vaga, arredondada para 2 casas "
              "(considere só vagas com ao menos uma skill). Ordem por `modelo`.",
              "contar skills por vaga numa subconsulta e fazer AVG por modelo",
              "SELECT modelo, ROUND(AVG(n), 2) FROM (SELECT v.modelo, COUNT(*) AS n FROM vagas v "
              "JOIN vaga_skill s ON s.id = v.id GROUP BY v.id, v.modelo) GROUP BY modelo ORDER BY modelo",
              True),
    Exercicio(69, "agregação filtrada", "Dias com mais de 10 vagas",
              "Liste `publicada` (como data, `CAST(publicada AS DATE)`) e a quantidade de vagas nos dias "
              "com mais de 10 vagas publicadas. Ordem por data.",
              "GROUP BY CAST(publicada AS DATE) HAVING COUNT(*) > 10",
              "SELECT CAST(publicada AS DATE) AS dia, COUNT(*) FROM vagas "
              "GROUP BY dia HAVING COUNT(*) > 10 ORDER BY dia", True),
    Exercicio(70, "agregação filtrada", "Júnior ou estágio por empresa",
              "Para cada empresa com ao menos 1 vaga `estágio` ou `júnior/trainee`, devolva `empresa` e "
              "quantas vagas de entrada ela tem (use FILTER com IN). Ordem: mais vagas primeiro, "
              "depois `empresa`.",
              "FILTER (WHERE nivel IN (...)) e HAVING sobre o mesmo filtro",
              "SELECT empresa, COUNT(*) FILTER (WHERE nivel IN ('estágio', 'júnior/trainee')) "
              "FROM vagas GROUP BY empresa "
              "HAVING COUNT(*) FILTER (WHERE nivel IN ('estágio', 'júnior/trainee')) >= 1 "
              "ORDER BY 2 DESC, empresa", True),
    Exercicio(71, "cte", "Empresas acima da média",
              "Liste `empresa` e quantas vagas ela tem, só das empresas com mais vagas que a média "
              "por empresa. Use WITH. Ordem: mais vagas primeiro, depois `empresa`.",
              "WITH por_empresa AS (...) e compare com (SELECT AVG(n) FROM por_empresa)",
              "WITH por_empresa AS (SELECT empresa, COUNT(*) AS n FROM vagas GROUP BY empresa) "
              "SELECT empresa, n FROM por_empresa WHERE n > (SELECT AVG(n) FROM por_empresa) "
              "ORDER BY n DESC, empresa", True),
    Exercicio(72, "cte", "Skills das vagas remotas",
              "Use um WITH com os `id` das vagas remotas e liste as 5 `skill` mais pedidas nelas, com "
              "a contagem. Ordem: mais vagas primeiro, depois `skill`.",
              "WITH remotas AS (SELECT id ...) JOIN vaga_skill, LIMIT 5",
              "WITH remotas AS (SELECT id FROM vagas WHERE modelo = 'remoto') "
              "SELECT s.skill, COUNT(*) FROM vaga_skill s JOIN remotas r ON r.id = s.id "
              "GROUP BY s.skill ORDER BY 2 DESC, s.skill LIMIT 5", True),
    Exercicio(73, "cte", "Duas CTEs: total e remotas por nível",
              "Com duas CTEs, devolva `nivel`, o total de vagas do nível e quantas delas são remotas "
              "(0 se nenhuma). Ordem por `nivel`.",
              "uma CTE com o total, outra com as remotas, LEFT JOIN e COALESCE",
              "WITH total AS (SELECT nivel, COUNT(*) AS n FROM vagas GROUP BY nivel), "
              "rem AS (SELECT nivel, COUNT(*) AS n FROM vagas WHERE modelo = 'remoto' GROUP BY nivel) "
              "SELECT t.nivel, t.n, COALESCE(r.n, 0) FROM total t LEFT JOIN rem r ON r.nivel = t.nivel "
              "ORDER BY t.nivel", True),
    Exercicio(74, "cte", "Empresa líder de cada nível",
              "Para cada `nivel`, devolva a empresa com mais vagas nele e a quantidade (em empate, a "
              "primeira em ordem alfabética). Ordem por `nivel`.",
              "CTE que conta por nivel e empresa, outra com ROW_NUMBER() OVER (PARTITION BY nivel ...)",
              "WITH c AS (SELECT nivel, empresa, COUNT(*) AS n FROM vagas GROUP BY nivel, empresa), "
              "r AS (SELECT nivel, empresa, n, ROW_NUMBER() OVER (PARTITION BY nivel "
              "ORDER BY n DESC, empresa) AS rn FROM c) "
              "SELECT nivel, empresa, n FROM r WHERE rn = 1 ORDER BY nivel", True),
    Exercicio(75, "cte", "Dias acima da média",
              "Liste os dias (`CAST(publicada AS DATE)`) com mais vagas que a média diária, com a "
              "quantidade. Ordem por data.",
              "WITH d AS (SELECT CAST(publicada AS DATE) AS dia, COUNT(*) AS n ...)",
              "WITH d AS (SELECT CAST(publicada AS DATE) AS dia, COUNT(*) AS n FROM vagas GROUP BY dia) "
              "SELECT dia, n FROM d WHERE n > (SELECT AVG(n) FROM d) ORDER BY dia", True),
    Exercicio(76, "rollup", "Vagas por modelo com total",
              "Devolva `modelo` e a quantidade de vagas, mais uma linha final com o total geral "
              "(`modelo` NULL). Use GROUP BY ROLLUP. Ordem: modelos em ordem alfabética, total por último.",
              "GROUP BY ROLLUP(modelo) e ORDER BY GROUPING(modelo), modelo",
              "SELECT modelo, COUNT(*) FROM vagas GROUP BY ROLLUP(modelo) "
              "ORDER BY GROUPING(modelo), modelo", True),
    Exercicio(77, "rollup", "Nível e modelo com subtotais",
              "Devolva `nivel`, `modelo` e a quantidade, com subtotal por nível e total geral "
              "(GROUP BY ROLLUP(nivel, modelo)). Ordem: GROUPING(nivel), nivel, GROUPING(modelo), modelo.",
              "ROLLUP(nivel, modelo) gera os subtotais por nivel e o total",
              "SELECT nivel, modelo, COUNT(*) FROM vagas GROUP BY ROLLUP(nivel, modelo) "
              "ORDER BY GROUPING(nivel), nivel, GROUPING(modelo), modelo", True),
    Exercicio(78, "rollup", "Rótulo TOTAL",
              "Como o 76, mas troque o NULL do total geral pelo texto 'TOTAL' na coluna `modelo`. "
              "Ordem: modelos em ordem alfabética, 'TOTAL' por último.",
              "COALESCE(modelo, 'TOTAL') e ORDER BY GROUPING(modelo), modelo",
              "SELECT COALESCE(modelo, 'TOTAL') AS modelo, COUNT(*) FROM vagas GROUP BY ROLLUP(modelo) "
              "ORDER BY GROUPING(modelo), modelo", True),
    Exercicio(79, "cte", "Sequência com WITH RECURSIVE",
              "Gere os números de 1 a 5 com `WITH RECURSIVE` e devolva cada número e o seu quadrado. "
              "Ordem pelo número.",
              "WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 5)",
              "WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 5) "
              "SELECT i, i * i FROM n ORDER BY i", True),
    Exercicio(80, "rollup", "Remotas por estado com total",
              "Use um WITH com as vagas remotas que têm `uf` e devolva `uf`, a quantidade e uma linha "
              "final com o total (ROLLUP). Ordem: estados com mais vagas primeiro, depois `uf`, total por último.",
              "WITH rem AS (...) SELECT uf, COUNT(*) FROM rem GROUP BY ROLLUP(uf)",
              "WITH rem AS (SELECT uf FROM vagas WHERE modelo = 'remoto' AND uf IS NOT NULL) "
              "SELECT uf, COUNT(*) FROM rem GROUP BY ROLLUP(uf) "
              "ORDER BY GROUPING(uf), 2 DESC, uf", True),
    Exercicio(81, "derivadas", "Média de vagas por empresa",
              "Qual a média de vagas por empresa? Use uma subconsulta no FROM que conta por empresa. "
              "Uma coluna, arredondada para 2 casas.",
              "SELECT ROUND(AVG(n), 2) FROM (SELECT COUNT(*) AS n ... GROUP BY empresa) t",
              "SELECT ROUND(AVG(n), 2) FROM (SELECT COUNT(*) AS n FROM vagas GROUP BY empresa) t"),
    Exercicio(82, "derivadas", "Recorde de vagas de uma empresa",
              "Quantas vagas tem a empresa que mais contrata? Use uma subconsulta no FROM. Uma coluna.",
              "MAX(n) sobre uma tabela derivada que conta por empresa",
              "SELECT MAX(n) FROM (SELECT COUNT(*) AS n FROM vagas GROUP BY empresa) t"),
    Exercicio(83, "derivadas", "Empresas por tamanho",
              "Quantas empresas têm 1 vaga, 2 vagas, 3 vagas...? Colunas: `vagas` e `empresas`. "
              "Ordem por `vagas`.",
              "agrupe duas vezes: primeiro por empresa (no FROM), depois pelo número de vagas",
              "SELECT n AS vagas, COUNT(*) AS empresas FROM "
              "(SELECT empresa, COUNT(*) AS n FROM vagas GROUP BY empresa) t GROUP BY n ORDER BY n", True),
    Exercicio(84, "derivadas", "Skills por vaga, em média",
              "Em média, quantas skills cada vaga pede (considere só vagas que aparecem em `vaga_skill`)? "
              "Uma coluna, arredondada para 2 casas.",
              "conte por id numa subconsulta no FROM e tire a média",
              "SELECT ROUND(AVG(k), 2) FROM (SELECT COUNT(*) AS k FROM vaga_skill GROUP BY id) t"),
    Exercicio(85, "derivadas", "Vagas com 5 skills ou mais",
              "Quantas vagas pedem 5 skills ou mais? Use uma subconsulta no FROM com HAVING. Uma coluna.",
              "SELECT COUNT(*) FROM (SELECT id FROM vaga_skill GROUP BY id HAVING COUNT(*) >= 5) t",
              "SELECT COUNT(*) FROM (SELECT id FROM vaga_skill GROUP BY id HAVING COUNT(*) >= 5) t"),
    Exercicio(86, "derivadas", "Vagas que pedem SQL (IN)",
              "Liste `titulo` e `empresa` das vagas que pedem a skill 'SQL', usando IN com subconsulta "
              "(sem JOIN). Ordem: `empresa`, depois `titulo`.",
              "WHERE id IN (SELECT id FROM vaga_skill WHERE skill = '...')",
              "SELECT titulo, empresa FROM vagas WHERE id IN (SELECT id FROM vaga_skill WHERE skill = 'SQL') "
              "ORDER BY empresa, titulo", True),
    Exercicio(87, "derivadas", "Empresas sem vaga remota (NOT IN)",
              "Quantas empresas diferentes não têm nenhuma vaga remota? Use NOT IN com subconsulta. "
              "Uma coluna.",
              "NOT IN quebra se a subconsulta devolver NULL: filtre IS NOT NULL dentro dela",
              "SELECT COUNT(DISTINCT empresa) FROM vagas WHERE empresa NOT IN "
              "(SELECT empresa FROM vagas WHERE modelo = 'remoto' AND empresa IS NOT NULL)"),
    Exercicio(88, "derivadas", "Empresas líderes (>= ALL)",
              "Liste a(s) `empresa`(s) com o maior número de vagas, usando `>= ALL` com subconsulta "
              "no HAVING. Ordem por `empresa`.",
              "HAVING COUNT(*) >= ALL (SELECT COUNT(*) FROM vagas GROUP BY empresa)",
              "SELECT empresa FROM vagas GROUP BY empresa "
              "HAVING COUNT(*) >= ALL (SELECT COUNT(*) FROM vagas GROUP BY empresa) ORDER BY empresa", True),
    Exercicio(89, "derivadas", "Vagas de quem contrata estagiário",
              "Quantas vagas pertencem a empresas que têm pelo menos uma vaga de `estágio`? Use IN. "
              "Uma coluna.",
              "WHERE empresa IN (SELECT empresa FROM vagas WHERE nivel = '...')",
              "SELECT COUNT(*) FROM vagas WHERE empresa IN (SELECT empresa FROM vagas WHERE nivel = 'estágio')"),
    Exercicio(90, "derivadas", "Skills acima da média de pedidos",
              "Liste `skill` e em quantas vagas aparece, só das skills pedidas em mais vagas que a média "
              "por skill. Ordem: mais vagas primeiro, depois `skill`.",
              "tabela derivada no FROM e, no WHERE, uma subconsulta que também calcula a média",
              "SELECT skill, n FROM (SELECT skill, COUNT(*) AS n FROM vaga_skill GROUP BY skill) t "
              "WHERE n > (SELECT AVG(c) FROM (SELECT COUNT(*) AS c FROM vaga_skill GROUP BY skill) u) "
              "ORDER BY n DESC, skill", True),
]
