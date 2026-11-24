"""Reconciliação entre o Passe 1 e o Passe 2 de um livro (insumo do controle B1/B2).

Mede a concordância e lista TODA divergência (nada é resolvido automaticamente):
  * por versículo: tem unidade (com_unidade ou parte_de_unidade) ou não;
  * por unidade: pareia unidades dos dois passes por sobreposição de intervalo e compara
    tipo_unidade, origem_real e natureza; unidades sem par são listadas.

Saída: auditoria/reconciliacao_<LIV>.json. Uso: python -I reconciliar.py GEN [--base dados]
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_promessas import *  # noqa: F401,F403


def carregar_passe(base, liv, n):
    probs = []
    regs = [r for _, r in ler_jsonl(Path(base) / "varredura" / f"{liv}.passe{n}.jsonl", probs)]
    return regs


def unidades(regs):
    return [u for r in regs for u in (r.get("unidades") or [])]


_STOP = set("a o as os um uma de do da dos das em no na nos nas por para com que e ou se ao aos seu sua seus suas ele ela eu tu te me vos vós nos lhe lhes ser foi sera".split())


def _toks(s):
    import re
    import unicodedata
    s = "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")
    return {w for w in re.findall(r"[a-z0-9]+", s) if len(w) >= 3 and w not in _STOP}


def parear(u1, u2, corpus):
    """Pareia unidades dos dois passes: versículos em comum e, entre os candidatos, maior similaridade de âncora.
    Retorna (pares, sem_par_p1, sem_par_p2). Guloso por pontuação decrescente."""
    faixas1 = {u["uid"]: set(corpus.intervalo(u["ref_inicio"], u["ref_fim"]) or []) for u in u1}
    faixas2 = {u["uid"]: set(corpus.intervalo(u["ref_inicio"], u["ref_fim"]) or []) for u in u2}
    t1 = {u["uid"]: _toks(u["ancora_texto"]) for u in u1}
    t2 = {u["uid"]: _toks(u["ancora_texto"]) for u in u2}
    cand = []
    for a in u1:
        for b in u2:
            ov = len(faixas1[a["uid"]] & faixas2[b["uid"]])
            if not ov:
                continue
            x, y = t1[a["uid"]], t2[b["uid"]]
            sim = len(x & y) / len(x | y) if (x | y) else 0.0
            score = sim + 0.05 * (a["tipo_unidade"] == b["tipo_unidade"]) + 0.01 * ov
            if sim >= 0.12 or (not x or not y):
                cand.append((score, a["uid"], b["uid"]))
    cand.sort(reverse=True)
    usa1, usa2, pares = set(), set(), []
    por1 = {u["uid"]: u for u in u1}
    por2 = {u["uid"]: u for u in u2}
    for score, i1, i2 in cand:
        if i1 in usa1 or i2 in usa2:
            continue
        usa1.add(i1)
        usa2.add(i2)
        pares.append((por1[i1], por2[i2]))
    return pares, [u for u in u1 if u["uid"] not in usa1], [u for u in u2 if u["uid"] not in usa2]


def reconciliar(base: Path, liv: str, corpus: Corpus):
    p1, p2 = carregar_passe(base, liv, 1), carregar_passe(base, liv, 2)
    if not p1 or not p2:
        raise SystemExit("faltam arquivos de passe para o livro")
    tem1 = {r["ref"] for r in p1 if r.get("estado") != "sem_unidade"}
    tem2 = {r["ref"] for r in p2 if r.get("estado") != "sem_unidade"}
    uniao, inter = tem1 | tem2, tem1 & tem2
    div_versiculos = sorted(uniao - inter, key=lambda x: corpus.pos[parse_ref(x)])
    u1, u2 = unidades(p1), unidades(p2)

    pares, sem_par1_u, sem_par2_u = parear(u1, u2, corpus)
    sem_par1 = [u["uid"] for u in sem_par1_u]
    sem_par2 = [u["uid"] for u in sem_par2_u]
    diverg_unidade = []
    for a, b in pares:
        dif = {c: [a.get(c), b.get(c)] for c in ("tipo_unidade", "origem_real", "natureza") if a.get(c) != b.get(c)}
        if dif:
            diverg_unidade.append({"p1": a["uid"], "p2": b["uid"], "diferencas": dif})
    n_classe_ok = len(pares) - len(diverg_unidade)
    res = {
        "livro": liv,
        "versiculos": len(corpus.refs_do_livro(liv)),
        "leitor_passe1": sorted({r.get("leitor") for r in p1}),
        "leitor_passe2": sorted({r.get("leitor") for r in p2}),
        "versiculos_com_unidade_p1": len(tem1),
        "versiculos_com_unidade_p2": len(tem2),
        "concordancia_versiculos_com_unidade_jaccard": round(len(inter) / len(uniao), 4) if uniao else 1.0,
        "unidades_p1": len(u1), "unidades_p2": len(u2), "unidades_pareadas": len(pares),
        "concordancia_classe_entre_pareadas": round(n_classe_ok / len(pares), 4) if pares else None,
        "divergencias_de_versiculo": div_versiculos,
        "divergencias_de_unidade": diverg_unidade,
        "unidades_so_no_passe1": sem_par1,
        "unidades_so_no_passe2": sem_par2,
        "metas_do_piloto": {"jaccard_minimo": 0.90, "concordancia_classe_minima": 0.85},
    }
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("livro")
    ap.add_argument("--base", default=str(RAIZ / "dados"))
    a = ap.parse_args()
    res = reconciliar(Path(a.base), a.livro, Corpus())
    saida = RAIZ / "auditoria" / f"reconciliacao_{a.livro}.json"
    saida.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in res.items() if not k.startswith(("divergencias", "unidades_so"))}, ensure_ascii=False, indent=2))
    print(f"divergências de versículo: {len(res['divergencias_de_versiculo'])}; de unidade: {len(res['divergencias_de_unidade'])}; "
          f"sem par: {len(res['unidades_so_no_passe1'])}+{len(res['unidades_so_no_passe2'])}. Detalhe em {saida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
