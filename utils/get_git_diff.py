import subprocess

def get_git_diff(logic_candidate):
    diff_text = ""
    try:
        res = subprocess.run(["git", "diff", logic_candidate], capture_output=True, text=True)
        diff_text = res.stdout.strip()
        if not diff_text:
            res = subprocess.run(["git", "--no-pager", "diff", "--cached", logic_candidate], capture_output=True, text=True)
            diff_text = res.stdout.strip()
        if not diff_text:
            res = subprocess.run(["git", "--no-pager", "diff", "HEAD~1", "HEAD", "--", logic_candidate], capture_output=True, text=True)
            diff_text = res.stdout.strip()
    except Exception as git_e:
        logger.warning(f"Could not retrieve git diff for {logic_candidate}: {git_e}")
    return diff_text

