from pathlib import Path


def check_files_changed(target_files):
    files_to_add = []
    for file_str in target_files:
        p = Path(file_str)
        if p.exists():
            res = _run_git(["git", "status", "--porcelain", file_str], capture_output=True, text=True)
            if res.stdout.strip():
                files_to_add.append(file_str)
    return files_to_add

