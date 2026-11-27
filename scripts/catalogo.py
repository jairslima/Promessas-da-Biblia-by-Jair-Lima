"""Catálogo por livro: registros normalizados, catálogo legível (Markdown), contagem por categoria e CONTAGEM_GERAL.md.

Um registro do catálogo é uma UNIDADE identificada como promessa candidata (ainda não deduplicada entre livros).
O texto bíblico é sempre injetado do corpus (nunca digitado). Estados:
  aprovada_ia_provisoria   dois leitores concordam, ou adjudicada, sem campo pendente
  candidata_um_leitor      só um leitor registrou, ou só uma leitura existe: exige segunda leitura ou revisão
  divergencia_pendente     os leitores divergem em tipo, origem ou natureza: exige adjudicação ou revisão
  revisao_recomendada      classificação decidida pela IA ou pela auditoria que o autor ainda deve ratificar
  campo_pendente           falta campo exegético (promitente, reforço, condição...), nunca presumido
Funções: normalizar_genesis(), gravar_livro(liv, registros, cobertura), atualizar_contagem_geral().
Uso: python -I catalogo.py genesis      gera o catálogo de Gênesis a partir de dados_v04
     python -I catalogo.py geral        refaz CONTAGEM_GERAL.md
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_promessas import *  # noqa: F401,F403

PASTA = RAIZ / "catalogo"
NOMES = {"GEN": "Gênesis", "EXO": "Êxodo", "LEV": "Levítico", "NUM": "Números", "DEU": "Deuteronômio"}
ESTADOS = ("aprovada_ia_provisoria", "revisao_recomendada", "candidata_um_leitor", "divergencia_pendente", "campo_pendente")


def categoria(r):
    if r.get("tipo_unidade") != "promessa":
        return "nao_promessa"
    o, n = r.get("origem_real"), r.get("natureza")
    if n not in ("bencao", "juizo"):
        return "natureza_pendente"
    if o in ORIGENS_DIVINAS:
        if n == "bencao":
            return "divina_bencao"
        return "divina_sentenca" if r.get("forma_expressao") == "sentenca" else "divina_juizo"
    if o == "profetica_patriarcal":
        if r.get("fundamentacao_divina") == "insuficiente":
            return "patriarcal_insuficiente"
        return "patriarcal_bencao" if n == "bencao" else "patriarcal_juizo"
    if o == "apostolica_garantia":
        return "apostolica_garantia_bencao" if n == "bencao" else "apostolica_garantia_juizo"
    if o == "humana_em_nome_proprio":
        return "humana_beneficio" if n == "bencao" else "humana_prejuizo"
    if o == "adversaria_ou_falsa":
        return "adversaria_ou_falsa"
    return "outra_origem"


# categorias que compõem o indicador principal provisório (promessas de Deus de bênção); a escolha final do indicador cabe ao Jair
PRINCIPAL = ("divina_bencao", "patriarcal_bencao", "apostolica_garantia_bencao")
ORDEM_CAT = ("divina_bencao", "patriarcal_bencao", "apostolica_garantia_bencao", "divina_juizo", "divina_sentenca", "patriarcal_juizo", "apostolica_garantia_juizo",
             "humana_beneficio", "humana_prejuizo", "adversaria_ou_falsa", "natureza_pendente", "patriarcal_insuficiente", "outra_origem")


def livro_nome(liv):
    return NOMES.get(liv, liv)


DUVIDAS_GEN = [
    ("GEN 2:18", "caso B5 mantido como promessa divina; aguarda ratificação do autor"),
    ("GEN 19:8", "compromisso humano de prejuízo por decisão da auditoria de 2026-11-20; aguarda ratificação do autor"),
    ("GEN 32:28", "promitente deus_indistinto por decisão da auditoria (Gn 32:24-30 e Os 12:3-5); aguarda ratificação do autor"),
    ("GEN 35:3", "caso B5 mantido só como promessa humana; aguarda ratificação do autor"),
    ("GEN 46:31", "caso B5 mantido como promessa humana; aguarda ratificação do autor"),
    ("GEN 48:19", "dividido em dois compromissos (Manassés e Efraim); origem divina fundamentada em Hb 11:21; aguarda ratificação do autor"),
    ("GEN 49:8", "bênção tribal promovida a promessa por critério da IA (D-35, provisório)"),
    ("GEN 49:10", "promessa profética messiânica por decisão do autor (D-35); leitura posterior em Hb 7:14, 1Cr 5:2, Sl 78:67-72, Ap 5:5"),
    ("GEN 49:13", "bênção tribal promovida a promessa por critério da IA (D-35, provisório)"),
    ("GEN 49:16", "bênção tribal promovida a promessa por critério da IA (D-35, provisório)"),
    ("GEN 49:19", "bênção tribal promovida a promessa por critério da IA (D-35, provisório)"),
    ("GEN 49:20", "bênção tribal promovida a promessa por critério da IA (D-35, provisório)"),
]


def normalizar_genesis(corpus):
    regs = []
    for _, r in ler_jsonl(RAIZ / "dados_v04" / "promessas" / "GEN.jsonl", []):
        duv = []
        if r.get("campos_pendentes"):
            duv.append("campo pendente: " + ", ".join(r["campos_pendentes"]))
        for ref, texto in DUVIDAS_GEN:
            if r["ref_inicio"] == ref:
                duv.append(texto)
        if r.get("confianca") == "baixa":
            duv.append("confiança baixa do leitor")
        estado = "campo_pendente" if r.get("campos_pendentes") else ("revisao_recomendada" if duv else "aprovada_ia_provisoria")
        regs.append({"id": r["id"], "livro": "GEN", "ref_inicio": r["ref_inicio"], "ref_fim": r["ref_fim"], "tipo_unidade": "promessa",
                     "origem_real": r["origem_real"], "natureza": r["natureza"], "destinatario_tipo": r.get("destinatario_tipo"),
                     "destinatario_nome": r.get("destinatario_nome"), "promitente": r.get("promitente") or r.get("promitente_nome"),
                     "condicao_tipo": r.get("condicao_tipo"), "forma_expressao": r.get("forma_expressao"), "fundamentacao_divina": r.get("fundamentacao_divina"),
                     "resumo": r["resumo_proprio"], "relacao": r.get("relacao"), "familia": r.get("familia_id"), "estado": estado, "duvidas": duv,
                     "leituras": r.get("status")})
    return regs


def md_citacao(corpus, ini, fim):
    refs = corpus.intervalo(ini, fim) or [ini]
    return "\n".join(f"> **{r}** {corpus.texto[r]}" for r in refs)


def gravar_livro(liv, regs, cobertura, corpus, destino_md=None):
    """Grava JSONL, catálogo legível e contagem de um livro. `cobertura`: dict com versiculos_lidos, versiculos_do_livro, leituras (lista), nota."""
    pasta = PASTA / liv
    pasta.mkdir(parents=True, exist_ok=True)
    regs = sorted(regs, key=lambda r: (corpus.pos[parse_ref(r["ref_inicio"])], r["id"]))
    for r in regs:
        r["categoria"] = categoria(r)
    escrever_jsonl(pasta / f"{liv}.jsonl", regs)
    (pasta / "cobertura.json").write_text(json.dumps(cobertura, ensure_ascii=False, indent=1), encoding="utf-8")
    nome = livro_nome(liv)
    cats, estados, cruz = {}, {}, {}
    for r in regs:
        cats[r["categoria"]] = cats.get(r["categoria"], 0) + 1
        estados[r["estado"]] = estados.get(r["estado"], 0) + 1
        cruz[(r["categoria"], r["estado"])] = cruz.get((r["categoria"], r["estado"]), 0) + 1
    prom = [r for r in regs if r["categoria"] != "nao_promessa"]
    # ---- contagem
    C = [f"# CONTAGEM: {nome} ({liv})", "",
         f"**Provisória.** Unidades classificadas como promessa candidata, **ainda sem deduplicação global**. Cobertura: **{cobertura['versiculos_lidos']} de {cobertura['versiculos_do_livro']} versículos lidos** "
         f"({', '.join(cobertura.get('leituras', []))}). {cobertura.get('nota', '')}", "",
         "## Por categoria", "", "| Categoria | Registros |", "| --------- | --------: |"]
    for k in ORDEM_CAT:
        if cats.get(k):
            C.append(f"| {k}{' (indicador principal provisório)' if k in PRINCIPAL else ''} | {cats[k]} |")
    C += [f"| **Total de promessas candidatas** | **{len(prom)}** |", "", "## Por estado", "", "| Estado | Registros |", "| ------ | --------: |"]
    for e in ESTADOS:
        C.append(f"| {e} | {estados.get(e, 0)} |")
    C += ["", f"**Componentes do indicador principal provisório:** " + " + ".join(f"{k} {cats.get(k, 0)}" for k in PRINCIPAL) + f" = **{sum(cats.get(k, 0) for k in PRINCIPAL)}**. Nenhum indicador foi escolhido para o título.", ""]
    (pasta / "CONTAGEM.md").write_text("\n".join(C) + "\n", encoding="utf-8", newline="\n")
    # ---- catálogo
    L = [f"# CATÁLOGO DE PROMESSAS: {nome} ({liv})", "",
         "Texto bíblico literal da **Bíblia Almeida Livre by Jair Lima** (injetado do corpus). Classificação feita por leitura assistida por computador. "
         "O estado de cada registro indica o que ainda falta. Reafirmações e duplicações entre livros ainda **não foram unificadas**.", "",
         f"Cobertura: {cobertura['versiculos_lidos']} de {cobertura['versiculos_do_livro']} versículos lidos. Registros: {len(regs)} (promessas candidatas: {len(prom)}). Ver `CONTAGEM.md`.", ""]
    por_cap = {}
    for r in regs:
        por_cap.setdefault(parse_ref(r["ref_inicio"])[1], []).append(r)
    for cap in sorted(por_cap):
        L += [f"## {nome} {cap}", ""]
        for r in por_cap[cap]:
            rr = r["ref_inicio"] if r["ref_inicio"] == r["ref_fim"] else f"{r['ref_inicio']} a {r['ref_fim']}"
            L.append(f"### {r['id']}: {rr}")
            L.append(md_citacao(corpus, r["ref_inicio"], r["ref_fim"]))
            L.append("")
            dest = r.get("destinatario_tipo") or "(pendente)"
            if r.get("destinatario_nome"):
                dest += f" ({r['destinatario_nome']})"
            L.append(f"* **Classificação:** `{r['categoria']}` ({r['origem_real']}, {r.get('natureza') or 'natureza pendente'}); **destinatário:** {dest}; "
                     f"**promitente:** {r.get('promitente') or '(pendente)'}; **condição:** {r.get('condicao_tipo') or '(pendente)'}")
            L.append(f"* **Resumo do leitor:** {r['resumo']}")
            L.append(f"* **Estado:** `{r['estado']}`" + (f"; **dúvidas:** {'; '.join(r['duvidas'])}" if r.get("duvidas") else ""))
            if r.get("possivel_reafirmacao_de"):
                L.append(f"* **Possível reafirmação de** {r['possivel_reafirmacao_de']} (não unificada)")
            L.append("")
    (pasta / "CATALOGO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    # ---- dúvidas
    D = [f"# DÚVIDAS PARA REVISÃO: {nome} ({liv})", "", "Itens que ainda exigem revisão. Nenhum bloqueou a leitura dos demais livros.", ""]
    n = 0
    for r in regs:
        if r["estado"] != "aprovada_ia_provisoria" or r.get("duvidas"):
            n += 1
            rr = r["ref_inicio"] if r["ref_inicio"] == r["ref_fim"] else f"{r['ref_inicio']} a {r['ref_fim']}"
            D.append(f"* **{r['id']}** {rr}: `{r['estado']}`; {'; '.join(r.get('duvidas') or ['sem detalhe'])}")
    D.append("")
    D.insert(3, f"Total de registros com pendência ou dúvida: **{n}**.\n")
    (pasta / "DUVIDAS.md").write_text("\n".join(D) + "\n", encoding="utf-8", newline="\n")
    if destino_md:  # cópias na raiz (Gênesis)
        (RAIZ / destino_md[0]).write_text((pasta / "CATALOGO.md").read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
        (RAIZ / destino_md[1]).write_text((pasta / "CONTAGEM.md").read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
    return cats, estados


def atualizar_contagem_geral(corpus):
    livros = [x for x in CANON if x in corpus.ordem]
    total_vers = len(corpus.pos)
    linhas, tot_v, tot_lidos, tot_prom = [], 0, 0, 0
    cat_tot, est_tot = {}, {}
    for liv in livros:
        nv = len(corpus.refs_do_livro(liv))
        tot_v += nv
        arq = PASTA / liv / "cobertura.json"
        if not arq.exists():
            linhas.append(f"| {liv} | {nv} | 0 | 0 | 0 | não iniciado |")
            continue
        cob = json.loads(arq.read_text(encoding="utf-8"))
        regs = [r for _, r in ler_jsonl(PASTA / liv / f"{liv}.jsonl", [])]
        prom = [r for r in regs if r.get("categoria") != "nao_promessa"]
        princ = sum(1 for r in prom if r["categoria"] in PRINCIPAL)
        for r in prom:
            cat_tot[r["categoria"]] = cat_tot.get(r["categoria"], 0) + 1
        for r in regs:
            est_tot[r["estado"]] = est_tot.get(r["estado"], 0) + 1
        tot_lidos += cob["versiculos_lidos"]
        tot_prom += len(prom)
        sit = "completo" if cob["versiculos_lidos"] >= nv else "parcial"
        linhas.append(f"| {liv} | {nv} | {cob['versiculos_lidos']} | {len(prom)} | {princ} | {sit}; {', '.join(cob.get('leituras', []))} |")
    L = ["# CONTAGEM GERAL (avanço acumulado da catalogação)", "",
         "**Provisória e sem deduplicação global.** Cada linha conta unidades identificadas como promessas candidatas, não promessas distintas estimadas. nenhum número é meta; "
         "nenhum indicador foi escolhido para o título.", "",
         f"**Cobertura:** {tot_lidos} de {total_vers} versículos lidos ({100 * tot_lidos / total_vers:.1f}%). **Promessas candidatas:** {tot_prom}.", "",
         "| Livro | Versículos | Lidos | Promessas candidatas | Indicador principal provisório | Situação |", "| ----- | ---------: | ----: | -------------------: | -----------------------------: | -------- |"]
    L += linhas
    L += ["", "## Por categoria (livros catalogados)", "", "| Categoria | Registros |", "| --------- | --------: |"]
    for k in ORDEM_CAT:
        if cat_tot.get(k):
            L.append(f"| {k} | {cat_tot[k]} |")
    L += ["", "## Por estado", "", "| Estado | Registros |", "| ------ | --------: |"] + [f"| {e} | {est_tot.get(e, 0)} |" for e in ESTADOS]
    (RAIZ / "CONTAGEM_GERAL.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")


def main():
    corpus = Corpus()
    if len(sys.argv) > 1 and sys.argv[1] == "genesis":
        regs = normalizar_genesis(corpus)
        nv = len(corpus.refs_do_livro("GEN"))
        cats, est = gravar_livro("GEN", regs, {"versiculos_lidos": nv, "versiculos_do_livro": nv, "leituras": ["2 leitores", "adjudicação", "conferência de campos pelo texto"],
                                               "nota": "Gênesis foi lido integralmente e revisto nas versões v0.2 a v0.4."}, corpus,
                                 destino_md=("CATALOGO_PROMESSAS_GENESIS.md", "CONTAGEM_GENESIS.md"))
        print("GEN", sum(cats.values()), cats, est)
    atualizar_contagem_geral(corpus)


if __name__ == "__main__":
    main()
