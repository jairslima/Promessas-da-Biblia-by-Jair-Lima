"""FIXTURE DE TESTE. NÃO É RESULTADO DE PESQUISA.

Gera, em diretório temporário, um conjunto de dados sintético mas bem-formado sobre versículos reais
(livros curtos e NÃO Gênesis) para provar que os controles aceitam dados corretos e acusam dados
defeituosos. As classificações abaixo existem só para exercitar o esquema e NÃO representam
nenhuma conclusão exegética. Nada disto é gravado em dados/.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from lib_promessas import *  # noqa: F401,F403
import injetar_citacao

DATA = "2026-11-18"


def uid(passe, ref, n):
    liv, cap, v = parse_ref(ref)
    return f"U{passe}-{liv}-{cap:03d}:{v:03d}-{n}"


def unidade(corpus, passe, ref, n, ancora, fim=None, tipo="promessa", **extra):
    fim = fim or ref
    assert ws(ancora) in ws(corpus.texto_intervalo(ref, fim)), f"fixture: âncora não literal em {ref}: {ancora}"
    u = {"uid": uid(passe, ref, n), "tipo_unidade": tipo, "ref_inicio": ref, "ref_fim": fim,
         "ancora_texto": ancora, "origem_real": "divina_direta", "resumo_proprio": f"fixture {ref}",
         "evidencia_exegetica": [{"ref": ref, "observacao": "fixture de teste"}], "confianca": "alta"}
    if tipo == "promessa":
        u.update({"natureza": "bencao", "promitente": "deus_indistinto", "destinatario_tipo": "israel",
                  "condicao_tipo": "nenhuma", "reforco": "nenhum"})
    u.update(extra)
    return u


def registros_passe(corpus, liv, passe, leitor, unidades):
    saida = []
    for ref in corpus.refs_do_livro(liv):
        comeca = [u for u in unidades if u["ref_inicio"] == ref]
        parte = [u["uid"] for u in unidades
                 if u["ref_inicio"] != ref and ref in (corpus.intervalo(u["ref_inicio"], u["ref_fim"]) or [])]
        estado = "com_unidade" if comeca else ("parte_de_unidade" if parte else "sem_unidade")
        saida.append({"ref": ref, "passe": passe, "leitor": leitor, "estado": estado,
                      "unidades": sorted(comeca, key=lambda u: u["uid"]), "parte_de": parte, "data": DATA})
    return saida


def promessa(corpus, pid, ref, ancora, uids, fim=None, **extra):
    fim = fim or ref
    assert ws(ancora) in ws(corpus.texto_intervalo(ref, fim)), f"fixture: âncora não literal em {ref}"
    r = {"id": pid, "familia_id": "F-TESTE", "relacao": "original", "tipo_unidade": "promessa",
         "origem_real": "divina_direta", "natureza": "bencao", "promitente": "deus_indistinto",
         "destinatario_tipo": "israel", "aplicabilidade": "direta", "condicao_tipo": "nenhuma",
         "reforco": "nenhum", "etapa_reveladora": "monarquica_e_profetica", "ref_inicio": ref, "ref_fim": fim,
         "ancora_texto": ancora, "resumo_proprio": f"fixture {pid}",
         "evidencia_exegetica": [{"ref": ref, "observacao": "fixture de teste"}],
         "acao_canonica": "fortalecer", "objeto_canonico": "forca", "beneficiario_canonico": "povo",
         "condicao_canonica": "nenhuma", "criterio_distincao": "primeira enunciação (fixture)",
         "cumprimento_status": "nao_declarado", "cumprimento_justificativa": "fixture",
         "confianca": "alta", "status": "reconciliada", "unidades_origem": uids,
         "criado_por": "fixture_teste", "criado_em": DATA}
    r.update(extra)
    return r


def ocorrencia(oid, pid, ref, fim=None, tipo="enunciacao_inicial"):
    return {"id": oid, "promessa_id": pid, "ref_inicio": ref, "ref_fim": fim or ref, "tipo": tipo}


def nao_promessa(corpus, nid, ref, ancora, tipo, uids, **extra):
    assert ws(ancora) in ws(corpus.texto[ref])
    r = {"id": nid, "tipo_unidade": tipo, "ref_inicio": ref, "ref_fim": ref, "ancora_texto": ancora,
         "origem_real": "indeterminada", "resumo_proprio": f"fixture {nid}",
         "evidencia_exegetica": [{"ref": ref, "observacao": "fixture de teste"}],
         "confianca": "alta", "motivo_exclusao": "fixture: não é promessa", "unidades_origem": uids,
         "status": "reconciliada", "criado_por": "fixture_teste", "criado_em": DATA}
    r.update(extra)
    return r


def passe_oba(corpus, passe, leitor, omitir_c=False, extra_16=False):
    us = [
        unidade(corpus, passe, "OBA 1:15", 1, "Como você fez, assim se fará a você", natureza="juizo",
                destinatario_tipo="nacoes_especificas"),
        unidade(corpus, passe, "OBA 1:17", 1, "haverá livramento"),
        unidade(corpus, passe, "OBA 1:17", 3, "A casa de Jacó será fogo", fim="OBA 1:18",
                tipo="profecia_sem_compromisso"),
        unidade(corpus, passe, "OBA 1:21", 1, "o reino será do SENHOR", tipo="profecia_sem_compromisso"),
    ]
    if not omitir_c:
        us.append(unidade(corpus, passe, "OBA 1:17", 2, "A casa de Jacó possuirá suas propriedades",
                          destinatario_tipo="familia_ou_linhagem"))
    if extra_16:
        us.append(unidade(corpus, passe, "OBA 1:16", 1, "todas as nações beberão continuamente", tipo="advertencia"))
    return registros_passe(corpus, "OBA", passe, leitor, us)


def construir_limpo(base: Path, corpus: Corpus):
    base = Path(base)
    escrever_jsonl(base / "varredura" / "OBA.passe1.jsonl", passe_oba(corpus, 1, "leitor_A"))
    escrever_jsonl(base / "varredura" / "OBA.passe2.jsonl", passe_oba(corpus, 2, "leitor_B"))
    p = [
        promessa(corpus, "P-OBA-0001", "OBA 1:17", "haverá livramento", ["U1-OBA-001:017-1"],
                 acao_canonica="livrar", objeto_canonico="livramento", beneficiario_canonico="monte_siao"),
        promessa(corpus, "P-OBA-0002", "OBA 1:17", "A casa de Jacó possuirá suas propriedades", ["U1-OBA-001:017-2"],
                 acao_canonica="restituir", objeto_canonico="propriedades", beneficiario_canonico="casa_de_jaco",
                 destinatario_tipo="familia_ou_linhagem"),
        promessa(corpus, "P-OBA-0003", "OBA 1:15", "Como você fez, assim se fará a você", ["U1-OBA-001:015-1"],
                 natureza="juizo", destinatario_tipo="nacoes_especificas", acao_canonica="retribuir",
                 objeto_canonico="retribuicao", beneficiario_canonico="edom"),
    ]
    escrever_jsonl(base / "promessas" / "OBA.jsonl", p)
    escrever_jsonl(base / "promessas" / "ISA.jsonl", [
        promessa(corpus, "P-ISA-0001", "ISA 41:10", "Eu o fortaleço", ["U1-ISA-041:010-1"],
                 acao_canonica="fortalecer", objeto_canonico="forca", beneficiario_canonico="povo_de_deus"),
        promessa(corpus, "P-ISA-0002", "ISA 41:10", "ajudo e sustento", ["U1-ISA-041:010-2"],
                 acao_canonica="socorrer", objeto_canonico="amparo", beneficiario_canonico="povo_de_deus",
                 resumo_proprio="fixture socorro e sustento"),
    ])
    escrever_jsonl(base / "promessas" / "MAT.jsonl", [
        promessa(corpus, "P-MAT-0001", "MAT 28:20", "Eis que estou convosco todos os dias", ["U1-MAT-028:020-1"],
                 promitente="filho", destinatario_tipo="grupo_especifico",
                 contexto_destinatario="fixture: discípulos que ouviram a ordem final",
                 etapa_reveladora="cristo_e_apostolos", acao_canonica="estar_com", objeto_canonico="presenca",
                 beneficiario_canonico="discipulos"),
    ])
    escrever_jsonl(base / "promessas" / "JDG.jsonl", [
        promessa(corpus, "P-JDG-0001", "JDG 11:31", "será do SENHOR", ["U1-JDG-011:031-1"],
                 origem_real="humana_em_nome_proprio", natureza="bencao", promitente=None,
                 promitente_nome="Jefté", destinatario_tipo="pessoa", acao_canonica="oferecer",
                 objeto_canonico="holocausto", beneficiario_canonico="senhor", etapa_reveladora="monarquica_e_profetica"),
        promessa(corpus, "P-JDG-0002", "JDG 11:31", "eu o oferecerei em holocausto", ["U1-JDG-011:031-2"],
                 origem_real="humana_em_nome_proprio", natureza="juizo", promitente=None,
                 promitente_nome="Jefté", destinatario_tipo="pessoa", acao_canonica="sacrificar",
                 objeto_canonico="vida_de_quem_sair", beneficiario_canonico="quem_sair_da_casa",
                 etapa_reveladora="monarquica_e_profetica"),
    ])
    for r in [x for f in ("OBA", "ISA", "MAT", "JDG") for _, x in ler_jsonl(base / "promessas" / f"{f}.jsonl", [])]:
        pass
    ocs = {}
    n = 0
    for f in ("OBA", "ISA", "MAT", "JDG"):
        regs = [x for _, x in ler_jsonl(base / "promessas" / f"{f}.jsonl", [])]
        lista = []
        for r in regs:
            n += 1
            lista.append(ocorrencia(f"O-{f}-{len(lista) + 1:04d}", r["id"], r["ref_inicio"], r["ref_fim"]))
        escrever_jsonl(base / "ocorrencias" / f"{f}.jsonl", lista)
    escrever_jsonl(base / "nao_promessas" / "PRO.jsonl", [
        nao_promessa(corpus, "N-PRO-0001", "PRO 10:4", "a mão dos diligentes enriquece", "principio_sapiencial",
                     ["U1-PRO-010:004-1"]),
    ])
    escrever_jsonl(base / "nao_promessas" / "RUT.jsonl", [
        nao_promessa(corpus, "N-RUT-0001", "RUT 2:12", "Que o SENHOR recompense o que você fez", "desejo_ou_bencao_votiva",
                     ["U1-RUT-002:012-1"], origem_real="humana_votiva"),
    ])
    escrever_jsonl(base / "nao_promessas" / "JDG.jsonl", [
        nao_promessa(corpus, "N-JDG-0001", "JDG 11:30", "Jefté fez um voto ao SENHOR", "declaracao_sem_compromisso",
                     ["U1-JDG-011:030-1"]),
    ])
    escrever_jsonl(base / "familias.jsonl", [
        {"id": "F-TESTE", "nome": "Família de teste", "descricao": "fixture", "criterio_de_pertenca": "fixture"}])
    escrever_jsonl(base / "decisoes.jsonl", [
        {"id": "D-01", "assunto": "fixture", "decisao": "fixture", "justificativa": "fixture",
         "evidencias": ["OBA 1:17"], "decidido_por": "regra_do_protocolo", "data": DATA, "escopo": "teste"}])
    escrever_jsonl(base / "revisao_humana.jsonl", [])
    injetar_citacao.processar(base, corpus, refazer=True)
    return base
