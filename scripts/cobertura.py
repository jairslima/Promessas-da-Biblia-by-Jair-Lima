"""Controle A4 (cobertura por versículo) e A13 (isolamento dos passes).

Para cada arquivo `varredura/<LIV>.passe<N>.jsonl`:
  * o conjunto de versículos é EXATAMENTE o do livro no corpus (sem faltar, sobrar ou repetir);
  * o campo `passe` e o leitor são constantes e coerentes com o nome do arquivo;
  * toda unidade iniciada cobre um intervalo cujos versículos estão marcados (com_unidade ou parte_de_unidade);
  * todo `parte_de` aponta para unidade existente cujo intervalo contém o versículo;
  * (A13) se existem os dois passes do mesmo livro, os leitores são diferentes.

Uso: python -I cobertura.py [--base dados] [--livro GEN]
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_promessas import *  # noqa: F401,F403

RE_ARQ = re.compile(r"^([0-9A-Z]{3})\.passe([12])\.jsonl$")


def verificar_arquivo(f: Path, corpus: Corpus, problemas):
    m = RE_ARQ.match(f.name)
    if not m:
        problemas.append(Problema("A4", f.name, 0, "-", "nome deve ser <LIV>.passe1|2.jsonl"))
        return None
    liv, passe = m.group(1), int(m.group(2))
    regs = ler_jsonl(f, problemas)
    esperado = corpus.refs_do_livro(liv)
    if not esperado:
        problemas.append(Problema("A4", f.name, 0, "-", f"livro {liv} inexistente no corpus"))
        return None
    cont = Counter(r.get("ref") for _, r in regs)
    dup = sorted(k for k, n in cont.items() if n > 1)
    falt = [r for r in esperado if r not in cont]
    sobra = sorted(k for k in cont if k not in set(esperado))
    if falt:
        problemas.append(Problema("A4", f.name, 0, liv, f"{len(falt)} versículo(s) sem estado: {falt[:8]}"))
    if dup:
        problemas.append(Problema("A4", f.name, 0, liv, f"versículos repetidos: {dup[:8]}"))
    if sobra:
        problemas.append(Problema("A4", f.name, 0, liv, f"versículos fora do livro ou inexistentes: {sobra[:8]}"))
    leitores = {r.get("leitor") for _, r in regs}
    if len(leitores) > 1:
        problemas.append(Problema("A13", f.name, 0, liv, f"mais de um leitor no mesmo passe: {sorted(map(str, leitores))}"))
    for i, r in regs:
        if r.get("passe") != passe:
            problemas.append(Problema("A4", f.name, i, r.get("ref", "?"), f"campo passe={r.get('passe')} difere do arquivo ({passe})"))
    # intervalos das unidades
    marcadas = {}
    intervalos = {}
    for i, r in regs:
        for u in r.get("unidades", []) or []:
            refs = corpus.intervalo(u.get("ref_inicio"), u.get("ref_fim"))
            if refs is None:
                problemas.append(Problema("A2", f.name, i, u.get("uid", "?"), "intervalo da unidade inválido"))
                continue
            intervalos[u.get("uid")] = refs
            for x in refs:
                marcadas.setdefault(x, set()).add(u.get("uid"))
    estado = {r.get("ref"): (i, r) for i, r in regs}
    for uid, refs in intervalos.items():
        for x in refs:
            if x in estado and estado[x][1].get("estado") == "sem_unidade":
                problemas.append(Problema("A4", f.name, estado[x][0], x, f"versículo marcado sem_unidade mas coberto pela unidade {uid}"))
            elif x in estado and x != refs[0]:
                r = estado[x][1]
                if uid not in (r.get("parte_de") or []):
                    problemas.append(Problema("A4", f.name, estado[x][0], x, f"unidade {uid} cobre este versículo mas parte_de não a lista"))
    for ref, (i, r) in estado.items():
        for uid in r.get("parte_de") or []:
            if uid not in intervalos or ref not in intervalos[uid]:
                problemas.append(Problema("A4", f.name, i, ref, f"parte_de aponta para unidade inexistente ou que não cobre o versículo: {uid}"))
    return liv, passe, (next(iter(leitores)) if len(leitores) == 1 else None)


def verificar(base: Path, corpus: Corpus, livro=None):
    problemas = []
    pasta = Path(base) / "varredura"
    achados = {}
    for f in sorted(pasta.glob("*.jsonl")) if pasta.exists() else []:
        if livro and not f.name.startswith(livro + "."):
            continue
        r = verificar_arquivo(f, corpus, problemas)
        if r:
            achados.setdefault(r[0], {})[r[1]] = r[2]
    if livro:
        for n in (1, 2):
            if not (pasta / f"{livro}.passe{n}.jsonl").exists():
                problemas.append(Problema("A4", f"{livro}.passe{n}.jsonl", 0, livro, "passe ausente (ainda não recebido)"))
    for liv, passes in achados.items():
        if 1 in passes and 2 in passes and passes[1] is not None and passes[1] == passes[2]:
            problemas.append(Problema("A13", f"{liv}.passe*.jsonl", 0, liv, f"passes 1 e 2 com o mesmo leitor ({passes[1]}): sem independência"))
    return problemas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=str(RAIZ / "dados"))
    ap.add_argument("--livro")
    a = ap.parse_args()
    probs = verificar(Path(a.base), Corpus(), a.livro)
    for p in probs:
        print(p)
    print(f"cobertura: {len(probs)} problema(s)")
    return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main())
