"""build_submission.py — packages the promoted iteration into a Kaggle-ready .tar.gz"""
import tarfile, shutil, json
from pathlib import Path
from datetime import datetime

# 1. Sync the promoted deck_new.csv into submission/
promoted_deck = Path("staging/deck_new.csv")
shutil.copy2(promoted_deck, Path("submission/deck.csv"))
shutil.copy2(promoted_deck, Path("submission/cb_agents/deck_new.csv"))
print("Synced promoted deck.")

# 2. Write a manifest
manifest = {
    "built_at": datetime.now().isoformat(),
    "promoted_version": "v_20260618_081305",
    "version_score": 0.2487,
    "iteration": 28,
    "deck_file": "cb_agents/deck_new.csv",
}
(Path("submission") / "manifest.json").write_text(json.dumps(manifest, indent=2))
print("Wrote manifest.json")

# 3. Build .tar.gz — exclude PDFs, pyc, pycache, old agents/ mirror
tar_path = Path("submission_iter28_v0248.tar.gz")
with tarfile.open(tar_path, "w:gz") as tar:
    for f in sorted(Path("submission").rglob("*")):
        if not f.is_file():
            continue
        if "__pycache__" in str(f):
            continue
        if f.suffix in (".pyc", ".pdf"):
            continue
        # Skip the old agents/ mirror if it somehow exists
        if "submission/agents/" in str(f).replace("\\", "/"):
            continue
        arcname = str(f.relative_to("submission"))
        tar.add(f, arcname=arcname)
        print(f"  + {arcname}")

print(f"\nTar created: {tar_path}  ({tar_path.stat().st_size:,} bytes)")
