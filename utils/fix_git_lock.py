
def fix_git_lock():
    import os
    for lock_file in [".git/index.lock", ".git/FETCH_HEAD.lock"]:
        if os.path.exists(lock_file):
            try:
                os.remove(lock_file)
            except Exception:
                pass

