import json
from pathlib import Path

def main():
    p = Path("scratch/validation_steps.json")
    if not p.exists():
        print("File not found")
        return
        
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    types = set()
    def find_select_types(obj):
        if isinstance(obj, dict):
            if "select" in obj and isinstance(obj["select"], dict):
                options = obj["select"].get("option", [])
                for opt in options:
                    if isinstance(opt, dict) and "type" in opt:
                        types.add(opt["type"])
            for k, v in obj.items():
                find_select_types(v)
        elif isinstance(obj, list):
            for item in obj:
                find_select_types(item)
                
    find_select_types(data)
    print(f"All unique option types in select prompts: {types}")

if __name__ == "__main__":
    main()
