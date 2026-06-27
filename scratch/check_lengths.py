import glob
from pathlib import Path

def main():
    dirs = ['agents', 'factory', 'router', 'scratch']
    for d in dirs:
        print(f"\n--- Directory: {d} ---")
        files = sorted(glob.glob(f"{d}/**/*.py", recursive=True))
        for f in files:
            path = Path(f)
            if path.is_file():
                try:
                    lines = len(path.read_text(encoding='utf-8').splitlines())
                    if lines > 100:
                        print(f"[OVER 100] {f}: {lines} lines")
                    else:
                        print(f"  {f}: {lines} lines")
                except Exception as e:
                    print(f"  Error reading {f}: {e}")

if __name__ == '__main__':
    main()
