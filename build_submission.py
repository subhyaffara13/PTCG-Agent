"""build_submission.py — packages the promoted iteration into a Kaggle-ready .tar.gz"""
import tarfile
import shutil
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# 1. Build C++ extension in-place
print("Building C++ extension...")
try:
    subprocess.run([sys.executable, "setup.py", "build_ext", "--inplace"], check=True)
    print("C++ extension built successfully.")
except Exception as e:
    print(f"WARNING: C++ extension build failed: {e}")

# 2. Sync the promoted deck_new.csv from agents/ into submission/
promoted_deck = Path("agents/deck_new.csv")
if promoted_deck.exists():
    shutil.copy2(promoted_deck, Path("submission/deck.csv"))
    shutil.copy2(promoted_deck, Path("submission/cb_agents/deck_new.csv"))
    print("Synced promoted deck.")
else:
    print("WARNING: agents/deck_new.csv not found!")

# 3. Sync all agents to submission/cb_agents and adjust imports
print("Syncing agents to submission/cb_agents...")
submission_cb_agents = Path("submission/cb_agents")
submission_cb_agents.mkdir(parents=True, exist_ok=True)
for f in Path("agents").glob("*.py"):
    dest = submission_cb_agents / f.name
    shutil.copy2(f, dest)
    content = dest.read_text(encoding="utf-8")
    content = content.replace("from agents.", "from cb_agents.")
    content = content.replace("import agents.", "import cb_agents.")
    dest.write_text(content, encoding="utf-8")

# Copy C++ binaries (*.pyd, *.so) to submission/cb_agents/
for ext in ("*.pyd", "*.so"):
    for f in Path(".").glob(ext):
        if "ptcg_core" in f.name:
            dest = submission_cb_agents / f.name
            shutil.copy2(f, dest)
            print(f"Bundled extension: {f.name} -> {dest}")
            if f.suffix == ".so":
                try:
                    subprocess.run(["strip", "--strip-unneeded", str(dest)], check=False)
                    print(f"Stripped symbols from {dest.name}")
                except Exception as e:
                    pass

# 4. Load best version from history dynamically
history_file = Path("versions/version_history.json")
best_version, best_score, best_iter = "v_20260618_150827", 0.6522, "5580"
if history_file.exists():
    try:
        history = json.loads(history_file.read_text(encoding="utf-8"))
        promoted = [x for x in history if x.get("promoted")]
        if promoted:
            best_entry = max(promoted, key=lambda x: x.get("version_score", 0.0))
            best_version = best_entry.get("version_id", "unknown")
            best_score = best_entry.get("version_score", 0.0)
            best_iter = best_version
            print(f"Best promoted version: {best_version} with score {best_score}")
    except Exception as e:
        print(f"Error loading version history: {e}")

# Write a manifest
manifest = {
    "built_at": datetime.now().isoformat(),
    "promoted_version": best_version,
    "version_score": best_score,
    "iteration": best_iter,
    "deck_file": "cb_agents/deck_new.csv",
}
(Path("submission") / "manifest.json").write_text(json.dumps(manifest, indent=2))

# 5. Build .tar.gz — exclude PDFs, pyc, pycache, and include .pyd/.so
tar_path = Path("submission.tar.gz")
with tarfile.open(tar_path, "w:gz") as tar:
    for f in sorted(Path("submission").rglob("*")):
        if not f.is_file():
            continue
        if "__pycache__" in str(f):
            continue
        if f.suffix in (".pyc", ".pdf"):
            continue
        if "submission/agents/" in str(f).replace("\\", "/"):
            continue
        arcname = str(f.relative_to("submission"))
        tar.add(f, arcname=arcname)
        print(f"  + {arcname}")

print(f"\nTar created: {tar_path}  ({tar_path.stat().st_size:,} bytes)")
