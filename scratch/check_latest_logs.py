import os
from pathlib import Path

def main():
    logs_dir = Path("logs")
    if not logs_dir.exists():
        print("logs/ not found")
        return
        
    files = sorted(
        [f for f in logs_dir.glob("**/*") if f.is_file()],
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )
    
    print("Newest 15 files in logs/:")
    for f in files[:15]:
        mtime = f.stat().st_mtime
        from datetime import datetime
        print(f"  {f}: {datetime.fromtimestamp(mtime)} ({f.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
