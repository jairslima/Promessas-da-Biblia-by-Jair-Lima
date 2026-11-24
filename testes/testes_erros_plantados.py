"""Testes com erros plantados: provam que cada controle acusa a falha que deve acusar,
e que um conjunto de dados correto passa sem nenhum problema.

Tudo roda em diretórios temporários com FIXTURE sintética (testes/fixture.py).
Nada é gravado em dados/. Única exceção controlada: o teste A1 adultera uma cópia do manifesto e
restaura o original, conferindo o hash ao final.

Uso: python -I testes_erros_plantados.py       (saída 0 se todos os testes passarem)
Relatório: auditoria/testes_erros_plantados.md
"""
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
sys.path.insert(0, str(RAIZ / "testes"))
import auditar_refs
import cobertura
import congelar
import consolidar
import contar
import duplicatas
import fixture
import injetar_citacao
import montar_passe
import preparar_passes
import receber_passe
import reconciliar
import validar_esquema
from lib_promessas import *  # noqa: F401,F403

CORPUS = Corpus()
RESULTADOS = []


# ---------------------------------------------------------------- utilidades
def todos(base):
    p = []
    p += validar_esquema.verificar(base, CORPUS)
    p += auditar_refs.verificar(base, CORPUS)
    p += cobertura.verificar(base, CORPUS)
    p += duplicatas.verificar(base)
    p += [Problema("A3", "ocorrencias", 0, "-", x) for x in injetar_citacao.processar(base, CORPUS, gravar=False)]
    p += congelar.verificar(base)
    return p


def novo_limpo():
    t = Path(tempfile.mkdtemp(prefix="promessas_teste_"))
    fixture.construir_limpo(t, CORPUS)
    return t


def editar(base, rel, fn):
    f = Path(base) / rel
    regs = [r for _, r in ler_jsonl(f, [])]
    fn(regs)
    escrever_jsonl(f, regs)


def reg(regs, rid, chave="id"):
    return next(r for r in regs if r.get(chave) == rid)


def registrar(nome, esperado, codigos, extra=""):
    ok = esperado in codigos
    RESULTADOS.append((nome, esperado, ok, ",".join(sorted(codigos)) or "nenhum", extra))
    print(("PASS " if ok else "FAIL ") + f"{nome} (esperado {esperado}; acusou {sorted(codigos) or 'nada'}) {extra}")


def plantar(nome, esperado, mutador):
    base = novo_limpo()
    try:
        mutador(base)
        registrar(nome, esperado, {p.controle for p in todos(base)})
    finally:
        shutil.rmtree(base, ignore_errors=True)


def _seguro(s):
    enc = sys.stdout.encoding or "utf-8"
    return s.encode(enc, "replace").decode(enc)


def afirmar(nome, condicao, detalhe=""):
    RESULTADOS.append((nome, "-", bool(condicao), "-", detalhe))
    print(_seguro(("PASS " if condicao else "FAIL ") + f"{nome} {detalhe}"))


# ---------------------------------------------------------------- 0. linha de base
def teste_linha_de_base():
    base = novo_limpo()
    try:
        probs = todos(base)
        afirmar("L0 dados corretos passam em todos os controles", not probs, "; ".join(map(str, probs[:3])))
        c1, c2 = contar.contar(base, CORPUS), contar.contar(base, CORPUS)
        afirmar("A10 contagem reprodutível (duas execuções idênticas)", c1 == c2)
        pb = c1["nivel_B_promessas_distintas_por_categoria"]
        afirmar("CONT indicador principal conta só promessa divina de bênção",
                c1["indicador_principal_promessas_divinas_de_bencao"] == 5 and pb.get("divina_bencao") == 5, str(pb))
        afirmar("CONT juízo divino, humana de benefício e humana de prejuízo (D-08) ficam em totais separados",
                pb.get("divina_juizo") == 1 and pb.get("humana_beneficio") == 1 and pb.get("humana_prejuizo") == 1, str(pb))
        afirmar("CONT princípio sapiencial e voto ficam fora das promessas",
                c1["unidades_fora_da_contagem_de_promessas_por_tipo"] == {"declaracao_sem_compromisso": 1, "desejo_ou_bencao_votiva": 1, "principio_sapiencial": 1}
                and sum(pb.values()) == 8, str(c1["unidades_fora_da_contagem_de_promessas_por_tipo"]))
        afirmar("CONT promessa de Cristo contada com promitente filho",
                c1["promessas_divinas_por_promitente"].get("divina_bencao:filho") == 1)
        afirmar("CONT versículos com 2+ promessas distintas (classificação por unidade, não por versículo)",
                c1["versiculos_com_duas_ou_mais_promessas_distintas"] == 3, str(c1["versiculos_com_duas_ou_mais_promessas_distintas"]))
    finally:
        shutil.rmtree(base, ignore_errors=True)


# ---------------------------------------------------------------- 1. erros plantados
def mut(base, rel, rid, **campos):
    def f(regs):
        reg(regs, rid).update(campos)
    editar(base, rel, f)


def teste_erros():
    # A2 referências
    plantar("A2 ref inexistente (OBA 1:99)", "A2", lambda b: mut(b, "promessas/OBA.jsonl", "P-OBA-0001", ref_fim="OBA 1:99"))
    plantar("A2 capítulo inexistente em evidência exegética (GEN 51:1)", "A2",
            lambda b: mut(b, "promessas/OBA.jsonl", "P-OBA-0001", evidencia_exegetica=[{"ref": "GEN 51:1", "observacao": "x"}]))
    plantar("A2 ref malformada", "A2", lambda b: mut(b, "promessas/OBA.jsonl", "P-OBA-0002", refs_extensao=["Gênesis 12"], aplicabilidade="estendida_pelo_texto"))
    plantar("A2 intervalo invertido", "A2", lambda b: mut(b, "promessas/OBA.jsonl", "P-OBA-0003", ref_inicio="OBA 1:17", ref_fim="OBA 1:15"))
    plantar("A2 ref inexistente em decisão", "A2", lambda b: editar(b, "decisoes.jsonl", lambda r: r[0].update(evidencias=["OBA 9:9"])))
    # A3 citação e âncora
    plantar("A3 âncora que não é trecho literal", "A3",
            lambda b: mut(b, "promessas/OBA.jsonl", "P-OBA-0001", ancora_texto="haverá livramento total e eterno"))
    plantar("A3 evidência adulterada", "A3",
            lambda b: editar(b, "ocorrencias/OBA.jsonl", lambda r: r[0].update(evidencia=r[0]["evidencia"].replace("livramento", "salvação"))))
    plantar("A3 hash da evidência errado", "A3",
            lambda b: editar(b, "ocorrencias/OBA.jsonl", lambda r: r[0].update(evidencia_sha256="0" * 64)))
    plantar("A3 âncora falsa dentro da varredura", "A3",
            lambda b: editar(b, "varredura/OBA.passe1.jsonl",
                             lambda r: next(x for x in r if x["unidades"])["unidades"][0].update(ancora_texto="texto inventado")))
    # A4 cobertura
    plantar("A4 versículo sem estado no passe", "A4",
            lambda b: editar(b, "varredura/OBA.passe1.jsonl", lambda r: r.pop(5)))
    plantar("A4 versículo repetido", "A4",
            lambda b: editar(b, "varredura/OBA.passe2.jsonl", lambda r: r.append(dict(r[3]))))
    plantar("A4 versículo inexistente no passe", "A4",
            lambda b: editar(b, "varredura/OBA.passe1.jsonl", lambda r: r.append({**r[0], "ref": "OBA 1:22"})))
    plantar("A4 versículo coberto por unidade marcado sem_unidade", "A4",
            lambda b: editar(b, "varredura/OBA.passe1.jsonl",
                             lambda r: reg(r, "OBA 1:18", "ref").update(estado="sem_unidade", parte_de=[])))
    plantar("A4 parte_de aponta unidade inexistente", "A4",
            lambda b: editar(b, "varredura/OBA.passe1.jsonl",
                             lambda r: reg(r, "OBA 1:02", "ref") if False else reg(r, "OBA 1:2", "ref").update(estado="parte_de_unidade", parte_de=["U1-OBA-009:009-1"])))
    # A13 independência
    plantar("A13 mesmo leitor nos dois passes", "A13",
            lambda b: editar(b, "varredura/OBA.passe2.jsonl", lambda r: [x.update(leitor="leitor_A") for x in r]))
    plantar("A13 dois leitores no mesmo passe", "A13",
            lambda b: editar(b, "varredura/OBA.passe2.jsonl", lambda r: r[0].update(leitor="outro")))
    # A5 esquema
    plantar("A5 campo obrigatório vazio (resumo_proprio)", "A5", lambda b: mut(b, "promessas/ISA.jsonl", "P-ISA-0001", resumo_proprio=""))
    plantar("A5 enum inválido (destinatario_tipo)", "A5", lambda b: mut(b, "promessas/ISA.jsonl", "P-ISA-0001", destinatario_tipo="todo_mundo"))
    plantar("A5 evidência exegética ausente", "A5", lambda b: mut(b, "promessas/ISA.jsonl", "P-ISA-0001", evidencia_exegetica=[]))
    plantar("A5 slug canônico fora do vocabulário", "A5", lambda b: mut(b, "promessas/ISA.jsonl", "P-ISA-0001", objeto_canonico="Força Divina"))
    plantar("A5 JSON corrompido", "A5",
            lambda b: (b / "promessas" / "ISA.jsonl").write_text("{isto não é json\n", encoding="utf-8"))
    plantar("A5 id duplicado ou formato inválido", "A5", lambda b: mut(b, "promessas/ISA.jsonl", "P-ISA-0002", id="P-ISA-02"))
    # A6/A7 duplicação
    def dup_sinonimo(b):
        def f(regs):
            x = dict(reg(regs, "P-ISA-0001"))
            x.update(id="P-ISA-0003", beneficiario_canonico="povo_de_deus", objeto_canonico="forca_certamente",
                     acao_canonica="fortalecer", resumo_proprio="outra redação")
            regs.append(x)
        editar(b, "promessas/ISA.jsonl", f)
        editar(b, "ocorrencias/ISA.jsonl", lambda r: r.append(fixture.ocorrencia("O-ISA-0003", "P-ISA-0003", "ISA 41:10")))
        injetar_citacao.processar(b, CORPUS)
    plantar("A6 duplicata por intensificador ('certamente') no objeto", "A6", dup_sinonimo)
    def dup_sinonimo2(b):
        def f(regs):
            x = dict(reg(regs, "P-ISA-0002"))
            x.update(id="P-ISA-0003", acao_canonica="auxiliar", objeto_canonico="amparo", resumo_proprio="mesmo sentido")
            regs.append(x)
        editar(b, "promessas/ISA.jsonl", f)
        editar(b, "ocorrencias/ISA.jsonl", lambda r: r.append(fixture.ocorrencia("O-ISA-0003", "P-ISA-0003", "ISA 41:10")))
        injetar_citacao.processar(b, CORPUS)
    plantar("A6 duplicata por sinônimo de ação (ajudar/auxiliar)", "A6", dup_sinonimo2)
    def dup_lexical(b):
        def f(regs):
            x = dict(reg(regs, "P-ISA-0002"))
            x.update(id="P-ISA-0003", acao_canonica="proteger_amplamente", objeto_canonico="resguardo",
                     resumo_proprio="fixture socorro e sustento")
            regs.append(x)
        editar(b, "promessas/ISA.jsonl", f)
        editar(b, "ocorrencias/ISA.jsonl", lambda r: r.append(fixture.ocorrencia("O-ISA-0003", "P-ISA-0003", "ISA 41:10", tipo="reafirmacao")))
        injetar_citacao.processar(b, CORPUS)
    plantar("A7 par suspeito por vocabulário sem slug igual", "A7", dup_lexical)
    plantar("A6 ocorrência repetida", "A6",
            lambda b: editar(b, "ocorrencias/ISA.jsonl", lambda r: r.append({**r[0], "id": "O-ISA-0009"})))
    # A8 estrutura
    plantar("A8 ocorrência órfã", "A8",
            lambda b: editar(b, "ocorrencias/ISA.jsonl", lambda r: r.append(fixture.ocorrencia("O-ISA-0007", "P-ISA-0099", "ISA 41:10", tipo="reafirmacao"))))
    plantar("A8 promessa sem enunciacao_inicial", "A8",
            lambda b: editar(b, "ocorrencias/ISA.jsonl", lambda r: r.pop(0)))
    plantar("A8 ciclo em promessa_mae_id", "A8",
            lambda b: (mut(b, "promessas/ISA.jsonl", "P-ISA-0001", relacao="desdobramento", promessa_mae_id="P-ISA-0002"),
                       mut(b, "promessas/ISA.jsonl", "P-ISA-0002", relacao="desdobramento", promessa_mae_id="P-ISA-0001")))
    plantar("A8 família inexistente", "A8", lambda b: mut(b, "promessas/ISA.jsonl", "P-ISA-0001", familia_id="F-NAOEXISTE"))
    plantar("A8 unidade de origem inexistente na varredura", "A8",
            lambda b: mut(b, "promessas/OBA.jsonl", "P-OBA-0001", unidades_origem=["U1-OBA-001:020-1"]))
    plantar("A8 id de promessa duplicado", "A8",
            lambda b: editar(b, "promessas/ISA.jsonl", lambda r: r.append(dict(r[0]))))
    # A9 consistência
    plantar("A9 estendida_pelo_texto sem refs_extensao", "A9",
            lambda b: mut(b, "promessas/ISA.jsonl", "P-ISA-0001", aplicabilidade="estendida_pelo_texto"))
    plantar("A9 confiança baixa sem item de revisão humana", "A9",
            lambda b: mut(b, "promessas/ISA.jsonl", "P-ISA-0001", confianca="baixa"))
    plantar("A9 cumprimento declarado sem refs_cumprimento", "A9",
            lambda b: mut(b, "promessas/ISA.jsonl", "P-ISA-0001", cumprimento_status="declarado_no_texto"))
    plantar("A9 condição explícita sem condicao_ref", "A9",
            lambda b: mut(b, "promessas/ISA.jsonl", "P-ISA-0001", condicao_tipo="explicita"))
    plantar("A9 estado com_unidade sem unidades", "A9",
            lambda b: editar(b, "varredura/OBA.passe1.jsonl", lambda r: reg(r, "OBA 1:3", "ref").update(estado="com_unidade")))
    plantar("A9 renovação sem promessa_mae_id", "A9", lambda b: mut(b, "promessas/ISA.jsonl", "P-ISA-0002", relacao="renovacao"))
    plantar("A9 decisão nao_equivalencia sem os dois ids", "A9",
            lambda b: editar(b, "decisoes.jsonl", lambda r: r.append({**r[0], "id": "D-02", "tipo": "nao_equivalencia", "ids": ["P-ISA-0001"]})))
    # A12 coerência de categoria (decisões 1, 6, 7, 8)
    plantar("A12 promessa de Cristo sem contexto_destinatario", "A12",
            lambda b: mut(b, "promessas/MAT.jsonl", "P-MAT-0001", contexto_destinatario=""))
    plantar("A12 bênção votiva registrada como promessa", "A12",
            lambda b: mut(b, "promessas/ISA.jsonl", "P-ISA-0001", origem_real="humana_votiva"))
    plantar("A12 princípio sapiencial com origem divina identificável", "A12",
            lambda b: mut(b, "nao_promessas/PRO.jsonl", "N-PRO-0001", origem_real="divina_direta"))
    plantar("A5 promessa humana com natureza nao_se_aplica (D-08 exige benefício ou prejuízo)", "A5",
            lambda b: mut(b, "promessas/JDG.jsonl", "P-JDG-0001", natureza="nao_se_aplica"))
    plantar("A5 promessa divina sem natureza", "A5", lambda b: mut(b, "promessas/ISA.jsonl", "P-ISA-0001", natureza="nao_se_aplica"))
    plantar("A12 promessa humana de prejuízo com tipo desejo votivo (voto não é ameaça)", "A12",
            lambda b: mut(b, "promessas/JDG.jsonl", "P-JDG-0002", origem_real="humana_votiva"))
    plantar("A12 promessa com origem indeterminada", "A12",
            lambda b: mut(b, "promessas/ISA.jsonl", "P-ISA-0001", origem_real="indeterminada"))
    plantar("A5 divina_relatada_por_humano sem atribuicao_divina_ref", "A5",
            lambda b: mut(b, "promessas/ISA.jsonl", "P-ISA-0001", origem_real="divina_relatada_por_humano", promitente_nome="Fulano"))
    plantar("A5 promessa humana sem promitente_nome", "A5",
            lambda b: mut(b, "promessas/JDG.jsonl", "P-JDG-0001", promitente_nome=""))


# ---------------------------------------------------------------- 2. A1, A11, congelamento, citação, passes
def teste_a1():
    man = RAIZ / "dados" / "manifesto_sha256.txt"
    original = man.read_bytes()
    h0 = sha256_arquivo(man)
    try:
        txt = original.decode("utf-8")
        man.write_bytes(("0" + txt[1:]).encode("utf-8"))
        r = subprocess.run([sys.executable, "-I", str(RAIZ / "scripts" / "auditar_corpus.py")], capture_output=True, text=True, encoding="utf-8")
        afirmar("A1 manifesto divergente da fonte é acusado", r.returncode == 1 and "A1" in r.stdout, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "")
    finally:
        man.write_bytes(original)
    r = subprocess.run([sys.executable, "-I", str(RAIZ / "scripts" / "auditar_corpus.py")], capture_output=True, text=True, encoding="utf-8")
    afirmar("A1 restauração: manifesto original voltou e a fonte confere", sha256_arquivo(man) == h0 and r.returncode == 0)


def teste_congelamento():
    base = novo_limpo()
    try:
        editar(base, "revisao_humana.jsonl", lambda r: r.append({"id": "R-1", "ref": "OBA 1:17", "motivo": "atomicidade",
                "opcoes": ["uma promessa", "duas promessas"], "recomendacao_da_ia": "duas", "resposta_jair": None}))
        reg_, erros = congelar.congelar(base, "OBA", CORPUS)
        afirmar("A11 congelamento recusado com revisão humana pendente", reg_ is None and any("pendente" in e for e in erros), str(erros))
        editar(base, "revisao_humana.jsonl", lambda r: r[0].update(resposta_jair="duas", data_resposta="2026-11-18"))
        reg_, erros = congelar.congelar(base, "OBA", CORPUS)
        afirmar("A11 congelamento aceito sem pendências", reg_ is not None, str(erros))
        afirmar("A11 verificação logo após congelar não acusa nada", not congelar.verificar(base))
        editar(base, "promessas/OBA.jsonl", lambda r: r[0].update(resumo_proprio="alterado depois de congelar"))
        registrar("A11 arquivo congelado alterado", "A11", {p.controle for p in congelar.verificar(base)})
    finally:
        shutil.rmtree(base, ignore_errors=True)
    base = novo_limpo()
    try:
        mut(base, "promessas/OBA.jsonl", "P-OBA-0001", ref_fim="OBA 1:99")
        reg_, erros = congelar.congelar(base, "OBA", CORPUS)
        afirmar("A11 congelamento recusado quando há erro nos dados", reg_ is None and erros)
    finally:
        shutil.rmtree(base, ignore_errors=True)


def teste_citacao():
    base = novo_limpo()
    try:
        editar(base, "ocorrencias/OBA.jsonl", lambda r: [x.pop("evidencia") or x.pop("evidencia_sha256") for x in r])
        pend = injetar_citacao.processar(base, CORPUS, gravar=False)
        afirmar("CIT verificação acusa evidência ausente", len(pend) > 0)
        injetar_citacao.processar(base, CORPUS)
        afirmar("CIT injeção restaura evidência literal do corpus", not injetar_citacao.processar(base, CORPUS, gravar=False))
        afirmar("CIT citação injetada é idêntica ao corpus",
                reg([x for _, x in ler_jsonl(base / "ocorrencias" / "OBA.jsonl", [])], "O-OBA-0001")["evidencia"] == CORPUS.texto["OBA 1:17"])
    finally:
        shutil.rmtree(base, ignore_errors=True)


def teste_receber_passe():
    base = novo_limpo()
    saida = Path(tempfile.mkdtemp(prefix="promessas_rec_"))
    try:
        for p in (1, 2):
            (base / "varredura" / f"OBA.passe{p}.jsonl").unlink()
        bom = fixture.passe_oba(CORPUS, 1, "leitor_A")
        arq = saida / "bom.jsonl"
        escrever_jsonl(arq, bom)
        erros = receber_passe.receber("OBA", 1, "leitor_A", arq, base, CORPUS)
        afirmar("PAS capítulo correto é aceito e gravado", not erros and (base / "varredura" / "OBA.passe1.jsonl").exists(), str(erros[:2]))
        arq2 = saida / "incompleto.jsonl"
        escrever_jsonl(arq2, bom[:-1])
        e = receber_passe.receber("OBA", 2, "leitor_B", arq2, base, CORPUS)
        afirmar("PAS capítulo com versículo faltando é recusado e nada é gravado", e and not (base / "varredura" / "OBA.passe2.jsonl").exists(), str(e[:1]))
        ruim = json.loads(json.dumps(fixture.passe_oba(CORPUS, 2, "leitor_B")))
        next(x for x in ruim if x["unidades"])["unidades"][0]["ancora_texto"] = "inventada"
        escrever_jsonl(arq2, ruim)
        e = receber_passe.receber("OBA", 2, "leitor_B", arq2, base, CORPUS)
        afirmar("PAS âncora não literal é recusada", bool(e) and not (base / "varredura" / "OBA.passe2.jsonl").exists())
        escrever_jsonl(arq2, fixture.passe_oba(CORPUS, 2, "leitor_B"))
        e = receber_passe.receber("OBA", 2, "outro_leitor", arq2, base, CORPUS)
        afirmar("PAS leitor diferente do informado é recusado", bool(e))
        e = receber_passe.receber("OBA", 1, "leitor_A", arq2, base, CORPUS)
        afirmar("PAS passe diferente do informado é recusado", bool(e))
        e = receber_passe.receber("OBA", 2, "leitor_B", arq2, base, CORPUS)
        afirmar("PAS passe 2 aceito com leitor diferente do passe 1", not e, str(e[:1]))
        afirmar("PAS cobertura e independência aprovadas depois de receber os dois passes", not cobertura.verificar(base, CORPUS))
    finally:
        shutil.rmtree(base, ignore_errors=True)
        shutil.rmtree(saida, ignore_errors=True)


def teste_reconciliacao():
    base = novo_limpo()
    try:
        r = reconciliar.reconciliar(base, "OBA", CORPUS)
        afirmar("REC passes idênticos em conteúdo dão concordância 1.0", r["concordancia_versiculos_com_unidade_jaccard"] == 1.0
                and r["concordancia_classe_entre_pareadas"] == 1.0 and not r["divergencias_de_versiculo"])
        escrever_jsonl(base / "varredura" / "OBA.passe2.jsonl",
                       fixture.passe_oba(CORPUS, 2, "leitor_B", omitir_c=True, extra_16=True))
        r = reconciliar.reconciliar(base, "OBA", CORPUS)
        afirmar("REC lista divergência de versículo (1:16) e unidade sem par", "OBA 1:16" in r["divergencias_de_versiculo"]
                and len(r["unidades_so_no_passe1"]) == 1 and len(r["unidades_so_no_passe2"]) == 1
                and r["concordancia_versiculos_com_unidade_jaccard"] < 1.0, str(r["divergencias_de_versiculo"]))
    finally:
        shutil.rmtree(base, ignore_errors=True)


def teste_preparo():
    tmp = Path(tempfile.mkdtemp(prefix="promessas_prep_"))
    antigo = preparar_passes.PASSES
    try:
        shutil.copy(RAIZ / "passes" / "CARTAO_DE_CRITERIOS.md", tmp)
        shutil.copy(RAIZ / "passes" / "PROMPT_LEITOR_modelo.md", tmp)
        preparar_passes.PASSES = tmp
        preparar_passes.preparar("OBA", CORPUS, "leitor_A", "leitor_B")
        afirmar("PRE preparo íntegro (entradas idênticas, texto literal do corpus)", not preparar_passes.verificar("OBA", CORPUS))
        arq = tmp / "OBA" / "passe2" / "entrada" / "OBA_001.md"
        orig = arq.read_text(encoding="utf-8")
        arq.write_text(orig.replace("livramento", "salvação"), encoding="utf-8")
        afirmar("PRE entrada alterada é acusada", bool(preparar_passes.verificar("OBA", CORPUS)))
        arq.write_text(orig, encoding="utf-8")
        mf = tmp / "OBA" / "passe2" / "manifest.json"
        m = json.loads(mf.read_text(encoding="utf-8"))
        m["leitor"] = "leitor_A"
        mf.write_text(json.dumps(m), encoding="utf-8")
        afirmar("PRE leitores iguais nos dois passes são acusados", any("iguais" in e for e in preparar_passes.verificar("OBA", CORPUS)))
        p2 = tmp / "OBA" / "passe2" / "PROMPT_LEITOR.md"
        p2.write_text(p2.read_text(encoding="utf-8") + "\nveja passe1/saida\n", encoding="utf-8")
        afirmar("PRE prompt que cita a saída do outro passe é acusado", any("outro passe" in e for e in preparar_passes.verificar("OBA", CORPUS)))
    finally:
        preparar_passes.PASSES = antigo
        shutil.rmtree(tmp, ignore_errors=True)


def teste_montar():
    liv = "OBA"
    n = len(CORPUS.refs_do_livro(liv))
    un = {"i": 17, "f": 18, "t": "pro", "o": "dd", "n": "b", "p": "ind", "d": "isr", "c": "n", "r": "n",
          "a": "haverá livramento", "s": "fixture", "e": "fixture", "k": "a"}
    mapa = ["."] * n
    mapa[16], mapa[17] = "U", "p"
    obj = {"capitulo": 1, "mapa": "".join(mapa), "unidades": [un]}
    regs, erros = montar_passe.montar_capitulo(obj, liv, 1, "leitor_A", CORPUS)
    afirmar("MON capítulo compacto correto é expandido (21 versículos, 1 unidade, parte_de no v.18)",
            regs and not erros and len(regs) == 21 and regs[17]["estado"] == "parte_de_unidade" and regs[16]["unidades"][0]["uid"] == "U1-OBA-001:017-1", str(erros[:2]))
    base = Path(tempfile.mkdtemp(prefix="promessas_mon_"))
    try:
        lote = base / "lote.json"
        lote.write_text(json.dumps(obj), encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", str(RAIZ / "scripts" / "montar_passe.py"), liv, "1", "--leitor", "leitor_A",
                            "--lote", str(lote), "--base", str(base)], capture_output=True, text=True, encoding="utf-8", errors="replace")
        afirmar("MON montar e receber gravam o passe", r.returncode == 0 and (base / "varredura" / "OBA.passe1.jsonl").exists(), r.stdout[-200:])
    finally:
        shutil.rmtree(base, ignore_errors=True)
    ruim = dict(obj, mapa="." * n)
    _, e = montar_passe.montar_capitulo(ruim, liv, 1, "leitor_A", CORPUS)
    afirmar("MON mapa que diverge das unidades é recusado", bool(e), str(e[:1]))
    _, e = montar_passe.montar_capitulo(dict(obj, mapa="." * (n - 1)), liv, 1, "leitor_A", CORPUS)
    afirmar("MON mapa com menos letras que versículos é recusado", bool(e), str(e[:1]))
    _, e = montar_passe.montar_capitulo(dict(obj, unidades=[dict(un, a="")]), liv, 1, "leitor_A", CORPUS)
    afirmar("MON unidade sem âncora é recusada", bool(e))
    regs, e = montar_passe.montar_capitulo(dict(obj, unidades=[dict(un, o="hv")]), liv, 1, "leitor_A", CORPUS)
    probs = validar_esquema.validar_registro_varredura if False else None
    import tempfile as _t
    with _t.TemporaryDirectory() as tmp:
        escrever_jsonl(Path(tmp) / "varredura" / "OBA.passe1.jsonl", regs)
        cods = {p.controle for p in validar_esquema.verificar(Path(tmp), CORPUS)}
    afirmar("MON voto (origem hv) marcado como promessa é acusado como A12", "A12" in cods, str(cods))
    regs, e = montar_passe.montar_capitulo(dict(obj, unidades=[dict(un, t="xyz")]), liv, 1, "leitor_A", CORPUS)
    afirmar("MON tipo inválido é recusado", bool(e))


def _preparar_consolidacao(chaves_txt):
    base = novo_limpo()
    for sub in ("promessas", "ocorrencias", "nao_promessas"):
        shutil.rmtree(base / sub)
    (base / "revisao_humana.jsonl").write_text("", encoding="utf-8")
    cons = base / "consolidacao"
    cons.mkdir()
    (cons / "OBA_chaves_p1.txt").write_text(chaves_txt, encoding="utf-8")
    (cons / "OBA_cumprimentos_p1.txt").write_text("", encoding="utf-8")
    (cons / "OBA_familias.json").write_text(json.dumps({"F-X": {"nome": "x", "descricao": "d", "criterio_de_pertenca": "c"}}), encoding="utf-8")
    return base


CHAVES_OBA = (
    "U1-OBA-001:015-1 | retribuir | retribuicao | edom | nenhuma | F-X\n"
    "U1-OBA-001:017-1 | livrar | livramento | monte_siao | nenhuma | F-X\n"
    "U1-OBA-001:017-2 | restituir | propriedades | casa_de_jaco | nenhuma | F-X\n"
)


def teste_consolidar():
    base = _preparar_consolidacao(CHAVES_OBA)
    try:
        r = consolidar.consolidar(base, "OBA", CORPUS)
        st = {p["id"]: p["status"] for p in r["promessas"]}
        afirmar("CON passes concordantes geram 3 promessas B reconciliadas, 2 não promessas e nenhum item de revisão",
                len(r["promessas"]) == 3 and set(st.values()) == {"reconciliada"} and len(r["nao_promessas"]) == 2 and not r["revisao"], str(st))
        consolidar.gravar(base, "OBA", r, CORPUS)
        probs = todos(base)
        afirmar("CON dados consolidados passam em todos os controles automáticos", not probs, "; ".join(map(str, probs[:3])))
    finally:
        shutil.rmtree(base, ignore_errors=True)
    # passes divergentes
    base = _preparar_consolidacao(CHAVES_OBA)
    try:
        escrever_jsonl(base / "varredura" / "OBA.passe2.jsonl", fixture.passe_oba(CORPUS, 2, "leitor_B", omitir_c=True, extra_16=True))
        r = consolidar.consolidar(base, "OBA", CORPUS)
        st = {p["acao_canonica"]: p["status"] for p in r["promessas"]}
        afirmar("CON unidade sem par no Passe 2 vira promessa proposta e a unidade só do Passe 2 vai à revisão",
                st["restituir"] == "proposta" and st["livrar"] == "reconciliada" and len(r["revisao"]) == 2, str(st))
        consolidar.gravar(base, "OBA", r, CORPUS)
        probs = todos(base)
        afirmar("CON dados com divergência também passam nos controles estruturais", not probs, "; ".join(map(str, probs[:3])))
    finally:
        shutil.rmtree(base, ignore_errors=True)
    # equivalência: mesma chave vira ocorrência; mesma ação, outro beneficiário vira renovação
    chaves = (CHAVES_OBA.replace("restituir | propriedades | casa_de_jaco", "livrar | livramento | monte_siao"))
    base = _preparar_consolidacao(chaves)
    try:
        r = consolidar.consolidar(base, "OBA", CORPUS)
        tipos = sorted(o["tipo"] for o in r["ocorrencias"])
        fundida = [x for x in r["promessas"] if len(x["unidades_origem"]) >= 4]
        afirmar("CON unidades com a mesma chave no mesmo versículo viram UMA promessa e UMA ocorrência (todas as unidades ficam na origem)",
                len(r["promessas"]) == 2 and tipos == ["enunciacao_inicial", "enunciacao_inicial"] and len(fundida) == 1, str(tipos))
    finally:
        shutil.rmtree(base, ignore_errors=True)
    chaves = CHAVES_OBA.replace("restituir | propriedades | casa_de_jaco", "livrar | livramento | casa_de_jaco")
    base = _preparar_consolidacao(chaves)
    try:
        r = consolidar.consolidar(base, "OBA", CORPUS)
        rel = {p["beneficiario_canonico"]: (p["relacao"], p.get("promessa_mae_id")) for p in r["promessas"]}
        afirmar("CON mesma ação e família com beneficiário diferente vira renovação ligada à original",
                rel["monte_siao"][0] == "original" and rel["casa_de_jaco"][0] == "renovacao" and rel["casa_de_jaco"][1], str(rel))
    finally:
        shutil.rmtree(base, ignore_errors=True)
    base = _preparar_consolidacao(CHAVES_OBA.splitlines(True)[0])
    try:
        try:
            consolidar.consolidar(base, "OBA", CORPUS)
            afirmar("CON unidade promissória sem chave canônica é recusada", False)
        except SystemExit as e:
            afirmar("CON unidade promissória sem chave canônica é recusada", "sem chave" in str(e), str(e)[:80])
    finally:
        shutil.rmtree(base, ignore_errors=True)


def teste_pareamento():
    import reconciliar
    base = novo_limpo()
    try:
        u1 = [u for r in reconciliar.carregar_passe(base, "OBA", 1) for u in r["unidades"]]
        u2 = [u for r in reconciliar.carregar_passe(base, "OBA", 2) for u in r["unidades"]]
        pares, so1, so2 = reconciliar.parear(u1, u2, CORPUS)
        ok = len(pares) == len(u1) and not so1 and not so2 and all(a["ancora_texto"] == b["ancora_texto"] for a, b in pares)
        afirmar("PAR duas unidades no mesmo versículo são pareadas pela âncora, não pela ordem", ok, f"{len(pares)}/{len(u1)}")
    finally:
        shutil.rmtree(base, ignore_errors=True)


def teste_v03():
    # origem profética sem fundamento textual (A12) e forma de expressão inválida (A5)
    def add_prof(b, **extra):
        reg_ = fixture.nao_promessa(CORPUS, "N-OBA-0009", "OBA 1:21", "o reino será do SENHOR", "profecia_sem_compromisso", ["U1-OBA-001:021-1"],
                                    origem_real="profetica_patriarcal", **extra)
        editar(b, "nao_promessas/PRO.jsonl", lambda r: r.append(reg_)) if False else None
        f = Path(b) / "nao_promessas" / "OBA.jsonl"
        escrever_jsonl(f, [reg_])
    plantar("A12 origem profetica_patriarcal sem fundamento_textual", "A12", lambda b: add_prof(b))
    base = novo_limpo()
    try:
        add_prof(base, fundamento_textual=["OBA 1:21"])
        afirmar("V03 origem profetica_patriarcal com fundamento_textual é aceita", not [p for p in todos(base) if p.controle in ("A5", "A12")])
    finally:
        shutil.rmtree(base, ignore_errors=True)
    plantar("A5 forma_expressao fora do vocabulário", "A5", lambda b: mut(b, "promessas/ISA.jsonl", "P-ISA-0001", forma_expressao="forma_inventada"))
    plantar("A5 forca_textual fora do vocabulário", "A5", lambda b: mut(b, "promessas/ISA.jsonl", "P-ISA-0001", forca_textual="enorme"))
    # nível D
    def add_dev(b, **campos):
        d = {"id": "V-ISA-0001", "ref_inicio": "ISA 41:10", "ref_fim": "ISA 41:10", "tipo": "conexao", "nota": "teste", "promessa_id": "P-ISA-0001"}
        d.update(campos)
        escrever_jsonl(Path(b) / "desenvolvimento" / "ISA.jsonl", [d])
    base = novo_limpo()
    try:
        add_dev(base)
        afirmar("V03 registro de nível D válido passa nos controles", not todos(base))
        c = contar.contar(base, CORPUS)
        afirmar("V03 nível D é contado à parte e NÃO soma nas promessas",
                c["nivel_D_desenvolvimento_por_tipo_NAO_SOMADO"] == {"conexao": 1} and sum(c["nivel_B_promessas_distintas_por_categoria"].values()) == 8)
    finally:
        shutil.rmtree(base, ignore_errors=True)
    plantar("A5 nível D com tipo inválido", "A5", lambda b: add_dev(b, tipo="inventado"))
    plantar("A8 nível D ligado a promessa inexistente", "A8", lambda b: add_dev(b, promessa_id="P-ISA-0099"))
    plantar("A2 nível D com referência inexistente", "A2", lambda b: add_dev(b, ref_fim="ISA 41:99"))
    # contagem ampliada e B fundamental
    base = novo_limpo()
    try:
        mut(base, "promessas/OBA.jsonl", "P-OBA-0002", origem_real="profetica_patriarcal", promitente_nome="Jacó", fundamento_textual=["OBA 1:17"])
        for rr in ("promitente",):
            editar(base, "promessas/OBA.jsonl", lambda regs: reg(regs, "P-OBA-0002").pop(rr, None))
        c = contar.contar(base, CORPUS)
        afirmar("V03 patriarcal profética fica fora do indicador principal e entra na contagem ampliada",
                c["indicador_principal_promessas_divinas_de_bencao"] == 4 and c["contagem_ampliada_bencao"] == 5, str(c["nivel_B_promessas_distintas_por_categoria"]))
    finally:
        shutil.rmtree(base, ignore_errors=True)
    base = novo_limpo()
    try:
        editar(base, "promessas/ISA.jsonl", lambda regs: reg(regs, "P-ISA-0002").update(acao_canonica="fortalecer", objeto_canonico="forca",
               beneficiario_canonico="povo_de_deus", condicao_canonica="explicita_x", resumo_proprio="outro resumo totalmente diferente"))
        c = contar.contar(base, CORPUS)
        afirmar("V03 B fundamental ignora a condição (preserva a contagem fina)",
                c["nivel_B_promessas_distintas_por_categoria"]["divina_bencao"] == 5 and c["nivel_B_fundamental_por_categoria"]["divina_bencao"] == 4,
                str(c["nivel_B_fundamental_por_categoria"]))
    finally:
        shutil.rmtree(base, ignore_errors=True)



def teste_v04():
    import contar_v04
    import consolidar_v04
    import validar_semantica
    # campo pendente preenchido, desconhecido e registro pendente aprovado
    plantar("A9 campo listado como pendente mas preenchido", "A9", lambda b: mut(b, "promessas/ISA.jsonl", "P-ISA-0001", campos_pendentes=["reforco"]))
    plantar("A5 campos_pendentes com campo desconhecido", "A5", lambda b: mut(b, "promessas/ISA.jsonl", "P-ISA-0001", campos_pendentes=["inventado"]))
    plantar("A9 registro com campo pendente não pode estar revisado", "A9",
            lambda b: mut(b, "promessas/ISA.jsonl", "P-ISA-0001", campos_pendentes=["reforco"], status="revisada_humano", reforco=None))
    # promitente pendente é aceito (não presumido) no registro adjudicado
    base = novo_limpo()
    try:
        editar(base, "promessas/ISA.jsonl", lambda regs: (reg(regs, "P-ISA-0001").pop("promitente", None), reg(regs, "P-ISA-0001").update(campos_pendentes=["promitente"])))
        afirmar("V04 promitente nulo e pendente é aceito sem valor presumido", not [p for p in todos(base) if p.controle in ("A5", "A9")])
    finally:
        shutil.rmtree(base, ignore_errors=True)
    # cumprimento narrado exige base e fórmula literal
    def dev(b, **campos):
        d = {"id": "V-ISA-0001", "ref_inicio": "ISA 41:10", "ref_fim": "ISA 41:10", "tipo": "cumprimento_narrado", "nota": "t", "promessa_id": "P-ISA-0001"}
        d.update(campos)
        escrever_jsonl(Path(b) / "desenvolvimento" / "ISA.jsonl", [d])
    plantar("A5 cumprimento_narrado sem base", "A5", lambda b: dev(b))
    plantar("A9 declarado_pelo_texto sem fórmula textual", "A9", lambda b: dev(b, base="declarado_pelo_texto"))
    plantar("A3 fórmula textual que não é trecho literal", "A3", lambda b: dev(b, base="declarado_pelo_texto", formula_textual="texto inexistente no capítulo"))
    # linha patriarcal: 'a ti' e 'à tua descendência' são a mesma promessa
    k1 = consolidar_v04.normalizar_linha({"acao": "dar", "objeto": "terra", "benef": "descendencia_de_abraao", "cond": "nenhuma", "fam": "F-X"})
    k2 = consolidar_v04.normalizar_linha({"acao": "dar", "objeto": "terra", "benef": "abraao", "cond": "nenhuma", "fam": "F-X"})
    k3 = consolidar_v04.normalizar_linha({"acao": "dar", "objeto": "terra", "benef": "isaque", "cond": "nenhuma", "fam": "F-X"})
    afirmar("V04 mesma linha patriarcal normalizada; Isaque segue distinto", k1["benef"] == k2["benef"] == "abraao_e_descendencia" and k3["benef"] != k1["benef"])
    # coerência semântica: animais não são crente_individual
    afirmar("V04 animais incompatíveis com crente_individual", "crente_individual" not in (validar_semantica.esperado_destinatario("animais_aquaticos_e_aves") or set()))
    # menção histórica fica fora de C
    base = novo_limpo()
    try:
        editar(base, "ocorrencias/ISA.jsonl", lambda regs: regs[0].update(tipo="mencao_historica"))
        c0 = contar_v04.contar4(novo_limpo_ref, CORPUS) if False else None
        c = contar_v04.contar4(base, CORPUS)
        afirmar("V04 menção histórica não entra no nível C", c["mencoes_historicas_fora_de_C"] == 1)
    finally:
        shutil.rmtree(base, ignore_errors=True)


def teste_fonte_intacta():
    """Prova de que a fonte da Bíblia Almeida Livre não foi tocada: hash de todos os capítulos contra o manifesto."""
    import auditar_corpus as ac
    atual = []
    for pasta in sorted(ac.TEXTO.iterdir()):
        for f in sorted(pasta.glob("*.md")):
            atual.append(f"{ac.sha256(f)}  {pasta.name}/{f.name}")
    man = (RAIZ / "dados" / "manifesto_sha256.txt").read_text(encoding="utf-8").splitlines()
    afirmar("FONTE todos os 1.189 capítulos da Almeida Livre idênticos ao manifesto", sorted(atual) == sorted(man), f"{len(atual)} arquivos")


def main():
    teste_linha_de_base()
    teste_erros()
    teste_a1()
    teste_congelamento()
    teste_citacao()
    teste_receber_passe()
    teste_reconciliacao()
    teste_preparo()
    teste_montar()
    teste_pareamento()
    teste_consolidar()
    teste_v03()
    teste_v04()
    teste_fonte_intacta()
    total, ok = len(RESULTADOS), sum(1 for r in RESULTADOS if r[2])
    linhas = [f"# Testes com erros plantados ({date.today().isoformat()})", "",
              f"Resultado: **{ok} de {total} aprovados**.", "",
              "| Teste | Controle esperado | Resultado | Controles que acusaram |", "| --- | --- | --- | --- |"]
    for nome, esp, passou, cods, extra in RESULTADOS:
        linhas.append(f"| {nome} | {esp} | {'PASS' if passou else 'FAIL'} | {cods} |")
    (RAIZ / "auditoria" / "testes_erros_plantados.md").write_text("\n".join(linhas) + "\n", encoding="utf-8", newline="\n")
    print(f"\n{ok}/{total} testes aprovados")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
