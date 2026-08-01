import os
import logging
from utils._run_git import _run_git

def get_local_version():
    try:
        repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        head_file = os.path.join(repo_dir, ".git", "HEAD")
        if os.path.exists(head_file):
            with open(head_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if content.startswith("ref:"):
                ref_relative = content.split(":", 1)[1].strip()
                ref_path = os.path.join(repo_dir, ".git", ref_relative)
                if os.path.exists(ref_path):
                    with open(ref_path, "r", encoding="utf-8") as rf:
                        commit_hash = rf.read().strip()
                        if len(commit_hash) >= 7:
                            return commit_hash
            elif len(content) >= 7 and all(c in "0123456789abcdefABCDEF" for c in content):
                return content
    except Exception:
        pass

    try:
        result = _run_git(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception as e:
        logging.warning(f"Git version fallback check skipped: {e}")
        return None
