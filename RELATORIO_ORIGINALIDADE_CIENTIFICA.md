# RELATÓRIO DE ORIGINALIDADE CIENTÍFICA E REVISÃO DO ESTADO DA ARTE
**Projeto:** Pesquisa Promessas da Bíblia by Jair Lima (*As 3 Mil Promessas da Bíblia*)  
**Autor e Pesquisador Responsável:** Jair Lima (Lima Editora do Brasil)  
**Data da Revisão Bibliográfica:** 24 de novembro de 2026

---

## 1. Escopo e Estratégia de Busca Acadêmica

Para situar o levantamento das **3.224 unidades promissórias confirmadas** (**2.945 promessas distintas**) nos 66 livros do cânon protestante dentro da literatura científica e teológica internacional, realizou-se uma revisão bibliográfica direcionada ao estado da arte em três idiomas (**português, inglês e espanhol**), consultando as bases e repositórios:
* **Google Scholar, Crossref, OpenAlex e Semantic Scholar** (literatura revisada por pares em estudos bíblicos, humanidades digitais, linguística de corpus e processamento de linguagem natural aplicado a textos religiosos);
* **Zenodo e OSF** (datasets abertos de estudos bíblicos e teologia computacional);
* **GitHub** (repositórios estruturados de dados bíblicos, morfologia, anotações sintáticas e classificadores semânticos).

**Descritores utilizados:**
* **Português:** `"promessas da Bíblia" contagem corpus`, `"exegese computacional" promessas`, `"teologia computacional" Bíblia classificação`, `"catálogo estruturado" promessas bíblicas`.
* **Inglês:** `"promises of the Bible" count corpus`, `"Everek R. Storms" OR "Everett R. Storms" 7487 8810`, `"computational theology" biblical corpus NLP LLM`, `"speech act theory" biblical promises corpus`, `"LLM-as-a-judge" biblical exegesis classification`.
* **Espanhol:** `"promesas de la Biblia" conteo corpus`, `"teología computacional" análisis de corpus bíblico`, `"clasificación de promesas bíblicas" inteligencia artificial`.

---

## 2. Síntese do Estado da Arte em Quatro Eixos

### 2.1. Coletâneas Pastorais Clássicas e Levantamentos Manuais (Séculos XVIII a XX)
1. **Samuel Clarke (1720):** *A Collection of the Promises of Scripture, under their Proper Heads* (Londres: J. Clark; 2ª ed. 1738 com recomendação de Isaac Watts). Constitui o marco clássico das antologias temáticas protestantes, agrupando passagens de consolação espiritual e deveres cristãos por tópicos doutrinários. Não realizou recenseamento quantitativo dos 31.104 versículos nem incluiu promessas de juízo, compromissos humanos ou garantias históricas já cumpridas.
2. **Everek R. Storms (c. 1954–1956):** Professor escolar canadense (Kitchener, Ontário) que, durante sua 27ª leitura da Bíblia ao longo de 18 meses, realizou a contagem manual que deu origem à cifra mais repetida na literatura cristã contemporânea: **8.810 promessas totais**, divididas em **7.487 promessas de Deus ao homem**, 991 de humano a humano, 290 do homem a Deus (votos), 28 de anjos, 9 de Satanás, 2 do Pai ao Filho, 2 de espíritos malignos e 1 de homem a anjo. Embora meritório pelo esforço individual, Storms não publicou uma base de dados versículo a versículo auditável nem separou predições proféticas gerais, desdobramentos verbais internos à mesma oração, máximas sapienciais e votos devocionais humanos.
3. **Herbert Lockyer (1962):** *All the Promises of the Bible* (Grand Rapids: Zondervan, 351 p.). Sistematizou a exposição pastoral das promessas bíblicas e popularizou a estatística de Storms no meio homilético mundial, porém sem disponibilizar catálogo estruturado verificável por registro.

### 2.2. Linguística de Corpus Bíblico e Bases Morfossintáticas Abertas
* Projetos acadêmicos de referência — como a base **ETCBC (Eep Talstra Centre for Bible and Computer / SHEBANQ)** na Vrije Universiteit Amsterdam (BHSA — *Biblia Hebraica Stuttgartensia Amstelodamensis*), o **OpenText.org**, o **MACULA Hebrew and Greek Syntax Datasets** (Clear Bible / GitHub) e o **STEPBible (Tyndale House, Cambridge)** — forneceram à comunidade científica árvores morfológicas, sintáticas e léxicos alinhados em nível de palavra e oração.
* Contudo, a revisão desses repositórios demonstra que eles mapeiam estruturas **gramaticais, morfológicas e discursivas** (tempos verbais, cláusulas, participantes), mas **não possuem uma camada de anotação pragmático-teológica das promessas** em todo o cânon que distinga atos de fala comissivos (promessas de bênção e de juízo) de atos diretivos (mandamentos), assertivos (relatos e doutrinas) ou expressivos (desejos e bênçãos votivas).

### 2.3. Teologia Computacional, Atos de Fala e Processamento de Linguagem Natural (PLN / LLMs)
* A aplicação da **Teoria dos Atos de Fala** (Austin, 1962; Searle, 1969; Briggs, *Words in Action: Speech Act Theory and Biblical Interpretation*, 2001) à exegese bíblica estabeleceu teoricamente que uma promessa bíblica é um **ato ilocucionário comissivo** (em que o falante se obriga a uma ação futura ou continuada em favor ou desfavor de um destinatário), não redutível à presença do vocábulo "promessa" (*epangelia*) ou ao tempo verbal futuro.
* Na literatura recente de **Humanidades Digitais e PLN aplicado a textos sagrados** (2020–2026), destacam-se estudos de mapeamento intertextual por *embeddings* semânticos, classificação temática supervisionada de versículos e avaliação de vieses hermenêuticos de Grandes Modelos de Linguagem (LLMs).
* Entretanto, **não foi encontrado na literatura indexada (Google Scholar, Crossref, OpenAlex, Semantic Scholar, Zenodo ou GitHub)** nenhum dataset público que combine:
  1. Varredura integral, versículo a versículo, dos **31.104 versículos dos 66 livros** sob uma definição operacional comissiva explícita;
  2. Dupla leitura cega independente seguida de **arbitragem exegética por terceiro modelo independente** (*LLM-as-a-Judge* com independência cruzada por livro);
  3. Separação formal entre **promitente** (autor do compromisso) e **comunicador humano** (profeta, apóstolo ou narrador que relata a palavra);
  4. Estimativa matemática de **promessas distintas** por agrupamento de similaridade lexical de Jaccard com análise de sensibilidade de limiar (0,35 a 0,65) e correção por taxa empírica de revocação.

---

## 3. Matriz Comparativa do Estado da Arte

| Dimensão Analítica | Samuel Clarke (1720) | Everek R. Storms (déc. 1950) / Lockyer (1962) | Corpora Morfossintáticos (ETCBC / MACULA / STEPBible) | Estudos Recentes de PLN Bíblico (2020–2026) | **Pesquisa Atual — Jair Lima (2026)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Cobertura do Cânon** | Seletiva (tópicos devocionais) | 66 livros (leitura individual manual) | 66 livros (hebraico/grego) | Amostras ou recortes temáticos | **66 livros, 1.189 capítulos, 31.104 versículos (100%)** |
| **Unidade de Registro Auditável** | Tópicos pastorais com versículos | Apenas totais agregados (8.810 / 7.487) | Morfema, palavra e oração sintática | Versículo ou parágrafo | **3.224 unidades catalogadas individualmente com ID (`P-LIV-NNNN`)** |
| **Definição Operacional Exegética** | Consolação e deveres cristãos | Critério amplo não formalizado (inclui votos humanos a Deus e predições) | Gramatical e morfossintática (sem camada promissória) | Classificação por palavras-chave ou *embeddings* | **Compromisso futuro/continuado com promitente, objeto e destinatário; exclui máximas sapienciais sem falante comissivo** |
| **Método de Verificação e Arbitragem** | Seleção autoral única | Leitura humana única sem revisão cruzada | Anotação acadêmica morfológica | Modelo único ou *fine-tuning* supervisionado | **3 Fases: 2 leituras independentes cegas + 3º agente árbitro independente nos 1.808 casos divergentes** |
| **Separação Promitente vs. Comunicador** | Não | Parcial (apenas em totais gerais) | Participantes sintáticos | Não documentada | **Sim (promitente divino separado do comunicador humano em 1.487 registros)** |
| **Distinção entre Unidades e Promessas Distintas** | Não | Não (repetições somadas ao total bruto) | Não aplicável | Agrupamento vetorial não calibrado para promessas | **Sim: 3.224 unidades confirmadas vs. 2.945 promessas distintas (Jaccard 0,45) e sensibilidade 0,35–0,65** |
| **Dados Abertos e Reprodutibilidade** | Domínio público (texto impresso) | Não (lista completa nunca publicada em banco de dados) | Sim (GitHub / Zenodo / SHEBANQ) | Parcial | **Sim: CSV, XLSX, JSONL por livro, scripts Python, testes e memória de cálculo (GitHub + Zenodo DOI)** |

---

## 4. Diferenciais Originais e Contribuição Científica do Projeto

Sem reivindicar pioneirismo mundial absoluto sobre toda e qualquer iniciativa não indexada, a presente pesquisa oferece **cinco contribuições originais documentadas e verificáveis** para a teologia bíblica e as humanidades digitais:

1. **Primeiro catálogo aberto versículo a versículo das promessas dos 66 livros em língua portuguesa (e com metadados bilíngues PT/EN):** diferentemente da contagem histórica de Everek R. Storms (cujos 8.810 registros jamais foram publicados em formato tabular verificável passagem por passagem), cada uma das **3.224 unidades confirmadas** possui código único, referência de início e fim, categoria, natureza, promitente, comunicador, destinatário, condição, resumo exegético e via de confirmação.
2. **Protocolo de Tripla Fase com Arbitragem Independente Cruzada:** demonstração prática de um fluxo de controle de qualidade em que nenhum candidato apontado por um único leitor entra no catálogo final sem o julgamento exegético de um terceiro modelo independente que não participou da leitura daquele livro (resultando na confirmação de 1.511 unidades e na rejeição fundamentada de 332 falsos positivos na Fase 3).
3. **Separação Metodológica entre Princípios Sapienciais, Declarações Doutrinárias e Atos Comissivos:** resolução rigorosa de distorções históricas (como a inclusão indevida de centenas de provérbios morais ou declarações doutrinárias em terceira pessoa, a exemplo de Ec 12.14, como se fossem promessas diretas).
4. **Modelagem Matemática da Redundância Promissória:** aplicação transparente do índice de similaridade lexical de Jaccard por categoria com curva de sensibilidade (limiares 0,35 a 0,65) e correção por taxa de revocação (0,84), distinguindo **contagem efetiva de ocorrências (3.224)**, **estimativa de promessas distintas (2.945)** e **projeção corrigida (3.506)**.
5. **Reprodutibilidade Integral Sem Dependência de Software Proprietário:** disponibilização dos scripts de validação, consolidação, agrupamento lexical e geração de gráficos utilizando biblioteca padrão do Python, auditáveis por qualquer pesquisador.
