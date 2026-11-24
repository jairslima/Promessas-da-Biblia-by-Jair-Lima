# PROJECT.md: Promessas da Bíblia by Jair Lima (Repositório Científico Público)

## Nome e descrição
Base de dados científica aberta, catálogo estruturado e análise computacional e exegética das **3.224 unidades promissórias confirmadas** (**2.945 promessas distintas** no limiar lexical de Jaccard 0,45) nos **66 livros, 1.189 capítulos e 31.104 versículos** do cânon protestante (Bíblia Almeida Livre by Jair Lima, CC BY-ND 4.0). Esta pesquisa fundamenta o livro *As 3 Mil Promessas da Bíblia: Da criação à eternidade: a história de um Deus que cumpre sua Palavra*, de **Jair Lima** (Lima Editora do Brasil, 2026).

## Stack e estrutura de pastas
* **Linguagem:** Python 3.10+ (biblioteca padrão para validação, consolidação e cálculo de similaridade lexical; `matplotlib` para geração de gráficos) + HTML5/CSS3/JS puro para o site estático interativo.
* **Estrutura:**
  * `catalogo-digital-completo.csv` e `.xlsx`: Catálogo completo das 3.224 unidades promissórias confirmadas.
  * `catalogo/<LIVRO>/`: 66 diretórios por livro bíblico (`<LIV>.jsonl`, `CATALOGO.md`, `CONTAGEM.md`, `cobertura.json`).
  * `evidencias_arbitragem_fase3/`: Os 36 lotes de entrada e saída da Fase 3 de arbitragem exegética independente (`1.808` casos).
  * `graficos/`: 12 gráficos em alta resolução (300 DPI, versões coloridas `_cor.png` e monocromáticas `_pb.png`).
  * `docs/`: Site estático bilíngue (**Observatório das Promessas Bíblicas**) publicado via GitHub Pages.
  * `scripts/` e `testes/`: Scripts de validação, consolidação, cálculo de Jaccard e 77 testes automatizados.
  * `ARTIGO_CIENTIFICO_PROMESSAS_DA_BIBLIA.md`, `RELATORIO_ORIGINALIDADE_CIENTIFICA.md`, `MEMORIA_DE_CALCULO.md`, `DICIONARIO_DE_CAMPOS.md`, `RELATORIO_LIMITACOES.md`.

## Comandos de verificação e reprodução
```bash
python -I testes/testes_erros_plantados.py
python -I scripts/apurar_numero.py
python -I scripts/memoria_de_calculo.py
```

## Licenças
* **Código-fonte:** MIT License (`LICENSE`) — Copyright (c) 2026 Jair Lima.
* **Metadados e catálogo analítico:** Creative Commons Attribution 4.0 International (`LICENSE-DATA`, CC BY 4.0).
* **Citações bíblicas:** Bíblia Almeida Livre by Jair Lima (CC BY-ND 4.0).
