"""Apuração do número de promessas a partir do catálogo (SOMENTE LEITURA sobre catalogo/*/*.jsonl). Três cenários declarados, em faixa, nunca em ponto.

  Unidades: registros do catálogo (uma por trecho identificado; reafirmações contam separadas).
  Versículos: versículos que fazem parte de ao menos uma promessa candidata.
  Distintas (estimativa): unidades agrupadas por similaridade do resumo (Jaccard de palavras >= limiar) dentro da mesma categoria.
Cenários:
  conservador  só registros em que os dois leitores concordam ou que foram adjudicados (estado aprovada_ia_provisoria)
  central      todas as candidatas
  liberal      central dividido pela revocação medida nos pilotos (0,89 a 0,80), para compensar o que os leitores não viram
Uso: python -I apurar_numero.py [--limiar 0.45]      grava auditoria/apuracao_numero.json
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_promessas import *  # noqa: F401,F403

PRINCIPAL = ("divina_bencao", "patriarcal_bencao", "apostolica_garantia_bencao")
DIVINAS = PRINCIPAL + ("divina_juizo", "divina_sentenca", "patriarcal_juizo", "apostolica_garantia_juizo")
STOP = set("a o as os um uma de do da dos das em no na nos nas por para com que e ou se ao aos seu sua seus suas deus senhor promete garante anuncia declara".split())


def tk(s):
    s = "".join(ch for ch in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(ch) != "Mn")
    return frozenset(w for w in re.findall(r"[a-z0-9]+", s) if len(w) >= 4 and w not in STOP)


def distintas(rs, lim):
    toks = [tk(r["resumo"]) for r in rs]
    pai = list(range(len(rs)))

    def f(x):
        while pai[x] != x:
            pai[x] = pai[pai[x]]
            x = pai[x]
        return x
    idx = {}
    for i, t in enumerate(toks):
        for w in t:
            idx.setdefault(w, []).append(i)
    for i, t in enumerate(toks):
        cand = {}
        for w in t:
            for j in idx[w]:
                if j < i:
                    cand[j] = cand.get(j, 0) + 1
        for j, n in cand.items():
            u = len(t | toks[j])
            if u and n / u >= lim and rs[i]["categoria"] == rs[j]["categoria"]:
                pai[f(i)] = f(j)
    return len({f(i) for i in range(len(rs))})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limiar", type=float, default=0.45)
    a = ap.parse_args()
    corpus = Corpus()
    regs = []
    for d in sorted((RAIZ / "catalogo").iterdir()):
        f = d / f"{d.name}.jsonl"
        if f.exists():
            regs += [r for _, r in ler_jsonl(f, [])]
    P = [r for r in regs if r.get("categoria") != "nao_promessa"]

    def vers(rs):
        s = set()
        for r in rs:
            s |= set(corpus.intervalo(r["ref_inicio"], r["ref_fim"]) or [r["ref_inicio"]])
        return len(s)

    def bloco(rs):
        pr = [r for r in rs if r["categoria"] in PRINCIPAL]
        dv = [r for r in rs if r["categoria"] in DIVINAS]
        return {"todas": {"unidades": len(rs), "versiculos": vers(rs), "distintas_estimadas": distintas(rs, a.limiar)},
                "divinas_bencao_e_juizo": {"unidades": len(dv), "versiculos": vers(dv), "distintas_estimadas": distintas(dv, a.limiar)},
                "principal_divinas_de_bencao": {"unidades": len(pr), "versiculos": vers(pr), "distintas_estimadas": distintas(pr, a.limiar)}}
    central = bloco(P)
    cons = bloco([r for r in P if r["estado"] == "aprovada_ia_provisoria"])
    lib = {k: {m: (round(v / 0.84) if m in ("unidades", "distintas_estimadas") else v) for m, v in d.items()} for k, d in central.items()}
    res = {"limiar_de_similaridade": a.limiar, "conservador": cons, "central": central,
           "liberal_(central_dividido_por_0,84)": lib,
           "versiculos_no_corpus": len(corpus.pos), "aviso": "Sem deduplicação global. Faixas, não pontos. Nenhum indicador foi escolhido para o título."}
    (RAIZ / "auditoria" / "apuracao_numero.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    for nome in ("conservador", "central", "liberal_(central_dividido_por_0,84)"):
        d = res[nome]
        print(nome, {k: (v["unidades"], v["versiculos"], v["distintas_estimadas"]) for k, v in d.items()})


if __name__ == "__main__":
    main()
