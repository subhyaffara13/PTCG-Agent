import subprocess

def repo_context(
    url, branch: str | None = None, quiet: bool = True, dest_ctx=robust_temp_dir
):
    """
    Check out the repo indicated by url.

    If dest_ctx is supplied, it should be a context manager
    to yield the target directory for the check out.

    >>> getfixture('ensure_git')
    >>> getfixture('needs_internet')
    >>> repo = repo_context('https://github.com/jaraco/jaraco.context')
    >>> with repo as dest:
    ...     listing = os.listdir(dest)
    >>> 'README.rst' in listing
    True
    """
    exe = 'git' if 'git' in url else 'hg'
    with dest_ctx() as repo_dir:
        cmd = [exe, 'clone', url, repo_dir]
        cmd.extend(['--branch', branch] * bool(branch))
        stream = subprocess.DEVNULL if quiet else None
        subprocess.check_call(cmd, stdout=stream, stderr=stream)
        yield repo_dir

