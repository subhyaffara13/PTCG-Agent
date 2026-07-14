import os
import subprocess
import sys

# Try importing ptcg_core or loading DLLs
try:
    import ptcg_core
    print("Successfully imported ptcg_core")
except Exception as e:
    print(f"Failed to import ptcg_core: {e}")

def test():
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    safe_cwd = os.path.dirname(repo_dir)
    print(f"Repo dir: {repo_dir}")
    print(f"Safe cwd: {safe_cwd}")
    
    try:
        # Run with default cwd (which will be repo_dir if we are in it)
        print("Running default...")
        res1 = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True)
        print(f"Default result: {res1.stdout.strip()}")
    except Exception as e:
        print(f"Default failed: {e}")
        
    try:
        # Run with safe cwd
        print("Running with safe cwd and -C...")
        git_args = ['git', '-C', repo_dir, 'rev-parse', 'HEAD']
        res2 = subprocess.run(git_args, cwd=safe_cwd, capture_output=True, text=True, check=True)
        print(f"Safe result: {res2.stdout.strip()}")
    except Exception as e:
        print(f"Safe failed: {e}")

if __name__ == "__main__":
    test()
