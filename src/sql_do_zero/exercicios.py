"""Os 30 exercícios. Cada um tem enunciado, dica e a consulta de gabarito.

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
]
