# Lattes PPGCS-UFBA

**Análise dos currículos Lattes do Corpo Docente Permanente do Programa de Pós-Graduação em Ciências Sociais (PPGCS) da Universidade Federal da Bahia (UFBA)**

## 📊 Visão Geral

Este repositório contém a extração, consolidação e visualização dos dados dos currículos Lattes de **23 docentes permanentes** do PPGCS-UFBA, totalizando:

| Métrica | Total |
|---|---|
| Docentes permanentes | 23 |
| Doutores | 22 |
| Pós-doutorado | 19 |
| Projetos de pesquisa | 714 |
| Orientações concluídas | 1.658 |
| Bancas de avaliação | 1.070 |
| Citações (Google Scholar) | 834 |
| Artigos científicos | — |
| Livros publicados | — |
| Capítulos de livros | — |

## 🔧 Metodologia

1. **Coleta de IDs Lattes:** Scraping da página oficial do PPGCS ([ppgcs.ufba.br/pt-br/corpo-docente](https://ppgcs.ufba.br/pt-br/corpo-docente))
2. **Download dos currículos:** Extração automatizada via [scriptLattes](https://github.com/jpmenachalco/scriptLattes) com resolução de CAPTCHA via [2Captcha](https://2captcha.com)
3. **Consolidação:** Script Python para extrair métricas estruturadas de cada currículo JSON
4. **Visualização:** Página HTML interativa com cards, rankings, busca e ordenação

## 📁 Estrutura do Repositório

```
lattes_ppgcs/
├── data/
│   ├── raw/                    # JSONs originais extraídos do Lattes (23 arquivos)
│   └── processed/              # Dataset consolidado e lista de docentes
│       ├── ppgcs_dataset.json  # Dados estruturados de todos os docentes
│       └── ppgcs_docentes_list.json  # Lista com nome, email, ID Lattes
├── docs/
│   └── index.html              # Página de visualização interativa
├── scripts/
│   ├── batch_download_ppgcs.py # Script de download em lote
│   └── consolidate_ppgcs.py    # Script de consolidação de dados
├── assets/
│   └── labhd-logo.webp         # Logo do LABHD-UFBA
├── LICENSE                     # MIT
└── README.md                   # Este arquivo
```

## 📈 Visualização

A página interativa ([`docs/index.html`](docs/index.html)) oferece:

- **Barra de estatísticas** agregadas (docentes, projetos, orientações, citações)
- **Rankings** top-5 por citações, projetos e orientações
- **Busca** por nome, área de atuação ou tema
- **Ordenação** alfabética, por projetos, citações ou orientações
- **Cards individuais** com dados completos de cada docente
- **Links diretos** para os currículos Lattes

Para visualizar localmente:
```bash
# Abrir no navegador
xdg-open docs/index.html
# Ou servir localmente
python3 -m http.server 8000 -d docs/
```

## 🔄 Atualização dos Dados

Para re-executar a coleta de dados:

```bash
# 1. Baixar currículos (requer TWOCAPTCHA_API_KEY)
python3 scripts/batch_download_ppgcs.py

# 2. Consolidar dados
python3 scripts/consolidate_ppgcs.py

# 3. Verificar página
python3 -m http.server 8000 -d docs/
```

## 📅 Data de Atualização

**Última coleta:** Julho de 2026

Os dados dos currículos Lattes refletem o estado da Plataforma Lattes na data da coleta. Cada currículo individual mostra a data de última atualização informada pelo próprio docente.

## 🏛️ Sobre o PPGCS-UFBA

O Programa de Pós-Graduação em Ciências Sociais da UFBA oferece cursos de mestrado e doutorado, com linhas de pesquisa em Sociologia, Antropologia e Ciência Política. Mais informações em [ppgcs.ufba.br](https://ppgcs.ufba.br).

## 🧪 Sobre o LABHD-UFBA

Este projeto foi desenvolvido pelo **Laboratório de Humanidades Digitais da UFBA (LABHD-UFBA)**, que pesquisa as interfaces entre tecnologia digital, dados e ciências sociais, mantendo a maior coleção de traces digitais do Brasil para pesquisa acadêmica.

- 🌐 [labhdufba.github.io](https://labhdufba.github.io)
- 📧 leofn@ufba.br
- 🔬 GitHub: [@LABHDUFBA](https://github.com/LABHDUFBA)

## 📄 Licença

MIT License — veja [LICENSE](LICENSE).

## 📧 Contato

**Leonardo Fernandes Nascimento**  
PPGCS-UFBA / LABHD-UFBA  
leofn@ufba.br | [Lattes](http://lattes.cnpq.br/4785350J1)