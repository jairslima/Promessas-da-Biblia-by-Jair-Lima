"""Contagem derivada e reproduzível (controle A10). NÃO contém nenhuma regra exegética.

A categoria de contagem é derivada apenas de campos já decididos:
  divina_bencao        origem divina e natureza bencao   -> INDICADOR PRINCIPAL
  divina_juizo         origem divina e natureza juizo
  humana_beneficio     origem humana_em_nome_proprio e natureza bencao (voto, juramento, promessa de benefício)
  humana_prejuizo      origem humana_em_nome_proprio e natureza juizo (ameaça ou compromisso de causar prejuízo)
  adversaria_ou_falsa  origem adversaria_ou_falsa
Princípios sapienciais e demais unidades não promissórias ficam em `nao_promessas/` e são
relatados à parte (nunca somados às promessas).

Os totais são RESULTADO da pesquisa; nenhum número é meta. A saída não contém data nem
aleatoriedade: duas execuções sobre os mesmos arquivos geram saída idêntica.

Uso: python -I contar.py [--base dados] [--somente-congelados] [--saida arq.json]
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_promessas import *  # noqa: F401,F403
from validar_esquema import _carregar

AT = ("GEN EXO LEV NUM DEU JOS JDG RUT 1SA 2SA 1KI 2KI 1CH 2CH EZR NEH EST JOB PSA PRO ECC SNG ISA JER LAM "
      "EZK DAN HOS JOL AMO OBA JON MIC NAM HAB ZEP HAG ZEC MAL").split()


def categoria(r):
    o = r.get("origem_real")
    if o in ORIGENS_DIVINAS:
        return "divina_bencao" if r.get("natureza") == "bencao" else "divina_juizo"
    if o == "profetica_patriarcal":
        return "profetica_patriarcal_bencao" if r.get("natureza") == "bencao" else "profetica_patriarcal_juizo"
    if o == "humana_em_nome_proprio":
        return "humana_beneficio" if r.get("natureza") == "bencao" else "humana_prejuizo"
    if o == "adversaria_ou_falsa":
        return "adversaria_ou_falsa"
    return "fora_de_categoria"


def _inc(d, k, n=1):
    d[k] = d.get(k, 0) + n


def contar(base: Path, corpus: Corpus, somente_congelados=False, status=None):
    base = Path(base)
    problemas = []
    d = _carregar(base, problemas)
    if status:
        aceita = lambda r: r.get("status") in status
    elif somente_congelados:
        aceita = lambda r: r.get("status") == "congelada"
    else:
        aceita = lambda r: r.get("status") != "rejeitada"
    promessas = [r for _, _, r in d["promessas"] if aceita(r)]
    ids = {r["id"] for r in promessas}
    ocorr = [r for _, _, r in d["ocorrencias"] if r.get("promessa_id") in ids]
    nao_prom = [r for _, _, r in d["nao_promessas"] if aceita(r)]

    por_cat, por_promitente, por_origem, por_testamento, por_livro = {}, {}, {}, {}, {}
    por_cat_familia = {}
    for r in promessas:
        c = categoria(r)
        _inc(por_cat, c)
        _inc(por_origem, r.get("origem_real"))
        if c.startswith("divina"):
            _inc(por_promitente, f"{c}:{r.get('promitente')}")
        liv = str(r.get("ref_inicio"))[:3]
        _inc(por_livro, f"{c}:{liv}")
        _inc(por_testamento, f"{c}:{'AT' if liv in AT else 'NT'}")
        por_cat_familia.setdefault(c, set()).add(r.get("familia_id"))
    cat_de = {r["id"]: categoria(r) for r in promessas}
    ocorr_por_tipo, ocorr_por_cat = {}, {}
    versiculos = {"qualquer_categoria": set(), "divina_bencao": set()}
    cont_por_versiculo = {}
    for o in ocorr:
        _inc(ocorr_por_tipo, o.get("tipo"))
        _inc(ocorr_por_cat, cat_de[o["promessa_id"]])
        refs = corpus.intervalo(o.get("ref_inicio"), o.get("ref_fim")) or []
        for x in refs:
            versiculos["qualquer_categoria"].add(x)
            if cat_de[o["promessa_id"]] == "divina_bencao":
                versiculos["divina_bencao"].add(x)
            cont_por_versiculo.setdefault(x, set()).add(o["promessa_id"])
    multiplas = sum(1 for s in cont_por_versiculo.values() if len(s) >= 2)
    # nível B fundamental: ignora a condição (preserva a contagem fina; ex.: Gn 18:26-32)
    fund = {}
    for r in promessas:
        fund.setdefault(categoria(r), set()).add((r.get("acao_canonica"), r.get("objeto_canonico"), r.get("beneficiario_canonico")))
    dev = [r for _, _, r in d.get("desenvolvimento", [])]
    dev_tipo = {}
    for r in dev:
        _inc(dev_tipo, r.get("tipo"))
    nao_por_tipo = {}
    for r in nao_prom:
        _inc(nao_por_tipo, r.get("tipo_unidade"))

    entradas = {}
    for sub in ("promessas", "ocorrencias", "nao_promessas", "varredura"):
        pasta = base / sub
        for f in sorted(pasta.glob("*.jsonl")) if pasta.exists() else []:
            entradas[f"{sub}/{f.name}"] = sha256_arquivo(f)
    for nome in ("familias.jsonl", "decisoes.jsonl", "revisao_humana.jsonl", "equivalencias.json"):
        if (base / nome).exists():
            entradas[nome] = sha256_arquivo(base / nome)

    return {
        "aviso": "Totais são resultado da pesquisa, não metas. Indicador principal = promessas divinas de bênção.",
        "somente_congelados": bool(somente_congelados),
        "filtro_de_status": sorted(status) if status else None,
        "indicador_principal_promessas_divinas_de_bencao": por_cat.get("divina_bencao", 0),
        "nivel_B_promessas_distintas_por_categoria": dict(sorted(por_cat.items())),
        "nivel_A_familias_por_categoria": {k: len(v) for k, v in sorted(por_cat_familia.items())},
        "nivel_B_fundamental_por_categoria": {k: len(v) for k, v in sorted(fund.items())},
        "contagem_ampliada_bencao": por_cat.get("divina_bencao", 0) + por_cat.get("profetica_patriarcal_bencao", 0),
        "nivel_D_desenvolvimento_por_tipo_NAO_SOMADO": dict(sorted(dev_tipo.items())),
        "nivel_C_ocorrencias_por_tipo": dict(sorted(ocorr_por_tipo.items())),
        "nivel_C_ocorrencias_por_categoria": dict(sorted(ocorr_por_cat.items())),
        "promessas_por_origem_real": dict(sorted(por_origem.items())),
        "promessas_divinas_por_promitente": dict(sorted(por_promitente.items())),
        "promessas_por_testamento": dict(sorted(por_testamento.items())),
        "promessas_por_livro": dict(sorted(por_livro.items())),
        "unidades_fora_da_contagem_de_promessas_por_tipo": dict(sorted(nao_por_tipo.items())),
        "versiculos_com_ocorrencia_qualquer_categoria": len(versiculos["qualquer_categoria"]),
        "versiculos_com_ocorrencia_divina_de_bencao": len(versiculos["divina_bencao"]),
        "versiculos_com_duas_ou_mais_promessas_distintas": multiplas,
        "sha256_das_entradas": entradas,
        "problemas_de_leitura": [str(p) for p in problemas],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=str(RAIZ / "dados"))
    ap.add_argument("--somente-congelados", action="store_true")
    ap.add_argument("--status", help="lista separada por vírgulas, ex.: reconciliada,revisada_humano,congelada")
    ap.add_argument("--saida")
    a = ap.parse_args()
    res = contar(Path(a.base), Corpus(), a.somente_congelados, set(a.status.split(',')) if a.status else None)
    txt = json.dumps(res, ensure_ascii=False, indent=2, sort_keys=True)
    if a.saida:
        Path(a.saida).write_text(txt + "\n", encoding="utf-8", newline="\n")
    print(txt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
