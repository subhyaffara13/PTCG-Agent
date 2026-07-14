from pathlib import Path

def main():
    p = Path(r"C:\Users\subhy\.gemini\antigravity\brain\ef81758f-268f-4938-a674-73dc184f884f\.system_generated\tasks\task-2477.log")
    if not p.exists():
        print("Log not found")
        return
        
    found = False
    with open(p, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            # Check for python traceback indicators or Agent execution crashed
            if "traceback" in line.lower() or "exception" in line.lower() or "crashed" in line.lower():
                # Exclude the known OpenSpiel warning about poker
                if "universal_poker" in line or "quoridor" in line:
                    continue
                print(f"L{line_num}: {line.strip()}")
                found = True
                
    if not found:
        print("No agent errors or tracebacks found in the log!")

if __name__ == "__main__":
    main()
