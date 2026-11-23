import json
from pathlib import Path

from sql_do_zero.cli import main
from sql_do_zero.corretor import conectar
from sql_do_zero.exercicios import EXERCICIOS
from sql_do_zero.lote import (
    achar_arquivos,
    carregar,
    corrigir_pasta,
    registrar,
    resumo_progresso,
)


def test_resumo_progresso_conta_acertos_e_media():
    dados = {"1": {"tentativas": 2, "acertou_em": 2}, "2": {"tentativas": 3, "acertou_em": None},
             "3": {"tentativas": 1, "acertou_em": 1}}
    r = resumo_progresso(dados, {1: "básico", 2: "básico", 3: "agrupar", 4: "agrupar"})
    assert r["acertados"] == [1, 3]
    assert r["pendentes"] == [2, 4]
    assert r["media_tentativas"] == 1.5
    assert r["por_nivel"] == {"básico": [2, 1], "agrupar": [2, 1]}


def test_resumo_progresso_vazio_e_json_quebrado(tmp_path):
    assert carregar(tmp_path / "nao-existe.json") == {}
    quebrado = tmp_path / "q.json"
    quebrado.write_text("{nao é json", encoding="utf-8")
    assert carregar(quebrado) == {}
    assert resumo_progresso({}, {1: "básico"})["media_tentativas"] is None


def test_cli_progresso(tmp_path, capsys):
    arq = tmp_path / "p.json"
    arq.write_text('{"1": {"tentativas": 1, "acertou_em": 1}}', encoding="utf-8")
    assert main(["progresso", str(arq)]) == 0
    saida = capsys.readouterr().out
    assert "1/40 exercícios resolvidos" in saida and "Próximo a tentar: 2" in saida
    assert main(["progresso", str(tmp_path / "x.json")]) == 2


def test_achar_arquivos_por_prefixo(tmp_path):
    (tmp_path / "07.sql").write_text("x")
    (tmp_path / "3-top.sql").write_text("x")
    (tmp_path / "notas.sql").write_text("x")
    assert sorted(achar_arquivos(tmp_path)) == [3, 7]


def test_corrigir_pasta_mistura_certo_errado_e_inexistente(tmp_path):
    (tmp_path / "1.sql").write_text(EXERCICIOS[0].gabarito)
    (tmp_path / "2.sql").write_text("select 1")
    (tmp_path / "999.sql").write_text("select 1")
    res = {n: ok for n, ok, _ in corrigir_pasta(conectar(), tmp_path)}
    assert res == {1: True, 2: False, 999: False}


def test_registrar_conta_ate_acertar(tmp_path):
    f = tmp_path / "t.json"
    registrar(f, 5, False)
    registrar(f, 5, True)
    registrar(f, 5, True)
    assert json.loads(f.read_text())["5"] == {"tentativas": 2, "acertou_em": 2}


def test_registrar_ignora_json_quebrado(tmp_path):
    f = tmp_path / "t.json"
    f.write_text("{quebrado")
    assert registrar(f, 1, False)["1"]["tentativas"] == 1


def test_cli_todos_e_tentativas(tmp_path, capsys):
    (tmp_path / "1.sql").write_text(EXERCICIOS[0].gabarito)
    t = tmp_path / "t.json"
    assert main(["corrigir", "--todos", str(tmp_path), "--tentativas", str(t)]) == 0
    assert "1/1 corretos" in capsys.readouterr().out
    assert json.loads(t.read_text())["1"]["acertou_em"] == 1


def test_cli_todos_pasta_vazia_ou_inexistente(tmp_path):
    assert main(["corrigir", "--todos", str(tmp_path)]) == 1
    assert main(["corrigir", "--todos", str(tmp_path / "nao")]) == 2
    assert main(["corrigir"]) == 2


def test_progresso_de_exemplo_roda_no_cli(capsys):
    exemplo = Path(__file__).resolve().parent.parent / "dados" / "progresso-exemplo.json"
    assert main(["progresso", str(exemplo)]) == 0
    saida = capsys.readouterr().out
    assert "4/40 exercícios resolvidos" in saida
    assert "Média de tentativas até acertar: 1.8" in saida
