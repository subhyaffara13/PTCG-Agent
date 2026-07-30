import os
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI

# Initialize the OpenAI client.
# Assuming the user has OPENAI_API_KEY in their environment (from MCP config).
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_codebase_files():
    files = []
    for ext in ["*.py", "*.cpp", "*.h"]:
        files.extend(list(Path("factory").rglob(ext)))
        files.extend(list(Path("src").rglob(ext)))
    return files

def read_files_in_batches(files, max_chars=30000):
    batches = []
    current_batch = ""
    for f in files:
        try:
            content = f.read_text(encoding="utf-8")
            chunk = f"\n\n--- FILE: {f} ---\n{content}"
            if len(current_batch) + len(chunk) > max_chars:
                batches.append(current_batch)
                current_batch = chunk
            else:
                current_batch += chunk
        except Exception:
            pass
    if current_batch:
        batches.append(current_batch)
    return batches

def agent_1_architect(code_chunk):
    """Architecture & Dependencies Subagent"""
    prompt = (
        "You are Subagent 1: Architectural Lead for a PTCG (Pokémon Trading Card Game) AI.\n"
        "Your task is to review the following code and look specifically for:\n"
        "1. Circular imports or dependencies.\n"
        "2. Improper exports or redundant definitions (e.g. C++ Pybind modules).\n"
        "3. Anything that isn't up to par with a 'perfect' system architecture.\n"
        "Be concise. If you find nothing critical, just say 'No major architectural issues found.'\n\n"
        f"CODE:\n{code_chunk}"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Agent 1 Error: {e}"

def agent_2_resilience(code_chunk):
    """Resilience & Logic Subagent"""
    prompt = (
        "You are Subagent 2: Resilience & Logic Lead for a PTCG AI.\n"
        "Your task is to review the following code and look specifically for:\n"
        "1. Missing error catches (e.g., bare try-except, missing try-except on IO/network).\n"
        "2. Circular loops or logic that might cause crashes.\n"
        "3. Anything that isn't up to par with a 'perfect' robust system.\n"
        "Be concise. If you find nothing critical, just say 'No major logic/resilience issues found.'\n\n"
        f"CODE:\n{code_chunk}"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Agent 2 Error: {e}"

def main():
    print("Collecting files...")
    files = get_codebase_files()
    
    # Process a few batches for efficiency to not blow up API costs
    batches = read_files_in_batches(files)[:3]
    
    print(f"Running LLM audit on {len(batches)} batches...")
    report = []
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        for i, batch in enumerate(batches):
            print(f"Dispatching Batch {i+1}...")
            future1 = executor.submit(agent_1_architect, batch)
            future2 = executor.submit(agent_2_resilience, batch)
            
            report.append(f"### Batch {i+1}\n")
            report.append(f"**Agent 1 (Architecture):**\n{future1.result()}\n")
            report.append(f"**Agent 2 (Resilience):**\n{future2.result()}\n")
            
    # Save the report to artifacts
    report_path = r"C:\Users\subhy\.gemini\antigravity-ide\brain\6cb59a4d-8fcc-45d4-b8d7-47815660574e\llm_audit_summary.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# LLM Subagent Audit Report\n\n" + "\n".join(report))
        
    print(f"Audit complete. Report saved to {report_path}")

if __name__ == "__main__":
    main()
