# PROJECT.md: Observatório das Promessas Bíblicas

## Identificação institucional
* **Projeto:** Observatório das Promessas Bíblicas: Uma investigação integral das promessas de Gênesis a Apocalipse
* **Pesquisa e autoria:** Jair Lima
* **Instituição / Editora:** Lima Editora do Brasil (2026)
* **Portal público:** https://jairslima.github.io/Promessas-da-Biblia-by-Jair-Lima/
* **Repositório oficial:** https://github.com/jairslima/Promessas-da-Biblia-by-Jair-Lima

## Resumo da pesquisa
Investigação integral dos **66 livros, 1.189 capítulos e 31.104 versículos** do cânon protestante (tendo como corpus de referência a *Bíblia Almeida Livre*, CC BY-ND 4.0), estruturada em três etapas metodológicas de identificação, conferência cruzada e arbitragem exegética assistida por computador. O estudo confirmou **3.224 unidades promissórias** (em 64 livros com registros catalogados e 4.373 versículos associados, equivalentes a 14,1% do corpus), das quais se estimam **2.945 promessas distintas estimadas** pelo agrupamento de similaridade lexical de Jaccard (limiar 0,45). O indicador principal de bênção divina soma **1.622 unidades confirmadas** e **1.481 promessas distintas estimadas**.

## Organização dos arquivos públicos
* `catalogo-digital-completo.csv` e `catalogo-digital-completo.xlsx`: Catálogo consolidado das 3.224 unidades promissórias confirmadas.
* `catalogo/<LIVRO>/`: 66 diretórios correspondentes aos livros do cânon (`<LIV>.jsonl`, `CATALOGO.md`, `CONTAGEM.md`, `cobertura.json`).
* `ARTIGO_CIENTIFICO_PROMESSAS_DA_BIBLIA.md`: Artigo científico bilíngue (português e inglês).
* `MEMORIA_DE_CALCULO.md`: Memória de cálculo aritmética e análise de sensibilidade.
* `RELATORIO_ORIGINALIDADE_CIENTIFICA.md`: Revisão bibliográfica e matriz comparativa do estado da arte.
* `DICIONARIO_DE_CAMPOS.md` e `RELATORIO_LIMITACOES.md`: Documentação das variáveis e limitações metodológicas.
* `DOCUMENTACAO_TECNICA_REPRODUTIBILIDADE.md`: Apêndice técnico para reprodução computacional dos resultados.
* `evidencias_arbitragem_fase3/`: Registros históricos dos 36 lotes da terceira etapa de arbitragem (`1.808` casos).
* `graficos/`: Gráficos analíticos em alta resolução (450 DPI `.png` e vetoriais `.svg`, em versões coloridas e escala de cinza).
* `docs/`: Portal institucional e catálogo interativo publicado no GitHub Pages.
* `scripts/` e `testes/`: Scripts Python de validação, consolidação, cálculo de similaridade e 77 testes controlados.

## Reprodução dos cálculos e testes
```bash
python -I testes/testes_erros_plantados.py
python -I scripts/apurar_numero.py
python -I scripts/memoria_de_calculo.py
```

## Licenças e direitos autorais
* **Scripts e código (`scripts/`, `testes/`, `docs/`):** MIT License (`LICENSE`) — Copyright (c) 2026 Jair Lima.
* **Metadados e catálogo analítico:** Creative Commons Attribution 4.0 International (`LICENSE-DATA`, CC BY 4.0).
* **Texto bíblico citado:** *Bíblia Almeida Livre by Jair Lima* (CC BY-ND 4.0).
* **Obra comercial:** O manuscrito e as edições do livro *As 3 Mil Promessas da Bíblia* (Lima Editora do Brasil, 2026) são privados e protegidos por direitos autorais.
