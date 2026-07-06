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

# 1.5 Clean old target subfolders in submission/ to avoid packaging stale files
print("Cleaning old target directories in submission/...")
for folder in ("cb_agents", "router", "skills"):
    p = Path("submission") / folder
    if p.exists():
        shutil.rmtree(p)

# 2. Sync the promoted deck_new.csv from agents/ into submission/
promoted_deck = Path("agents/deck_new.csv")
if promoted_deck.exists():
    Path("submission").mkdir(parents=True, exist_ok=True)
    shutil.copy2(promoted_deck, Path("submission/deck.csv"))
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

# Copy the promoted deck inside the cb_agents directory as well
if promoted_deck.exists():
    shutil.copy2(promoted_deck, Path("submission/cb_agents/deck_new.csv"))

# 3.1 Sync all router files to submission/router and adjust imports
print("Syncing router files to submission/router...")
submission_router = Path("submission/router")
submission_router.mkdir(parents=True, exist_ok=True)
for f in Path("router").glob("*.py"):
    dest = submission_router / f.name
    shutil.copy2(f, dest)
    content = dest.read_text(encoding="utf-8")
    content = content.replace("from agents.", "from cb_agents.")
    content = content.replace("import agents.", "import cb_agents.")
    dest.write_text(content, encoding="utf-8")

# 3.2 Sync all skills files to submission/skills (excluding reference PDF)
print("Syncing skills files to submission/skills...")
submission_skills = Path("submission/skills")
submission_skills.mkdir(parents=True, exist_ok=True)
for f in Path("skills").glob("*"):
    if f.is_file() and f.suffix not in (".pdf", ".pyc"):
        dest = submission_skills / f.name
        shutil.copy2(f, dest)

# 3.3 Create package marker __init__.py files for all subpackages
print("Creating package markers (__init__.py)...")
for folder in ("cb_agents", "router", "skills"):
    (Path("submission") / folder / "__init__.py").touch(exist_ok=True)

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

# 3.4 Copy model weights checkpoint
weights_src = Path("m71.pt")
if weights_src.exists():
    weights_dest_dir = Path("submission/logs")
    weights_dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(weights_src, weights_dest_dir / "model_weights.pth")
    print("Bundled model weights checkpoint to submission/logs/model_weights.pth")
else:
    print("WARNING: m71.pt not found, skipping weights bundling!")

# 3.5 Sync C++ source files and build scripts for Kaggle compilation
print("Syncing C++ source files and build configurations for Kaggle compilation...")
submission_src = Path("submission/src")
submission_src.mkdir(parents=True, exist_ok=True)
for f in Path("src").glob("*"):
    if f.is_file():
        shutil.copy2(f, submission_src / f.name)
shutil.copy2("setup.py", "submission/setup.py")
if Path("CMakeLists.txt").exists():
    shutil.copy2("CMakeLists.txt", "submission/CMakeLists.txt")

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
        if f.suffix in (".pyc", ".pdf", ".pyd"):
            continue
        if "submission/agents/" in str(f).replace("\\", "/"):
            continue
        arcname = str(f.relative_to("submission"))
        tar.add(f, arcname=arcname)
        print(f"  + {arcname}")

print(f"\nTar created: {tar_path}  ({tar_path.stat().st_size:,} bytes)")
