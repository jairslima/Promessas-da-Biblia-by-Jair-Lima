# Apêndice Técnico de Reprodutibilidade (`DOCUMENTACAO_TECNICA_REPRODUTIBILIDADE.md`)

**Observatório das Promessas Bíblicas**  
*Uma investigação integral das promessas de Gênesis a Apocalipse*  
**Pesquisa e autoria:** Jair Lima (Lima Editora do Brasil, 2026)

---

## 1. Finalidade deste Documento

Este apêndice técnico reúne exclusivamente os detalhes operacionais das ferramentas computacionais, ambientes de execução, especificações de verificação programática e identificadores de sistemas utilizados nas etapas de análise textual e arbitragem da pesquisa, conforme as normas de transparência e reprodutibilidade científica.

A concepção intelectual da pesquisa, a formulação da definição operacional de promessa bíblica, as regras exegéticas de inclusão e exclusão, a taxonomia em dez categorias e a responsabilidade autoral pertencem integralmente a **Jair Lima**. Os sistemas computacionais descritos abaixo atuaram estritamente como instrumentos de processamento sob protocolo determinístico de validação.

---

## 2. Ambiente Computacional e Requisitos de Reprodução

* **Linguagem de programação:** Python 3.10 ou superior (os scripts de validação, consolidação, cálculo de similaridade lexical de Jaccard e geração da memória de cálculo utilizam exclusivamente a biblioteca padrão do Python).
* **Geração gráfica:** `matplotlib` e `numpy` (para reprodução dos gráficos em 450 DPI `.png` e vetoriais `.svg`).
* **Codificação de arquivos:** UTF-8 (com BOM nos arquivos `.csv` para compatibilidade direta com Microsoft Excel).
* **Corpus de referência:** *Bíblia Almeida Livre by Jair Lima* (66 livros, 1.189 capítulos, 31.104 versículos, auditados por manifesto criptográfico SHA-256).

### Comandos para reprodução integral dos cálculos e testes

```bash
# 1. Executar a suíte de 77 testes controlados (validação de esquema e detecção de erros plantados)
python -I testes/testes_erros_plantados.py

# 2. Recalcular as contagens de promessas distintas estimadas (limiares de Jaccard 0,35 a 0,65)
python -I scripts/apurar_numero.py

# 3. Gerar e conferir a Memória de Cálculo completa
python -I scripts/memoria_de_calculo.py
```

---

## 3. Especificação Técnica das Ferramentas de Análise Textual e Arbitragem

Para assegurar a independência operacional entre as duas análises textuais iniciais (Etapas 1 e 2) e a terceira etapa de avaliação (Etapa 3 — arbitragem exegética assistida por computador), o protocolo determinou que a ferramenta empregada na Etapa 3 de cada livro bíblico fosse sempre de família arquitetural distinta das duas ferramentas que realizaram as leituras das Etapas 1 e 2 daquele mesmo livro:

1. **Etapa 1 (Identificação inicial) e Etapa 2 (Conferência cruzada independente):**
   * Executadas em sessões isoladas, sem compartilhamento de memória ou acesso às saídas da outra análise.
   * Sistemas utilizados conforme a divisão canônica documentada nos registros históricos (`catalogo/<LIVRO>/CONTAGEM.md`): modelos das famílias Anthropic Claude, DeepSeek (V4.1 Flash High), Google Gemini e OpenAI Codex.
   * Todas as saídas brutas passaram pelo validador determinístico (`scripts/validar_passe.py`), que confere a cobertura exata dos versículos do capítulo, o esquema JSONL, os valores permitidos de categoria e a presença literal da âncora textual no versículo correspondente do corpus.
2. **Etapa 3 (Arbitragem exegética assistida por computador):**
   * Aplicada aos casos de identificação unilateral ou de divergência de classificação entre as Etapas 1 e 2 (`1.808` casos nos 56 livros da etapa complementar, distribuídos em 36 lotes auditáveis em `evidencias_arbitragem_fase3/`, além das adjudicações de Gênesis, Pentateuco e Evangelhos).
   * Regra de independência cruzada por livro:
     * Nos 42 livros analisados nas Etapas 1 e 2 por Claude e DeepSeek (ou Claude e Codex), a terceira avaliação foi processada por Gemini.
     * Nos 14 livros analisados nas Etapas 1 e 2 por Claude e Gemini (Josué a Salmos), a terceira avaliação foi processada por DeepSeek.
     * Nos livros do Pentateuco (Êxodo a Deuteronômio) e Evangelhos (Mateus e Marcos) analisados nas Etapas 1 e 2 por DeepSeek e Gemini/Codex, a terceira avaliação foi processada por Claude.
   * Os identificadores originais nos arquivos JSONL (`catalogo/*/*.jsonl` e `evidencias_arbitragem_fase3/*`) foram integralmente preservados sem alteração para fins de auditoria histórica.

---

## 4. Algoritmo de Agrupamento Lexical (Índice de Jaccard)

O script `scripts/apurar_numero.py` estima o número de compromissos distintos dentro de cada uma das 10 categorias taxonômicas aplicando os seguintes passos determinísticos:

1. **Tokenização e normalização:** remoção de acentos, conversão para minúsculas e extração de vocábulos com 4 ou mais caracteres alfabéticos a partir do resumo exegético (`resumo` / `objeto_prometido`) de cada uma das 3.224 unidades confirmadas.
2. **Filtragem de palavras funcionais e verbos promissórios genéricos:** exclusão de palavras vazias (*stopwords* da língua portuguesa) e dos termos estruturais comuns a todas as formulações (*deus, senhor, promete, garante, anuncia, declara*).
3. **Cálculo de similaridade par a par:** para dois registros $A$ e $B$ da mesma categoria com conjuntos de vocábulos $T_A$ e $T_B$, calcula-se $J(A, B) = \frac{|T_A \cap T_B|}{|T_A \cup T_B|}$.
4. **Agrupamento guloso por limiar ($\tau$):** registros com $J(A, B) \ge \tau$ são reunidos no mesmo grupo lexical. No limiar padrão $\tau = 0,45$, as 3.224 unidades confirmadas formam **2.945 promessas distintas estimadas** (sendo **1.481** nas categorias de bênção divina). A análise de sensibilidade completa é reportada para $\tau \in \{0,35; 0,45; 0,55; 0,65\}$.
