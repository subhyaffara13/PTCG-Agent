from pathlib import Path

def main():
    p = Path("scratch/validation_steps.json")
    if not p.exists():
        print("File not found")
        return
        
    # Read the file and print lines matching type 11
    count = 0
    with open(p, "r", encoding="utf-8") as f:
        for line in f:
            if '"type": 11' in line:
                print(line.strip())
                count += 1
                if count >= 10:
                    break

if __name__ == "__main__":
    main()
