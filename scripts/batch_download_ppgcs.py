#!/usr/bin/env python3
"""Download em lote dos currículos Lattes dos docentes permanentes do PPGCS/UFBA."""

import json
import os
import sys
import time
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "output" / "ppgcs"
PYTHON_BIN = str(SCRIPT_DIR / "venv" / "bin" / "python3")
DOWNLOADER = str(SCRIPT_DIR / "lattes_downloader.py")
DOCENTES_FILE = SCRIPT_DIR / "ppgcs_docentes.json"

# Load env
env_path = os.path.expanduser("~/.hermes/.env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())

def main():
    with open(DOCENTES_FILE) as f:
        docentes = json.load(f)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    results = []
    total = len(docentes)
    
    for i, docente in enumerate(docentes, 1):
        nome = docente["nome"]
        lattes_id = docente["lattes_id"]
        print(f"\n{'='*60}")
        print(f"[{i}/{total}] {nome} — ID: {lattes_id}")
        print(f"{'='*60}")
        
        # Skip if already downloaded
        json_file = OUTPUT_DIR / f"{lattes_id}.json"
        if json_file.exists():
            print(f"  ⏭️  Já existe — pulando")
            results.append({"nome": nome, "id": lattes_id, "status": "skipped", "file": str(json_file)})
            continue
        
        cmd = [PYTHON_BIN, DOWNLOADER, lattes_id, "--output", str(OUTPUT_DIR)]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300, 
                                   env=os.environ.copy(), cwd=str(SCRIPT_DIR))
            if result.returncode == 0:
                print(f"  ✅ Sucesso!")
                # Verificar se JSON foi criado
                if json_file.exists():
                    size = json_file.stat().st_size
                    print(f"  📄 JSON: {size} bytes")
                    results.append({"nome": nome, "id": lattes_id, "status": "ok", "file": str(json_file), "size": size})
                else:
                    # Procurar qualquer JSON novo
                    jsons = list(OUTPUT_DIR.glob("*.json"))
                    if jsons:
                        latest = max(jsons, key=lambda f: f.stat().st_mtime)
                        print(f"  📄 JSON encontrado: {latest.name} ({latest.stat().st_size} bytes)")
                        results.append({"nome": nome, "id": lattes_id, "status": "ok", "file": str(latest), "size": latest.stat().st_size})
                    else:
                        print(f"  ⚠️  JSON não encontrado")
                        results.append({"nome": nome, "id": lattes_id, "status": "no_json"})
            else:
                print(f"  ❌ Erro (exit {result.returncode})")
                print(f"  stderr: {result.stderr[-300:] if result.stderr else 'N/A'}")
                results.append({"nome": nome, "id": lattes_id, "status": "error", "stderr": result.stderr[-500:] if result.stderr else ""})
        except subprocess.TimeoutExpired:
            print(f"  ⏱️ Timeout (5min)")
            results.append({"nome": nome, "id": lattes_id, "status": "timeout"})
        except Exception as e:
            print(f"  💥 Exception: {e}")
            results.append({"nome": nome, "id": lattes_id, "status": "exception", "error": str(e)})
        
        # Pequena pausa entre downloads para não saturar
        if i < total:
            time.sleep(3)
    
    # Salvar resumo
    summary_file = OUTPUT_DIR / "_batch_summary.json"
    with open(summary_file, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Relatório final
    ok = sum(1 for r in results if r["status"] in ("ok", "skipped"))
    errors = sum(1 for r in results if r["status"] not in ("ok", "skipped"))
    print(f"\n{'='*60}")
    print(f"RESUMO: {ok} OK / {errors} erros / {total} total")
    print(f"Arquivos em: {OUTPUT_DIR}")
    print(f"Resumo: {summary_file}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()