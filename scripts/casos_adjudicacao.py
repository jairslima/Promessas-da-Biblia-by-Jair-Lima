"""Monta os CASOS DE ADJUDICAÇÃO do protocolo v0.3 a partir da união dos candidatos dos Passes 1 e 2.

Agrupa unidades dos dois passes em aglomerados (versículos em comum e similaridade de âncora), tipifica
automaticamente a divergência (identificação, exegética, granularidade, nomenclatura, destinatário, condição,
equivalência semântica, falha de pareamento; o adjudicador confirma ou corrige) e grava:
  adjudicacao/casos_<LIV>.json    todos os casos, com texto literal do corpus e as leituras dos dois passes
  adjudicacao/lotes/lote_NN.md    lotes de casos prontos para o adjudicador

Não decide nada. Somente leitura sobre dados/. Uso: python -I casos_adjudicacao.py GEN [--por-lote 20]
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import reconciliar
from lib_promessas import *  # noqa: F401,F403

NAO_PROMESSA_TROCAVEIS = {"indeterminada", "profecia_sem_compromisso", "declaracao_sem_compromisso", "desejo_ou_bencao_votiva", "advertencia"}


def compacta(u, chaves=None):
    d = {"uid": u["uid"], "ref": u["ref_inicio"] if u["ref_inicio"] == u["ref_fim"] else f"{u['ref_inicio']}-{u['ref_fim'].split(' ')[1]}",
         "tipo": u["tipo_unidade"], "origem": u["origem_real"], "natureza": u.get("natureza"),
         "ancora": u["ancora_texto"], "resumo": u["resumo_proprio"], "confianca": u["confianca"]}
    for c, k in (("destinatario_tipo", "destinatario"), ("destinatario_nome", "dest_nome"), ("condicao_tipo", "condicao"),
                 ("promitente_nome", "promitente_nome"), ("promitente", "promitente")):
        if u.get(c):
            d[k] = u[c]
    ev = u.get("evidencia_exegetica") or []
    if ev:
        d["evidencia"] = ev[0].get("observacao", "")[:220]
    if chaves and u["uid"] in chaves:
        d["chave_existente"] = chaves[u["uid"]]
    return d


def eh_promessa(u):
    return u["tipo_unidade"] == "promessa"


def tipificar(a, b):
    """a = unidades do Passe 1 do aglomerado, b = do Passe 2. Retorna lista de tipos de divergência (sugestão)."""
    tipos = []
    if not a or not b:
        tipos.append("identificacao")
        return tipos
    if len(a) != len(b):
        tipos.append("granularidade")
    prom_a, prom_b = sum(map(eh_promessa, a)), sum(map(eh_promessa, b))
    if prom_a != prom_b and len(a) == len(b):
        tipos.append("exegetica")
    if len(a) == len(b) == 1:
        x, y = a[0], b[0]
        if eh_promessa(x) and eh_promessa(y):
            if x["origem_real"] != y["origem_real"] or x.get("natureza") != y.get("natureza"):
                tipos.append("exegetica")
            if x.get("destinatario_tipo") != y.get("destinatario_tipo"):
                tipos.append("destinatario")
            if x.get("condicao_tipo") != y.get("condicao_tipo"):
                tipos.append("condicao")
        elif not eh_promessa(x) and not eh_promessa(y):
            if x["tipo_unidade"] != y["tipo_unidade"] or x["origem_real"] != y["origem_real"]:
                tipos.append("nomenclatura")
        elif eh_promessa(x) != eh_promessa(y):
            tipos.append("exegetica")
    elif len(a) == len(b):
        if {u["tipo_unidade"] for u in a} != {u["tipo_unidade"] for u in b}:
            tipos.append("equivalencia_semantica")
    return sorted(set(tipos))


def concordante(a, b):
    """Aglomerado sem caso: um para um, mesma classificação (promessa) ou não promessa com mesmos rótulos."""
    if len(a) != 1 or len(b) != 1:
        return False
    x, y = a[0], b[0]
    if eh_promessa(x) and eh_promessa(y):
        return (x["origem_real"] == y["origem_real"] and x.get("natureza") == y.get("natureza")
                and x.get("destinatario_tipo") == y.get("destinatario_tipo") and x.get("condicao_tipo") == y.get("condicao_tipo"))
    # bênção votiva e cumprimento narrado com mesmo rótulo nos dois passes não exigem adjudicação
    return x["tipo_unidade"] == y["tipo_unidade"] and x["origem_real"] == y["origem_real"] and x["tipo_unidade"] in ("desejo_ou_bencao_votiva", "cumprimento_narrado")


def aglomerar(u1, u2, corpus):
    """Componentes conexos por (versículo em comum E similaridade de âncora >= 0,12)."""
    f1 = {u["uid"]: set(corpus.intervalo(u["ref_inicio"], u["ref_fim"]) or []) for u in u1}
    f2 = {u["uid"]: set(corpus.intervalo(u["ref_inicio"], u["ref_fim"]) or []) for u in u2}
    t1 = {u["uid"]: reconciliar._toks(u["ancora_texto"]) for u in u1}
    t2 = {u["uid"]: reconciliar._toks(u["ancora_texto"]) for u in u2}
    nos = [("1", u) for u in u1] + [("2", u) for u in u2]
    pai = {(p, u["uid"]): (p, u["uid"]) for p, u in nos}

    def achar(x):
        while pai[x] != x:
            pai[x] = pai[pai[x]]
            x = pai[x]
        return x

    for a in u1:
        for b in u2:
            if not (f1[a["uid"]] & f2[b["uid"]]):
                continue
            x, y = t1[a["uid"]], t2[b["uid"]]
            sim = len(x & y) / len(x | y) if (x | y) else 0
            if sim >= 0.12:
                pai[achar(("1", a["uid"]))] = achar(("2", b["uid"]))
    grupos = {}
    for p, u in nos:
        grupos.setdefault(achar((p, u["uid"])), []).append((p, u))
    return list(grupos.values())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("livro")
    ap.add_argument("--base", default=str(RAIZ / "dados"))
    ap.add_argument("--por-lote", type=int, default=20)
    a = ap.parse_args()
    corpus = Corpus()
    base = Path(a.base)
    u1 = reconciliar.unidades(reconciliar.carregar_passe(base, a.livro, 1))
    u2 = reconciliar.unidades(reconciliar.carregar_passe(base, a.livro, 2))
    chaves = {}
    ck = base / "consolidacao" / f"{a.livro}_chaves_p1.txt"
    if ck.exists():
        for l in ck.read_text(encoding="utf-8").splitlines():
            if l.strip() and not l.startswith("#"):
                c = [x.strip() for x in l.split("|")]
                chaves[c[0]] = {"acao": c[1], "objeto": c[2], "benef": c[3], "cond": c[4], "familia": c[5]}
    ags = aglomerar(u1, u2, corpus)
    casos, simples = [], 0
    for g in ags:
        A = [u for p, u in g if p == "1"]
        B = [u for p, u in g if p == "2"]
        if concordante(A, B):
            simples += 1
            continue
        todos = A + B
        ini = min((corpus.pos[parse_ref(u["ref_inicio"])], u["ref_inicio"]) for u in todos)[1]
        fim = max((corpus.pos[parse_ref(u["ref_fim"])], u["ref_fim"]) for u in todos)[1]
        refs = corpus.intervalo(ini, fim) or [ini]
        ctx_ini = corpus.ordem[parse_ref(ini)[0]][max(0, corpus.pos[parse_ref(ini)] - 1)]
        casos.append({"ini": ini, "fim": fim, "p1": [compacta(u, chaves) for u in sorted(A, key=lambda u: u["uid"])],
                      "p2": [compacta(u) for u in sorted(B, key=lambda u: u["uid"])],
                      "divergencias_sugeridas": tipificar(A, B),
                      "texto": {r: corpus.texto[r] for r in refs}})
    casos.sort(key=lambda c: corpus.pos[parse_ref(c["ini"])])
    for n, c in enumerate(casos, 1):
        c["id"] = f"C-{n:03d}"
    pasta = RAIZ / "adjudicacao"
    (pasta / "lotes").mkdir(parents=True, exist_ok=True)
    (pasta / f"casos_{a.livro}.json").write_text(json.dumps(casos, ensure_ascii=False, indent=1), encoding="utf-8")
    for i in range(0, len(casos), a.por_lote):
        lote = casos[i:i + a.por_lote]
        (pasta / "lotes" / f"lote_{i // a.por_lote + 1:02d}.json").write_text(json.dumps(lote, ensure_ascii=False), encoding="utf-8")
    por_tipo = {}
    for c in casos:
        for t in (c["divergencias_sugeridas"] or ["(nenhuma)"]):
            por_tipo[t] = por_tipo.get(t, 0) + 1
    print(f"aglomerados={len(ags)} concordantes sem caso={simples} casos={len(casos)} lotes={-(-len(casos) // a.por_lote)}")
    print(json.dumps(por_tipo, ensure_ascii=False))


if __name__ == "__main__":
    main()
