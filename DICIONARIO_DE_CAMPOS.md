# Dicionário de Campos do Catálogo (`DICIONARIO_DE_CAMPOS.md`)

| Campo (CSV / JSONL) | Tipo | Descrição e Valores Permitidos |
| :--- | :--- | :--- |
| `id` | `string` | Identificador canônico único da unidade promissória confirmada no formato `P-<LIVRO>-<NNNN>` (ex.: `P-GEN-0009`). |
| `livro` | `string` | Código internacional de 3 caracteres do livro bíblico (`GEN` a `REV`). |
| `referencia` / `ref_inicio`, `ref_fim` | `string` | Passagem bíblica de início e fim da unidade (ex.: `Gn 3.15` no CSV; `GEN 3:15` no JSONL). |
| `categoria` | `string` | Uma das 10 categorias taxonômicas finais (`divina_bencao`, `divina_juizo`, `divina_sentenca`, `apostolica_garantia_bencao`, `apostolica_garantia_juizo`, `patriarcal_bencao`, `patriarcal_juizo`, `humana_beneficio`, `humana_prejuizo`, `adversaria_ou_falsa`). |
| `origem_real` | `string` | Origem do compromisso: `divina_direta`, `divina_relatada_por_humano`, `apostolica_garantia`, `profetica_patriarcal`, `humana_em_nome_proprio`, `adversaria_ou_falsa`. |
| `natureza` | `string` | Polaridade da promessa: `bencao` (benefício/livramento) ou `juizo` (punição/prejuízo). |
| `objeto_prometido` / `resumo` | `string` | Síntese exegética em uma frase do conteúdo prometido (100% preenchido nos 3.224 registros). |
| `promitente` | `string` | Quem assume a obrigação do compromisso. Nas origens divinas e garantias apostólicas, é sempre divino (`pai`, `filho`, `espirito`, `deus_indistinto`, `mensageiro_autorizado`). |
| `comunicador` | `string` | Portador ou enunciador humano que relata, profetiza ou invoca uma promessa divina (ex.: `Isaías`, `Jeremias`, `Paulo`, `Moisés`, `todo o Israel` em 1Cr 11.2). No CSV, aparece ao lado do promitente no formato `Deus ... (comunicador: Nome)`. |
| `destinatario` / `destinatario_tipo` | `string` | A quem o compromisso é dirigido (`pessoa`, `familia_ou_linhagem`, `israel`, `igreja`, `igreja_local`, `grupo_especifico`, `crente_individual`, `nacoes_especificas`, `humanidade`, `criacao`, `messias`). |
| `condicao_tipo` | `string` | Presença de condicionalidade: `nenhuma`, `explicita` ou `contextual`. |
| `reforco` | `string` | Elemento solene de confirmação no texto: `nenhum`, `alianca`, `juramento` ou `sinal`. |
| `leituras` / `estado_de_validacao` | `string` | Via de confirmação: `2 leitores (acordo direto)` (1.211 unidades) ou `2 leitores + árbitro <Modelo>` (2.013 unidades). |
| `tratamento_no_livro`, `capitulo_principal` | `string` | Indica se a unidade é `abordada na narrativa` (601 unidades com versículos citados no corpo do livro *As 3 Mil Promessas da Bíblia*) ou por `associação temática` (2.623 unidades). |
