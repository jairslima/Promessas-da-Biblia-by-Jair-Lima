"""Prepara os lotes da Fase 3 (Árbitro Independente) para todos os 1.808 casos divergentes dos 56 livros pendentes.
Garante independência estrita:
  - Livros lidos por Claude + Gemini -> Árbitro: DeepSeek Flash High (API direta)
  - Livros lidos por Claude + Flash ou Claude + Codex -> Árbitro: Gemini (subagentes paralelos)
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import casos_adjudicacao
import catalogar_livro
import reconciliar
from lib_promessas import *  # noqa: F401,F403


def nome_curto(regs, n):
    for r in regs:
        l = r.get("leitor") or ""
        return "Claude" if l.startswith("claude") else ("Flash" if "flash" in l else ("Gemini" if "gemini" in l else ("Codex" if "codex" in l else l)))
    return f"L{n}"


def compactar_un(u):
    ri, rf = u["ref_inicio"], u["ref_fim"]
    ref = ri if ri == rf else f"{ri}-{rf.split(' ')[1]}"
    return {
        "uid": u["uid"],
        "ref": ref,
        "tipo": u["tipo_unidade"],
        "origem": u["origem_real"],
        "natureza": u.get("natureza"),
        "destinatario": u.get("destinatario_tipo"),
        "condicao": u.get("condicao_tipo"),
        "promitente": u.get("promitente") or u.get("promitente_nome"),
        "ancora": u["ancora_texto"],
        "resumo": u["resumo_proprio"],
    }


def main():
    corpus = Corpus()
    base = RAIZ / "dados_leituras"
    out_dir = RAIZ / "adjudicacao" / "fase3_lotes"
    out_dir.mkdir(parents=True, exist_ok=True)
    (RAIZ / "adjudicacao" / "fase3_saidas").mkdir(parents=True, exist_ok=True)

    grupos_arbitro = {"gemini": [], "deepseek": []}
    todos_casos = {}

    for liv in CANON:
        if liv == "GEN" or liv not in corpus.ordem:
            continue
        p1 = reconciliar.carregar_passe(base, liv, 1)
        p2 = reconciliar.carregar_passe(base, liv, 2)
        u1, u2 = reconciliar.unidades(p1), reconciliar.unidades(p2)
        par = (nome_curto(p1, 1), nome_curto(p2, 2))
        arbitro = "deepseek" if "Gemini" in par else "gemini"
        adjud = catalogar_livro.carregar_adjudicacoes(liv, corpus)
        eh = lambda x: x["tipo_unidade"] == "promessa"
        idx = 0
        for g in casos_adjudicacao.aglomerar(u1, u2, corpus):
            A_prom = [x for p, x in g if p == "1" and eh(x)]
            B_prom = [x for p, x in g if p == "2" and eh(x)]
            chave = frozenset(x["uid"] for p, x in g)
            if chave in adjud:
                continue
            if not A_prom and not B_prom:
                continue
            if A_prom and B_prom:
                sig = lambda L: sorted((x["origem_real"], x.get("natureza")) for x in L)
                if sig(A_prom) == sig(B_prom):
                    continue
            idx += 1
            cid = f"F3-{liv}-{idx:03d}"
            A_all = [x for p, x in g if p == "1"]
            B_all = [x for p, x in g if p == "2"]
            todos_u = A_all + B_all
            ini = min((corpus.pos[parse_ref(u["ref_inicio"])], u["ref_inicio"]) for u in todos_u)[1]
            fim = max((corpus.pos[parse_ref(u["ref_fim"])], u["ref_fim"]) for u in todos_u)[1]
            refs = corpus.intervalo(ini, fim) or [ini]
            caso = {
                "id": cid,
                "livro": liv,
                "leitor_p1": par[0],
                "leitor_p2": par[1],
                "arbitro_designado": arbitro,
                "ini": ini,
                "fim": fim,
                "texto": {r: corpus.texto[r] for r in refs},
                "p1": [compactar_un(u) for u in sorted(A_all, key=lambda u: u["uid"])],
                "p2": [compactar_un(u) for u in sorted(B_all, key=lambda u: u["uid"])],
            }
            grupos_arbitro[arbitro].append(caso)
            todos_casos[cid] = caso

    (RAIZ / "adjudicacao" / "fase3_todos_casos.json").write_text(
        json.dumps(todos_casos, ensure_ascii=False, indent=1), encoding="utf-8"
    )

    TAM_DEEPSEEK = 35
    TAM_GEMINI = 60
    for arb, lista in grupos_arbitro.items():
        tam = TAM_DEEPSEEK if arb == "deepseek" else TAM_GEMINI
        for i in range(0, len(lista), tam):
            lote = lista[i : i + tam]
            n_lote = i // tam + 1
            arq = out_dir / f"lote_{arb}_{n_lote:02d}.json"
            arq.write_text(json.dumps(lote, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"Arbitro {arb}: {len(lista)} casos em {-(-len(lista) // tam)} lotes (tam={tam})")


if __name__ == "__main__":
    main()
