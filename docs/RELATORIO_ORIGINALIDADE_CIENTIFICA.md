# RELATÓRIO DE ORIGINALIDADE CIENTÍFICA E REVISÃO DO ESTADO DA ARTE
**Projeto:** Observatório das Promessas Bíblicas (*As 3 Mil Promessas da Bíblia*)  
**Pesquisa e autoria:** Jair Lima (Lima Editora do Brasil)  
**Data da Revisão Bibliográfica:** 24 de novembro de 2026

---

## 1. Escopo e Estratégia de Busca Acadêmica

Para situar o levantamento das **3.224 unidades promissórias confirmadas** (**2.945 promessas distintas estimadas**) nos 66 livros do cânon protestante dentro da literatura científica e teológica internacional, realizou-se uma revisão bibliográfica direcionada ao estado da arte em três idiomas (**português, inglês e espanhol**), consultando as bases e repositórios:
* **Google Scholar, Crossref, OpenAlex e Semantic Scholar** (literatura em estudos bíblicos, teologia bíblica, humanidades digitais, linguística de corpus e análise computacional aplicada a textos bíblicos);
* **Zenodo e OSF** (conjuntos de dados abertos de estudos bíblicos e humanidades digitais);
* **GitHub** (repositórios estruturados de dados bíblicos, morfologia, anotações sintáticas e análise de corpus).

**Descritores utilizados:**
* **Português:** `"promessas da Bíblia" contagem corpus`, `"exegese bíblica" promessas catálogo`, `"humanidades digitais" Bíblia classificação promessas`, `"atos de fala comissivos" promessas bíblicas`.
* **Inglês:** `"promises of the Bible" count corpus`, `"Everek R. Storms" OR "Everett R. Storms" 7487 8810`, `"digital humanities" biblical promises corpus`, `"speech act theory" commissives biblical promises`.
* **Espanhol:** `"promesas de la Biblia" conteo corpus`, `"humanidades digitales" análisis de corpus bíblico`, `"clasificación de promesas bíblicas"`.

---

## 2. Síntese do Estado da Arte em Três Eixos

### 2.1. Coletâneas Pastorais Clássicas e Levantamentos Manuais (Séculos XVIII a XX)
1. **Samuel Clarke (1720):** *A Collection of the Promises of Scripture, under their Proper Heads* (Londres: J. Clark; 2. ed. 1738 com recomendação introdutória de Isaac Watts). Constitui o marco clássico das antologias temáticas protestantes, agrupando passagens de consolação espiritual e deveres cristãos por tópicos doutrinários. Não teve por objetivo realizar um recenseamento quantitativo dos 31.104 versículos nem catalogar promessas de juízo, compromissos humanos ou garantias históricas já cumpridas.
2. **Everek Richard Storms (1956):** Professor escolar canadense (1914 a 1995, Kitchener, Ontário) que, durante sua 27ª leitura da Bíblia ao longo de 18 meses, realizou a contagem manual noticiada pela revista *Time* em 24 de dezembro de 1956 (seção *Religion*, "Promises"): **8.810 promessas totais**, divididas em **7.487 promessas de Deus ao homem**, 991 de humano a humano, 290 do homem a Deus, 28 de anjos, 9 de Satanás, 2 do Pai ao Filho, 2 de espíritos malignos e 1 de homem a anjo. Apesar de sua relevância histórica, o levantamento de Storms não foi localizado em formato de catálogo estruturado versículo a versículo que permita auditar suas decisões individuais de inclusão e segmentação.
3. **Herbert Lockyer (1962):** *All the Promises of the Bible* (Grand Rapids: Zondervan, 351 p.). Sistematizou a exposição pastoral das promessas bíblicas e difundiu a estatística de Storms no meio homilético internacional, sem disponibilizar conjunto de dados estruturado verificável por registro.

### 2.2. Linguística de Corpus Bíblico e Bases Morfossintáticas Abertas
* Projetos acadêmicos de referência, como a base **ETCBC (Eep Talstra Centre for Bible and Computer / SHEBANQ)** na Vrije Universiteit Amsterdam (BHSA), o **OpenText.org**, o **MACULA Hebrew and Greek Syntax Datasets** (Clear Bible) e o **STEPBible (Tyndale House, Cambridge)**, forneceram à comunidade científica árvores morfológicas, sintáticas e léxicos alinhados em nível de palavra e oração.
* Contudo, a revisão desses repositórios demonstra que eles mapeiam estruturas **gramaticais, morfológicas e sintáticas**, mas **não possuem uma camada de anotação pragmático-teológica das promessas** em todo o cânon que distinga atos de fala comissivos (promessas de bênção e de juízo) de atos diretivos (mandamentos), assertivos (relatos e afirmações doutrinárias) ou expressivos (desejos e bênçãos votivas).

### 2.3. Teoria dos Atos de Fala e Pesquisa Computacional Aplicada ao Texto Bíblico
* A aplicação da **Teoria dos Atos de Fala** (Austin, 1962; Searle, 1969, 1979; Thiselton, 1992; Vanhoozer, 1998; Briggs, 2001) à hermenêutica bíblica estabeleceu teoricamente que uma promessa bíblica é um **ato ilocucionário comissivo** (em que o falante se obriga a uma ação futura ou continuada em relação a um destinatário), não redutível à simples ocorrência lexical do vocábulo "promessa" ou ao tempo verbal futuro.
* Na literatura consultada (Google Scholar, Crossref, OpenAlex, Semantic Scholar, Zenodo e GitHub), não foi localizado um conjunto público de dados que reúna simultaneamente: (1) investigação integral dos 31.104 versículos dos 66 livros sob definição operacional comissiva explícita; (2) conferência cruzada independente seguida de terceira etapa de arbitragem exegética sobre todas as divergências; (3) separação sistemática entre promitente e comunicador humano; e (4) estimativa matemática de promessas distintas com análise de sensibilidade de limiar e memória de cálculo aberta.

---

## 3. Matriz Comparativa do Estado da Arte

| Dimensão Analítica | Samuel Clarke (1720 / 1738) | Everek R. Storms (1956) / Lockyer (1962) | Corpora Morfossintáticos (ETCBC / MACULA / STEPBible) | Estudos Recentes de Corpus Bíblico | **Pesquisa Atual: Jair Lima (2026)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Cobertura do Cânon** | Seletiva (tópicos devocionais) | 66 livros (leitura individual manual) | 66 livros (hebraico/grego) | Amostras ou recortes temáticos | **66 livros, 1.189 capítulos, 31.104 versículos (100%; 64 livros com registros)** |
| **Unidade de Registro Auditável** | Tópicos pastorais com versículos | Apenas totais agregados publicados (8.810 / 7.487) | Morfema, palavra e oração sintática | Versículo ou segmento textual | **3.224 unidades catalogadas individualmente com ID (`P-LIV-NNNN`)** |
| **Definição Operacional Exegética** | Consolação e deveres cristãos | Critérios internos não publicados caso a caso (inclui votos do homem a Deus) | Gramatical e morfossintática (sem camada promissória) | Classificação temática ou lexical | **Compromisso futuro/continuado com promitente, objeto e destinatário; exclui máximas sapienciais sem falante comissivo** |
| **Método de Verificação e Arbitragem** | Seleção autoral única | Leitura única sem conferência cruzada | Anotação acadêmica morfológica | Classificação automatizada simples | **3 Etapas: 2 análises independentes + 3ª etapa de arbitragem exegética nos 1.808 casos divergentes** |
| **Separação Promitente vs. Comunicador** | Não | Parcial (apenas em totais gerais) | Participantes sintáticos | Não documentada | **Sim (promitente divino separado do comunicador humano em 1.487 registros)** |
| **Distinção entre Unidades e Promessas Distintas** | Não | Não (repetições não separadas por agrupamento) | Não aplicável | Não calibrada para promessas | **Sim: 3.224 unidades confirmadas vs. 2.945 promessas distintas estimadas (Jaccard 0,45; faixa 0,35 a 0,65)** |
| **Dados Abertos e Reprodutibilidade** | Texto impresso em domínio público | Lista individual não localizada em banco de dados | Sim (GitHub / Zenodo / SHEBANQ) | Parcial | **Sim: CSV, XLSX, JSONL por livro, scripts Python, testes controlados e memória de cálculo** |

---

## 4. Contribuição Científica e Originalidade da Combinação Metodológica

Sem reivindicar pioneirismo mundial absoluto sobre iniciativas não indexadas, a pesquisa de **Jair Lima** oferece uma combinação metodológica original e integralmente verificável para a teologia bíblica e as humanidades digitais:

1. **Catálogo aberto versículo a versículo das promessas dos 66 livros:** cada uma das **3.224 unidades confirmadas** possui identificador único, referência de início e fim, categoria taxonômica, natureza, promitente, comunicador humano, destinatário, condição, resumo exegético e via de confirmação.
2. **Procedimento em três etapas com arbitragem exegética das divergências:** nenhuma unidade apontada unilateralmente nas duas primeiras etapas ingressou no catálogo final sem avaliação individualizada na terceira etapa (que confirmou 1.511 unidades e rejeitou 332 casos de falsos positivos).
3. **Distinção rigorosa entre atos comissivos, princípios sapienciais e declarações doutrinárias:** explicitação metodológica do motivo pelo qual máximas gerais de sabedoria (como em Provérbios) e afirmações doutrinárias em terceira pessoa (como em Ec 12.14 e Lm 3.22-32) não se confundem com oráculos promissórios em primeira pessoa.
4. **Modelagem da repetição promissória e análise de sensibilidade:** aplicação transparente do índice de similaridade lexical de Jaccard por categoria (limiares 0,35 a 0,65), distinguindo **contagem efetiva de unidades confirmadas (3.224)**, **estimativa de promessas distintas (2.945)** e **projeção analítica pela revocação (3.506)**.
5. **Reprodutibilidade integral em código aberto:** disponibilização dos scripts de validação, consolidação e cálculo aritmético sem dependência de softwares proprietários.
