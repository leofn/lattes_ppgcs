# Currículos Lattes — PPGCS/UFBA

Análise dos currículos Lattes dos **docentes permanentes** do Programa de Pós-Graduação em Ciências Sociais (PPGCS) da Universidade Federal da Bahia (UFBA).

## 📊 Visão Geral

| Métrica | Valor |
|---|---|
| **Docentes permanentes** | 23 |
| **Currículos baixados** | 23/23 (100%) |
| **Perfis Google Scholar** | 10/23 (43%) |
| **Projetos de pesquisa** | 714 |
| **Orientações** | 1.658 |
| **Bancas** | 1.070 |
| **Citações Google Scholar** | 2.956 |
| **Data de coleta** | 04/07/2026 |
| **Última atualização dos CVs** | janeiro–julho/2026 |

## 🌐 Página

A página interativa está disponível em:

**[leofn.com/lattes\_ppgcs](https://leofn.com/lattes_ppgcs/)**

### Funcionalidades

- **Cards individuais** com nome, formação, áreas, resumo, link Lattes e Google Scholar
- **Rankings** por citações, projetos e orientações
- **Busca** por nome, área ou tema
- **Ordenação** por nome, projetos, citações ou orientações
- **Badges** de doutorado, pós-doutorado, h-index e data de atualização
- **Estatísticas agregadas** do programa

## 📁 Estrutura do Repositório

```
lattes_ppgcs/
├── docs/                           # GitHub Pages (página interativa)
│   ├── index.html                  # Dashboard principal
│   └── assets/
│       └── labhd-logo.webp         # Logo LABHD-UFBA
├── data/
│   ├── raw/                        # Currículos Lattes originais (JSON)
│   │   ├── K4765153H0.json         # Um arquivo por docente
│   │   └── ... (23 arquivos)
│   ├── processed/
│   │   └── ppgcs_dataset.json      # Dataset consolidado com métricas
│   └── external/
│       └── scholar_profiles.json   # Dados do Google Scholar
├── scripts/
│   ├── batch_download_ppgcs.py     # Download em lote via Selenium + 2Captcha
│   └── consolidate_ppgcs.py        # Consolidação e extração de métricas
├── docs/
│   └── index.html                  # Página GitHub Pages
└── README.md
```

## 🔬 Metodologia

### Coleta de Dados

1. **Scraping do corpo docente**: A lista de docentes permanentes foi extraída do site oficial do PPGCS ([ppgcs.ufba.br/pt-br/corpo-docente](https://ppgcs.ufba.br/pt-br/corpo-docente)), identificando nome, e-mail e ID Lattes de cada professor.

2. **Download dos currículos**: Cada currículo foi baixado da Plataforma Lattes (CNPq) usando Selenium WebDriver com resolução automática de CAPTCHA via API do 2Captcha. O processo gera um arquivo JSON estruturado por seção para cada docente.

3. **Google Scholar**: Perfis públicos foram buscados manualmente para cada docente. 10 dos 23 docentes possuem perfil público confirmado (com ID, citações, h-index e total de trabalhos).

### Processamento

- **Extração de métricas**: Contagem de projetos, orientações, bancas, artigos, livros e capítulos via análise de padrões textuais do conteúdo estruturado do Lattes.
- **Formação acadêmica**: Identificação de doutorado, pós-doutorado e instituição via regex sobre a seção "Formação".
- **Consolidação**: Todos os dados foram unificados em um dataset único (`ppgcs_dataset.json`) com métricas padronizadas.

## ⚠️ Sobre o Período dos Dados

**Os currículos Lattes contêm a trajetória completa do docente** — desde a graduação até a data da última atualização. Isso significa:

- **Formação**: dados desde a graduação (décadas de 1970–1990 para a maioria)
- **Produção bibliográfica**: artigos, livros e capítulos desde o início da carreira
- **Projetos**: todos os projetos cadastrados no Lattes (incluindo em andamento)
- **Orientações e bancas**: histórico completo desde a primeira orientação
- **Atualização**: cada CV foi atualizado pelo docente entre janeiro e julho de 2026

### Limitações

1. **Cobertura do Google Scholar**: 13 dos 23 docentes não possuem perfil público no Google Scholar. Isso não significa que não tenham citações — apenas que não criaram perfil público. Pesquisadores em Ciências Sociais no Brasil frequentemente não mantêm perfis no Scholar.

2. **Contagem de produções**: As métricas (projetos, artigos, orientações, bancas) são extraídas via análise textual do HTML do Lattes. O Lattes estrutura os dados em seções (Dados Gerais, Formação, Atuação Profissional, Projetos, Produções, Orientações, Bancas), mas o parsing automático pode subestimar o total real em alguns casos.

3. **IDs Lattes em formato antigo**: 5 docentes tinham IDs no formato antigo (ex: `P28594`, `B244`) no site do PPGCS. Os IDs corretos no formato numérico atual foram fornecidos manualmente.

## 🔧 Ferramentas Utilizadas

- **[scriptLattes](https://github.com/leofn/scriptLattes)**: Pipeline de download de currículos Lattes com Selenium + 2Captcha
- **Selenium WebDriver**: Automação do navegador para navegação no Lattes
- **2Captcha API**: Resolução de CAPTCHA (necessário para download de CVs)
- **Python 3.11**: Processamento e consolidação de dados
- **GitHub Pages**: Hospedagem da página interativa

## 🏛️ Créditos

**Laboratório de Humanidades Digitais da UFBA — [LABHD-UFBA](https://labhdufba.github.io/)**

Desenvolvido por **Leonardo Fernandes Nascimento** (LABHD-UFBA / PPGCS-UFBA)

### Fontes dos Dados

- [Plataforma Lattes](https://lattes.cnpq.br/) — CNPq
- [Google Scholar](https://scholar.google.com)
- [PPGCS/UFBA](https://ppgcs.ufba.br/pt-br/corpo-docente)

## 📄 Licença

MIT