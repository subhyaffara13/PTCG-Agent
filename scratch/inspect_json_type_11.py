import json
from pathlib import Path

def find_type_11(obj, path="root"):
    if isinstance(obj, dict):
        if obj.get("type") == 11:
            print(f"Found type 11 option at {path}: {obj}")
        for k, v in obj.items():
            find_type_11(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            find_type_11(item, f"{path}[{idx}]")

def main():
    p = Path("scratch/validation_steps.json")
    if not p.exists():
        print("File not found")
        return
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    find_type_11(data)

if __name__ == "__main__":
    main()
