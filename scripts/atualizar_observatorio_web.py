"""Sincroniza e prepara todos os artefatos públicos do Observatório das Promessas Bíblicas em docs/ e na raiz do repositório público:
1. Limpa nomes comerciais de modelos da interface pública (docs/dados_observatorio.js), preservando os JSONL históricos intactos.
2. Copia os arquivos de download (CSV, XLSX, Artigo, Memória de Cálculo, Relatório de Originalidade, Dicionário de Campos, Limitações, Apêndice Técnico) e a pasta graficos/ para dentro de docs/, eliminando qualquer erro 404 no GitHub Pages (/Promessas-da-Biblia-by-Jair-Lima/).
3. Gera as páginas HTML de leitura acadêmica docs/artigo.html e docs/memoria-de-calculo.html.
4. Remove arquivos operacionais de orientação de agentes (como GEMINI.md) do repositório público, preservando-os localmente.
"""
import html
import json
import re
import shutil
from pathlib import Path

PUB = Path(r"C:\Users\jairs\Antigravity\Promessas-da-Biblia-by-Jair-Lima-Publico")
DOCS = PUB / "docs"
PROJ = Path(r"C:\Users\jairs\Documents\Meus Estudos Biblicos\Livros Teologia\As Promessas da Biblia (titulo provisorio)")


def limpar_dados_observatorio():
    js_path = DOCS / "dados_observatorio.js"
    raw = js_path.read_text(encoding="utf-8")
    prefix = "window.DADOS_OBSERVATORIO = "
    assert raw.startswith(prefix)
    json_str = raw[len(prefix):].strip().rstrip(";")
    data = json.loads(json_str)

    data["meta"]["livros_com_registros"] = 64
    data["meta"]["categorias"] = 10
    for r in data["registros"]:
        via = r.get("via", "")
        if "acordo" in via.lower():
            r["via"] = "Acordo direto (Etapas 1 e 2)"
        else:
            r["via"] = "Arbitragem exegética (Etapa 3)"

    out_js = prefix + json.dumps(data, ensure_ascii=False) + ";\n"
    js_path.write_text(out_js, encoding="utf-8", newline="\n")
    print(f"[OK] dados_observatorio.js atualizado ({len(data['registros'])} registros sem nomes comerciais de modelos).")


def md_para_html_academico(md_text: str, titulo_pag: str, arq_md_download: str) -> str:
    """Converte Markdown acadêmico (títulos, tabelas, listas, parágrafos, negrito/itálico/código) em HTML editorial elegante."""
    linhas = md_text.splitlines()
    blocos = []
    in_table = False
    table_rows = []
    in_list = False

    def format_inline(s: str) -> str:
        s = html.escape(s)
        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        return s

    def flush_table():
        nonlocal in_table, table_rows
        if not in_table or not table_rows:
            return
        h = ['<div class="table-wrap"><table>']
        for idx, r in enumerate(table_rows):
            cells = [c.strip() for c in r.strip().strip("|").split("|")]
            if idx == 1 and all(re.match(r"^:?-{2,}:?$", c.replace(" ", "")) for c in cells if c):
                continue
            tag = "th" if idx == 0 else "td"
            sec = "thead" if idx == 0 else None
            if idx == 0:
                h.append("<thead><tr>" + "".join(f"<{tag}>{format_inline(c)}</{tag}>" for c in cells) + "</tr></thead><tbody>")
            else:
                h.append("<tr>" + "".join(f"<{tag}>{format_inline(c)}</{tag}>" for c in cells) + "</tr>")
        h.append("</tbody></table></div>")
        blocos.append("\n".join(h))
        in_table = False
        table_rows = []

    def flush_list():
        nonlocal in_list
        if in_list:
            blocos.append("</ul>")
            in_list = False

    for ln in linhas:
        s = ln.strip()
        if s.startswith("|") and s.endswith("|"):
            flush_list()
            in_table = True
            table_rows.append(s)
            continue
        else:
            flush_table()

        if not s:
            flush_list()
            continue
        if s == "---":
            flush_list()
            blocos.append("<hr />")
        elif s.startswith("# "):
            flush_list()
            blocos.append(f"<h1>{format_inline(s[2:])}</h1>")
        elif s.startswith("## "):
            flush_list()
            blocos.append(f"<h2>{format_inline(s[3:])}</h2>")
        elif s.startswith("### "):
            flush_list()
            blocos.append(f"<h3>{format_inline(s[4:])}</h3>")
        elif s.startswith("* ") or s.startswith("- "):
            if not in_list:
                blocos.append("<ul>")
                in_list = True
            blocos.append(f"<li>{format_inline(s[2:])}</li>")
        elif re.match(r"^\d+\.\s+", s):
            if not in_list:
                blocos.append("<ul>")
                in_list = True
            blocos.append(f"<li>{format_inline(s)}</li>")
        else:
            flush_list()
            blocos.append(f"<p>{format_inline(s)}</p>")

    flush_table()
    flush_list()
    corpo = "\n".join(blocos)

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(titulo_pag)} | Observatório das Promessas Bíblicas — Jair Lima</title>
  <style>
    :root {{
      --navy-dark: #10233f;
      --navy: #1b365d;
      --gold: #8b6914;
      --bg: #faf8f3;
      --card: #ffffff;
      --border: #dfd9cc;
      --text: #2c3545;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: Georgia, 'Times New Roman', serif; background: var(--bg); color: var(--text); line-height: 1.75; }}
    header {{
      background: linear-gradient(180deg, var(--navy-dark), var(--navy));
      color: #fff; padding: 2rem 1.25rem; text-align: center; border-bottom: 4px solid #b88b1d;
      font-family: 'Segoe UI', system-ui, sans-serif;
    }}
    header a {{ color: #f3d47c; text-decoration: none; font-weight: 600; }}
    .toolbar {{
      max-width: 960px; margin: 1.2rem auto 0; padding: 0 1rem;
      display: flex; justify-content: space-between; flex-wrap: wrap; gap: 0.6rem;
      font-family: 'Segoe UI', system-ui, sans-serif;
    }}
    .btn {{
      display: inline-block; padding: 0.5rem 1rem; border-radius: 5px; font-size: 0.88rem;
      font-weight: 600; text-decoration: none; background: var(--navy); color: #fff;
    }}
    .btn.gold {{ background: var(--gold); }}
    article {{
      max-width: 960px; margin: 1.2rem auto 3rem; background: var(--card);
      border: 1px solid var(--border); border-radius: 8px; padding: 2.5rem 2.8rem;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }}
    h1 {{ font-size: 1.75rem; color: var(--navy-dark); margin-bottom: 0.8rem; line-height: 1.3; }}
    h2 {{ font-size: 1.38rem; color: var(--navy); margin: 1.8rem 0 0.8rem; padding-bottom: 0.4rem; border-bottom: 1px solid var(--border); }}
    h3 {{ font-size: 1.14rem; color: var(--navy-dark); margin: 1.3rem 0 0.5rem; }}
    p {{ margin-bottom: 1rem; text-align: justify; }}
    ul {{ margin: 0.5rem 0 1.1rem 1.5rem; }}
    li {{ margin-bottom: 0.45rem; }}
    hr {{ border: none; border-top: 1px solid var(--border); margin: 1.6rem 0; }}
    code {{ font-family: Consolas, monospace; font-size: 0.88em; background: #f3f0e8; padding: 0.1rem 0.35rem; border-radius: 3px; }}
    .table-wrap {{ overflow-x: auto; margin: 1.2rem 0; border: 1px solid var(--border); border-radius: 6px; }}
    table {{ width: 100%; border-collapse: collapse; font-family: 'Segoe UI', system-ui, sans-serif; font-size: 0.88rem; }}
    th, td {{ padding: 0.6rem 0.8rem; border-bottom: 1px solid var(--border); text-align: left; vertical-align: top; }}
    th {{ background: #f3f0e8; color: var(--navy-dark); font-weight: 700; }}
    footer {{ text-align: center; padding: 2rem 1rem; font-family: 'Segoe UI', system-ui, sans-serif; font-size: 0.86rem; color: #546072; }}
  </style>
</head>
<body>
  <header>
    <div style="font-size:0.78rem;text-transform:uppercase;letter-spacing:1.8px;color:#e6c875;font-weight:700;">Observatório das Promessas Bíblicas</div>
    <div style="font-size:1.35rem;font-weight:700;margin:0.3rem 0;">{html.escape(titulo_pag)}</div>
    <div style="font-size:0.9rem;color:#e2e8f0;">Pesquisa e autoria: Jair Lima • Lima Editora do Brasil, 2026</div>
  </header>
  <div class="toolbar">
    <a class="btn" href="./index.html">← Voltar ao Observatório das Promessas Bíblicas</a>
    <a class="btn gold" href="./{arq_md_download}" download="{arq_md_download}">Baixar documento original (.MD)</a>
  </div>
  <article>
    {corpo}
  </article>
  <footer>
    Observatório das Promessas Bíblicas • Pesquisa e autoria: Jair Lima • Lima Editora do Brasil, 2026.
  </footer>
</body>
</html>
"""


def main():
    limpar_dados_observatorio()

    # Copiar arquivos de download para docs/ (garantindo HTTP 200 em /Promessas-da-Biblia-by-Jair-Lima/<arquivo>)
    arquivos_publicos = [
        "catalogo-digital-completo.csv",
        "catalogo-digital-completo.xlsx",
        "ARTIGO_CIENTIFICO_PROMESSAS_DA_BIBLIA.md",
        "MEMORIA_DE_CALCULO.md",
        "RELATORIO_ORIGINALIDADE_CIENTIFICA.md",
        "DICIONARIO_DE_CAMPOS.md",
        "RELATORIO_LIMITACOES.md",
        "DOCUMENTACAO_TECNICA_REPRODUTIBILIDADE.md",
        "CONTAGEM_GERAL.md",
    ]
    for nm in arquivos_publicos:
        src = PUB / nm
        if src.exists():
            shutil.copy2(src, DOCS / nm)

    # Sincronizar também para a pasta do livro e publicacao-zenodo
    for nm in ("ARTIGO_CIENTIFICO_PROMESSAS_DA_BIBLIA.md", "MEMORIA_DE_CALCULO.md", "RELATORIO_ORIGINALIDADE_CIENTIFICA.md"):
        shutil.copy2(PUB / nm, PROJ / nm)
        if (PROJ / "publicacao-zenodo").exists():
            shutil.copy2(PUB / nm, PROJ / "publicacao-zenodo" / nm)

    # Copiar gráficos para docs/graficos/
    docs_graf = DOCS / "graficos"
    docs_graf.mkdir(parents=True, exist_ok=True)
    for g in (PUB / "graficos").glob("*"):
        if g.is_file():
            shutil.copy2(g, docs_graf / g.name)

    # Gerar páginas HTML de leitura do Artigo Científico e da Memória de Cálculo
    art_md = (PUB / "ARTIGO_CIENTIFICO_PROMESSAS_DA_BIBLIA.md").read_text(encoding="utf-8")
    (DOCS / "artigo.html").write_text(
        md_para_html_academico(art_md, "Artigo Científico: Quantas promessas existem na Bíblia?", "ARTIGO_CIENTIFICO_PROMESSAS_DA_BIBLIA.md"),
        encoding="utf-8",
        newline="\n",
    )

    mem_md = (PUB / "MEMORIA_DE_CALCULO.md").read_text(encoding="utf-8")
    (DOCS / "memoria-de-calculo.html").write_text(
        md_para_html_academico(mem_md, "Memória de Cálculo da Contagem de Promessas", "MEMORIA_DE_CALCULO.md"),
        encoding="utf-8",
        newline="\n",
    )

    # Remover GEMINI.md do repositório público (preservado localmente na pasta da pesquisa e do livro)
    gem_pub = PUB / "GEMINI.md"
    if gem_pub.exists():
        gem_pub.unlink()
        print("[OK] GEMINI.md removido do repositório público (preservado localmente).")

    print("[OK] Todos os arquivos e páginas de docs/ sincronizados com sucesso!")


if __name__ == "__main__":
    main()
