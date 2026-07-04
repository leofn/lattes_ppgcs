#!/usr/bin/env python3
"""Consolida os 23 currículos Lattes do PPGCS em um dataset único para análise."""

import json
import re
from pathlib import Path
from collections import Counter

OUTPUT_DIR = Path("/home/hermes/scriptLattes/output/ppgcs")
DOCENTES_FILE = Path("/home/hermes/scriptLattes/ppgcs_docentes.json")

with open(DOCENTES_FILE) as f:
    docentes = json.load(f)

# Mapear cada docente ao seu arquivo JSON correto
def find_json(lattes_id):
    """Encontra o arquivo JSON correto para um docente."""
    # Tentar arquivo direto
    jf = OUTPUT_DIR / f"{lattes_id}.json"
    if jf.exists():
        data = json.loads(jf.read_text())
        if data.get("nome") and data["nome"] != "N/A":
            return jf, data
    # Buscar em todos os arquivos
    for jf in sorted(OUTPUT_DIR.glob("*.json")):
        if jf.name.startswith("_"):
            continue
        data = json.loads(jf.read_text())
        sid = data.get("short_id", "")
        lid = data.get("lattes_id", "")
        if sid == lattes_id or lid == lattes_id:
            return jf, data
    return None, None

def extract_metrics(data, docente_info):
    """Extrai métricas-chave do JSON do Lattes."""
    metrics = {}
    
    # Campos estruturados
    metrics["nome"] = data.get("nome", docente_info.get("nome", "N/A"))
    metrics["nome_site"] = docente_info.get("nome", "")
    metrics["email"] = docente_info.get("email", "")
    metrics["lattes_url"] = f"http://lattes.cnpq.br/{docente_info.get('lattes_id', '')}"
    metrics["id_lattes"] = data.get("lattes_id", data.get("id_lattes", ""))
    metrics["short_id"] = data.get("short_id", "")
    metrics["ultima_atualizacao"] = data.get("ultima_atualizacao", "")
    
    # Resumo
    resumo = data.get("resumo", "")
    metrics["resumo"] = resumo[:800] if resumo else ""
    
    # Formação
    formacao = data.get("formacao_academica", "")
    metrics["formacao"] = formacao[:2000] if formacao else ""
    
    # Extrair graus
    metrics["doutorado"] = bool(re.search(r'Doutorado', formacao, re.I))
    metrics["pos_doutorado"] = bool(re.search(r'Pós-doutorado|Pós-Doutorado|Post-doctoral|Postdoctoral', formacao, re.I))
    metrics["mestrado"] = bool(re.search(r'Mestrado', formacao, re.I))
    
    # Áreas de atuação
    areas = data.get("areas_atuacao", "")
    metrics["areas"] = areas[:800] if areas else ""
    
    # Linhas de pesquisa
    linhas = data.get("linhas_pesquisa", "")
    metrics["linhas_pesquisa"] = linhas[:1500] if linhas else ""
    
    # Produções
    prod = data.get("producoes", "")
    metrics["producoes"] = prod[:5000] if prod else ""
    
    # Google Scholar
    scholar = re.search(r'Total de trabalhos:\s*(\d+).*?Total de citações:\s*(\d+)', prod, re.DOTALL)
    if scholar:
        metrics["scholar_trabalhos"] = int(scholar.group(1))
        metrics["scholar_citacoes"] = int(scholar.group(2))
    else:
        metrics["scholar_trabalhos"] = 0
        metrics["scholar_citacoes"] = 0
    
    # Contar tipos de produção
    metrics["num_artigos"] = len(re.findall(r'Artigos completos publicados em periódicos', prod))
    metrics["num_livros"] = len(re.findall(r'Livros publicados/organizados', prod))
    metrics["num_capitulos"] = len(re.findall(r'Capítulos de livros publicados', prod))
    metrics["num_textos_midia"] = len(re.findall(r'Textos em jornais|Textos em revistas|Textos em sites', prod))
    
    # Projetos
    proj = data.get("projetos_pesquisa", "")
    metrics["projetos"] = proj[:3000] if proj else ""
    metrics["num_projetos"] = len(re.findall(r'(?:20\d{2}|19\d{2})\s*-\s*(?:Atual|\d{2,4})', proj))
    
    # Projetos de extensão
    proj_ext = data.get("projetos_extensao", "")
    metrics["num_projetos_extensao"] = len(re.findall(r'(?:20\d{2}|19\d{2})\s*-\s*(?:Atual|\d{2,4})', proj_ext)) if proj_ext else 0
    
    # Projetos de desenvolvimento
    proj_dev = data.get("projetos_desenvolvimento", "")
    metrics["num_projetos_dev"] = len(re.findall(r'(?:20\d{2}|19\d{2})\s*-\s*(?:Atual|\d{2,4})', proj_dev)) if proj_dev else 0
    
    # Orientações
    orient = data.get("orientacoes", "")
    metrics["orientacoes"] = orient[:3000] if orient else ""
    metrics["num_orient_doutorado"] = len(re.findall(r'Tese de doutorado', orient))
    metrics["num_orient_mestrado"] = len(re.findall(r'Dissertação de mestrado|Dissertação \(Mestrado', orient))
    metrics["num_orient_ic"] = len(re.findall(r'Iniciação científica', orient, re.I))
    metrics["num_orient_tcc"] = len(re.findall(r'TCC|Trabalho de conclusão', orient, re.I))
    metrics["num_orient_total"] = metrics["num_orient_doutorado"] + metrics["num_orient_mestrado"] + metrics["num_orient_ic"] + metrics["num_orient_tcc"]
    
    # Bancas
    bancas = data.get("bancas", "")
    metrics["bancas"] = bancas[:1500] if bancas else ""
    metrics["num_bancas_doutorado"] = len(re.findall(r'Tese de doutorado', bancas))
    metrics["num_bancas_mestrado"] = len(re.findall(r'Dissertação de mestrado|Dissertação \(Mestrado', bancas))
    metrics["num_bancas_total"] = metrics["num_bancas_doutorado"] + metrics["num_bancas_mestrado"]
    
    # Eventos
    eventos = data.get("eventos", "")
    metrics["eventos"] = eventos[:1000] if eventos else ""
    
    # Prêmios
    premios = data.get("premios_titulos", "")
    metrics["premios"] = premios[:500] if premios else ""
    
    # Idiomas
    idiomas = data.get("idiomas", "")
    metrics["idiomas"] = idiomas[:400] if idiomas else ""
    
    # Atuação profissional
    atuacao = data.get("atuacao_profissional", "")
    metrics["atuacao"] = atuacao[:2000] if atuacao else ""
    
    # Inovação
    inovacao = data.get("inovacao", "")
    metrics["inovacao"] = inovacao[:500] if inovacao else ""
    
    # Educação e popularização
    educ = data.get("educacao_popularizacao", "")
    metrics["educacao"] = educ[:1000] if educ else ""
    
    # Seções
    metrics["secoes"] = data.get("_sections_found", [])
    metrics["num_secoes"] = len(metrics["secoes"])
    
    # Full text length
    metrics["full_text_len"] = len(data.get("_full_text", ""))
    
    return metrics


# Consolidar
dataset = []
for d in docentes:
    jf, data = find_json(d["lattes_id"])
    if data:
        metrics = extract_metrics(data, d)
        metrics["nome_site"] = d["nome"]
        metrics["email"] = d["email"]
        metrics["lattes_url"] = f"http://lattes.cnpq.br/{d['lattes_id']}"
        metrics["arquivo"] = jf.name if jf else ""
        dataset.append(metrics)
        print(f"OK  {d['nome'][:35]:35s} | {metrics['num_secoes']:2d} sec | {metrics['full_text_len']:6d} chars | {metrics['num_projetos']:3d} proj | {metrics['num_orient_total']:3d} orient | {metrics['scholar_citacoes']:4d} cit")
    else:
        print(f"ERR {d['nome'][:35]:35s} | NAO ENCONTRADO")

# Salvar dataset consolidado
out_file = OUTPUT_DIR / "ppgcs_dataset.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

print(f"\nDataset salvo: {out_file}")
print(f"Total: {len(dataset)} docentes")

# Estatísticas agregadas
print(f"\n=== ESTATÍSTICAS ===")
total_secoes = sum(d["num_secoes"] for d in dataset)
total_projetos = sum(d["num_projetos"] for d in dataset)
total_orient = sum(d["num_orient_total"] for d in dataset)
total_bancas = sum(d["num_bancas_total"] for d in dataset)
total_citacoes = sum(d["scholar_citacoes"] for d in dataset)
total_artigos = sum(d["num_artigos"] for d in dataset)
total_text = sum(d["full_text_len"] for d in dataset)
print(f"Total seções: {total_secoes}")
print(f"Total projetos: {total_projetos}")
print(f"Total orientações: {total_orient}")
print(f"Total bancas: {total_bancas}")
print(f"Total texto (chars): {total_text:,}")
print(f"Média seções/docente: {total_secoes/len(dataset):.1f}")
print(f"Média projetos/docente: {total_projetos/len(dataset):.1f}")
print(f"Média orientações/docente: {total_orient/len(dataset):.1f}")