"""Controles A6 (duplicação por equivalência semântica) e A7 (duplicação aproximada).

Teste de Equivalência Semântica (TES), automatizado em duas camadas:
  A6, camada canônica: duas promessas (não rejeitadas) com a mesma chave
      (origem, natureza, promitente, ação, objeto, beneficiário, condição) depois de normalizar
      sinônimos e remover intensificadores são a MESMA promessa: a segunda deve ser ocorrência.
      Exceção só com decisão `excecao_equivalencia` listando o id.
  A7, camada lexical: resumos próprios com sobreposição de vocabulário acima do limiar,
      para o mesmo beneficiário canônico, vão à revisão, salvo decisão `nao_equivalencia` com os dois ids.
  Ocorrências repetidas (mesma promessa, mesmo intervalo, mesmo tipo) também são A6.

Uso: python -I duplicatas.py [--base dados] [--limiar 0.6]
"""
import argparse
import json
import re
import sys
import unicodedata
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_promessas import *  # noqa: F401,F403
from validar_esquema import _carregar

LIMIAR_PADRAO = 0.6


def sem_acento(t: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")


def carregar_equivalencias(base: Path):
    p = Path(base) / "equivalencias.json"
    if not p.exists():
        p = RAIZ / "dados" / "equivalencias.json"
    return json.loads(p.read_text(encoding="utf-8"))


def canon_slug(slug: str, eq: dict) -> str:
    sin, inten = eq["sinonimos"], set(eq["intensificadores"])
    toks = []
    for t in str(slug).split("_"):
        t = sin.get(t, t)
        if t and t not in inten:
            toks.append(t)
    return "_".join(sorted(set(toks)))


def tokens_texto(t: str, eq: dict):
    sin, inten, stop = eq["sinonimos"], set(eq["intensificadores"]), set(eq["stopwords"])
    saida = set()
    for w in re.findall(r"[a-z0-9]+", sem_acento(t)):
        w = sin.get(w, w)
        if len(w) >= 3 and w not in stop and w not in inten:
            saida.add(w)
    return saida


def chave(r, eq):
    origem = "divina" if r.get("origem_real") in ORIGENS_DIVINAS else r.get("origem_real")
    quem = r.get("promitente") if origem == "divina" else r.get("promitente_nome")
    return (origem, r.get("natureza"), quem,
            canon_slug(r.get("acao_canonica", ""), eq), canon_slug(r.get("objeto_canonico", ""), eq),
            canon_slug(r.get("beneficiario_canonico", ""), eq), canon_slug(r.get("condicao_canonica", ""), eq))


def verificar(base: Path, limiar=LIMIAR_PADRAO):
    base = Path(base)
    problemas = []
    d = _carregar(base, problemas)
    eq = carregar_equivalencias(base)
    ativas = [(a, i, r) for a, i, r in d["promessas"] if r.get("status") != "rejeitada"]
    excecoes, nao_equiv = set(), set()
    for _, _, r in d["decisoes"]:
        if r.get("tipo") == "excecao_equivalencia":
            excecoes.update(r.get("ids", []))
        if r.get("tipo") == "nao_equivalencia":
            for x, y in combinations(sorted(r.get("ids", [])), 2):
                nao_equiv.add((x, y))
    # A6 camada canônica
    por_chave = {}
    for a, i, r in ativas:
        por_chave.setdefault(chave(r, eq), []).append((a, i, r))
    em_a6 = set()
    for k, grupo in por_chave.items():
        if len(grupo) < 2:
            continue
        for a, i, r in grupo[1:]:
            if r.get("id") in excecoes or grupo[0][2].get("id") in excecoes:
                continue
            em_a6.add(tuple(sorted((r.get("id"), grupo[0][2].get("id")))))
            problemas.append(Problema("A6", a, i, r.get("id", "?"),
                f"equivalente a {grupo[0][2].get('id')} (mesma ação, objeto, beneficiário e condição após normalização): registrar como ocorrência"))
    # A6 ocorrências repetidas
    vistos = {}
    for a, i, r in d["ocorrencias"]:
        k = (r.get("promessa_id"), r.get("ref_inicio"), r.get("ref_fim"), r.get("tipo"))
        if k in vistos:
            problemas.append(Problema("A6", a, i, r.get("id", "?"), f"ocorrência repetida de {vistos[k]}"))
        else:
            vistos[k] = r.get("id")
    # A7 camada lexical
    toks = {r.get("id"): tokens_texto(str(r.get("resumo_proprio", "")) + " " + str(r.get("objeto_canonico", "")).replace("_", " "), eq)
            for _, _, r in ativas}
    for (a1, i1, r1), (a2, i2, r2) in combinations(ativas, 2):
        x, y = sorted((r1.get("id"), r2.get("id")))
        if (x, y) in em_a6 or (x, y) in nao_equiv or x in excecoes or y in excecoes:
            continue
        if canon_slug(r1.get("beneficiario_canonico", ""), eq) != canon_slug(r2.get("beneficiario_canonico", ""), eq):
            continue
        t1, t2 = toks[r1.get("id")], toks[r2.get("id")]
        if not t1 or not t2:
            continue
        j = len(t1 & t2) / len(t1 | t2)
        if j >= limiar:
            problemas.append(Problema("A7", a2, i2, r2.get("id", "?"),
                f"par suspeito com {r1.get('id')} (similaridade {j:.2f}): registrar decisão nao_equivalencia ou fundir"))
    return problemas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=str(RAIZ / "dados"))
    ap.add_argument("--limiar", type=float, default=LIMIAR_PADRAO)
    a = ap.parse_args()
    probs = verificar(Path(a.base), a.limiar)
    for p in probs:
        print(p)
    print(f"duplicatas: {len(probs)} problema(s)")
    return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main())
