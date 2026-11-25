"""Correção em lote (`corrigir --todos`) e contagem de tentativas por exercício."""

import json
import re
from pathlib import Path

from .corretor import buscar, corrigir

_NUM = re.compile(r"^(\d+)")


def achar_arquivos(pasta: Path) -> dict[int, Path]:
    """Mapeia número -> arquivo .sql cujo nome começa com o número (`07.sql`, `7-top.sql`)."""
    achados: dict[int, Path] = {}
    for arq in sorted(pasta.glob("*.sql")):
        m = _NUM.match(arq.stem)
        if m:
            achados.setdefault(int(m.group(1)), arq)
    return achados


def corrigir_pasta(con, pasta: Path) -> list[tuple[int, bool, str]]:
    """Corrige cada arquivo da pasta. Número inexistente vira linha com erro, sem derrubar o lote."""
    linhas = []
    for numero, arq in sorted(achar_arquivos(pasta).items()):
        try:
            ex = buscar(numero)
        except KeyError as e:
            linhas.append((numero, False, e.args[0]))
            continue
        r = corrigir(con, ex, arq.read_text(encoding="utf-8"))
        linhas.append((numero, r.ok, r.mensagem))
    return linhas


def registrar(arquivo: Path, numero: int, ok: bool) -> dict:
    """Soma uma tentativa no JSON; guarda também em qual tentativa acertou."""
    dados = {}
    if arquivo.is_file():
        try:
            dados = json.loads(arquivo.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            dados = {}
    reg = dados.setdefault(str(numero), {"tentativas": 0, "acertou_em": None})
    if reg["acertou_em"] is None:
        reg["tentativas"] += 1
        if ok:
            reg["acertou_em"] = reg["tentativas"]
    arquivo.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
    return dados


def carregar(arquivo: Path) -> dict:
    """Lê o JSON de tentativas; arquivo ausente ou quebrado vira dicionário vazio."""
    if not arquivo.is_file():
        return {}
    try:
        dados = json.loads(arquivo.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return dados if isinstance(dados, dict) else {}


def resumo_progresso(dados: dict, niveis: dict[int, str]) -> dict:
    """Resume o progresso: acertados, pendentes, média de tentativas e acertos por nível.

    `niveis` mapeia número do exercício -> nível; números fora dele são ignorados.
    """
    acertados, pendentes, tentativas_acerto = [], [], []
    por_nivel: dict[str, list[int]] = {}
    for numero, nivel in sorted(niveis.items()):
        reg = dados.get(str(numero))
        feito = isinstance(reg, dict) and reg.get("acertou_em") is not None
        (acertados if feito else pendentes).append(numero)
        total, ok = por_nivel.get(nivel, [0, 0])
        por_nivel[nivel] = [total + 1, ok + feito]
        if feito:
            tentativas_acerto.append(reg["acertou_em"])
    media = round(sum(tentativas_acerto) / len(tentativas_acerto), 1) if tentativas_acerto else None
    return {"acertados": acertados, "pendentes": pendentes, "media_tentativas": media, "por_nivel": por_nivel}


def agrupar_por_nivel(exercicios) -> dict[str, list[int]]:
    """Números dos exercícios por nível, na ordem em que cada nível aparece."""
    r: dict[str, list[int]] = {}
    for ex in exercicios:
        r.setdefault(ex.nivel, []).append(ex.numero)
    return r
