"""Gera os gráficos individuais redesenhados para leitura confortável no formato A5 (14,8 x 21,0 cm; largura útil de mancha 10,8 cm):
- Nenhum painel de KPIs em imagem pequena (o painel geral passa a ser página exclusiva com tipografia nativa do Word entre 30 e 44 pt!).
- Todos os gráficos separados (nenhum gráfico lado a lado / 2 colunas).
- Proporção calibrada para A5 (largura de figura 6.2 pol., fontes entre 10 e 13 pt, rótulos diretos nas barras).
- Salva em PNG de alta resolução (450 DPI) E em SVG/PDF vetorial, nas versões colorida (`_cor`) e escala de cinza com hachuras (`_pb`).
"""
import json
import sys
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PESQ = Path(r"C:\Users\jairs\Claude\Promessas-da-Biblia-by-Jair-Lima")
PROJ = Path(r"C:\Users\jairs\Documents\Meus Estudos Biblicos\Livros Teologia\As Promessas da Biblia (titulo provisorio)")

sys.path.insert(0, str(PESQ / "scripts"))
from lib_promessas import ler_jsonl  # noqa: E402

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
    ("Pentateuco (5 livros)", ["GEN", "EXO", "LEV", "NUM", "DEU"]),
    ("Históricos AT (12 livros)", ["JOS", "JDG", "RUT", "1SA", "2SA", "1KI", "2KI", "1CH", "2CH", "EZR", "NEH", "EST"]),
    ("Poéticos e Sapienciais (5 livros)", ["JOB", "PSA", "PRO", "ECC", "SNG"]),
    ("Profetas Maiores (5 livros)", ["ISA", "JER", "LAM", "EZK", "DAN"]),
    ("Profetas Menores (12 livros)", ["HOS", "JOL", "AMO", "OBA", "JON", "MIC", "NAM", "HAB", "ZEP", "HAG", "ZEC", "MAL"]),
    ("Evangelhos e Atos (5 livros)", ["MAT", "MRK", "LUK", "JHN", "ACT"]),
    ("Epístolas e Apocalipse (22 livros)", ["ROM", "1CO", "2CO", "GAL", "EPH", "PHP", "COL", "1TH", "2TH", "1TI", "2TI", "TIT", "PHM", "HEB", "JAS", "1PE", "2PE", "1JN", "2JN", "3JN", "JUD", "REV"]),
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
    plt.rcParams["axes.edgecolor"] = "#999999"
    plt.rcParams["axes.linewidth"] = 0.9
    plt.rcParams["xtick.labelsize"] = 9.5
    plt.rcParams["ytick.labelsize"] = 10.0


def salvar(fig, dest_dir, nome_base, mono):
    suf = "_pb" if mono else "_cor"
    arq_png = dest_dir / f"{nome_base}{suf}.png"
    arq_svg = dest_dir / f"{nome_base}{suf}.svg"
    fig.savefig(arq_png, bbox_inches="tight", dpi=450)
    fig.savefig(arq_svg, bbox_inches="tight")
    plt.close(fig)
    return arq_png


def g2_categorias(regs, dest_dir, mono=False):
    cat = Counter(r["categoria"] for r in regs)
    itens = sorted(cat.items(), key=lambda x: x[1])
    nomes = [ROTULO_CAT.get(k, k) for k, _ in itens]
    vals = [v for _, v in itens]
    tot = len(regs)

    fig, ax = plt.subplots(figsize=(6.4, 4.8), dpi=450)
    cores = []
    for k, _ in itens:
        if mono:
            cores.append("#2B2B2B" if "bencao" in k or "beneficio" in k else "#8C8C8C")
        else:
            if k in ("divina_bencao", "apostolica_garantia_bencao", "patriarcal_bencao"):
                cores.append("#1E56A0")
            elif k in ("divina_juizo", "divina_sentenca", "apostolica_garantia_juizo", "patriarcal_juizo"):
                cores.append("#A63A2B")
            elif "humana" in k:
                cores.append("#2E7D5B")
            else:
                cores.append("#6B5B95")

    bars = ax.barh(nomes, vals, color=cores, edgecolor="#111111" if mono else "#222222", linewidth=0.6, height=0.68)
    if mono:
        for bar, (k, _) in zip(bars, itens):
            if "juizo" in k or "sentenca" in k or "prejuizo" in k:
                bar.set_hatch("//")

    ax.set_xlim(0, max(vals) * 1.30)
    for bar, v in zip(bars, vals):
        pct = 100 * v / tot
        ax.text(v + 20, bar.get_y() + bar.get_height() / 2, f"{fmt(v)} ({pct:.1f}%)", va="center", ha="left", fontsize=9.5, fontweight="bold", color="#111111")

    ax.set_title("As 10 Categorias da Pesquisa (3.224 Unidades Confirmadas)", fontsize=11.5, fontweight="bold", pad=10, color="#111111" if mono else "#1E3A5F")
    ax.set_xlabel("Unidades promissórias confirmadas", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", linestyle="--", alpha=0.45)
    return salvar(fig, dest_dir, "grafico_02_dez_categorias", mono)


def g3_funil_fase3(regs, mc, dest_dir, mono=False):
    etapas = [
        "1. Candidatas iniciais\n(Fases 1 e 2)",
        "2. Rejeitadas na Fase 3\n(332 casos = 334 unid.)",
        "3. Consolidadas na Fase 3\n(granularidade: 34 casos)",
        "4. Duplicatas estritas\n(mesmo versículo/objeto)",
        "5. Unidades confirmadas\n(1.211 acordo + 2.013 arb.)",
        "6. Promessas distintas estimadas\n(estimativa Jaccard 0,45)",
    ]
    valores = [3609, -334, -37, -14, 3224, 2945]
    textos = ["3.609", "-334", "-37", "-14", "3.224", "2.945"]

    fig, ax = plt.subplots(figsize=(6.4, 4.5), dpi=450)
    y = np.arange(len(etapas))[::-1]
    larguras = [abs(v) for v in valores]
    if mono:
        cores = ["#4D4D4D", "#B0B0B0", "#B0B0B0", "#B0B0B0", "#1F1F1F", "#3B3B3B"]
    else:
        cores = ["#4A6FA5", "#C0392B", "#D35400", "#8E44AD", "#1B4F72", "#1E8449"]

    bars = ax.barh(y, larguras, color=cores, edgecolor="#111111" if mono else "#222222", linewidth=0.6, height=0.62)
    if mono:
        for i in (1, 2, 3):
            bars[i].set_hatch("//")

    ax.set_yticks(y)
    ax.set_yticklabels(etapas, fontsize=9.5)
    ax.set_xlim(0, 4450)
    for bar, t, v in zip(bars, textos, larguras):
        ax.text(v + 60, bar.get_y() + bar.get_height() / 2, f"{t}", va="center", ha="left", fontsize=10, fontweight="bold", color="#111111")

    ax.set_title("Conciliação das 3 Fases: de 3.609 Candidatas a 3.224 Confirmadas", fontsize=11.2, fontweight="bold", pad=10, color="#111111" if mono else "#1E3A5F")
    ax.set_xlabel("Unidades promissórias", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", linestyle="--", alpha=0.45)
    return salvar(fig, dest_dir, "grafico_03_funil_conciliacao", mono)


def g4_top_livros(regs, dest_dir, mono=False):
    por_liv = Counter(r["livro"] for r in regs)
    bencao_liv = Counter(r["livro"] for r in regs if r["categoria"] in ("divina_bencao", "apostolica_garantia_bencao", "patriarcal_bencao"))
    top15 = por_liv.most_common(15)[::-1]

    nomes = [f"{NOMES_LIV[k]}" for k, _ in top15]
    totais = [v for _, v in top15]
    bencaos = [bencao_liv[k] for k, _ in top15]
    outros = [t - b for t, b in zip(totais, bencaos)]

    fig, ax = plt.subplots(figsize=(6.4, 5.2), dpi=450)
    c_benc = "#2B2B2B" if mono else "#1E56A0"
    c_outr = "#BDBDBD" if mono else "#D98880"

    b1 = ax.barh(nomes, bencaos, color=c_benc, edgecolor="#111111" if mono else "#222222", linewidth=0.5, height=0.66, label="Bênção divina (ind. principal)")
    b2 = ax.barh(nomes, outros, left=bencaos, color=c_outr, edgecolor="#111111" if mono else "#222222", linewidth=0.5, height=0.66, label="Juízo divino, humanas e outras")
    if mono:
        for bar in b2:
            bar.set_hatch("//")

    ax.set_xlim(0, max(totais) * 1.25)
    for y_pos, t, b in zip(range(len(nomes)), totais, bencaos):
        ax.text(t + 6, y_pos, f"{t} ({b} bênção)", va="center", ha="left", fontsize=9.0, fontweight="bold", color="#111111")

    ax.set_title("Os 15 Livros com Maior Número de Unidades Confirmadas", fontsize=11.5, fontweight="bold", pad=10, color="#111111" if mono else "#1E3A5F")
    ax.set_xlabel("Unidades confirmadas", fontsize=10)
    ax.legend(loc="lower right", fontsize=8.8, frameon=True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", linestyle="--", alpha=0.45)
    return salvar(fig, dest_dir, "grafico_04_top15_livros", mono)


def g5_divisoes_canon(regs, dest_dir, mono=False):
    por_liv = Counter(r["livro"] for r in regs)
    benc_liv = Counter(r["livro"] for r in regs if r["categoria"] in ("divina_bencao", "apostolica_garantia_bencao", "patriarcal_bencao"))
    juiz_liv = Counter(r["livro"] for r in regs if r["categoria"] in ("divina_juizo", "divina_sentenca", "apostolica_garantia_juizo", "patriarcal_juizo"))

    grupos = [g for g, _ in DIVISAO_CANON][::-1]
    benc = [sum(benc_liv[l] for l in ls) for _, ls in DIVISAO_CANON][::-1]
    juiz = [sum(juiz_liv[l] for l in ls) for _, ls in DIVISAO_CANON][::-1]
    hum = [sum(por_liv[l] - benc_liv[l] - juiz_liv[l] for l in ls) for _, ls in DIVISAO_CANON][::-1]
    tots = [b + j + h for b, j, h in zip(benc, juiz, hum)]

    fig, ax = plt.subplots(figsize=(6.4, 4.6), dpi=450)
    c1 = "#222222" if mono else "#1E56A0"
    c2 = "#888888" if mono else "#C0392B"
    c3 = "#DEDEDE" if mono else "#2E7D5B"

    ax.barh(grupos, benc, color=c1, edgecolor="#111111", linewidth=0.5, height=0.6, label="Bênção divina (1.622)")
    j_bar = ax.barh(grupos, juiz, left=benc, color=c2, edgecolor="#111111", linewidth=0.5, height=0.6, label="Juízo e sentença divina (1.065)")
    left_h = [b + j for b, j in zip(benc, juiz)]
    h_bar = ax.barh(grupos, hum, left=left_h, color=c3, edgecolor="#111111", linewidth=0.5, height=0.6, label="Compromissos humanos e outros (537)")
    if mono:
        for bar in j_bar:
            bar.set_hatch("//")
        for bar in h_bar:
            bar.set_hatch("..")

    ax.set_xlim(0, max(tots) * 1.24)
    for y_pos, t in enumerate(tots):
        ax.text(t + 14, y_pos, f"{fmt(t)} ({100*t/len(regs):.1f}%)", va="center", ha="left", fontsize=9.2, fontweight="bold", color="#111111")

    ax.set_title("Unidades Confirmadas pelas 7 Divisões do Cânon (66 Livros)", fontsize=11.3, fontweight="bold", pad=10, color="#111111" if mono else "#1E3A5F")
    ax.set_xlabel("Unidades promissórias confirmadas", fontsize=10)
    ax.legend(loc="lower right", fontsize=8.5, frameon=True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", linestyle="--", alpha=0.45)
    return salvar(fig, dest_dir, "grafico_05_divisoes_canon", mono)


def g6_sensibilidade_individual(mc, dest_dir, mono=False):
    """Gráfico individual (não lado a lado!) para leitura confortável em A5: Impacto dos 276 resumos e sensibilidade ao limiar."""
    fig, ax = plt.subplots(figsize=(6.2, 4.2), dpi=450)
    lims = ["0,35", "0,45 (padrão)", "0,55", "0,65"]
    chaves = ["0.35", "0.45", "0.55", "0.65"]
    antes_276 = [2559, 2763, 2858, 2897]
    depois_276 = [mc["sensibilidade"][k]["distintas_confirmadas"] for k in chaves]
    bencao_276 = [mc["sensibilidade"][k]["bencao_distintas_confirmadas"] for k in chaves]

    x = np.arange(len(lims))
    w = 0.27
    c_ant = "#B0B0B0" if mono else "#95A5A6"
    c_dep = "#222222" if mono else "#1E56A0"
    c_ben = "#6E6E6E" if mono else "#D4AC0D"

    b1 = ax.bar(x - w, antes_276, width=w, color=c_ant, edgecolor="#111111", linewidth=0.6, label="Antes dos 276 resumos (todas)")
    b2 = ax.bar(x, depois_276, width=w, color=c_dep, edgecolor="#111111", linewidth=0.6, label="Após 276 resumos (todas distintas)")
    b3 = ax.bar(x + w, bencao_276, width=w, color=c_ben, edgecolor="#111111", linewidth=0.6, label="Bênção divina (distintas)")
    if mono:
        for b in b1:
            b.set_hatch("//")
        for b in b3:
            b.set_hatch("..")

    ax.set_xticks(x)
    ax.set_xticklabels(lims, fontsize=9.5, fontweight="bold")
    ax.set_ylim(0, 3650)
    for b in b1:
        v = int(b.get_height())
        ax.text(b.get_x() + b.get_width() / 2, v + 40, fmt(v), ha="center", va="bottom", fontsize=8.0, color="#444444")
    for b in b2:
        v = int(b.get_height())
        ax.text(b.get_x() + b.get_width() / 2, v + 40, fmt(v), ha="center", va="bottom", fontsize=8.8, fontweight="bold", color="#111111")
    for b in b3:
        v = int(b.get_height())
        ax.text(b.get_x() + b.get_width() / 2, v + 40, fmt(v), ha="center", va="bottom", fontsize=8.3, fontweight="bold", color="#222222")

    ax.set_title("Sensibilidade ao Limiar de Jaccard e Recuperação dos 276 Resumos", fontsize=11.0, fontweight="bold", pad=10, color="#111111" if mono else "#1E3A5F")
    ax.set_xlabel("Limiar de similaridade lexical de Jaccard", fontsize=9.8)
    ax.set_ylabel("Promessas distintas estimadas", fontsize=9.8)
    ax.legend(loc="upper left", fontsize=8.5, frameon=True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.45)
    return salvar(fig, dest_dir, "grafico_06_sensibilidade_jaccard", mono)


def g7_comparacao_storms_individual(dest_dir, mono=False):
    """Gráfico individual (separado do de sensibilidade!) para leitura ampla e confortável em A5: Storms vs. Pesquisa Atual."""
    fig, ax = plt.subplots(figsize=(6.2, 4.2), dpi=450)
    cats_comp = [
        "Total geral\nde registros",
        "Promessas divinas\n(total)",
        "Bênção divina\n(unidades confirmadas)",
        "Compromissos\nhumanos",
    ]
    storms_v = [8810, 7487, 7487, 1281]
    lima_v = [3224, 2687, 1622, 514]

    x = np.arange(len(cats_comp))
    w = 0.35
    cs1 = "#A0A0A0" if mono else "#7F8C8D"
    cs2 = "#222222" if mono else "#1B4F72"

    bs1 = ax.bar(x - w / 2, storms_v, width=w, color=cs1, edgecolor="#111111", linewidth=0.6, label="Contagem de E. R. Storms (déc. 1950)")
    bs2 = ax.bar(x + w / 2, lima_v, width=w, color=cs2, edgecolor="#111111", linewidth=0.6, label="Pesquisa atual — Jair Lima (2026)")
    if mono:
        for b in bs1:
            b.set_hatch("//")

    ax.set_xticks(x)
    ax.set_xticklabels(cats_comp, fontsize=9.2, fontweight="bold")
    ax.set_ylim(0, 10100)
    for b in bs1:
        v = int(b.get_height())
        ax.text(b.get_x() + b.get_width() / 2, v + 140, fmt(v), ha="center", va="bottom", fontsize=8.8, color="#333333")
    for b in bs2:
        v = int(b.get_height())
        ax.text(b.get_x() + b.get_width() / 2, v + 140, fmt(v), ha="center", va="bottom", fontsize=9.2, fontweight="bold", color="#111111")

    ax.set_title("Contagem Histórica de E. R. Storms vs. Pesquisa Atual (2026)", fontsize=11.2, fontweight="bold", pad=10, color="#111111" if mono else "#1E3A5F")
    ax.set_ylabel("Unidades contabilizadas", fontsize=9.8)
    ax.legend(loc="upper right", fontsize=8.8, frameon=True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.45)
    return salvar(fig, dest_dir, "grafico_07_comparacao_storms", mono)


def main():
    configurar_estilo()
    regs, apur, mc = carregar_dados()
    dest_dir = PROJ / "livro" / "graficos"
    dest_dir.mkdir(parents=True, exist_ok=True)

    gerados = []
    for mono in (False, True):
        gerados.append(g2_categorias(regs, dest_dir, mono))
        gerados.append(g3_funil_fase3(regs, mc, dest_dir, mono))
        gerados.append(g4_top_livros(regs, dest_dir, mono))
        gerados.append(g5_divisoes_canon(regs, dest_dir, mono))
        gerados.append(g6_sensibilidade_individual(mc, dest_dir, mono))
        gerados.append(g7_comparacao_storms_individual(dest_dir, mono))
        # Mantém cópia em grafico_06_sensibilidade_e_comparacao para compatibilidade com links antigos
        import shutil
        suf = "_pb" if mono else "_cor"
        shutil.copyfile(dest_dir / f"grafico_07_comparacao_storms{suf}.png", dest_dir / f"grafico_06_sensibilidade_e_comparacao{suf}.png")

    print(f"Gerados {len(gerados)} gráficos individuais de alta legibilidade (450 DPI + SVG vetorial) para formato A5.")


if __name__ == "__main__":
    main()
