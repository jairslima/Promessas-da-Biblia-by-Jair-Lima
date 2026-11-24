"""Auditoria de COERÊNCIA SEMÂNTICA entre beneficiário, destinatário, promitente, objeto e categoria (protocolo v0.4).

Não corrige nada. Aponta registros em que os campos se contradizem, com gravidade:
  S1 destinatário_tipo incompatível com o beneficiário canônico (ex.: animais como "crente individual")
  S2 natureza incompatível com a ação (benefício com verbo de destruição, juízo com verbo de bênção)
  S3 origem incompatível com o promitente (divina sem promitente; humana com promitente divino; Cristo no AT)
  S4 relação incompatível com a família (renovação com o mesmo beneficiário; desdobramento com beneficiário diferente)
  S5 nome em destinatario_nome que contradiz o beneficiário canônico
  S6 beneficiário canônico que não aparece no resumo nem na âncora (possível troca de destinatário)
  S7 campo pendente ou ausente em registro já aprovado
Uso: python -I validar_semantica.py [--base dados_v03] [--saida auditoria/validacao_semantica_<base>.json]
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_promessas import *  # noqa: F401,F403

PESSOAS = {"abraao", "abrao", "isaque", "jaco", "israel", "noe", "sara", "agar", "ismael", "lo", "caim", "adao", "eva", "jose", "esau", "rebeca",
           "abimeleque", "labao", "lia", "raquel", "tamar", "judah", "juda", "efrom", "efraim", "manasses", "benjamim", "hamor", "siquem", "faraó", "farao", "mulher"}
COLETIVO = ("nacoes", "familias_da_terra", "humanidade", "toda_carne", "povo_do_egito", "egipcios", "filhos_de_israel", "sodoma")
CRIACAO = ("animais", "aves", "criacao", "terra_e_humanidade", "ciclos", "seres")
LINHAGEM = ("descendencia", "familia", "filhos", "e_descendencia", "irmaos", "casa_de")
BENEFICIO = {"abencoar", "dar", "multiplicar", "fazer", "estabelecer", "guardar", "estar_com", "poupar", "conceder", "libertar", "prover", "sustentar",
             "preservar", "vingar", "manter", "confirmar", "mostrar", "fazer_voltar", "fazer_subir", "engrandecer", "tornar", "gerar", "ser", "trazer", "voltar",
             "nao_destruir", "nao_amaldicoar", "fazer_bem", "estar_presente", "expandir", "cumprir", "oferecer", "pagar", "ceder", "servir", "jurar", "liberar"}
PREJUIZO = {"destruir", "amaldicoar", "julgar", "por", "requerer", "multiplicar_dor", "limitar", "apagar", "matar", "ferir", "escravizar", "entregar",
            "fazer_mal", "sujeitar_a_morte", "assumir_culpa", "reter", "partir", "dividir", "enviar_chuva"}
NT = {"MAT", "MRK", "LUK", "JHN", "ACT", "ROM", "1CO", "2CO", "GAL", "EPH", "PHP", "COL", "1TH", "2TH", "1TI", "2TI", "TIT", "PHM", "HEB", "JAS", "1PE", "2PE", "1JN", "2JN", "3JN", "JUD", "REV"}


ALIAS = {"abrao": "abraao", "israel": "jaco"}


def norm(s):
    s = "".join(c for c in unicodedata.normalize("NFD", str(s).lower()) if unicodedata.category(c) != "Mn")
    return re.sub(r"\b(" + "|".join(ALIAS) + r")\b", lambda m: ALIAS[m.group(1)], s)


def esperado_destinatario(benef):
    b = norm(benef)
    if "viventes" in b or b.startswith(("rei_de", "quem_", "servo_de", "demais_", "um_ao_outro")):
        return None
    if any(k in b for k in CRIACAO):
        return {"criacao", "humanidade"}
    if any(k in b for k in LINHAGEM) and ("descendencia" in b or "familia" in b or "filhos" in b or "casa_de" in b):
        return {"familia_ou_linhagem", "grupo_especifico", "pessoa", "israel"}
    if any(k in b for k in COLETIVO):
        return {"humanidade", "nacoes_especificas", "grupo_especifico", "israel", "criacao", "familia_ou_linhagem"}
    toks = set(b.split("_"))
    if toks & PESSOAS:
        return {"pessoa", "familia_ou_linhagem", "grupo_especifico", "crente_individual", "israel"}
    return None  # sem regra: não opina


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="dados_v03")
    ap.add_argument("--livro", default="GEN")
    a = ap.parse_args()
    base = RAIZ / a.base
    P = [r for _, r in ler_jsonl(base / "promessas" / f"{a.livro}.jsonl", [])]
    por_id = {p["id"]: p for p in P}
    ach = []

    def add(p, cod, grav, msg):
        ach.append({"id": p["id"], "ref": p["ref_inicio"], "cod": cod, "gravidade": grav, "msg": msg})

    for p in P:
        if p.get("status") == "rejeitada":
            continue
        # S1
        esp = esperado_destinatario(p.get("beneficiario_canonico", ""))
        dt = p.get("destinatario_tipo")
        if esp and dt and dt not in esp and dt != "indeterminado" and p.get("natureza") != "juizo":
            add(p, "S1", "alta", f"destinatário '{dt}' incompatível com beneficiário '{p['beneficiario_canonico']}' (esperado: {sorted(esp)})")
        if dt == "crente_individual" and parse_ref(p["ref_inicio"])[0] not in NT:
            add(p, "S1", "alta", "crente_individual no Antigo Testamento (provável confusão de 'cri' com criação)")
        # S2
        acao, nat = p.get("acao_canonica", ""), p.get("natureza")
        if nat == "bencao" and acao in PREJUIZO and acao not in BENEFICIO:
            add(p, "S2", "media", f"natureza bencao com ação de prejuízo '{acao}'")
        if nat == "juizo" and "dor" not in str(p.get("objeto_canonico")) and acao in BENEFICIO and not acao.startswith("nao_") and acao not in PREJUIZO:
            add(p, "S2", "media", f"natureza juizo com ação de benefício '{acao}'")
        # S3
        o = p.get("origem_real")
        pend = p.get("campos_pendentes") or []
        if o in ORIGENS_DIVINAS and not p.get("promitente") and "promitente" not in pend:
            add(p, "S3", "alta", "origem divina sem promitente")
        if o == "humana_em_nome_proprio" and p.get("promitente"):
            add(p, "S3", "alta", f"origem humana com promitente divino '{p['promitente']}'")
        if p.get("promitente") == "filho" and parse_ref(p["ref_inicio"])[0] not in NT and not (p.get("contexto_destinatario")):
            add(p, "S3", "alta", "promitente 'filho' fora do NT sem contexto")
        if o in ("humana_em_nome_proprio", "profetica_patriarcal", "divina_relatada_por_humano") and not p.get("promitente_nome") and "promitente_nome" not in pend:
            add(p, "S3", "alta", "origem humana ou relatada sem promitente_nome")
        # S4
        mae = por_id.get(p.get("promessa_mae_id"))
        if p.get("relacao") == "renovacao" and mae and mae["beneficiario_canonico"] == p["beneficiario_canonico"]:
            add(p, "S4", "media", "renovação com o mesmo beneficiário da promessa-mãe")
        if p.get("relacao") == "desdobramento" and mae and mae["beneficiario_canonico"] != p["beneficiario_canonico"]:
            add(p, "S4", "media", "desdobramento com beneficiário diferente da promessa-mãe")
        # S5
        dn = norm(p.get("destinatario_nome", "") or "")
        bt = set(norm(p.get("beneficiario_canonico", "")).split("_"))
        nomes_dn = {x for x in re.split(r"\W+", dn) if x in PESSOAS}
        if nomes_dn and not (nomes_dn & bt) and not any(k in norm(p["beneficiario_canonico"]) for k in ("descendencia", "familia", "filhos", "nacoes", "humanidade", "toda_carne", "familias")):
            add(p, "S5", "media", f"destinatario_nome '{p.get('destinatario_nome')}' não aparece no beneficiário '{p['beneficiario_canonico']}'")
        # S6
        texto = norm(p.get("resumo_proprio", "") + " " + p.get("ancora_texto", ""))
        pess_b = [x for x in bt if x in PESSOAS and x not in ("mulher",)]
        if pess_b and not any(x in texto for x in pess_b) and not any(x in texto for x in ("ti", "te", "tu", "teu", "tua", "voce")) and p.get("origem_real") in ORIGENS_DIVINAS:
            add(p, "S6", "baixa", f"beneficiário '{p['beneficiario_canonico']}' não aparece no resumo nem na âncora")
        # S7
        if p.get("campos_pendentes") and p.get("status") in ("revisada_humano", "congelada"):
            add(p, "S7", "alta", f"campos pendentes em registro aprovado: {p['campos_pendentes']}")
    res = {"base": a.base, "total_promessas": len(P), "achados": ach,
           "por_codigo": {}, "por_gravidade": {}}
    for x in ach:
        res["por_codigo"][x["cod"]] = res["por_codigo"].get(x["cod"], 0) + 1
        res["por_gravidade"][x["gravidade"]] = res["por_gravidade"].get(x["gravidade"], 0) + 1
    saida = RAIZ / "auditoria" / f"validacao_semantica_{a.base}.json"
    saida.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(P), "promessas;", len(ach), "achados;", res["por_codigo"], res["por_gravidade"])
    for x in ach[:60]:
        print(x["id"], x["ref"], x["cod"], x["gravidade"], x["msg"][:130])


if __name__ == "__main__":
    main()
