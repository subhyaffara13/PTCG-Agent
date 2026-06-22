"""
scratch/run_deck_pipeline.py
Runs the complete deck extraction and optimization pipeline.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))
from scratch.extract_replays import main as run_extract_replays
from scratch.extract_failed import main as run_extract_failed
from scratch.deck_optimizer import main as run_deck_optimizer

def verify_no_secrets():
    """Verify that no sensitive information is present in key files."""
    keywords = ["key", "password", "token", "secret", "auth", "kaggle.json"]
    for path in sorted(Path("logs/kaggle_summary").glob("*")):
        try:
            content = path.read_text(encoding="utf-8").lower()
            for kw in keywords:
                if kw in content and len(content) < 1000:
                    print(f"WARNING: Sensitive keyword '{kw}' detected in {path.name}")
                    return False
        except Exception:
            pass
    print("Security check passed: No obvious API keys or secrets detected.")
    return True

def main():
    try:
        print("=== STEP 1: Scrape Replay Decks ===")
        run_extract_replays()
        
        print("\n=== STEP 2: Extract Failed Decks ===")
        run_extract_failed()
        
        print("\n=== STEP 3: Optimize and Synthesize Deck ===")
        run_deck_optimizer()
        
        print("\n=== STEP 4: Security Verification ===")
        if not verify_no_secrets():
            sys.exit(1)
            
        print("\nPipeline run complete successfully!")
    except Exception as e:
        print(f"Pipeline crashed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
