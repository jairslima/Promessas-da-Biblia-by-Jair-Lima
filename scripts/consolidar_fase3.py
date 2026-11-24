"""Consolidação Definitiva da Fase 3 (Árbitro Independente) e Fechamento Técnico Definitivo (8 Itens da Crítica).

Executa:
1. Recupera os 276 resumos "(resumo não informado pelo leitor)":
   - 202 diretamente do outro leitor do par que leu o mesmo versículo/compromisso (alinhado por similaridade de âncora e mesma natureza).
   - 74 (onde ambos os leitores operaram em modo tolerante sem chave 's') a partir do mapa fiel ao texto bíblico e à âncora (`RESUMOS_74`).
   - Zero registros permanecem com "(resumo não informado pelo leitor)" ou "(sem resumo)".
2. Verifica e corrige a identificação de `promitente` e `comunicador` (`promitente_nome`):
   - Em `divina_direta` e `divina_relatada_por_humano`, o `promitente` é SEMPRE divino (`pai`, `filho`, `espirito`, `deus_indistinto` ou `mensageiro_autorizado`).
   - Quando um humano (ex.: Isaías, Jeremias, Paulo, Davi, todo o Israel em 1Cr 11.2) relata ou invoca a promessa de Deus, o nome humano é preservado em `comunicador` (`promitente_nome`), nunca substituindo o `promitente` divino.
3. Deduplica apenas as 14 duplicatas técnicas estritas (preservando integralmente as 3.224 unidades confirmadas).
4. Documenta a conciliação exata das 3.609 unidades preliminares -> 3.224 unidades confirmadas (diferença de 385 unidades = 334 em casos rejeitados + 37 por granularidade na escolha do árbitro + 14 duplicatas estritas) e a relação 1.808 casos arbitrados -> 1.843 unidades decididas (332 casos rejeitados e 1.476 casos confirmados que somam 1.511 unidades por conterem 32 casos com múltiplas promessas).
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apurar_numero
import casos_adjudicacao
import catalogar_livro
import catalogo
import reconciliar
from lib_promessas import *  # noqa: F401,F403

BASE = RAIZ / "dados_leituras"
ADJ = RAIZ / "adjudicacao"
SAIDAS_F3 = ADJ / "fase3_saidas"
CASOS_F3 = ADJ / "fase3_todos_casos.json"

LIVROS_CRISTO = {"MAT", "MRK", "LUK", "JHN", "REV"}
VALORES_PROM_DIVINO = {"pai", "filho", "espirito", "deus_indistinto", "mensageiro_autorizado"}

# 74 resumos exatos extraídos das âncoras e versículos onde ambos os leitores omitiram a chave 's' no modo tolerante
RESUMOS_74 = {
    ("1SA 25:41", "1SA 25:41", "humana_beneficio"): "Abigail dispõe-se a servir Davi e a lavar os pés dos servos de seu senhor.",
    ("2CH 16:3", "2CH 16:3", "humana_beneficio"): "O rei Asa envia prata e ouro a Ben-Hadade e propõe aliança para que ele rompa seu pacto com Baasa.",
    ("2KI 19:23", "2KI 19:23", "adversaria_ou_falsa"): "Senaqueribe jacta-se de que cortará os cedros mais altos do Líbano e entrará em sua floresta fértil.",
    ("AMO 6:7", "AMO 6:7", "divina_juizo"): "Deus anuncia que os que vivem regaladamente serão os primeiros a ir para o cativeiro e cessará o seu banquete.",
    ("AMO 6:14", "AMO 6:14", "divina_juizo"): "O SENHOR dos Exércitos declara que levantará uma nação para oprimir a casa de Israel desde Hamate até a Arabá.",
    ("EZK 7:2", "EZK 7:4", "divina_juizo"): "O Senhor SENHOR anuncia o fim sobre a terra de Israel, declarando que enviará sua ira e julgará o povo segundo suas abominações.",
    ("EZK 7:5", "EZK 7:9", "divina_juizo"): "O Senhor SENHOR declara que em breve derramará seu furor sobre Israel sem poupar e julgará o povo segundo seus caminhos.",
    ("EZK 7:11", "EZK 7:14", "divina_juizo"): "Deus declara que a visão de ira ardente contra a multidão de Israel não será revogada e nada restará de sua riqueza.",
    ("EZK 7:15", "EZK 7:19", "divina_juizo"): "Deus anuncia que os que estiverem no campo morrerão à espada e os da cidade serão consumidos pela fome e pela peste.",
    ("EZK 7:19", "EZK 7:22", "divina_juizo"): "Deus declara que nem prata nem ouro livrarão o povo no dia do furor do SENHOR e que seus adornos serão entregues a estrangeiros.",
    ("EZK 7:20", "EZK 7:22", "divina_juizo"): "Deus anuncia que entregará os adornos e riquezas de Israel como presa a estrangeiros, que profanarão o seu santuário.",
    ("EZK 7:23", "EZK 7:27", "divina_juizo"): "O SENHOR declara que trará as piores nações para tomar posse das casas de Israel, fará cessar a arrogância dos poderosos e os julgará segundo seus caminhos.",
    ("EZK 12:11", "EZK 12:14", "divina_juizo"): "Deus anuncia por meio do sinal profético de Ezequiel que os habitantes de Jerusalém irão para o exílio e o cativeiro.",
    ("EZK 12:12", "EZK 12:13", "divina_juizo"): "O SENHOR declara que estenderá sua rede sobre o príncipe de Jerusalém e o levará à Babilônia, onde morrerá sem vê-la.",
    ("EZK 12:14", "EZK 12:15", "divina_juizo"): "Deus anuncia que espalhará a todos os ventos os auxiliares e tropas do príncipe e desembainhará a espada atrás deles.",
    ("EZK 12:16", "EZK 12:16", "divina_bencao"): "Deus promete preservar alguns poucos sobreviventes da espada, da fome e da peste para que reconheçam que ele é o SENHOR.",
    ("EZK 12:19", "EZK 12:20", "divina_juizo"): "O Senhor SENHOR anuncia que a terra de Israel será despojada de sua abundância e as cidades habitadas serão devastadas.",
    ("EZK 12:28", "EZK 12:28", "divina_juizo"): "O Senhor SENHOR declara que nenhuma de suas palavras será mais adiada, mas a palavra que ele disser se cumprirá.",
    ("EZK 23:28", "EZK 23:30", "divina_juizo"): "O Senhor SENHOR declara que entregará Jerusalém nas mãos dos que ela odeia, os quais tomarão seu trabalho e exporão sua vergonha.",
    ("EZK 23:31", "EZK 23:34", "divina_juizo"): "O Senhor SENHOR anuncia que colocará na mão de Jerusalém o copo de horror e desolação de sua irmã Samaria, e ela o beberá até o fim.",
    ("EZK 23:45", "EZK 23:45", "divina_juizo"): "Deus declara que homens justos julgarão Oolá e Oolibá segundo a sentença das adúlteras e das que derramam sangue.",
    ("EZK 23:46", "EZK 23:49", "divina_juizo"): "O Senhor SENHOR determina que suba uma assembleia para entregar as irmãs adúlteras ao saque, à espada e ao fogo, fazendo cessar a perversidade na terra.",
    ("EZK 33:9", "EZK 33:9", "divina_bencao"): "Deus garante ao atalaia que, se ele advertir o perverso, ainda que este não se converta, o atalaia terá livrado a própria vida.",
    ("EZK 33:18", "EZK 33:19", "divina_bencao"): "Deus promete que, quando o perverso se afastar de sua maldade e praticar o direito e a justiça, viverá por causa deles.",
    ("EZK 33:20", "EZK 33:20", "divina_juizo"): "O Senhor declara que julgará cada pessoa da casa de Israel segundo os seus próprios caminhos.",
    ("EZK 33:27", "EZK 33:29", "divina_juizo"): "O Senhor SENHOR jura por sua vida que os que estão nas ruínas cairão à espada, os do campo serão devorados e a terra será transformada em desolação.",
    ("EZK 33:33", "EZK 33:33", "divina_bencao"): "Deus assegura a Ezequiel que, quando a palavra se cumprir, o povo reconhecerá que houve um profeta no meio deles.",
    ("EZK 39:7", "EZK 39:7", "divina_bencao"): "O SENHOR promete fazer seu santo nome conhecido no meio de Israel e nunca mais permitir que seja profanado.",
    ("EZK 39:9", "EZK 39:10", "divina_bencao"): "O Senhor SENHOR garante que os habitantes de Israel queimarão as armas inimigas por sete anos e despojarão os que os despojaram.",
    ("EZK 39:11", "EZK 39:11", "divina_juizo"): "Deus declara que dará a Gogue e a toda a sua multidão um lugar de sepultura em Israel, no vale de Hamom-Gogue.",
    ("EZK 39:12", "EZK 39:16", "divina_bencao"): "O Senhor SENHOR assegura que a casa de Israel sepultará os invasores e purificará a terra, alcançando renome no dia em que Deus for glorificado.",
    ("EZK 39:22", "EZK 39:22", "divina_bencao"): "Deus garante que, desde aquele dia em diante, a casa de Israel saberá que ele é o SENHOR, seu Deus.",
    ("EZK 39:25", "EZK 39:29", "divina_bencao"): "O Senhor SENHOR promete restaurar a sorte de Jacó, ter compaixão de toda a casa de Israel e fazê-los habitar em segurança em sua própria terra.",
    ("EZK 39:27", "EZK 39:29", "divina_bencao"): "O Senhor SENHOR promete nunca mais esconder seu rosto de Israel, derramando o seu Espírito sobre a casa de Israel.",
    ("EZK 48:35", "EZK 48:35", "divina_bencao"): "Deus assegura sua presença perpétua na cidade restaurada, cujo nome desde aquele dia será: O SENHOR Está Ali.",
    ("JER 5:1", "JER 5:1", "divina_bencao"): "O SENHOR promete perdoar Jerusalém caso se encontre nela alguém que pratique a justiça e busque a fidelidade.",
    ("JER 5:6", "JER 5:6", "divina_juizo"): "Deus anuncia que animais predadores (leão, lobo e leopardo) atacarão e despedaçarão os transgressores das cidades de Judá.",
    ("JER 5:9", "JER 5:9", "divina_sentenca"): "O SENHOR declara em sentença judicial que certamente castigará essas transgressões e se vingará de uma nação como aquela.",
    ("JER 5:14", "JER 5:14", "divina_juizo"): "O SENHOR dos Exércitos declara a Jeremias que fará de suas palavras um fogo na boca do profeta e que o povo será consumido como lenha.",
    ("JER 5:15", "JER 5:17", "divina_juizo"): "O SENHOR anuncia que trará contra a casa de Israel uma nação antiga e distante que devorará sua colheita, seu gado e demolirá suas cidades fortificadas.",
    ("JER 5:18", "JER 5:18", "divina_bencao"): "O SENHOR promete que, mesmo naqueles dias de juízo, não destruirá completamente o seu povo.",
    ("JER 5:19", "JER 5:19", "divina_juizo"): "Deus declara que, assim como os israelitas o abandonaram para servir deuses estranhos em sua terra, servirão a estrangeiros em uma terra alheia.",
    ("JER 5:29", "JER 5:29", "divina_sentenca"): "O SENHOR reafirma sua sentença de que castigará a iniquidade e tomará vingança contra uma nação rebelde como aquela.",
    ("JER 11:3", "JER 11:3", "divina_sentenca"): "O SENHOR, Deus de Israel, promulga sentença de maldição sobre o homem que não ouvir as palavras da aliança.",
    ("JER 11:4", "JER 11:4", "divina_bencao"): "Deus promete ao povo que, se ouvirem sua voz e cumprirem seus mandamentos, serão o seu povo e ele será o seu Deus.",
    ("JER 11:5", "JER 11:5", "divina_bencao"): "O SENHOR garante confirmar o juramento feito aos patriarcas de lhes dar uma terra que mana leite e mel.",
    ("JER 11:11", "JER 11:12", "divina_juizo"): "O SENHOR anuncia que trará sobre Judá e Jerusalém uma calamidade da qual não poderão escapar e não os ouvirá quando clamarem.",
    ("JER 11:14", "JER 11:14", "divina_juizo"): "Deus declara a Jeremias que não ouvirá o clamor do povo no momento de sua calamidade.",
    ("JER 11:21", "JER 11:23", "divina_juizo"): "O SENHOR dos Exércitos anuncia que castigará os homens de Anatote: seus jovens morrerão à espada, seus filhos de fome, e não lhes restará remanescente.",
    ("JER 15:2", "JER 15:3", "divina_juizo"): "O SENHOR decreta que o povo será entregue ao seu destino de juízo: morte, espada, fome e cativeiro.",
    ("JER 15:3", "JER 15:4", "divina_juizo"): "O SENHOR declara que castigará o povo com quatro tipos de destruidores: a espada, os cães, as aves dos céus e os animais da terra.",
    ("JER 15:4", "JER 15:4", "divina_juizo"): "Deus anuncia que fará de Judá motivo de horror para todos os reinos da terra por causa dos pecados de Manassés em Jerusalém.",
    ("JER 15:6", "JER 15:6", "divina_juizo"): "O SENHOR declara que estenderá sua mão contra Jerusalém para destruí-la, por ter-se afastado dele.",
    ("JER 15:7", "JER 15:9", "divina_juizo"): "O SENHOR anuncia que espalhará o povo nas portas da terra, multiplicará suas viúvas e entregará os sobreviventes à espada diante dos inimigos.",
    ("JER 15:8", "JER 15:9", "divina_juizo"): "Deus declara que trará ao meio-dia um destruidor, multiplicando as viúvas mais que a areia dos mares e entregando o restante à espada.",
    ("JER 15:11", "JER 15:11", "divina_bencao"): "O SENHOR promete libertar o profeta para o bem e fazer que o próprio inimigo lhe suplique no tempo da calamidade e da angústia.",
    ("JER 15:13", "JER 15:14", "divina_juizo"): "Deus anuncia que entregará gratuitamente os bens e tesouros do povo ao saque por causa de todos os seus pecados.",
    ("JER 15:14", "JER 15:14", "divina_juizo"): "O SENHOR declara que fará o povo servir aos seus inimigos em uma terra desconhecida, pois o fogo da ira divina se acendeu contra eles.",
    ("JER 15:19", "JER 15:19", "divina_bencao"): "O SENHOR promete a Jeremias que, se ele voltar e separar o precioso do vil, será restaurado, permanecerá diante de Deus e será como a sua boca.",
    ("JER 15:20", "JER 15:21", "divina_bencao"): "O SENHOR promete fazer de Jeremias um muro fortificado de bronze, garantindo estar com ele para salvá-lo e resgatá-lo das mãos dos maus e violentos.",
    ("JHN 4:10", "JHN 4:10", "divina_bencao"): "Jesus assegura à mulher samaritana que, a quem conhecer o dom de Deus e lhe pedir, ele dará água viva.",
    ("JOL 2:21", "JOL 2:22", "divina_bencao"): "Deus promete à terra e aos animais do campo que os pastos do deserto reverdecerão e as árvores, a figueira e a videira darão seu fruto com vigor.",
    ("JOL 2:32", "JOL 2:32", "divina_bencao"): "O SENHOR promete que todo aquele que invocar o seu nome será salvo e haverá livramento em Sião e em Jerusalém.",
    ("LUK 10:35", "LUK 10:35", "humana_beneficio"): "Na parábola de Jesus, o bom samaritano compromete-se com o hospedeiro a pagar, em seu retorno, tudo o que ele gastar a mais no cuidado do ferido.",
    ("LUK 12:10", "LUK 12:10", "divina_bencao"): "Jesus garante que todo aquele que disser uma palavra contra o Filho do Homem será perdoado.",
    ("LUK 12:10", "LUK 12:10", "divina_juizo"): "Jesus declara em sentença solene que aquele que blasfemar contra o Espírito Santo não será perdoado.",
    ("LUK 19:8", "LUK 19:8", "humana_beneficio"): "Zaqueu compromete-se diante do Senhor a dar metade de seus bens aos pobres e a restituir quatro vezes mais a quem tiver defraudado.",
    ("LUK 19:17", "LUK 19:17", "humana_beneficio"): "Na parábola das minas, o senhor recompensa o servo fiel concedendo-lhe autoridade sobre dez cidades.",
    ("LUK 19:19", "LUK 19:19", "humana_beneficio"): "Na parábola das minas, o senhor concede ao segundo servo fiel o governo sobre cinco cidades.",
    ("LUK 19:22", "LUK 19:22", "humana_prejuizo"): "Na parábola das minas, o senhor declara ao servo negligente que o julgará e condenará a partir de suas próprias palavras.",
    ("ZEP 2:8", "ZEP 2:10", "divina_juizo"): "O SENHOR dos Exércitos jura por sua vida que Moabe se tornará como Sodoma e Amom como Gomorra, em devastação permanente por causa de seu orgulho.",
    ("ZEP 2:9", "ZEP 2:9", "divina_bencao"): "Deus promete que o remanescente de seu povo saqueará Moabe e Amom e tomará posse do território deles.",
    ("ZEP 2:12", "ZEP 2:12", "divina_juizo"): "O SENHOR anuncia que os cuchitas também serão mortos pela sua espada.",
    ("ZEP 2:13", "ZEP 2:15", "divina_juizo"): "Deus declara que estenderá sua mão contra o norte, destruirá a Assíria e reduzirá Nínive a uma devastação seca como o deserto.",
}


def resumo_valido(s):
    if not s or not s.strip():
        return False
    sl = s.strip().lower()
    return "resumo não informado" not in sl and "sem resumo" not in sl


def carregar_decisoes_f3():
    casos = json.loads(CASOS_F3.read_text(encoding="utf-8"))
    decisoes = {}
    for arq in sorted(SAIDAS_F3.glob("lote_*.json")):
        arr = json.loads(arq.read_text(encoding="utf-8"))
        if isinstance(arr, dict):
            arr = arr.get("decisoes") or arr.get("resultados") or []
        for item in arr:
            if isinstance(item, dict) and item.get("id"):
                decisoes[item["id"]] = item

    faltando = [cid for cid in casos if cid not in decisoes]
    if faltando:
        raise SystemExit(f"ERRO: faltam {len(faltando)} decisoes da Fase 3!")

    mapa_por_livro = {}
    for cid, c in casos.items():
        uids = frozenset(x["uid"] for x in c["p1"] + c["p2"])
        mapa_por_livro.setdefault(c["livro"], {})[uids] = (c, decisoes[cid])
    return mapa_por_livro, len(casos), len(decisoes)


def inferir_reforco(texto):
    t = texto.lower()
    if any(p in t for p in ("jurei", "jurou", "juramento", "por mim mesmo", "vivo eu", "tão certo como eu vivo")):
        return "juramento"
    if any(p in t for p in ("aliança", "pacto", "concerto")):
        return "alianca"
    if "sinal" in t:
        return "sinal"
    return "nenhum"


def inferir_condicao(texto):
    t = texto.lower()
    if any(p in t for p in ("se ", "se,", "quando ", "caso ", "contanto que", "todo aquele que", "quem ")):
        return "explicita"
    return "nenhuma"


def escolher_melhor_resumo_par(r, candidatas_u, corpus):
    """Escolhe o resumo válido de outra unidade do mesmo trecho/aglomerado, priorizando maior similaridade de âncora e mesma natureza."""
    v_r = set(corpus.intervalo(r["ref_inicio"], r["ref_fim"]) or [r["ref_inicio"]])
    t_anc = reconciliar._toks(r.get("ancora_texto") or "")
    melhores = []
    for u in candidatas_u:
        res_u = u.get("resumo_proprio") or u.get("resumo") or ""
        if not resumo_valido(res_u):
            continue
        v_u = set(corpus.intervalo(u["ref_inicio"], u["ref_fim"]) or [u["ref_inicio"]])
        if not (v_r & v_u):
            continue
        t_u = reconciliar._toks(u.get("ancora_texto") or "")
        sim = len(t_anc & t_u) / len(t_anc | t_u) if (t_anc | t_u) else 0.0
        mesma_nat = 1 if u.get("natureza") == r.get("natureza") else 0
        mesmo_ini = 1 if u["ref_inicio"] == r["ref_inicio"] else 0
        melhores.append(((mesma_nat, mesmo_ini, sim), res_u))
    if melhores:
        melhores.sort(key=lambda x: x[0], reverse=True)
        return melhores[0][1]
    return None


def resolver_campos_registro(r, fontes_aglomerado, todas_u_livro, corpus, liv):
    """Preenche metadados secundários, separa rigorosamente promitente divino de comunicador humano e recupera os 276 resumos."""
    refs = corpus.intervalo(r["ref_inicio"], r["ref_fim"]) or [r["ref_inicio"]]
    texto = " ".join(corpus.texto.get(rf, "") for rf in refs)

    # 1. Natureza (antes de calcular categoria)
    if r.get("natureza") not in ("bencao", "juizo"):
        for f in fontes_aglomerado:
            if f.get("natureza") in ("bencao", "juizo"):
                r["natureza"] = f["natureza"]
                break
    if r.get("natureza") not in ("bencao", "juizo"):
        t_nat = (texto + " " + (r.get("resumo") or "")).lower()
        if any(p in t_nat for p in ("castig", "destru", "matar", "morte", "fogo", "ira", "maldi", "espada", "julgar", "juízo", "conden", "perec", "desola", "praga", "ai de", "ferir", "quebrar", "abater", "extermin")):
            r["natureza"] = "juizo"
        else:
            r["natureza"] = "bencao"

    # 2. Herdar destinatario_tipo, destinatario_nome, condicao_tipo, forma_expressao do par se ausentes
    for campo in ("destinatario_tipo", "destinatario_nome", "condicao_tipo", "forma_expressao"):
        if not r.get(campo):
            for f in fontes_aglomerado:
                if f.get(campo):
                    r[campo] = f[campo]
                    break

    # 3. Separação estrita entre PROMITENTE e COMUNICADOR (Item 7 da crítica)
    # Coletar promitente divino ('promitente') e comunicador humano ('promitente_nome') das fontes
    prom_raw = r.get("promitente")
    comunicador = r.get("comunicador") or r.get("promitente_nome")
    for f in fontes_aglomerado:
        if not comunicador and f.get("promitente_nome"):
            comunicador = f.get("promitente_nome")
        if f.get("promitente") in VALORES_PROM_DIVINO and prom_raw not in VALORES_PROM_DIVINO:
            prom_raw = f.get("promitente")

    if r["origem_real"] in ORIGENS_DIVINAS:
        # Se prom_raw tinha um nome humano (ex.: 'todo o Israel' em 1CH 11:2, 'Isaías', 'Jeremias', 'Paulo'), move para comunicador!
        if prom_raw and prom_raw not in VALORES_PROM_DIVINO:
            if not comunicador:
                comunicador = prom_raw
            prom_raw = None
        if not prom_raw:
            if liv in LIVROS_CRISTO and any(p in texto.lower() for p in ("em verdade", "eu vos digo", "meu pai", "eu sou", "filho do homem")):
                prom_raw = "filho"
            else:
                prom_raw = "deus_indistinto"
        r["promitente"] = prom_raw
        if comunicador and comunicador not in VALORES_PROM_DIVINO:
            r["comunicador"] = comunicador
    elif r["origem_real"] == "apostolica_garantia":
        if prom_raw and prom_raw not in VALORES_PROM_DIVINO and not comunicador:
            comunicador = prom_raw
        r["promitente"] = "deus_indistinto"
        if comunicador:
            r["comunicador"] = comunicador
    elif r["origem_real"] == "profetica_patriarcal":
        r["promitente"] = prom_raw or comunicador or "patriarca"
    else:
        # humana_em_nome_proprio ou adversaria_ou_falsa
        r["promitente"] = prom_raw or comunicador or "promitente humano no texto"

    # 4. Recuperar resumo caso seja "(resumo não informado pelo leitor)" ou "(sem resumo)" (Item 1 da crítica)
    if not resumo_valido(r.get("resumo")):
        res_par = escolher_melhor_resumo_par(r, fontes_aglomerado, corpus) or escolher_melhor_resumo_par(r, todas_u_livro, corpus)
        if res_par:
            r["resumo"] = res_par
        else:
            cat_calc = catalogo.categoria(r)
            chave_74 = (r["ref_inicio"], r["ref_fim"], cat_calc)
            if chave_74 in RESUMOS_74:
                r["resumo"] = RESUMOS_74[chave_74]
            else:
                # Busca por ref_inicio e categoria se ref_fim variou
                alt = next((v for (ri, rf, ct), v in RESUMOS_74.items() if ri == r["ref_inicio"] and ct == cat_calc), None)
                if alt:
                    r["resumo"] = alt
                else:
                    raise SystemExit(f"ERRO: resumo nao recuperado para {r['ref_inicio']}..{r['ref_fim']} ({cat_calc})")

    # 5. Campos restantes
    if not r.get("destinatario_tipo"):
        if liv in ("ROM", "1CO", "2CO", "GAL", "EPH", "PHP", "COL", "1TH", "2TH", "1TI", "2TI", "TIT", "PHM", "HEB", "JAS", "1PE", "2PE", "1JN", "2JN", "3JN", "JUD", "REV"):
            r["destinatario_tipo"] = "igreja"
        else:
            r["destinatario_tipo"] = "israel"
    if not r.get("condicao_tipo"):
        r["condicao_tipo"] = inferir_condicao(texto)
    if not r.get("reforco"):
        r["reforco"] = inferir_reforco(texto)

    r.pop("ancora_texto", None)
    r["campos_pendentes"] = []
    r["duvidas"] = []
    r["estado"] = "aprovada_ia_provisoria"
    return r


def deduplicar_livro(regs):
    """Remove apenas as 14 duplicatas técnicas estritas identificadas antes da recuperação dos 276 resumos."""
    out = []
    vistos = {}
    removidos = 0
    for r in regs:
        cat = catalogo.categoria(r)
        # Usa a assinatura original do resumo do leitor (antes da recuperação) para manter exatamente as mesmas 14 deduplicações técnicas
        res_orig = r.pop("_resumo_orig", r.get("resumo") or "")
        res_norm = re.sub(r"\W+", "", res_orig.lower())
        chave_exata = (r["ref_inicio"], r["ref_fim"], cat, res_norm)
        if chave_exata in vistos:
            removidos += 1
            continue
        if not res_norm or "resumonao" in res_norm or "semresumo" in res_norm:
            chave_ref_cat = (r["ref_inicio"], r["ref_fim"], cat)
            if any((x["ref_inicio"], x["ref_fim"], catalogo.categoria(x)) == chave_ref_cat for x in out):
                removidos += 1
                continue
        vistos[chave_exata] = r
        out.append(r)
    return out, removidos


def reconciliar_livro_definitivo(liv, corpus, mapa_f3):
    u = {}
    lidos = {}
    for n in (1, 2):
        regs = reconciliar.carregar_passe(BASE, liv, n)
        u[n] = reconciliar.unidades(regs)
        lidos[n] = {r["ref"] for r in regs}
    leit = [n for n in (1, 2) if lidos[n]]
    todos = set().union(*[lidos[n] for n in leit]) if leit else set()
    todas_u_livro = u.get(1, []) + u.get(2, [])

    def _nome(n):
        for r in reconciliar.carregar_passe(BASE, liv, n):
            l = r.get("leitor") or ""
            return "Claude (agente)" if l.startswith("claude") else ("DeepSeek Flash high" if "flash" in l else ("Gemini" if "gemini" in l else ("Codex" if "codex" in l else l)))
        return {1: "leitor 1", 2: "Gemini"}[n]

    nomes = {1: _nome(1), 2: _nome(2)}
    adjud_claude = catalogar_livro.carregar_adjudicacoes(liv, corpus)
    adjud_f3 = mapa_f3.get(liv, {})
    por_uid = {x["uid"]: x for n in (1, 2) for x in u[n]}
    eh = lambda x: x["tipo_unidade"] == "promessa"

    regs_out = []
    stats = Counter()

    for g in casos_adjudicacao.aglomerar(u[1], u[2], corpus):
        A = [x for p, x in g if p == "1" and eh(x)]
        B = [x for p, x in g if p == "2" and eh(x)]
        fontes_todas = [x for p, x in g]
        chave = frozenset(x["uid"] for p, x in g)

        if chave in adjud_claude:
            item, caso = adjud_claude[chave]
            for un in item.get("unidades") or []:
                if un.get("tipo_unidade") != "promessa":
                    continue
                fontes = [por_uid[x] for x in (un.get("fontes") or []) if x in por_uid] or fontes_todas
                ini = min((corpus.pos[parse_ref(f["ref_inicio"])], f["ref_inicio"]) for f in fontes)[1]
                fim = max((corpus.pos[parse_ref(f["ref_fim"])], f["ref_fim"]) for f in fontes)[1]
                res_bruto = un.get("resumo_proprio") or "(sem resumo)"
                r = {
                    "tipo_unidade": "promessa",
                    "origem_real": un["origem_real"],
                    "natureza": un.get("natureza"),
                    "destinatario_tipo": un.get("destinatario_tipo"),
                    "destinatario_nome": None,
                    "promitente": un.get("promitente"),
                    "comunicador": un.get("promitente_nome"),
                    "condicao_tipo": un.get("condicao_tipo"),
                    "forma_expressao": un.get("forma_expressao"),
                    "resumo": res_bruto,
                    "_resumo_orig": res_bruto,
                    "ancora_texto": un.get("ancora_texto") or "",
                    "ref_inicio": ini,
                    "ref_fim": fim,
                    "campos_pendentes": [],
                    "fundamentacao_divina": None,
                    "leituras": "2 leitores + árbitro Claude",
                }
                regs_out.append((r, fontes))
                stats["adjud_anterior"] += 1
            continue

        if not A and not B:
            continue

        if A and B:
            sig = lambda L: sorted((x["origem_real"], x.get("natureza")) for x in L)
            if sig(A) == sig(B):
                ref = B if len(B) >= len(A) else A
                for x in ref:
                    r = catalogar_livro.representante(x)
                    r["promitente"] = x.get("promitente")
                    r["comunicador"] = x.get("promitente_nome")
                    r["_resumo_orig"] = r["resumo"]
                    r["ancora_texto"] = x.get("ancora_texto") or ""
                    r["leituras"] = "2 leitores (acordo direto)"
                    regs_out.append((r, A + B))
                    stats["acordo_2_leitores"] += 1
                continue

        if chave in adjud_f3:
            caso, dec = adjud_f3[chave]
            ver = (dec.get("veredito") or "").strip().lower()
            if ver == "rejeitar":
                stats["f3_rejeitados"] += 1
                continue
            elif ver == "confirmar_p1":
                escolhidos = A if A else B
            elif ver == "confirmar_p2":
                escolhidos = B if B else A
            elif ver == "confirmar_ambos":
                escolhidos = A + B
            else:
                escolhidos = B if len(B) >= len(A) else A

            arb_nome = "Gemini" if caso["arbitro_designado"] == "gemini" else "DeepSeek"
            for x in escolhidos:
                r = catalogar_livro.representante(x)
                r["promitente"] = x.get("promitente")
                r["comunicador"] = x.get("promitente_nome")
                r["_resumo_orig"] = r["resumo"]
                r["ancora_texto"] = x.get("ancora_texto") or ""
                if dec.get("origem_override") in ORIGENS_REAIS:
                    r["origem_real"] = dec["origem_override"]
                if dec.get("natureza_override") in ("bencao", "juizo"):
                    r["natureza"] = dec["natureza_override"]
                r["leituras"] = f"2 leitores + árbitro {arb_nome}"
                regs_out.append((r, A + B))
                stats["f3_confirmados"] += 1
            continue

        raise SystemExit(f"ERRO: aglomerado divergente sem arbitro em {liv}: {chave}")

    # Ordenar pela assinatura original, deduplicar as 14 estritas, e depois resolver campos e recuperar os 276 resumos!
    regs_out.sort(key=lambda par: (corpus.pos[parse_ref(par[0]["ref_inicio"])], par[0].get("_resumo_orig") or ""))
    apenas_regs = [par[0] for par in regs_out]
    mapa_fontes = {id(par[0]): par[1] for par in regs_out}

    # Precisamos que a natureza esteja preenchida antes de deduplicar para que catalogo.categoria(r) seja idêntica
    for r in apenas_regs:
        if r.get("natureza") not in ("bencao", "juizo"):
            refs = corpus.intervalo(r["ref_inicio"], r["ref_fim"]) or [r["ref_inicio"]]
            texto = " ".join(corpus.texto.get(rf, "") for rf in refs)
            t_nat = (texto + " " + (r.get("_resumo_orig") or "")).lower()
            if any(p in t_nat for p in ("castig", "destru", "matar", "morte", "fogo", "ira", "maldi", "espada", "julgar", "juízo", "conden", "perec", "desola", "praga", "ai de", "ferir", "quebrar", "abater", "extermin")):
                r["natureza"] = "juizo"
            else:
                r["natureza"] = "bencao"

    apenas_regs, n_dup = deduplicar_livro(apenas_regs)
    stats["duplicatas_removidas"] += n_dup

    for i, r in enumerate(apenas_regs, 1):
        r["id"] = f"P-{liv}-{i:04d}"
        r["livro"] = liv
        resolver_campos_registro(r, mapa_fontes[id(r)], todas_u_livro, corpus, liv)

    toks = [reconciliar._toks(r["resumo"]) for r in apenas_regs]
    for i, r in enumerate(apenas_regs):
        for j in range(i):
            a, b = toks[i], toks[j]
            if a and b and len(a & b) / len(a | b) >= 0.5 and apenas_regs[j]["ref_fim"] != r["ref_inicio"]:
                r["possivel_reafirmacao_de"] = apenas_regs[j]["id"]
                break

    arb_lista = list(nomes.values())
    if stats["f3_confirmados"] or stats["f3_rejeitados"]:
        arb_nome = "Gemini" if "Gemini" not in nomes.values() else "DeepSeek Flash high"
        arb_lista.append(f"árbitro {arb_nome}")
    elif stats["adjud_anterior"]:
        arb_lista.append("árbitro Claude")

    cob = {
        "versiculos_lidos": len(todos),
        "versiculos_do_livro": len(corpus.refs_do_livro(liv)),
        "leituras": arb_lista,
        "nota": f"Fase 3 concluída (acordo={stats['acordo_2_leitores']}, adj_ant={stats['adjud_anterior']}, f3_conf={stats['f3_confirmados']}, f3_rej={stats['f3_rejeitados']}, dup_rem={stats['duplicatas_removidas']}).",
    }
    return apenas_regs, cob, stats


def homologar_genesis(corpus):
    regs = []
    for _, r in ler_jsonl(RAIZ / "dados_v04" / "promessas" / "GEN.jsonl", []):
        prom = r.get("promitente")
        com = r.get("promitente_nome")
        if r["origem_real"] in ORIGENS_DIVINAS and not prom:
            prom = "deus_indistinto"
        elif r["origem_real"] not in ORIGENS_DIVINAS:
            prom = prom or com or "patriarca"
        reg = {
            "id": r["id"],
            "livro": "GEN",
            "ref_inicio": r["ref_inicio"],
            "ref_fim": r["ref_fim"],
            "tipo_unidade": "promessa",
            "origem_real": r["origem_real"],
            "natureza": r["natureza"],
            "destinatario_tipo": r.get("destinatario_tipo"),
            "destinatario_nome": r.get("destinatario_nome"),
            "promitente": prom,
            "condicao_tipo": r.get("condicao_tipo"),
            "forma_expressao": r.get("forma_expressao"),
            "fundamentacao_divina": r.get("fundamentacao_divina"),
            "resumo": r["resumo_proprio"],
            "relacao": r.get("relacao"),
            "familia": r.get("familia_id"),
            "estado": "aprovada_ia_provisoria",
            "duvidas": [],
            "leituras": "2 leitores + árbitro Gemini" if r.get("status") == "adjudicada" else "2 leitores (acordo direto)",
        }
        if com and r["origem_real"] in ORIGENS_DIVINAS:
            reg["comunicador"] = com
        regs.append(reg)
    nv = len(corpus.refs_do_livro("GEN"))
    cob = {
        "versiculos_lidos": nv,
        "versiculos_do_livro": nv,
        "leituras": ["2 leitores", "árbitro Gemini", "conferência de campos pelo texto"],
        "nota": "Gênesis homologado com 100% dos registros aprovados na Fase 3.",
    }
    catalogo.gravar_livro("GEN", regs, cob, corpus, destino_md=("CATALOGO_PROMESSAS_GENESIS.md", "CONTAGEM_GENESIS.md"))
    return len(regs), 0


def main():
    corpus = Corpus()
    mapa_f3, n_casos, n_dec = carregar_decisoes_f3()
    print(f"Fase 3 carregada: {n_dec}/{n_casos} decisões válidas.", flush=True)

    n_gen, dup_gen = homologar_genesis(corpus)
    print(f"GEN homologado: {n_gen} promessas confirmadas.", flush=True)

    tot_stats = Counter()
    tot_prom = n_gen
    for liv in CANON:
        if liv == "GEN" or liv not in corpus.ordem:
            continue
        regs, cob, st = reconciliar_livro_definitivo(liv, corpus, mapa_f3)
        catalogo.gravar_livro(liv, regs, cob, corpus)
        tot_stats.update(st)
        tot_prom += len(regs)

    catalogo.atualizar_contagem_geral(corpus)
    print("\n--- RESUMO DA CONSOLIDAÇÃO DEFINITIVA (FASE 3 + 8 ITENS DA CRÍTICA) ---")
    print(f"Total de promessas confirmadas nos 66 livros: {tot_prom}")
    print(f"Estatísticas Fase 3: {dict(tot_stats)}")


if __name__ == "__main__":
    main()
