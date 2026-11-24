"""Controles A5 (esquema), A8 (órfãos e ciclos), A9 (consistência cruzada) e A12 (coerência de categoria).

Uso: python -I validar_esquema.py [--base dados] [--exigir-passes]
Somente leitura. Saída 0 sem problemas, 1 com problemas.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_promessas import *  # noqa: F401,F403

RE_ID = {
    "promessa": re.compile(r"^P-[0-9A-Z]{3}-\d{4}$"),
    "ocorrencia": re.compile(r"^O-[0-9A-Z]{3}-\d{4}$"),
    "nao_promessa": re.compile(r"^N-[0-9A-Z]{3}-\d{4}$"),
    "familia": re.compile(r"^F-[A-Z0-9_-]+$"),
    "decisao": re.compile(r"^D-\d+$"),
    "revisao": re.compile(r"^R-\d+$"),
    "desenvolvimento": re.compile(r"^V-[0-9A-Z]{3}-\d{4}$"),
}


def _adder(problemas, arq, linha, rid):
    def add(controle, msg):
        problemas.append(Problema(controle, arq, linha, rid, msg))
    return add


def _checa_unidade(u, add, base_corpus_permite=True):
    validar_unidade_comum(u, add)


def validar_registro_varredura(rec, add, arquivo):
    if parse_ref(rec.get("ref")) is None:
        add("A5", f"ref inválida: {rec.get('ref')!r}")
    if rec.get("passe") not in (1, 2):
        add("A5", "passe deve ser 1 ou 2")
    if not str(rec.get("leitor", "")).strip():
        add("A5", "leitor ausente")
    if rec.get("estado") not in ESTADOS_VARREDURA:
        add("A5", f"estado inválido: {rec.get('estado')!r}")
    if not RE_DATA.match(str(rec.get("data", ""))):
        add("A5", "data ausente ou fora do formato ISO")
    unidades = rec.get("unidades", [])
    parte = rec.get("parte_de", [])
    if not isinstance(unidades, list) or not isinstance(parte, list):
        add("A5", "unidades e parte_de devem ser listas")
        return
    est = rec.get("estado")
    if est == "sem_unidade" and (unidades or parte):
        add("A9", "estado sem_unidade com unidades ou parte_de preenchidos")
    if est == "com_unidade" and not unidades:
        add("A9", "estado com_unidade sem unidades iniciadas neste versículo")
    if est == "parte_de_unidade" and (unidades or not parte):
        add("A9", "estado parte_de_unidade exige parte_de e nenhuma unidade iniciada")
    for u in unidades:
        uadd = _adder_prefix(add, u.get("uid", "?"))
        m = RE_UID.match(str(u.get("uid", "")))
        if not m:
            uadd("A5", "uid fora do formato U<passe>-<LIV>-<cap3>:<ver3>-<n>")
        else:
            if int(m.group(1)) != rec.get("passe"):
                uadd("A5", "uid de passe diferente do registro")
            ref_uid = f"{m.group(2)} {int(m.group(3))}:{int(m.group(4))}"
            if ref_uid != rec.get("ref") or u.get("ref_inicio") != rec.get("ref"):
                uadd("A9", "uid e ref_inicio devem coincidir com o versículo em que a unidade começa")
        validar_unidade_comum(u, uadd)


def _adder_prefix(add, uid):
    def f(c, m):
        add(c, f"[{uid}] {m}")
    return f


def validar_promessa(rec, add):
    if not RE_ID["promessa"].match(str(rec.get("id", ""))):
        add("A5", "id fora do formato P-LIV-0000")
    if rec.get("tipo_unidade") != "promessa":
        add("A5", "registro em promessas/ deve ter tipo_unidade promessa")
    validar_unidade_comum(rec, add)
    if rec.get("relacao") not in RELACOES:
        add("A5", f"relacao inválida: {rec.get('relacao')!r}")
    if not RE_ID["familia"].match(str(rec.get("familia_id", ""))):
        add("A5", "familia_id fora do formato F-...")
    for c in ("acao_canonica", "objeto_canonico", "beneficiario_canonico", "condicao_canonica"):
        if not RE_SLUG.match(str(rec.get(c, ""))):
            add("A5", f"{c} ausente ou fora do vocabulário canônico (a-z, 0-9, _)")
    if not str(rec.get("criterio_distincao", "")).strip():
        add("A5", "criterio_distincao obrigatório")
    if rec.get("aplicabilidade") not in APLICABILIDADES:
        add("A5", f"aplicabilidade inválida: {rec.get('aplicabilidade')!r}")
    elif rec["aplicabilidade"] == "estendida_pelo_texto":
        refs = rec.get("refs_extensao")
        if not isinstance(refs, list) or not refs:
            add("A9", "estendida_pelo_texto exige refs_extensao")
    if rec.get("etapa_reveladora") not in ETAPAS:
        add("A5", f"etapa_reveladora inválida: {rec.get('etapa_reveladora')!r}")
    cum = rec.get("cumprimento_status")
    if cum not in CUMPRIMENTOS:
        add("A5", f"cumprimento_status inválido: {cum!r}")
    elif cum == "nao_declarado":
        if not str(rec.get("cumprimento_justificativa", "")).strip():
            add("A9", "nao_declarado exige cumprimento_justificativa")
    else:
        if not isinstance(rec.get("refs_cumprimento"), list) or not rec["refs_cumprimento"]:
            add("A9", "cumprimento_status exige refs_cumprimento")
    if rec.get("status") not in STATUS_PROMESSA:
        add("A5", f"status inválido: {rec.get('status')!r}")
    if rec.get("campos_pendentes") and rec.get("status") in ("revisada_humano", "congelada"):
        add("A9", f"registro com campos pendentes não pode estar {rec['status']}: {rec['campos_pendentes']}")
    if rec.get("cumprimento_status") == "correspondencia_narrativa" and not rec.get("refs_cumprimento"):
        add("A9", "correspondencia_narrativa exige refs_cumprimento")
    if rec.get("grupo_fundamental") is not None and not re.match(r"^PF-[0-9A-Z]{3}-\d{4}$", str(rec.get("grupo_fundamental"))):
        add("A5", "grupo_fundamental fora do formato PF-LIV-0000")
    if not isinstance(rec.get("unidades_origem"), list) or not rec["unidades_origem"]:
        add("A5", "unidades_origem deve listar ao menos um uid de passe")
    if not str(rec.get("criado_por", "")).strip() or not RE_DATA.match(str(rec.get("criado_em", ""))):
        add("A5", "criado_por e criado_em obrigatórios")
    if rec.get("relacao") in ("renovacao", "desdobramento") and not rec.get("promessa_mae_id"):
        add("A9", "renovacao ou desdobramento exige promessa_mae_id")


def validar_ocorrencia(rec, add):
    if not RE_ID["ocorrencia"].match(str(rec.get("id", ""))):
        add("A5", "id fora do formato O-LIV-0000")
    if not RE_ID["promessa"].match(str(rec.get("promessa_id", ""))):
        add("A5", "promessa_id inválido")
    for c in ("ref_inicio", "ref_fim"):
        if parse_ref(rec.get(c)) is None:
            add("A5", f"{c} inválida")
    if rec.get("tipo") not in TIPOS_OCORRENCIA:
        add("A5", f"tipo de ocorrência inválido: {rec.get('tipo')!r}")
    if "evidencia" in rec and not re.match(r"^[0-9a-f]{64}$", str(rec.get("evidencia_sha256", ""))):
        add("A5", "evidencia exige evidencia_sha256 (use injetar_citacao.py)")


def validar_nao_promessa(rec, add):
    if not RE_ID["nao_promessa"].match(str(rec.get("id", ""))):
        add("A5", "id fora do formato N-LIV-0000")
    if rec.get("tipo_unidade") == "promessa":
        add("A5", "nao_promessas/ não aceita tipo_unidade promessa")
    validar_unidade_comum(rec, add)
    if not str(rec.get("motivo_exclusao", "")).strip():
        add("A5", "motivo_exclusao obrigatório")
    if not isinstance(rec.get("unidades_origem"), list) or not rec["unidades_origem"]:
        add("A5", "unidades_origem deve listar ao menos um uid de passe")
    if rec.get("status") not in STATUS_PROMESSA:
        add("A5", "status inválido")


def validar_desenvolvimento(rec, add):
    if not RE_ID["desenvolvimento"].match(str(rec.get("id", ""))):
        add("A5", "id fora do formato V-LIV-0000")
    for c in ("ref_inicio", "ref_fim"):
        if parse_ref(rec.get(c)) is None:
            add("A5", f"{c} inválida")
    if rec.get("tipo") not in TIPOS_DESENVOLVIMENTO:
        add("A5", f"tipo de desenvolvimento inválido: {rec.get('tipo')!r}")
    if rec.get("tipo") == "cumprimento_narrado" and rec.get("base") not in BASES_CUMPRIMENTO:
        add("A5", "cumprimento_narrado exige base (declarado_pelo_texto ou correspondencia_narrativa)")
    if rec.get("base") == "declarado_pelo_texto" and not rec.get("formula_textual"):
        add("A9", "declarado_pelo_texto exige formula_textual (trecho literal do corpus que declara o cumprimento)")
    if not str(rec.get("nota", "")).strip():
        add("A5", "nota obrigatória")
    if rec.get("promessa_id") is not None and not RE_ID["promessa"].match(str(rec.get("promessa_id"))):
        add("A5", "promessa_id inválido")


def validar_familia(rec, add):
    if not RE_ID["familia"].match(str(rec.get("id", ""))):
        add("A5", "id fora do formato F-...")
    for c in ("nome", "descricao", "criterio_de_pertenca"):
        if not str(rec.get(c, "")).strip():
            add("A5", f"{c} obrigatório")


def validar_decisao(rec, add):
    if not RE_ID["decisao"].match(str(rec.get("id", ""))):
        add("A5", "id fora do formato D-n")
    for c in ("assunto", "decisao", "justificativa", "escopo"):
        if not str(rec.get(c, "")).strip():
            add("A5", f"{c} obrigatório")
    if rec.get("decidido_por") not in DECIDIDO_POR:
        add("A5", f"decidido_por inválido: {rec.get('decidido_por')!r}")
    if not RE_DATA.match(str(rec.get("data", ""))):
        add("A5", "data inválida")
    if not isinstance(rec.get("evidencias", []), list):
        add("A5", "evidencias deve ser lista")
    if rec.get("tipo", "criterio") not in TIPOS_DECISAO:
        add("A5", f"tipo de decisão inválido: {rec.get('tipo')!r}")
    if rec.get("tipo") in ("nao_equivalencia", "excecao_equivalencia"):
        ids = rec.get("ids")
        minimo = 2 if rec["tipo"] == "nao_equivalencia" else 1
        if not isinstance(ids, list) or len(ids) < minimo:
            add("A9", f"decisão {rec['tipo']} exige ids com ao menos {minimo} promessa(s)")


def validar_revisao(rec, add):
    if not RE_ID["revisao"].match(str(rec.get("id", ""))):
        add("A5", "id fora do formato R-n")
    if parse_intervalo(rec.get("ref")) is None:
        add("A5", "ref inválida")
    if rec.get("motivo") not in MOTIVOS_REVISAO:
        add("A5", f"motivo inválido: {rec.get('motivo')!r}")
    if not isinstance(rec.get("opcoes"), list) or len(rec["opcoes"]) < 2:
        add("A5", "opcoes deve ter ao menos duas alternativas")
    if not str(rec.get("recomendacao_da_ia", "")).strip():
        add("A5", "recomendacao_da_ia obrigatória")


def _carregar(base: Path, problemas):
    d = {"varredura": [], "promessas": [], "ocorrencias": [], "nao_promessas": [],
         "familias": [], "decisoes": [], "revisao": [], "desenvolvimento": []}
    for sub, chave in (("varredura", "varredura"), ("promessas", "promessas"),
                       ("ocorrencias", "ocorrencias"), ("nao_promessas", "nao_promessas"), ("desenvolvimento", "desenvolvimento")):
        for f in sorted((base / sub).glob("*.jsonl")) if (base / sub).exists() else []:
            for i, r in ler_jsonl(f, problemas):
                d[chave].append((f.name, i, r))
    for nome, chave in (("familias.jsonl", "familias"), ("decisoes.jsonl", "decisoes"),
                        ("revisao_humana.jsonl", "revisao")):
        for i, r in ler_jsonl(base / nome, problemas):
            d[chave].append((nome, i, r))
    return d


def verificar(base: Path, corpus=None, exigir_passes=False):
    base = Path(base)
    problemas = []
    d = _carregar(base, problemas)
    ids_vistos = {}
    promessas_ids = {r.get("id") for _, _, r in d["promessas"]}

    def unico(chave, arq, i, rid):
        k = (chave, rid)
        if k in ids_vistos:
            problemas.append(Problema("A8", arq, i, rid, f"id duplicado (também em {ids_vistos[k]})"))
        else:
            ids_vistos[k] = f"{arq}:{i}"

    for arq, i, r in d["varredura"]:
        validar_registro_varredura(r, _adder(problemas, arq, i, r.get("ref", "?")), arq)
    for arq, i, r in d["promessas"]:
        validar_promessa(r, _adder(problemas, arq, i, r.get("id", "?")))
        unico("P", arq, i, r.get("id"))
    for arq, i, r in d["ocorrencias"]:
        validar_ocorrencia(r, _adder(problemas, arq, i, r.get("id", "?")))
        unico("O", arq, i, r.get("id"))
    for arq, i, r in d["nao_promessas"]:
        validar_nao_promessa(r, _adder(problemas, arq, i, r.get("id", "?")))
        unico("N", arq, i, r.get("id"))
    for arq, i, r in d["desenvolvimento"]:
        validar_desenvolvimento(r, _adder(problemas, arq, i, r.get("id", "?")))
        unico("V", arq, i, r.get("id"))
        if r.get("promessa_id") and r["promessa_id"] not in promessas_ids:
            problemas.append(Problema("A8", arq, i, r.get("id", "?"), "desenvolvimento aponta promessa inexistente"))
    for arq, i, r in d["familias"]:
        validar_familia(r, _adder(problemas, arq, i, r.get("id", "?")))
        unico("F", arq, i, r.get("id"))
    for arq, i, r in d["decisoes"]:
        validar_decisao(r, _adder(problemas, arq, i, r.get("id", "?")))
        unico("D", arq, i, r.get("id"))
    for arq, i, r in d["revisao"]:
        validar_revisao(r, _adder(problemas, arq, i, r.get("id", "?")))
        unico("R", arq, i, r.get("id"))

    # ---- A8 e A9: relações entre registros
    promessas = {r.get("id"): (arq, i, r) for arq, i, r in d["promessas"]}
    familias = {r.get("id") for _, _, r in d["familias"]}
    ocorr_por_promessa = {}
    for arq, i, r in d["ocorrencias"]:
        pid = r.get("promessa_id")
        ocorr_por_promessa.setdefault(pid, []).append(r)
        if pid not in promessas:
            problemas.append(Problema("A8", arq, i, r.get("id", "?"), f"ocorrência órfã: promessa {pid} inexistente"))
    uids_por_passe = {}
    for _, _, r in d["varredura"]:
        for u in r.get("unidades", []) or []:
            uids_por_passe[u.get("uid")] = r.get("passe")
    livros_com_passe = {r.get("ref", "")[:3] for _, _, r in d["varredura"]}
    revisao_refs = [parse_intervalo(r.get("ref")) for _, _, r in d["revisao"]]
    for pid, (arq, i, r) in promessas.items():
        add = _adder(problemas, arq, i, pid)
        if r.get("status") == "rejeitada":
            continue
        if r.get("familia_id") not in familias:
            add("A8", f"familia_id {r.get('familia_id')} inexistente em familias.jsonl")
        if not any(o.get("tipo") == "enunciacao_inicial" for o in ocorr_por_promessa.get(pid, [])):
            add("A8", "promessa sem ocorrência enunciacao_inicial")
        mae = r.get("promessa_mae_id")
        if mae:
            if mae not in promessas:
                add("A8", f"promessa_mae_id {mae} inexistente")
            else:
                vistos, atual = {pid}, mae
                while atual:
                    if atual in vistos:
                        add("A8", "ciclo em promessa_mae_id")
                        break
                    vistos.add(atual)
                    atual = promessas.get(atual, (0, 0, {}))[2].get("promessa_mae_id")
        livro = str(r.get("ref_inicio", ""))[:3]
        if exigir_passes or livro in livros_com_passe:
            for uid in r.get("unidades_origem", []) or []:
                if uid not in uids_por_passe and not str(uid).startswith("ADJ-"):
                    add("A8", f"unidade de origem {uid} inexistente na varredura")
        if r.get("confianca") == "baixa":
            ini = r.get("ref_inicio")
            coberto = False
            for it in revisao_refs:
                if it and corpus is not None and ini and it[0][:3] == ini[:3]:
                    refs = corpus.intervalo(*it) or []
                    if ini in refs:
                        coberto = True
                elif it and it[0] == ini:
                    coberto = True
            if not coberto:
                add("A9", "confiança baixa sem item correspondente em revisao_humana.jsonl")
    for arq, i, r in d["nao_promessas"]:
        livro = str(r.get("ref_inicio", ""))[:3]
        if exigir_passes or livro in livros_com_passe:
            for uid in r.get("unidades_origem", []) or []:
                if uid not in uids_por_passe and not str(uid).startswith("ADJ-"):
                    problemas.append(Problema("A8", arq, i, r.get("id", "?"), f"unidade de origem {uid} inexistente"))
    return problemas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=str(RAIZ / "dados"))
    ap.add_argument("--exigir-passes", action="store_true")
    a = ap.parse_args()
    corpus = Corpus()
    probs = verificar(Path(a.base), corpus, a.exigir_passes)
    for p in probs:
        print(p)
    print(f"validar_esquema: {len(probs)} problema(s)")
    return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main())
