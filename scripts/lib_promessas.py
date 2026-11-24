"""Biblioteca comum do projeto Promessas da Bíblia by Jair Lima (protocolo v0.2).

Só biblioteca padrão. Somente leitura sobre o corpus. Rodar scripts com `python -I`.
"""
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CORPUS_PATH = RAIZ / "dados" / "corpus_al.jsonl"

CANON = ("GEN EXO LEV NUM DEU JOS JDG RUT 1SA 2SA 1KI 2KI 1CH 2CH EZR NEH EST JOB PSA PRO ECC SNG ISA JER LAM EZK DAN HOS JOL AMO OBA JON MIC NAM HAB ZEP HAG ZEC MAL "
         "MAT MRK LUK JHN ACT ROM 1CO 2CO GAL EPH PHP COL 1TH 2TH 1TI 2TI TIT PHM HEB JAS 1PE 2PE 1JN 2JN 3JN JUD REV").split()  # ordem canônica

# ----------------------------------------------------------------- enums (protocolo v0.2)
TIPOS_UNIDADE = {
    "promessa", "profecia_sem_compromisso", "mandamento", "advertencia",
    "desejo_ou_bencao_votiva", "fato_ou_atributo", "principio_sapiencial",
    "cumprimento_narrado", "declaracao_sem_compromisso", "indeterminada",
}
ORIGENS_REAIS = {
    "divina_direta", "divina_relatada_por_humano", "humana_em_nome_proprio",
    "humana_votiva", "adversaria_ou_falsa", "profetica_patriarcal", "apostolica_garantia", "indeterminada",
}
ORIGENS_DIVINAS = {"divina_direta", "divina_relatada_por_humano"}
NATUREZAS = {"bencao", "juizo", "nao_se_aplica"}
PROMITENTES = {"pai", "filho", "espirito", "deus_indistinto", "mensageiro_autorizado"}
DESTINATARIOS = {
    "pessoa", "familia_ou_linhagem", "israel", "igreja", "igreja_local", "grupo_especifico",
    "crente_individual", "humanidade", "criacao", "messias", "nacoes_especificas", "indeterminado",
}
CONDICAO_TIPOS = {"nenhuma", "explicita", "contextual"}
REFORCOS = {"nenhum", "juramento", "alianca", "sinal"}
ETAPAS = {"primeva", "patriarcal", "mosaica", "monarquica_e_profetica",
          "exilica_e_pos_exilica", "cristo_e_apostolos"}
APLICABILIDADES = {"direta", "estendida_pelo_texto"}
RELACOES = {"original", "renovacao", "desdobramento"}
CUMPRIMENTOS = {"declarado_no_texto", "declarado_em_texto_posterior", "correspondencia_narrativa", "em_curso",
                "futuro_segundo_o_texto", "nao_declarado"}
BASES_CUMPRIMENTO = {"declarado_pelo_texto", "correspondencia_narrativa"}
FUNDAMENTACOES = {"fundamentada", "insuficiente"}
CAMPOS_PENDENTES_VALIDOS = {"promitente", "promitente_nome", "destinatario_tipo", "condicao_tipo", "condicao_ref", "reforco",
                            "atribuicao_divina_ref", "fundamento_textual", "forma_expressao", "forca_textual", "natureza"}
CONFIANCAS = {"alta", "media", "baixa"}
STATUS_PROMESSA = {"proposta", "reconciliada", "adjudicada", "revisada_humano", "congelada", "rejeitada"}
FORMAS_EXPRESSAO = {"primeira_pessoa_futuro", "primeira_pessoa_presente", "perfeito_de_certeza",
                    "segunda_ou_terceira_pessoa_futuro", "imperativo_de_bencao", "sentenca", "passiva",
                    "juramento_ou_alianca", "transmitida"}
FORCAS_TEXTUAIS = {"forte", "media", "fraca"}
TIPOS_DESENVOLVIMENTO = {"citacao_posterior", "conexao", "cumprimento_narrado"}
TIPOS_OCORRENCIA = {"enunciacao_inicial", "reafirmacao", "reafirmacao_por_humano",
                    "citacao_posterior", "cumprimento_declarado", "mencao_historica"}
ESTADOS_VARREDURA = {"sem_unidade", "com_unidade", "parte_de_unidade"}
MOTIVOS_REVISAO = {"classe_incerta", "origem_incerta", "destinatario_incerto", "discordancia_passes",
                   "escola_interpretativa", "atomicidade", "equivalencia_semantica", "outro"}
DECIDIDO_POR = {"jair", "ia_com_ratificacao_pendente", "regra_do_protocolo"}
TIPOS_DECISAO = {"criterio", "nao_equivalencia", "excecao_equivalencia", "outro"}

RE_REF = re.compile(r"^([0-9A-Z]{3}) (\d+):(\d+)$")
RE_SLUG = re.compile(r"^[a-z0-9_]+$")
RE_DATA = re.compile(r"^\d{4}-\d{2}-\d{2}")
RE_UID = re.compile(r"^U([12])-([0-9A-Z]{3})-(\d{3}):(\d{3})-(\d+)$")


@dataclass
class Problema:
    controle: str
    arquivo: str
    linha: int
    id: str
    msg: str

    def __str__(self):
        return f"[{self.controle}] {self.arquivo}:{self.linha} {self.id} {self.msg}"


# ----------------------------------------------------------------- utilidades
def ws(t: str) -> str:
    return re.sub(r"\s+", " ", t).strip()


def sha256_texto(t: str) -> str:
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def sha256_arquivo(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def parse_ref(s):
    if not isinstance(s, str):
        return None
    m = RE_REF.match(s)
    return (m.group(1), int(m.group(2)), int(m.group(3))) if m else None


def fmt_ref(liv, cap, v):
    return f"{liv} {cap}:{v}"


def parse_intervalo(s):
    """'GEN 12:2' | 'GEN 12:2-3' | 'GEN 12:10-13:4' -> (ref_ini, ref_fim) ou None."""
    if not isinstance(s, str):
        return None
    if parse_ref(s):
        return s, s
    m = re.match(r"^([0-9A-Z]{3}) (\d+):(\d+)-(?:(\d+):)?(\d+)$", s)
    if not m:
        return None
    liv, c1, v1, c2, v2 = m.groups()
    c2 = c2 or c1
    return fmt_ref(liv, int(c1), int(v1)), fmt_ref(liv, int(c2), int(v2))


def ler_jsonl(path: Path, problemas: list):
    """Retorna [(numero_linha, registro)], registrando JSON inválido como A5."""
    saida = []
    p = Path(path)
    if not p.exists():
        return saida
    for i, linha in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if not linha.strip():
            continue
        try:
            rec = json.loads(linha)
        except json.JSONDecodeError as e:
            problemas.append(Problema("A5", p.name, i, "-", f"JSON inválido: {e}"))
            continue
        if not isinstance(rec, dict):
            problemas.append(Problema("A5", p.name, i, "-", "registro não é objeto JSON"))
            continue
        saida.append((i, rec))
    return saida


def escrever_jsonl(path: Path, registros):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for r in registros:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


class Corpus:
    def __init__(self, path=CORPUS_PATH):
        self.texto = {}
        self.ordem = {}   # livro -> [(cap, v)]
        self.pos = {}     # (livro,cap,v) -> indice
        for l in Path(path).read_text(encoding="utf-8").splitlines():
            r = json.loads(l)
            self.texto[r["ref"]] = r["texto"]
            self.ordem.setdefault(r["livro"], []).append((r["cap"], r["v"]))
        for liv, lst in self.ordem.items():
            lst.sort()
            for i, (c, v) in enumerate(lst):
                self.pos[(liv, c, v)] = i

    def existe(self, ref):
        return ref in self.texto

    def refs_do_livro(self, liv):
        return [fmt_ref(liv, c, v) for c, v in self.ordem.get(liv, [])]

    def intervalo(self, ini, fim):
        """Lista de refs entre ini e fim (inclusive), ou None se inválido."""
        a, b = parse_ref(ini), parse_ref(fim)
        if not a or not b or a[0] != b[0] or a not in self._keys() or b not in self._keys():
            return None
        i, j = self.pos[a], self.pos[b]
        if i > j:
            return None
        return [fmt_ref(a[0], c, v) for c, v in self.ordem[a[0]][i:j + 1]]

    def _keys(self):
        return self.pos

    def texto_intervalo(self, ini, fim):
        refs = self.intervalo(ini, fim)
        return None if refs is None else " ".join(self.texto[r] for r in refs)


# ----------------------------------------------------------------- campos e regras de unidade
def _obrig(rec, campos, tipo=str):
    return [c for c in campos if not isinstance(rec.get(c), tipo) or (tipo is str and not rec[c].strip())]


def validar_unidade_comum(u: dict, add):
    """Regras compartilhadas por unidades de passe, promessas (B) e não-promessas.
    `add(controle, msg)` registra problema."""
    tipo = u.get("tipo_unidade")
    if tipo not in TIPOS_UNIDADE:
        add("A5", f"tipo_unidade inválido: {tipo!r}")
        return
    if u.get("origem_real") not in ORIGENS_REAIS:
        add("A5", f"origem_real inválida: {u.get('origem_real')!r}")
    for c in _obrig(u, ["ref_inicio", "ref_fim", "ancora_texto", "resumo_proprio"]):
        add("A5", f"campo obrigatório ausente ou vazio: {c}")
    ev = u.get("evidencia_exegetica")
    if not isinstance(ev, list) or not ev:
        add("A5", "evidencia_exegetica deve ser lista não vazia")
    else:
        for e in ev:
            if not isinstance(e, dict) or not isinstance(e.get("ref"), str) or not str(e.get("observacao", "")).strip():
                add("A5", "evidencia_exegetica: cada item exige ref e observacao")
    if u.get("confianca") not in CONFIANCAS:
        add("A5", f"confianca inválida: {u.get('confianca')!r}")

    origem = u.get("origem_real")
    pend = set(u.get("campos_pendentes") or [])
    for c in pend:
        if c not in CAMPOS_PENDENTES_VALIDOS:
            add("A5", f"campos_pendentes lista campo desconhecido: {c}")
        elif u.get(c) not in (None, "", []):
            add("A9", f"campo {c} está em campos_pendentes mas foi preenchido (valor presumido?)")
    if u.get("forma_expressao") not in (None, "") and u["forma_expressao"] not in FORMAS_EXPRESSAO:
        add("A5", f"forma_expressao inválida: {u['forma_expressao']!r}")
    if u.get("forca_textual") not in (None, "") and u["forca_textual"] not in FORCAS_TEXTUAIS:
        add("A5", f"forca_textual inválida: {u['forca_textual']!r}")
    if origem == "profetica_patriarcal":
        ft = u.get("fundamento_textual")
        if (not isinstance(ft, list) or not ft) and "fundamento_textual" not in pend:
            add("A12", "profetica_patriarcal exige fundamento_textual (referências)")
        if tipo == "promessa" and u.get("fundamentacao_divina") not in FUNDAMENTACOES:
            add("A12", "promessa profetica_patriarcal exige fundamentacao_divina (fundamentada ou insuficiente)")
        if u.get("fundamentacao_divina") == "fundamentada" and not (u.get("leitura_posterior_refs") or u.get("fundamento_textual")):
            add("A12", "fundamentacao_divina fundamentada exige fundamento_textual ou leitura_posterior_refs")
    if tipo == "promessa":
        # Coerência de categoria (A12)
        if origem == "humana_votiva":
            add("A12", "voto ou bênção votiva não é promessa: usar tipo desejo_ou_bencao_votiva")
        if origem == "indeterminada":
            add("A12", "promessa com origem indeterminada: usar tipo indeterminada e fila de revisão")
        # D-08: toda promessa, de qualquer origem, é de benefício (bencao) ou de prejuízo (juizo)
        if u.get("natureza") not in {"bencao", "juizo"} and "natureza" not in pend:
            add("A5", "promessa exige natureza bencao (benefício) ou juizo (prejuízo)")
        if origem in ORIGENS_DIVINAS:
            if u.get("promitente") not in PROMITENTES and "promitente" not in pend:
                add("A5", f"promitente inválido ou ausente: {u.get('promitente')!r}")
        else:
            if not str(u.get("promitente_nome", "")).strip() and "promitente_nome" not in pend:
                add("A5", "promessa humana ou adversária exige promitente_nome")
        if origem == "divina_relatada_por_humano":
            if not parse_intervalo(u.get("atribuicao_divina_ref")) and "atribuicao_divina_ref" not in pend:
                add("A5", "divina_relatada_por_humano exige atribuicao_divina_ref válida")
            if not str(u.get("promitente_nome", "")).strip() and "promitente_nome" not in pend:
                add("A5", "divina_relatada_por_humano exige promitente_nome (quem relata)")
        if u.get("destinatario_tipo") not in DESTINATARIOS and "destinatario_tipo" not in pend:
            add("A5", f"destinatario_tipo inválido: {u.get('destinatario_tipo')!r}")
        if u.get("condicao_tipo") not in CONDICAO_TIPOS and "condicao_tipo" not in pend:
            add("A5", f"condicao_tipo inválido: {u.get('condicao_tipo')!r}")
        elif u.get("condicao_tipo") == "explicita" and not parse_intervalo(u.get("condicao_ref")) and "condicao_ref" not in pend:
            add("A9", "condicao_tipo explicita exige condicao_ref válida")
        if u.get("reforco") not in REFORCOS and "reforco" not in pend:
            add("A5", f"reforco inválido: {u.get('reforco')!r}")
        if u.get("promitente") == "filho" and not str(u.get("contexto_destinatario", "")).strip():
            add("A12", "promessa de Cristo exige contexto_destinatario (quem ouviu, em que situação)")
    else:
        if tipo == "principio_sapiencial" and origem in ORIGENS_DIVINAS:
            add("A12", "princípio sapiencial com origem divina identificável deve ser promessa ou ir à revisão")
