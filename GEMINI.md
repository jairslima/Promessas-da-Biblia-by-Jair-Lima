# GEMINI.md: Resumo Técnico de Continuidade — Promessas da Bíblia by Jair Lima (v1.0.0)

## 1. Visão Geral e Indicadores Finais Homologados
Repositório científico oficial da pesquisa **Promessas da Bíblia by Jair Lima**, que examinou integralmente os **66 livros, 1.189 capítulos e 31.104 versículos** da *Bíblia Almeida Livre* (CC BY-ND 4.0) em três fases (duas leituras independentes cegas e uma terceira fase de arbitragem exegética por terceiro modelo independente sobre todos os 1.808 casos divergentes).

* **Unidades candidatas preliminares (Fases 1 e 2):** 3.609
* **Unidades promissórias confirmadas (Total Final):** **3.224** (zero candidatos pendentes)
  * Confirmadas por acordo direto (Fases 1 e 2): **1.211** (37,6%)
  * Confirmadas por arbitragem independente (Fase 3): **2.013** (62,4%)
* **Conciliação aritmética exata (`3.609` $\rightarrow$ `3.224`):**
  `3.609 (preliminares) - 334 (unidades nos 332 casos rejeitados pelo árbitro) - 37 (subdivisões consolidadas por granularidade nos casos confirmados) - 14 (duplicatas técnicas estritas) = 3.224 unidades confirmadas`.
* **Promessas distintas estimadas (Jaccard $\tau = 0,45$, após recuperação integral dos 276 resumos):** **2.945** (faixa de sensibilidade: `2.729` em $\tau=0,35$ a `3.096` em $\tau=0,65$; projeção corrigida pela revocação de $0,84$: **3.506**).
* **Versículos associados a promessas:** **4.373** (**14,1%** dos 31.104 versículos da Bíblia).
* **Indicador Principal — Bênção Divina:** **1.622 unidades confirmadas** e **1.481 promessas distintas** (até `1.763` com correção pela revocação de $0,84$).

## 2. Distribuição nas Dez Categorias Taxonômicas
1. `divina_bencao` (Bênção divina): **1.448** (44,91%)
2. `divina_juizo` (Juízo divino): **952** (29,53%)
3. `humana_beneficio` (Compromisso humano de benefício): **432** (13,40%)
4. `apostolica_garantia_bencao` (Garantia apostólica de bênção): **161** (4,99%)
5. `humana_prejuizo` (Compromisso humano de prejuízo): **82** (2,54%)
6. `divina_sentenca` (Sentença divina): **73** (2,26%)
7. `apostolica_garantia_juizo` (Garantia apostólica de juízo): **37** (1,15%)
8. `adversaria_ou_falsa` (Promessa adversária ou falsa): **23** (0,71%)
9. `patriarcal_bencao` (Bênção patriarcal): **13** (0,40%)
10. `patriarcal_juizo` (Juízo patriarcal): **3** (0,09%)

## 3. Separação entre Promitente e Comunicador Humano
Em todas as 2.473 unidades de origem divina (`divina_direta` e `divina_relatada_por_humano`) e nas 198 de `apostolica_garantia`, o campo `promitente` identifica exclusivamente o autor divino do compromisso (`pai`, `filho`, `espirito`, `deus_indistinto` ou `mensageiro_autorizado`), enquanto o profeta, apóstolo ou personagem humano que relata ou invoca a palavra está registrado no campo `comunicador` (1.487 registros, como em 1Cr 11.2).
