import subprocess

def _run_git(args, **kwargs):
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    safe_cwd = os.path.dirname(repo_dir)
    git_args = ["git", "-C", repo_dir] + args[1:]
    env = os.environ.copy()
    if "SystemRoot" not in env:
        env["SystemRoot"] = r"C:\Windows"
    return subprocess.run(git_args, cwd=safe_cwd, env=env, **kwargs)


def _run_git(args, **kwargs):
    import os
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    safe_cwd = os.path.dirname(repo_dir)
    git_args = ["git", "-C", repo_dir] + args[1:]
    env = os.environ.copy()
    if "SystemRoot" not in env:
        env["SystemRoot"] = r"C:\Windows"
    return subprocess.run(git_args, cwd=safe_cwd, env=env, **kwargs)


def _run_git(args, **kwargs):
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    safe_cwd = os.path.dirname(repo_dir)
    git_args = ["git", "-C", repo_dir] + args[1:]
    env = os.environ.copy()
    if "SystemRoot" not in env:
        env["SystemRoot"] = r"C:\Windows"
    return subprocess.run(git_args, cwd=safe_cwd, env=env, **kwargs)

