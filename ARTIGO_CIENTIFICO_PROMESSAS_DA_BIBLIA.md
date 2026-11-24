# Quantas promessas existem na Bíblia? Uma análise computacional e exegética dos 66 livros do cânon protestante

# How Many Promises Are in the Bible? A Computational and Exegetical Analysis of the 66 Books of the Protestant Canon

**Autor / Author:** Jair Lima  
**Afiliação / Affiliation:** Lima Editora do Brasil; Assembleia de Deus de Três Coroas, Rio Grande do Sul, Brasil  
**Data / Date:** 24 de novembro de 2026  
**Versão do Dataset / Dataset Version:** v1.0.0 (`Promessas-da-Biblia-by-Jair-Lima`)  
**Status Editorial:** Preprint / Relatório Técnico-Científico de Pesquisa (ainda não submetido à revisão acadêmica por pares / *Preprint technical report, not yet peer-reviewed*)

---

## Resumo

A pergunta sobre quantas promessas existem na Bíblia produziu, ao longo dos últimos três séculos, estimativas amplamente divergentes — variando de coletâneas devocionais seletivas no século XVIII ao levantamento manual de Everek R. Storms na década de 1950 (8.810 promessas totais, das quais 7.487 atribuídas a Deus) e a lendas populares de até 30.000 promessas. Todavia, nenhuma dessas contagens históricas disponibilizou um banco de dados aberto, auditável versículo a versículo, fundamentado em uma definição operacional comissiva explícita e submetido a verificação cruzada independente. Este artigo apresenta a metodologia e os resultados de uma investigação computacional e exegética integral dos **66 livros, 1.189 capítulos e 31.104 versículos** do cânon protestante, tendo como corpus textual a *Bíblia Almeida Livre* (CC BY-ND 4.0). O protocolo foi estruturado em **três fases**: (1) primeira leitura integral independente; (2) segunda leitura integral cega por modelo distinto; e (3) arbitragem exegética independente por um terceiro agente sobre todos os 1.808 casos de divergência ou de identificação unilateral, complementada pela separação formal entre *promitente* e *comunicador humano* e pelo agrupamento lexical por índice de similaridade de Jaccard. Das **3.609 unidades candidatas** inicialmente levantadas nas duas primeiras fases, o árbitro da Fase 3 rejeitou **332 casos** de falsos positivos (334 unidades preliminares, como mandamentos sem garantia de benefício, votos humanos meramente desiderativos e relatos consumados sem projeção futura), consolidou **37 subdivisões excedentes** em 34 casos de granularidade divergente e removeu **14 duplicatas técnicas estritas**, estabelecendo o número final confirmado de **3.224 unidades promissórias** (**1.211** por acordo direto nas Fases 1 e 2 e **2.013** por arbitragem na Fase 3; zero candidatos pendentes), distribuídas em **4.373 versículos** (**14,1%** do corpus bíblico). Após a recuperação integral de 276 resumos de unidades lidas em modo tolerante, o agrupamento lexical no limiar padrão de Jaccard ($\tau = 0,45$) identificou **2.945 promessas distintas** (faixa de sensibilidade de 2.729 em $\tau = 0,35$ a 3.096 em $\tau = 0,65$; ou **3.506** na projeção corrigida pela taxa empírica de revocação de $0,84$). Para o indicador principal das **promessas divinas de bênção** (bênção divina, garantia apostólica de bênção e bênção patriarcal), confirmaram-se **1.622 unidades** (**1.481 promessas distintas**). Conclui-se que a cifra tradicional de 7.000 a 8.000 promessas não se confirma sob critérios comissivos estritos que separem máximas sapienciais, declarações doutrinárias em terceira pessoa e votos devocionais humanos, situando-se o universo promissório verificável das Escrituras na ordem de **3,2 mil ocorrências textuais** e **2,9 mil promessas distintas**.

**Palavras-chave:** Promessas bíblicas; Teologia computacional; Exegese de corpus; Teoria dos atos de fala; Arbitragem por modelos de linguagem; Bíblia Almeida Livre.

---

## Abstract

The question of how many promises exist in the Bible has yielded widely divergent estimates over the past three centuries, ranging from selective eighteenth-century devotional anthologies to Everek R. Storms's mid-1950s manual tally (8,810 total promises, including 7,487 divine promises to humankind) and popular claims of up to 30,000 promises. Yet none of these historical counts produced an open, verse-by-verse auditable dataset grounded in an explicit commissive operational definition and verified through independent cross-arbitration. This study presents the methodology and results of an exhaustive computational and exegetical investigation across all **66 books, 1,189 chapters, and 31,104 verses** of the Protestant canon, using the *Bíblia Almeida Livre* (CC BY-ND 4.0) as the reference corpus. The research protocol operated in **three phases**: (1) an initial full-canon reading; (2) a blind second reading by an independent model; and (3) third-agent exegetical arbitration across all 1,808 cases of inter-reader divergence or single-reader identification, combined with a formal distinction between *promisor* and *human communicator* and lexical clustering via Jaccard similarity. Out of **3,609 candidate units** initially flagged in Phases 1 and 2, Phase 3 arbitration rejected **332 false-positive cases** (334 preliminary units, such as commands without benefit guarantees, purely optative human wishes, and past historical narratives without future projection), consolidated **37 excess subdivisions** across 34 granularity-divergent cases, and removed **14 strict technical duplicates**, establishing a final confirmed count of **3,224 promissory units** (**1,211** by direct agreement and **2,013** by independent arbitration; zero pending candidates) spanning **4,373 verses** (**14.1%** of the biblical corpus). Following the complete recovery of 276 summaries from tolerant-mode passes, lexical clustering at the standard Jaccard threshold ($\tau = 0.45$) identified **2,945 distinct promises** (sensitivity range from 2,729 at $\tau = 0.35$ to 3,096 at $\tau = 0.65$; or **3,506** when adjusted by the empirical recall rate of $0.84$). For the primary indicator of **divine promises of blessing** (direct/reported divine blessing, apostolic guarantee of blessing, and patriarchal blessing), **1,622 confirmed units** (**1,481 distinct promises**) were established. The findings demonstrate that the traditional 7,000–8,000 figure is not corroborated when commissive speech acts are strictly separated from sapiential maxims, third-person doctrinal assertions, and human devotional vows, placing the verifiable promissory universe of Scripture at approximately **3,200 textual units** and **2,900 distinct promises**.

**Keywords:** Biblical promises; Computational theology; Corpus exegesis; Speech act theory; LLM-as-a-Judge arbitration; Bíblia Almeida Livre.

---

## 1. Introdução

A quantificação de fenômenos textuais nas Escrituras Sagradas possui longa tradição na filologia bíblica, desde a contagem de letras, palavras e versículos pelos massoretas até a moderna linguística de corpus. No entanto, quando o objeto de quantificação passa de unidades morfológicas (palavras ou lemas) para unidades pragmático-teológicas — como as **promessas bíblicas** —, observa-se uma lacuna histórica entre a cultura devocional e a verificação científica.

Durante décadas, manuais homiléticos, obras de divulgação e sermões repetiram que a Bíblia conteria exatamente **8.810 promessas** (ou **7.487 promessas de Deus ao ser humano**), além de estimativas informais que falam em 3.000, 7.000 ou 30.000 promessas. A ausência de um catálogo público que liste cada uma dessas unidades com sua referência bíblica, seu promitente, seu destinatário, sua natureza e seu critério de inclusão impediu, até hoje, que teólogos, exegetas e pesquisadores de humanidades digitais auditassem tais números.

O presente estudo enfrenta esse problema submetendo a totalidade do cânon protestante (66 livros, 1.189 capítulos e 31.104 versículos) a um protocolo formal de identificação, classificação, reconciliação e arbitragem exegética em três fases, disponibilizando publicamente o catálogo completo de **3.224 unidades promissórias confirmadas**, os scripts de agrupamento lexical e a memória de cálculo integral.

---

## 2. Revisão da Literatura

A literatura pertinente ao problema divide-se em três tradições principais:

1. **Antologias Temáticas e Recenseamentos Manuais (Séculos XVIII–XX):**
   Em 1720, o clérigo inglês não conformista Samuel Clarke (1684–1750) publicou *A Collection of the Promises of Scripture, under their Proper Heads* (Londres: J. Clark; 2ª ed. 1738 com prefácio de Isaac Watts), organizando promessas de bênção temporal, espiritual e eterna por categorias pastorais. Em meados da década de 1950, o professor canadense Everek R. Storms (Kitchener, Ontário), insatisfeito com a alegação popular de que existiriam 30.000 promessas na Bíblia, realizou ao longo de dezoito meses, durante sua vigésima sétima leitura bíblica, uma contagem manual que totalizou **8.810 promessas**, subdivididas em **7.487** promessas de Deus ao homem, **991** de um ser humano a outro, **290** do homem a Deus, **28** de anjos, **9** de Satanás, **2** de Deus Pai a Deus Filho, **2** de espíritos malignos ao Senhor e **1** de um homem a um anjo. Em 1962, Herbert Lockyer publicou *All the Promises of the Bible* (Grand Rapids: Zondervan), difundindo amplamente o recenseamento de Storms. Apesar de seu valor histórico, o levantamento de Storms jamais foi publicado como base de dados estruturada versículo a versículo, impossibilitando a verificação independente de suas fronteiras de segmentação.
2. **Teoria dos Atos de Fala e Hermenêutica Bíblica:**
   A filosofia da linguagem ordinária (Austin, 1962; Searle, 1969, 1979) e sua recepção na hermenêutica bíblica (Thiselton, 1992; Vanhoozer, 1998; Briggs, 2001) demonstraram que uma *promessa* pertence à classe dos **atos ilocucionários comissivos** (*commissives*): enunciados cujo propósito ilocucionário é comprometer o falante (*promisor*) com a realização de um curso futuro de ação em relação a um destinatário. Essa distinção teórica é crucial para a exegese de corpus, pois separa atos comissivos de atos *diretivos* (mandamentos e exortações), *assertivos* (relatos históricos consumados, descrições de atributos divinos e afirmações doutrinárias em terceira pessoa) e *expressivos* (orações, desejos e bênçãos votivas humanas).
3. **Teologia Computacional, Corpora Bíblicos e Modelos de Linguagem:**
   Bancos morfossintáticos como o ETCBC/BHSA (Vrije Universiteit Amsterdam), o MACULA Hebrew/Greek Syntax e o STEPBible mapearam com excelência a morfologia e a sintaxe das línguas bíblicas, mas não contêm anotação de atos comissivos em escala canônica. Por outro lado, avanços recentes em Processamento de Linguagem Natural e Grandes Modelos de Linguagem (LLMs) aplicados a corpora religiosos demonstraram a eficácia de arquiteturas de leitura dupla combinadas com arbitragem independente (*LLM-as-a-Judge*) para tarefas complexas de classificação semântica em larga escala, desde que submetidas a validação determinística de esquema e de literalidade textual.

---

## 3. Questão de Pesquisa e Definição Operacional

### 3.1. Questões de Pesquisa
1. Quantas unidades textuais promissórias (atos comissivos) são identificáveis nos 31.104 versículos dos 66 livros do cânon protestante quando submetidas a dupla leitura independente e arbitragem exegética de terceira fase?
2. Como essas unidades se distribuem entre promessas divinas de bênção, promessas divinas de juízo/sentença, garantias apostólicas e patriarcais, compromissos humanos e promessas adversárias?
3. Qual é a estimativa de **promessas distintas** quando se desconta a redundância de reafirmações por agrupamento de similaridade lexical, e por que o resultado diverge da cifra histórica de Everek R. Storms (8.810 / 7.487)?

### 3.2. Definição Operacional de Promessa
Define-se operacionalmente uma **unidade promissória** como toda declaração textual do corpus que:
1. Atribui a um **promitente identificável** (Deus Pai, Filho, Espírito Santo, Deus sem distinção de pessoa, mensageiro autorizado, patriarca, apóstolo, agente humano em nome próprio ou voz adversária) o **compromisso verificável** de realizar, garantir, manter ou executar algo futuro ou continuado;
2. Possui **conteúdo (objeto prometido)** e **destinatário reconhecível** (indivíduo, família/linhagem, Israel, Igreja, grupo específico, nações, humanidade ou criação), além de condição explícita ou contextual quando o próprio texto a estabelece;
3. Distingue a **origem do compromisso** (`origem_real`) da identidade do **comunicador humano** que relata, profetiza ou recorda a palavra.

**Critérios de exclusão (Não Promessas):**
Não são contabilizadas como promessas: (a) mandamentos e imperativos de tarefa sem garantia de benefício; (b) desejos, saudações ou bênçãos votivas humanas sem obrigação assumida pelo falante (ex.: *"O SENHOR te abençoe"*, *"Viva o rei"*); (c) relatos históricos de fatos já consumados sem efeito futuro projetado; (d) princípios sapienciais e máximas gerais de causa e efeito moral sem falante que se obrigue em primeira pessoa (ex.: provérbios gerais); (e) declarações doutrinárias ou confissões teológicas em terceira pessoa sobre atributos ou atos universais de Deus sem estrutura de oráculo promissório (ex.: Ec 12.14; Lm 3.22-32); e (f) votos devocionais do homem a Deus.

---

## 4. Corpus e Metodologia das Três Fases

### 4.1. Corpus Textual
O corpus único utilizado é a **Bíblia Almeida Livre** (Lima, 2026), licenciada sob *Creative Commons Atribuição-SemDerivações 4.0 Internacional* (CC BY-ND 4.0), composta pelos **66 livros** do cânon protestante (39 do Antigo Testamento e 27 do Novo Testamento), **1.189 capítulos** e **31.104 versículos** canônicos auditados por hash criptográfico SHA-256 (`manifesto_sha256.txt`).

### 4.2. Arquitetura das Três Fases
O processamento integral dos 31.104 versículos seguiu um pipeline auditável em três fases:

* **Fase 1 (Primeira Leitura Integral Independente):** Varredura capítulo a capítulo de todos os 66 livros com exigência de mapa posicional completo de versículos (`.`, `U`, `p`, `B`), âncora literal verificada contra o corpus e classificação de tipo de unidade, origem, natureza, promitente, destinatário e condição.
* **Fase 2 (Segunda Leitura Integral Cega):** Segunda varredura completa dos mesmos 1.189 capítulos em ambiente isolado (sem acesso às saídas da Fase 1 nem aos arquivos do projeto) por modelo de família distinta daquela empregada na Fase 1 do respectivo livro.
* **Reconciliação e Pareamento por Aglomerados:** As unidades dos Passes 1 e 2 foram agrupadas por componentes conexos de sobreposição de versículos e similaridade lexical da âncora ($\ge 0,12$). Quando ambos os leitores identificaram promessa com mesma origem e natureza, o registro foi homologado por **acordo direto** (**1.211 unidades**).
* **Fase 3 (Arbitragem Exegética por Terceiro Agente Independente):** Todos os aglomerados em que apenas um leitor havia apontado promessa ou em que houve divergência de origem, natureza ou granularidade — somando **1.808 casos divergentes** nos 56 livros restantes, além das adjudicações de Gênesis, Pentateuco e Evangelhos — foram submetidos a um **terceiro agente árbitro independente** (que não atuou como leitor na Fase 1 nem na Fase 2 daquele livro: Gemini para os 42 livros lidos por Claude + DeepSeek Flash ou Claude + Codex; DeepSeek Flash High para os 14 livros lidos por Claude + Gemini; e Claude para os livros lidos por DeepSeek Flash + Gemini/Codex).
* **Resolução de Metadados, Recuperação de Resumos e Deduplicação:**
  1. Os **276 registros** provenientes de passes em modo tolerante que traziam o marcador `"(resumo não informado pelo leitor)"` tiveram seus resumos integralmente recuperados (202 a partir do segundo leitor do par e 74 redigidos diretamente a partir da âncora e do texto bíblico literal).
  2. Em todos os registros de origem divina ou garantia apostólica, separou-se estritamente o campo `promitente` (sempre divino: `pai`, `filho`, `espirito`, `deus_indistinto` ou `mensageiro_autorizado`) do campo `comunicador` (1.487 registros com identificação do profeta, apóstolo ou personagem bíblico que enuncia ou recorda a promessa, como `"todo o Israel"` em 1Cr 11.2).
  3. Removeram-se **14 duplicatas técnicas estritas** (mesma referência, categoria e objeto prometido).

---

## 5. Resultados

### 5.1. Indicadores Globais e Conciliação Aritmética das Três Fases
A Tabela 1 apresenta a síntese quantitativa oficial e a conciliação exata entre o levantamento preliminar das Fases 1–2 e o fechamento definitivo pós-Fase 3.

**Tabela 1 — Indicadores globais e conciliação aritmética da pesquisa**

| Indicador / Etapa do Pipeline | Quantidade | Proporção / Observação |
| :--- | ---: | :--- |
| Livros bíblicos examinados | 66 | 39 AT / 27 NT (100% do cânon protestante) |
| Capítulos examinados | 1.189 | 100% dos capítulos |
| Versículos lidos e auditados | 31.104 | 100% dos versículos do corpus |
| Unidades candidatas preliminares (Fases 1 e 2) | 3.609 | Levantamento bruto antes da Fase 3 |
| Casos divergentes submetidos ao árbitro (Fase 3) | 1.808 | Continham 1.882 unidades preliminares |
| $( - )$ Unidades em casos rejeitados pelo árbitro (Fase 3) | $-334$ | 332 casos rejeitados (2 casos tinham 2 unidades) |
| $( - )$ Subdivisões consolidadas por granularidade (Fase 3) | $-37$ | 34 casos confirmados na formulação mais coesa |
| $( - )$ Duplicatas técnicas estritas removidas | $-14$ | Mesmo versículo, categoria e objeto prometido |
| **$( = )$ Unidades promissórias confirmadas (Total Final)** | **3.224** | **Zero candidatos ou divergências pendentes** |
| $\quad$ • Confirmadas por acordo direto (Fases 1 e 2) | 1.211 | 37,6% das unidades confirmadas |
| $\quad$ • Confirmadas por arbitragem independente (Fase 3) | 2.013 | 62,4% das unidades confirmadas |
| Versículos únicos cobertos por promessas confirmadas | 4.373 | **14,1%** de todos os versículos da Bíblia |
| **Promessas distintas estimadas (Jaccard $\tau = 0,45$)** | **2.945** | Faixa de sensibilidade: 2.729 ($\tau=0,35$) a 3.096 ($\tau=0,65$) |
| Projeção de distintas corrigida pela revocação ($0,84$) | 3.506 | Estimativa de teto teórico |
| **Indicador Principal — Bênção Divina (Unidades)** | **1.622** | 50,3% de todas as unidades promissórias |
| **Indicador Principal — Bênção Divina (Distintas, $\tau = 0,45$)** | **1.481** | Até 1.763 com correção pela revocação ($0,84$) |

A conciliação matemática entre os **1.808 casos arbitrados** na Fase 3 e os **1.843 resultados de unidades** (`1.511 unidades confirmadas + 332 casos rejeitados`) decorre do fato de que, dos 1.808 casos, **332 casos** foram rejeitados e **1.476 casos** foram confirmados (`332 + 1.476 = 1.808`). Como **32 dos 1.476 casos confirmados** continham múltiplas promessas distintas no mesmo trecho (30 casos com 2 unidades, 1 caso com 3 unidades e 1 caso com 4 unidades, somando $+35$ unidades), os 1.476 casos confirmados geraram exatamente **1.511 unidades confirmadas** (`1.476 + 35 = 1.511`).

Por sua vez, a diferença de **39 unidades** entre a subtração simples `3.609 - 332 - 14 = 3.263` e o total final de **3.224** explica-se pela soma das **2 unidades adicionais** existentes nos 2 casos rejeitados que possuíam 2 subdivisões preliminares (`334 - 332 = 2`) com as **37 subdivisões excedentes** consolidadas pelo árbitro nos 34 casos confirmados em que o catálogo preliminar havia tomado provisoriamente o leitor com maior número de subdivisões (`2 + 37 = 39`).

### 5.2. Análise das Dez Categorias Promissórias
A Tabela 2 detalha a distribuição das **3.224 unidades confirmadas** nas dez categorias taxonômicas da pesquisa.

**Tabela 2 — Distribuição das unidades confirmadas por categoria taxonômica**

| Categoria Taxonômica | Código | Origem e Natureza | Unidades | % do Total |
| :--- | :--- | :--- | ---: | ---: |
| **Bênção divina** *(Indicador Principal)* | `divina_bencao` | Divina direta ou relatada / Bênção | 1.448 | 44,91% |
| **Juízo divino** | `divina_juizo` | Divina direta ou relatada / Juízo | 952 | 29,53% |
| **Compromisso humano (benefício)** | `humana_beneficio` | Humana em nome próprio / Benefício | 432 | 13,40% |
| **Garantia apostólica de bênção** *(Ind. Principal)* | `apostolica_garantia_bencao` | Autoridade apostólica / Bênção | 161 | 4,99% |
| **Compromisso humano (prejuízo)** | `humana_prejuizo` | Humana em nome próprio / Prejuízo | 82 | 2,54% |
| **Sentença divina** | `divina_sentenca` | Divina em forma de sentença / Juízo | 73 | 2,26% |
| **Garantia apostólica de juízo** | `apostolica_garantia_juizo` | Autoridade apostólica / Juízo | 37 | 1,15% |
| **Promessa adversária ou falsa** | `adversaria_ou_falsa` | Voz adversária ou falso profeta | 23 | 0,71% |
| **Bênção patriarcal** *(Indicador Principal)* | `patriarcal_bencao` | Profética patriarcal (Gênesis) / Bênção | 13 | 0,40% |
| **Juízo patriarcal** | `patriarcal_juizo` | Profética patriarcal (Gênesis) / Juízo | 3 | 0,09% |
| **TOTAL CONFIRMADO** | — | — | **3.224** | **100,00%** |

Observa-se que as promessas de origem divina ou apostólica/patriarcal inspirada somam **2.687 unidades (83,34%)**, divididas entre **1.622 unidades de bênção divina (50,31%)** e **1.065 unidades de juízo e sentença divina (33,03%)**. Os compromissos humanos em nome próprio respondem por **514 unidades (15,94%)**, e as promessas de voz adversária ou falsa (como as ofertas enganosas da serpente em Gn 3.4-5, do diabo na tentação de Cristo em Mt 4.9/Lc 4.6-7 e de falsos profetas como Hananias em Jr 28) somam **23 unidades (0,71%)**.

### 5.3. Distribuição pelas Divisões do Cânon e Comportamento dos Livros Sapienciais
A distribuição das 3.224 unidades pelas sete divisões canônicas revela forte concentração na literatura profética e nas narrativas de aliança:
1. **Profetas Maiores (Isaías a Daniel):** **1.006 unidades (31,2%)**, liderados por Jeremias (389), Isaías (350) e Ezequiel (241), onde se concentram tanto os oráculos de juízo sobre Judá e as nações quanto as grandes promessas messiânicas e de restauração da Nova Aliança.
2. **Pentateuco (Gênesis a Deuteronômio):** **560 unidades (17,4%)**, com destaque para Gênesis (181), Êxodo (132) e Deuteronômio (132).
3. **Livros Históricos do AT (Josué a Ester):** **595 unidades (18,5%)**, com alta presença de compromissos reais, aliança davídica (2Sm 7; 1Cr 17) e palavras proféticas na monarquia (1Sm: 108; 1Rs: 94; 2Sm: 71; 2Rs: 71).
4. **Profetas Menores (Oseias a Malaquias):** **332 unidades (10,3%)**, destacando-se Oseias (72), Zacarias (67) e Amós (56).
5. **Evangelhos e Atos:** **344 unidades (10,7%)**, com altíssima densidade de bênção divina nas palavras de Cristo em João (94 unidades, sendo 86 de bênção), Lucas (89) e Mateus (79).
6. **Epístolas e Apocalipse:** **290 unidades (9,0%)**, lideradas por Romanos (58), Apocalipse (46), 1 Coríntios (32) e Hebreus (28).
7. **Poéticos e Sapienciais (Jó a Cantares):** **98 unidades (3,0%)**, concentradas nos Salmos (82 unidades, sobretudo salmos reais, messiânicos e oráculos divinos como Sl 2, 50, 89, 91, 110 e 132) e em Jó (11).

**Análise específica de Provérbios (1), Eclesiastes (0) e Lamentações (0):**
A baixa contagem nos livros estritamente sapienciais e elegíacos é consequência direta e intencional da definição operacional comissiva:
* Em **Provérbios**, os leitores identificaram mais de 600 unidades de *princípios sapienciais* (`principio_sapiencial`), isto é, observações gerais sobre a ordem moral do mundo sem um promitente que assuma obrigação pessoal em primeira pessoa. O único registro confirmado como ato comissivo explícito é **Pv 1.13-14** (`P-PRO-0001`), onde um falante coletivo definido (os pecadores que convidam o jovem) assume compromisso em primeira pessoa do plural do futuro (*"Encontraremos toda sorte de bens preciosos; encheremos nossas casas de despojos"*).
* Em **Eclesiastes (0 unidades)**, foram mapeados 90 princípios sapienciais e 41 declarações doutrinárias sem compromisso. Passagens como **Ec 11.9** e **Ec 12.14** (*"Porque Deus há de trazer a juízo toda obra, e até tudo o que está encoberto, quer seja bom, quer seja mau"*) constituem afirmações doutrinárias em terceira pessoa proferidas pelo Pregador para fundamentar o dever moral de temer a Deus (Ec 12.13), e não oráculos em que Deus toma a palavra como promitente.
* Em **Lamentações (0 unidades)**, os dois leitores concordaram na ausência de atos comissivos diretos nos 154 versículos; passagens célebres de esperança, como **Lm 3.22-32**, são meditações e confissões do poeta sobre os atributos de misericórdia e fidelidade do Senhor, sem estrutura ilocucionária de promessa direta.

### 5.4. Impacto da Recuperação dos 276 Resumos e Sensibilidade ao Limiar de Jaccard
Na consolidação preliminar, 276 registros oriundos de passes tolerantes continham a string padronizada `"(resumo não informado pelo leitor)"`. Como o algoritmo de agrupamento lexical (`apurar_numero.py`) calcula o índice de Jaccard sobre tokens de 4 ou mais letras dentro da mesma categoria, essas 276 unidades compartilhavam exatamente o conjunto de tokens `{'resumo', 'informado', 'pelo', 'leitor'}` ($J = 1,00$), colapsando artificialmente em um único grupo por categoria e subestimando as promessas distintas em 2.763.

Após a recuperação integral dos 276 resumos reais (zerando os resumos genéricos), o agrupamento lexical foi recalculado nos quatro limiares de sensibilidade (Tabela 3), elevando a estimativa central ($\tau = 0,45$) para **2.945 promessas distintas** ($+182$) e o indicador principal de bênção divina para **1.481 promessas distintas** ($+57$).

**Tabela 3 — Sensibilidade da estimativa de promessas distintas ao limiar de Jaccard ($\tau$)**

| Limiar de Jaccard ($\tau$) | Distintas Confirmadas (Todas) | Projeção c/ Revocação 0,84 (Todas) | Bênção Divina (Distintas Confirmadas) | Bênção Divina (Projeção c/ Revocação) |
| :---: | ---: | ---: | ---: | ---: |
| $0,35$ | 2.729 | 3.249 | 1.357 | 1.615 |
| **$0,45$ (Padrão)** | **2.945** | **3.506** | **1.481** | **1.763** |
| $0,55$ | 3.052 | 3.633 | 1.539 | 1.832 |
| $0,65$ | 3.096 | 3.686 | 1.564 | 1.862 |

---

## 6. Discussão e Comparação com Contagens Históricas

A Tabela 4 confronta os resultados do presente levantamento com a contagem manual realizada por Everek R. Storms em meados da década de 1950.

**Tabela 4 — Comparação entre o recenseamento de Everek R. Storms (déc. 1950) e a pesquisa atual (Lima, 2026)**

| Dimensão / Categoria | Everek R. Storms (déc. 1950) | Pesquisa Atual — Jair Lima (2026) | Razão Metodológica da Diferença |
| :--- | ---: | ---: | :--- |
| **Total geral de promessas registradas** | 8.810 | **3.224 unidades** (**2.945 distintas**) | Storms subdividia cláusulas verbais do mesmo versículo e incluía predições gerais, máximas sapienciais e votos humanos a Deus. |
| **Promessas divinas ao ser humano (Total)** | 7.487 | **2.687 unidades** (1.622 bênção + 1.065 juízo) | A presente pesquisa exige ato comissivo verificável e agrupa paralelismos sinônimos do mesmo objeto na mesma unidade. |
| **Promessas divinas de bênção** | Não separado de juízos no total de 7.487 | **1.622 unidades** (**1.481 distintas**) | Separação explícita entre natureza de `bencao` (1.622) e natureza de `juizo`/sentença (1.065). |
| **Compromissos de humano a humano** | 991 | **514 unidades** (432 benefício + 82 prejuízo) | Exclusão de ofertas já esgotadas no próprio ato narrativo e de saudações/desejos votivos sem obrigação futura. |
| **Votos do homem a Deus** | 290 | **0** (excluídos por definição) | Votos devocionais e orações de louvor são dirigidos a Deus, não constituindo promessas bíblicas ao destinatário humano. |
| **Promessas de Satanás / vozes adversárias** | 11 (9 Satanás + 2 espíritos) | **23 unidades** | Inclui Satanás/serpente e falsos profetas ou inimigos que prometem em oposição a Deus (ex.: Hananias, Senaqueribe/Rabsaqué). |
| **Auditabilidade registro a registro** | Inexistente (apenas totais publicados) | **100% auditável** (3.224 registros c/ ID, âncora e JSONL) | Dados abertos depositados com scripts de validação e memória de cálculo. |

A comparação demonstra que a contagem de Storms não precisa ser rotulada como fraudulenta para que se compreenda por que ela produziu mais que o dobro de registros: na ausência de uma distinção formal baseada na teoria dos atos de fala e de uma fase de arbitragem para conter a hipersegmentação, um leitor manual tende a contabilizar cada verbo no futuro dentro de um oráculo profético (por exemplo, cinco verbos paralelos em um único versículo de Isaías), além de somar votos humanos a Deus (290 casos) e provérbios sapienciais. Quando se aplica a granularidade média (um compromisso por objeto prometido, sem duplicar paralelismos sinônimos) e se exige compromisso ilocucionário verificável confirmado por arbitragem independente, o cânon protestante converge de maneira robusta para **3.224 unidades promissórias** e **2.945 promessas distintas**.

---

## 7. Limitações

1. **Dependência hermenêutica de fronteira:** A distinção entre promessa divina de juízo (`divina_juizo`), advertência condicional ainda não decidida (`advertencia`) e predição profética puramente descritiva (`profecia_sem_compromisso`) envolve zonas limítrofes na literatura profética (especialmente em Isaías, Jeremias e Ezequiel).
2. **Agrupamento lexical vs. equivalência teológica profunda:** A estimativa de **2.945 promessas distintas** baseia-se na similaridade lexical de Jaccard ($\tau = 0,45$) sobre os resumos normalizados dentro de cada categoria. Duas formulações com vocabulário inteiramente distinto que expressem o mesmo compromisso teológico podem não ser fundidas pelo índice lexical, razão pela qual o estudo apresenta a curva completa de sensibilidade ($\tau \in [0,35; 0,65]$).
3. **Corpus em tradução vernácula:** A leitura automatizada operou sobre o texto em língua portuguesa da *Bíblia Almeida Livre*, sem parsing morfológico direto do hebraico massorético ou do grego koiné, embora a tradução base siga equivalência formal rigorosa.
4. **Uso de modelos de linguagem sem revisão humana individualizada dos 31.104 versículos:** Embora a arquitetura do protocolo, os cartões de critérios, os testes de erros plantados e a auditoria amostral tenham sido conduzidos pelo autor, a varredura exaustiva dos 31.104 versículos e a arbitragem dos 1.808 casos foram executadas por modelos de inteligência artificial sob validação determinística por código.

---

## 8. Conclusão

A investigação integral dos 66 livros, 1.189 capítulos e 31.104 versículos da Bíblia Almeida Livre mediante protocolo de três fases (dupla leitura independente e arbitragem exegética cruzada) permite responder de forma empírica, transparente e reprodutível à questão sobre o número de promessas nas Escrituras:
1. Foram confirmadas **3.224 unidades textuais promissórias** (com zero candidatos pendentes), distribuídas em **4.373 versículos** (**14,1%** do corpus bíblico), sendo **1.211** confirmadas por acordo direto entre os dois leitores iniciais e **2.013** confirmadas por arbitragem independente na terceira fase.
2. Descontadas as repetições por agrupamento de similaridade lexical no limiar padrão de $0,45$ após a recuperação integral de todos os 3.224 resumos, estimam-se **2.945 promessas distintas** (ou **3.506** na projeção corrigida pela revocação de $0,84$).
3. As promessas divinas de bênção (indicador principal) totalizam **1.622 unidades confirmadas** e **1.481 promessas distintas**, enquanto as promessas divinas de juízo e sentença somam **1.065 unidades**, os compromissos humanos **514 unidades** e as promessas adversárias ou falsas **23 unidades**.
4. A cifra tradicional de 8.810 (ou 7.487) promessas atribuída a Everek R. Storms não se confirma sob critérios exegéticos estritos que separem atos comissivos de máximas sapienciais, declarações doutrinárias em terceira pessoa, votos humanos a Deus e paralelismos verbais intraversiculares. Tanto pela contagem de unidades confirmadas (**3.224**) quanto pela estimativa de compromissos distintos (**2.945**), o patrimônio promissório da Bíblia situa-se solidamente na marca de **três mil promessas**.

---

## Declaração de Disponibilidade dos Dados (Data Availability Statement)

O conjunto completo de dados que fundamenta este artigo — incluindo os catálogos estruturados das 3.224 unidades promissórias em formatos CSV, XLSX e JSONL por livro bíblico, as decisões dos 36 lotes da Fase 3 de arbitragem, os scripts Python de validação, consolidação e cálculo de similaridade de Jaccard, a suíte de 77 testes automatizados e a memória de cálculo — está publicamente disponível sob licença aberta Creative Commons Attribution 4.0 International (CC BY 4.0) para os metadados e MIT License para o código no repositório GitHub (`https://github.com/jairslima/Promessas-da-Biblia-by-Jair-Lima`) e arquivado permanentemente no Zenodo. O texto integral do livro comercial *As 3 Mil Promessas da Bíblia* (Lima Editora do Brasil) permanece protegido por direitos autorais e não integra o depósito público de dados.

## Declaração de Utilização de Inteligência Artificial (AI Disclosure Statement)

A concepção teórica, o desenho do protocolo de pesquisa em três fases, as regras de inclusão e exclusão exegética, os scripts de validação determinística e a responsabilidade intelectual integral pelo estudo são do autor, **Jair Lima**. Na execução computacional das leituras e da arbitragem, foram utilizados Grandes Modelos de Linguagem (Anthropic Claude, DeepSeek V4.1 Flash High, Google Gemini e OpenAI Codex) atuando sob isolamento de contexto entre os passes de leitura e com independência cruzada obrigatória na Fase 3 (de modo que o modelo árbitro de cada livro nunca coincidisse com nenhum dos dois modelos leitores daquele livro). Todas as saídas dos modelos foram submetidas a validação programática de esquema, conferência de âncoras literais contra o texto canônico da Bíblia Almeida Livre e reconciliação aritmética automatizada.

---

## Referências Bibliográficas Verificadas

* AUSTIN, John Langshaw. *How to Do Things with Words*. Oxford: Clarendon Press, 1962.
* BRIGGS, Richard S. *Words in Action: Speech Act Theory and Biblical Interpretation*. Edinburgh: T&T Clark, 2001.
* CLARKE, Samuel. *A Collection of the Promises of Scripture, under their Proper Heads: Representing I. The Blessings Promised. II. The Duties to which Promises are Made*. London: J. Clark, 1720 (2. ed. com recomendação de Isaac Watts, London, 1738).
* LIMA, Jair. *Bíblia Almeida Livre*. Três Coroas: Lima Editora do Brasil, 2026. Licenciada sob Creative Commons Atribuição-SemDerivações 4.0 Internacional (CC BY-ND 4.0).
* LIMA, Jair. *As 3 Mil Promessas da Bíblia: Da criação à eternidade: a história de um Deus que cumpre sua Palavra*. Três Coroas: Lima Editora do Brasil, 2026.
* LOCKYER, Herbert. *All the Promises of the Bible: A Unique Compilation and Exposition of Divine Promises in Scripture*. Grand Rapids: Zondervan Publishing House, 1962.
* SEARLE, John R. *Speech Acts: An Essay in the Philosophy of Language*. Cambridge: Cambridge University Press, 1969.
* SEARLE, John R. *Expression and Meaning: Studies in the Theory of Speech Acts*. Cambridge: Cambridge University Press, 1979.
* STORMS, Everek R. Levantamento estatístico das 8.810 promessas bíblicas (7.487 promessas divinas ao homem). Kitchener, Ontário, c. 1954–1956; documentado em *Time Magazine* e sistematizado em LOCKYER, Herbert, *All the Promises of the Bible*, Grand Rapids: Zondervan, 1962.
* THISELTON, Anthony C. *New Horizons in Hermeneutics: The Theory and Practice of Transforming Biblical Reading*. Grand Rapids: Zondervan, 1992.
* VANHOOZER, Kevin J. *Is There a Meaning in This Text? The Bible, the Reader, and the Morality of Literary Knowledge*. Grand Rapids: Zondervan, 1998.
