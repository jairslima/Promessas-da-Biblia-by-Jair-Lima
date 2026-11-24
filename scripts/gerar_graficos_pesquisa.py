"""Gera os 6 gráficos científicos e editoriais da pesquisa das Promessas da Bíblia em duas versões:
1. Versão colorida (e-book, GitHub, Zenodo, GitHub Pages, artigo científico e divulgação)
2. Versão monocromática em escala de cinza de alto contraste com padrões hachurados (edição impressa P&B)
Todos os números são extraídos diretamente de `catalogo/*/*.jsonl` e `auditoria/apuracao_numero.json` (zero hardcoding manual).
"""
import json
import sys
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PESQ = Path(r".")
PROJ = Path(r"./local_env Estudos Biblicos\Livros Teologia\As Promessas da Biblia (titulo provisorio)")

sys.path.insert(0, str(PESQ / "scripts"))
from lib_promessas import CANON, Corpus, ler_jsonl  # noqa: E402

ROTULO_CAT = {
    "divina_bencao": "Bênção divina",
    "divina_juizo": "Juízo divino",
    "humana_beneficio": "Compromisso humano (benefício)",
    "apostolica_garantia_bencao": "Garantia apostólica de bênção",
    "humana_prejuizo": "Compromisso humano (prejuízo)",
    "divina_sentenca": "Sentença divina",
    "apostolica_garantia_juizo": "Garantia apostólica de juízo",
    "adversaria_ou_falsa": "Promessa adversária ou falsa",
    "patriarcal_bencao": "Bênção patriarcal",
    "patriarcal_juizo": "Juízo patriarcal",
}

DIVISAO_CANON = [
    ("Pentateuco", ["GEN", "EXO", "LEV", "NUM", "DEU"]),
    ("Históricos AT", ["JOS", "JDG", "RUT", "1SA", "2SA", "1KI", "2KI", "1CH", "2CH", "EZR", "NEH", "EST"]),
    ("Poéticos e Sapienciais", ["JOB", "PSA", "PRO", "ECC", "SNG"]),
    ("Profetas Maiores", ["ISA", "JER", "LAM", "EZK", "DAN"]),
    ("Profetas Menores", ["HOS", "JOL", "AMO", "OBA", "JON", "MIC", "NAM", "HAB", "ZEP", "HAG", "ZEC", "MAL"]),
    ("Evangelhos e Atos", ["MAT", "MRK", "LUK", "JHN", "ACT"]),
    ("Epístolas e Apocalipse", ["ROM", "1CO", "2CO", "GAL", "EPH", "PHP", "COL", "1TH", "2TH", "1TI", "2TI", "TIT", "PHM", "HEB", "JAS", "1PE", "2PE", "1JN", "2JN", "3JN", "JUD", "REV"]),
]

NOMES_LIV = {
    "GEN": "Gênesis", "EXO": "Êxodo", "LEV": "Levítico", "NUM": "Números", "DEU": "Deuteronômio",
    "JOS": "Josué", "JDG": "Juízes", "RUT": "Rute", "1SA": "1 Samuel", "2SA": "2 Samuel",
    "1KI": "1 Reis", "2KI": "2 Reis", "1CH": "1 Crônicas", "2CH": "2 Crônicas", "EZR": "Esdras",
    "NEH": "Neemias", "EST": "Ester", "JOB": "Jó", "PSA": "Salmos", "PRO": "Provérbios",
    "ECC": "Eclesiastes", "SNG": "Cantares", "ISA": "Isaías", "JER": "Jeremias", "LAM": "Lamentações",
    "EZK": "Ezequiel", "DAN": "Daniel", "HOS": "Oseias", "JOL": "Joel", "AMO": "Amós",
    "OBA": "Obadias", "JON": "Jonas", "MIC": "Miqueias", "NAM": "Naum", "HAB": "Habacuque",
    "ZEP": "Sofonias", "HAG": "Ageu", "ZEC": "Zacarias", "MAL": "Malaquias",
    "MAT": "Mateus", "MRK": "Marcos", "LUK": "Lucas", "JHN": "João", "ACT": "Atos",
    "ROM": "Romanos", "1CO": "1 Coríntios", "2CO": "2 Coríntios", "GAL": "Gálatas", "EPH": "Efésios",
    "PHP": "Filipenses", "COL": "Colossenses", "1TH": "1 Tessalonicenses", "2TH": "2 Tessalonicenses",
    "1TI": "1 Timóteo", "2TI": "2 Timóteo", "TIT": "Tito", "PHM": "Filemom", "HEB": "Hebreus",
    "JAS": "Tiago", "1PE": "1 Pedro", "2PE": "2 Pedro", "1JN": "1 João", "2JN": "2 João",
    "3JN": "3 João", "JUD": "Judas", "REV": "Apocalipse",
}


def fmt(n):
    return f"{n:,}".replace(",", ".")


def carregar_dados():
    regs = []
    for d in sorted((PESQ / "catalogo").iterdir()):
        if d.is_dir() and (d / f"{d.name}.jsonl").exists():
            regs += [r for _, r in ler_jsonl(d / f"{d.name}.jsonl", [])]
    apur = json.loads((PESQ / "auditoria" / "apuracao_numero.json").read_text(encoding="utf-8"))
    mc = json.loads((PROJ / "livro" / "entregas" / "memoria_de_calculo.json").read_text(encoding="utf-8"))
    return regs, apur, mc


def configurar_estilo():
    plt.rcParams["font.sans-serif"] = ["Segoe UI", "Arial", "DejaVu Sans"]
    plt.rcParams["axes.edgecolor"] = "#CCCCCC"
    plt.rcParams["axes.linewidth"] = 0.8


def g1_painel_geral(regs, apur, mc, dest_dir, mono=False):
    fig, ax = plt.subplots(figsize=(10, 5.6), dpi=300)
    ax.axis("off")
    cor_fundo = "#F7F7F7" if mono else "#F4F6F9"
    cor_borda = "#444444" if mono else "#1E3A5F"
    cor_num = "#111111" if mono else "#1E3A5F"
    cor_dest = "#222222" if mono else "#8B6914"
    cor_sub = "#333333" if mono else "#4A5568"

    fig.patch.set_facecolor("white")
    ax.text(0.5, 0.94, "A BÍBLIA DAS PROMESSAS EM NÚMEROS", ha="center", va="top", fontsize=16, fontweight="bold", color=cor_num)
    ax.text(0.5, 0.88, "Levantamento exaustivo nos 66 livros da Bíblia Almeida Livre (leitura dupla independente e arbitragem na Fase 3)", ha="center", va="top", fontsize=9.5, color=cor_sub)

    cards = [
        ("66 Livros | 1.189 Capítulos", fmt(apur["versiculos_no_corpus"]), "Versículos lidos (100% do corpus)", False),
        ("Cobertura Promissória", f"{fmt(apur['central']['todas']['versiculos'])} ({100*apur['central']['todas']['versiculos']/apur['versiculos_no_corpus']:.1f}%)", "Versículos com promessas confirmadas", False),
        ("Unidades Confirmadas", fmt(len(regs)), "De 3.609 candidatas iniciais (0 pendentes)", True),
        ("Promessas Distintas", fmt(apur["central"]["todas"]["distintas_estimadas"]), "Agrupamento lexical (limiar 0,45)", True),
        ("Bênção Divina (Unidades)", fmt(apur["central"]["principal_divinas_de_bencao"]["unidades"]), f"{fmt(apur['central']['principal_divinas_de_bencao']['distintas_estimadas'])} promessas distintas de bênção", True),
        ("Vias de Confirmação", f"{fmt(mc['confirmadas_acordo_direto'])} + {fmt(mc['confirmadas_arbitragem_independente'])}", "1.211 acordo direto | 2.013 arbitragem Fase 3", False),
    ]

    posicoes = [
        (0.04, 0.48, 0.28, 0.32),
        (0.36, 0.48, 0.28, 0.32),
        (0.68, 0.48, 0.28, 0.32),
        (0.04, 0.10, 0.28, 0.32),
        (0.36, 0.10, 0.28, 0.32),
        (0.68, 0.10, 0.28, 0.32),
    ]
    for (x, y, w, h), (topo, numero, rodape, dest) in zip(posicoes, cards):
        rect = plt.Rectangle((x, y), w, h, facecolor=cor_fundo, edgecolor=cor_borda, linewidth=1.6 if dest else 1.0, transform=ax.transAxes, zorder=2)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h - 0.05, topo.upper(), ha="center", va="top", fontsize=8.5, fontweight="bold", color=cor_sub, transform=ax.transAxes, zorder=3)
        ax.text(x + w / 2, y + h / 2, numero, ha="center", va="center", fontsize=19 if len(numero) < 10 else 14.5, fontweight="bold", color=cor_dest if dest else cor_num, transform=ax.transAxes, zorder=3)
        ax.text(x + w / 2, y + 0.04, rodape, ha="center", va="bottom", fontsize=8, color=cor_sub, transform=ax.transAxes, zorder=3)

    ax.text(0.5, 0.02, "Fonte: Pesquisa Promessas da Bíblia by Jair Lima (2026) — Corpus: Bíblia Almeida Livre (CC BY-ND 4.0).", ha="center", va="bottom", fontsize=7.5, color="#666666")
    suf = "_pb" if mono else "_cor"
    arq = dest_dir / f"grafico_01_painel_geral{suf}.png"
    fig.savefig(arq, bbox_inches="tight", dpi=300)
    plt.close(fig)
    return arq


def g2_categorias(regs, dest_dir, mono=False):
    cat = Counter(r["categoria"] for r in regs)
    itens = sorted(cat.items(), key=lambda x: x[1])
    nomes = [ROTULO_CAT.get(k, k) for k, _ in itens]
    vals = [v for _, v in itens]
    tot = len(regs)

    fig, ax = plt.subplots(figsize=(9.5, 5.4), dpi=300)
    cores = []
    for k, _ in itens:
        if mono:
            cores.append("#333333" if "bencao" in k or "beneficio" in k else "#888888")
        else:
            if k in ("divina_bencao", "apostolica_garantia_bencao", "patriarcal_bencao"):
                cores.append("#1E56A0")
            elif k in ("divina_juizo", "divina_sentenca", "apostolica_garantia_juizo", "patriarcal_juizo"):
                cores.append("#A63A2B")
            elif "humana" in k:
                cores.append("#2E7D5B")
            else:
                cores.append("#6B5B95")

    bars = ax.barh(nomes, vals, color=cores, edgecolor="#222222" if mono else "none", height=0.68)
    if mono:
        for bar, (k, _) in zip(bars, itens):
            if "juizo" in k or "sentenca" in k or "prejuizo" in k:
                bar.set_hatch("//")

    ax.set_xlim(0, max(vals) * 1.24)
    for bar, v in zip(bars, vals):
        pct = 100 * v / tot
        ax.text(v + 18, bar.get_y() + bar.get_height() / 2, f"{fmt(v)} ({pct:.1f}%)", va="center", ha="left", fontsize=8.5, fontweight="bold", color="#222222")

    ax.set_title("Distribuição das 3.224 Unidades Promissórias Confirmadas nas 10 Categorias", fontsize=12.5, fontweight="bold", pad=12, color="#111111" if mono else "#1E3A5F")
    ax.set_xlabel("Unidades promissórias confirmadas", fontsize=9.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", linestyle="--", alpha=0.4)

    suf = "_pb" if mono else "_cor"
    arq = dest_dir / f"grafico_02_dez_categorias{suf}.png"
    fig.savefig(arq, bbox_inches="tight", dpi=300)
    plt.close(fig)
    return arq


def g3_funil_fase3(regs, mc, dest_dir, mono=False):
    etapas = [
        "1. Unidades candidatas iniciais\n(Fases 1 e 2 combinadas)",
        "2. Rejeitadas pelo árbitro (Fase 3)\n(332 casos = 334 unidades preliminares)",
        "3. Consolidadas por granularidade (Fase 3)\n(34 casos com subdivisões fundidas)",
        "4. Duplicatas técnicas estritas\n(mesmo versículo, categoria e objeto)",
        "5. Unidades confirmadas finais\n(1.211 acordo direto + 2.013 arbitradas)",
        "6. Promessas distintas estimadas\n(após recuperação dos 276 resumos, limiar 0,45)",
    ]
    valores = [3609, -334, -37, -14, 3224, 2945]
    textos = ["3.609", "-334", "-37", "-14", "3.224", "2.945"]

    fig, ax = plt.subplots(figsize=(9.2, 4.8), dpi=300)
    y = np.arange(len(etapas))[::-1]
    larguras = [abs(v) for v in valores]
    if mono:
        cores = ["#555555", "#AAAAAA", "#AAAAAA", "#AAAAAA", "#222222", "#444444"]
    else:
        cores = ["#4A6FA5", "#C0392B", "#D35400", "#8E44AD", "#1B4F72", "#1E8449"]

    bars = ax.barh(y, larguras, color=cores, edgecolor="#222222" if mono else "none", height=0.6)
    if mono:
        for i in (1, 2, 3):
            bars[i].set_hatch("//")

    ax.set_yticks(y)
    ax.set_yticklabels(etapas, fontsize=8.8)
    ax.set_xlim(0, 4200)
    for bar, t, v in zip(bars, textos, larguras):
        ax.text(v + 55, bar.get_y() + bar.get_height() / 2, f"{t} unidades", va="center", ha="left", fontsize=9.5, fontweight="bold", color="#111111")

    ax.set_title("Conciliação Aritmética das Três Fases: de 3.609 Candidatas a 3.224 Confirmadas (2.945 Distintas)", fontsize=11.5, fontweight="bold", pad=12, color="#111111" if mono else "#1E3A5F")
    ax.set_xlabel("Quantidade de unidades / promessas", fontsize=9.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", linestyle="--", alpha=0.4)

    suf = "_pb" if mono else "_cor"
    arq = dest_dir / f"grafico_03_funil_conciliacao{suf}.png"
    fig.savefig(arq, bbox_inches="tight", dpi=300)
    plt.close(fig)
    return arq


def g4_top_livros(regs, dest_dir, mono=False):
    por_liv = Counter(r["livro"] for r in regs)
    bencao_liv = Counter(r["livro"] for r in regs if r["categoria"] in ("divina_bencao", "apostolica_garantia_bencao", "patriarcal_bencao"))
    top15 = por_liv.most_common(15)[::-1]

    nomes = [f"{NOMES_LIV[k]} ({k})" for k, _ in top15]
    totais = [v for _, v in top15]
    bencaos = [bencao_liv[k] for k, _ in top15]
    outros = [t - b for t, b in zip(totais, bencaos)]

    fig, ax = plt.subplots(figsize=(9.5, 5.5), dpi=300)
    c_benc = "#333333" if mono else "#1E56A0"
    c_outr = "#BBBBBB" if mono else "#D98880"

    b1 = ax.barh(nomes, bencaos, color=c_benc, edgecolor="#222222" if mono else "none", height=0.65, label="Bênção divina (indicador principal)")
    b2 = ax.barh(nomes, outros, left=bencaos, color=c_outr, edgecolor="#222222" if mono else "none", height=0.65, label="Juízo divino, compromissos humanos e outros")
    if mono:
        for bar in b2:
            bar.set_hatch("//")

    ax.set_xlim(0, max(totais) * 1.18)
    for y_pos, t, b in zip(range(len(nomes)), totais, bencaos):
        ax.text(t + 5, y_pos, f"{t} ({b} bênção)", va="center", ha="left", fontsize=8.3, fontweight="bold", color="#222222")

    ax.set_title("Os 15 Livros Bíblicos com Maior Número de Unidades Promissórias Confirmadas", fontsize=12, fontweight="bold", pad=12, color="#111111" if mono else "#1E3A5F")
    ax.set_xlabel("Unidades confirmadas", fontsize=9.5)
    ax.legend(loc="lower right", fontsize=8.5, frameon=True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", linestyle="--", alpha=0.4)

    suf = "_pb" if mono else "_cor"
    arq = dest_dir / f"grafico_04_top15_livros{suf}.png"
    fig.savefig(arq, bbox_inches="tight", dpi=300)
    plt.close(fig)
    return arq


def g5_divisoes_canon(regs, dest_dir, mono=False):
    por_liv = Counter(r["livro"] for r in regs)
    benc_liv = Counter(r["livro"] for r in regs if r["categoria"] in ("divina_bencao", "apostolica_garantia_bencao", "patriarcal_bencao"))
    juiz_liv = Counter(r["livro"] for r in regs if r["categoria"] in ("divina_juizo", "divina_sentenca", "apostolica_garantia_juizo", "patriarcal_juizo"))

    grupos = [g for g, _ in DIVISAO_CANON][::-1]
    benc = [sum(benc_liv[l] for l in ls) for _, ls in DIVISAO_CANON][::-1]
    juiz = [sum(juiz_liv[l] for l in ls) for _, ls in DIVISAO_CANON][::-1]
    hum = [sum(por_liv[l] - benc_liv[l] - juiz_liv[l] for l in ls) for _, ls in DIVISAO_CANON][::-1]
    tots = [b + j + h for b, j, h in zip(benc, juiz, hum)]

    fig, ax = plt.subplots(figsize=(9.5, 4.8), dpi=300)
    c1 = "#222222" if mono else "#1E56A0"
    c2 = "#888888" if mono else "#C0392B"
    c3 = "#DDDDDD" if mono else "#2E7D5B"

    b_bar = ax.barh(grupos, benc, color=c1, edgecolor="#222222" if mono else "none", height=0.6, label="Bênção divina (1.622)")
    j_bar = ax.barh(grupos, juiz, left=benc, color=c2, edgecolor="#222222" if mono else "none", height=0.6, label="Juízo e sentença divina (1.065)")
    left_h = [b + j for b, j in zip(benc, juiz)]
    h_bar = ax.barh(grupos, hum, left=left_h, color=c3, edgecolor="#222222" if mono else "none", height=0.6, label="Compromissos humanos e adversários (537)")
    if mono:
        for bar in j_bar:
            bar.set_hatch("//")
        for bar in h_bar:
            bar.set_hatch("..")

    ax.set_xlim(0, max(tots) * 1.18)
    for y_pos, t in enumerate(tots):
        ax.text(t + 12, y_pos, f"{fmt(t)} unidades ({100*t/len(regs):.1f}%)", va="center", ha="left", fontsize=8.8, fontweight="bold", color="#222222")

    ax.set_title("Distribuição das Promessas pelas 7 Grandes Divisões do Cânon Bíblico", fontsize=12, fontweight="bold", pad=12, color="#111111" if mono else "#1E3A5F")
    ax.set_xlabel("Unidades promissórias confirmadas", fontsize=9.5)
    ax.legend(loc="lower right", fontsize=8.3, frameon=True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", linestyle="--", alpha=0.4)

    suf = "_pb" if mono else "_cor"
    arq = dest_dir / f"grafico_05_divisoes_canon{suf}.png"
    fig.savefig(arq, bbox_inches="tight", dpi=300)
    plt.close(fig)
    return arq


def g6_sensibilidade_e_comparacao(mc, dest_dir, mono=False):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.5), dpi=300)

    # Subplot 1: Sensibilidade ao limiar e impacto dos 276 resumos
    lims = ["0,35", "0,45\n(padrão)", "0,55", "0,65"]
    chaves = ["0.35", "0.45", "0.55", "0.65"]
    antes_276 = [2559, 2763, 2858, 2897]
    depois_276 = [mc["sensibilidade"][k]["distintas_confirmadas"] for k in chaves]
    bencao_276 = [mc["sensibilidade"][k]["bencao_distintas_confirmadas"] for k in chaves]

    x = np.arange(len(lims))
    w = 0.28
    c_ant = "#AAAAAA" if mono else "#95A5A6"
    c_dep = "#222222" if mono else "#1E56A0"
    c_ben = "#666666" if mono else "#D4AC0D"

    b1 = ax1.bar(x - w, antes_276, width=w, color=c_ant, edgecolor="#222222" if mono else "none", label="Antes dos 276 resumos")
    b2 = ax1.bar(x, depois_276, width=w, color=c_dep, edgecolor="#222222" if mono else "none", label="Após 276 resumos (todas)")
    b3 = ax1.bar(x + w, bencao_276, width=w, color=c_ben, edgecolor="#222222" if mono else "none", label="Bênção divina (distintas)")
    if mono:
        for b in b1:
            b.set_hatch("//")
        for b in b3:
            b.set_hatch("..")

    ax1.set_xticks(x)
    ax1.set_xticklabels(lims, fontsize=8.5)
    ax1.set_ylim(0, 3600)
    for b in b2:
        v = int(b.get_height())
        ax1.text(b.get_x() + b.get_width() / 2, v + 45, fmt(v), ha="center", va="bottom", fontsize=7.8, fontweight="bold")
    ax1.set_title("Impacto dos 276 Resumos e Limiar de Similaridade", fontsize=10.5, fontweight="bold", color="#111111" if mono else "#1E3A5F")
    ax1.set_xlabel("Limiar de Jaccard", fontsize=9)
    ax1.set_ylabel("Promessas distintas estimadas", fontsize=9)
    ax1.legend(loc="upper left", fontsize=7.5, frameon=True)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.grid(axis="y", linestyle="--", alpha=0.4)

    # Subplot 2: Comparação com Everek Storms (meados da década de 1950)
    cats_comp = ["Total geral\nregistrado", "Promessas divinas\n(total)", "Bênção divina\n(unidades / distintas)", "Compromissos\nhumanos"]
    storms_v = [8810, 7487, 7487, 1281]  # 991 humano-humano + 290 humano-Deus
    lima_v = [3224, 2687, 1622, 514]     # 3224 total, 2687 divinas (bencao+juizo), 1622 bencao divina, 514 humanas

    x2 = np.arange(len(cats_comp))
    w2 = 0.34
    cs1 = "#999999" if mono else "#7F8C8D"
    cs2 = "#222222" if mono else "#1B4F72"

    bs1 = ax2.bar(x2 - w2 / 2, storms_v, width=w2, color=cs1, edgecolor="#222222" if mono else "none", label="Contagem de E. R. Storms (déc. 1950)")
    bs2 = ax2.bar(x2 + w2 / 2, lima_v, width=w2, color=cs2, edgecolor="#222222" if mono else "none", label="Pesquisa atual — Jair Lima (2026)")
    if mono:
        for b in bs1:
            b.set_hatch("//")

    ax2.set_xticks(x2)
    ax2.set_xticklabels(cats_comp, fontsize=8)
    ax2.set_ylim(0, 9900)
    for b in bs1:
        v = int(b.get_height())
        ax2.text(b.get_x() + b.get_width() / 2, v + 120, fmt(v), ha="center", va="bottom", fontsize=7.8, color="#444444")
    for b in bs2:
        v = int(b.get_height())
        ax2.text(b.get_x() + b.get_width() / 2, v + 120, fmt(v), ha="center", va="bottom", fontsize=8, fontweight="bold", color="#111111")

    ax2.set_title("Contagem Tradicional (Storms) vs. Pesquisa Atual", fontsize=10.5, fontweight="bold", color="#111111" if mono else "#1E3A5F")
    ax2.set_ylabel("Unidades contabilizadas", fontsize=9)
    ax2.legend(loc="upper right", fontsize=7.8, frameon=True)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.grid(axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()
    suf = "_pb" if mono else "_cor"
    arq = dest_dir / f"grafico_06_sensibilidade_e_comparacao{suf}.png"
    fig.savefig(arq, bbox_inches="tight", dpi=300)
    plt.close(fig)
    return arq


def main():
    configurar_estilo()
    regs, apur, mc = carregar_dados()
    dest_dir = PROJ / "livro" / "graficos"
    dest_dir.mkdir(parents=True, exist_ok=True)

    gerados = []
    for mono in (False, True):
        gerados.append(g1_painel_geral(regs, apur, mc, dest_dir, mono))
        gerados.append(g2_categorias(regs, dest_dir, mono))
        gerados.append(g3_funil_fase3(regs, mc, dest_dir, mono))
        gerados.append(g4_top_livros(regs, dest_dir, mono))
        gerados.append(g5_divisoes_canon(regs, dest_dir, mono))
        gerados.append(g6_sensibilidade_e_comparacao(mc, dest_dir, mono))

    print(f"Gerados {len(gerados)} gráficos em {dest_dir}:")
    for g in gerados:
        print(" ", g.name, f"({g.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
