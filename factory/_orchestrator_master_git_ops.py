import subprocess
import os
from pathlib import Path

def _run_git(args, **kwargs):
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    safe_cwd = os.path.dirname(repo_dir)
    git_args = ["git", "-C", repo_dir] + args[1:]
    env = os.environ.copy()
    if "SystemRoot" not in env:
        env["SystemRoot"] = r"C:\Windows"
    return subprocess.run(git_args, cwd=safe_cwd, env=env, **kwargs)

def check_files_changed(target_files):
    files_to_add = []
    for file_str in target_files:
        p = Path(file_str)
        if p.exists():
            res = _run_git(["git", "status", "--porcelain", file_str], capture_output=True, text=True)
            if res.stdout.strip():
                files_to_add.append(file_str)
    return files_to_add

def handle_push_failure():
    import logging
    logger = logging.getLogger("orchestrator_master_git")
    try:
        _run_git(["git", "pull", "--rebase"], check=True, capture_output=True, text=True)
        _run_git(["git", "push"], check=True, capture_output=True, text=True)
        logger.info("Factory updates rebased and pushed successfully.")
    except Exception as rebase_err:
        logger.error(f"Git rebase/push recovery failed: {rebase_err}")
        raise

def fix_git_lock():
    import os
    for lock_file in [".git/index.lock", ".git/FETCH_HEAD.lock"]:
        if os.path.exists(lock_file):
            try:
                os.remove(lock_file)
            except Exception:
                pass
