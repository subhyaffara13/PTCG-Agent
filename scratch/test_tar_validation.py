import os
import sys
import shutil
import tarfile
from pathlib import Path

def main():
    print("==================================================")
    print("ISOLATED VALIDATION OF submission.tar.gz")
    print("==================================================")

    # 1. Clean and create extraction directory
    extract_dir = Path("scratch/test_tar_extract")
    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    extract_dir.mkdir(parents=True, exist_ok=True)

    # 2. Extract tar.gz
    tar_path = Path("submission.tar.gz")
    if not tar_path.exists():
        print("Error: submission.tar.gz not found.")
        return

    print("Extracting submission.tar.gz...")
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(extract_dir)

    # 3. Verify files
    print("\nExtracted files:")
    for p in sorted(extract_dir.rglob("*")):
        if p.is_file():
            print(f"  - {p.relative_to(extract_dir)}")

    # 4. Isolate sys.path
    original_path = sys.path.copy()
    
    # We want to import from scratch/test_tar_extract
    sys.path.insert(0, str(extract_dir.resolve()))
    
    # Remove the main workspace root from sys.path
    cwd = os.path.abspath(os.getcwd())
    sys.path = [p for p in sys.path if os.path.abspath(p) != cwd]

    # 5. Try importing main
    print("\nAttempting to import agent from main...")
    try:
        # Clear modules that could be cached
        for m in list(sys.modules.keys()):
            if m == "main" or m.startswith("cb_agents") or m.startswith("router"):
                del sys.modules[m]

        import main
        print("Import of main succeeded!")
        
        # Check DEFAULT_DECK
        deck = getattr(main, "DEFAULT_DECK", None)
        print(f"DEFAULT_DECK length: {len(deck) if deck else 'None'}")
        
        # Run local test steps using kaggle_environments
        from kaggle_environments import make
        env = make("cabt", debug=True)
        print("Running isolated 5-step simulation...")
        agent_path = str((extract_dir / "main.py").resolve())
        env.run([agent_path, agent_path])
        
        # Print statuses and errors
        print("\nFull steps details:")
        for idx, step in enumerate(env.steps):
            print(f"Step {idx}:")
            for p_idx, player in enumerate(step):
                print(f"  Player {p_idx}: {player}")
        
        print("\nEnvironment logs:")
        if hasattr(env, "logs"):
            print(env.logs)
        else:
            print("No env.logs attribute.")

    except Exception as e:
        print("\nCRITICAL: Import or run failed!")
        import traceback
        traceback.print_exc()

    finally:
        sys.path = original_path

if __name__ == "__main__":
    main()
