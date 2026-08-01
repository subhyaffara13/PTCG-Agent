
def get_keywords():
    """Get the keywords needed to look up the version information."""
    # these strings will be replaced by git during git-archive.
    # setup.py/versioneer.py will grep for the variable names, so they must
    # each be defined on a line of their own. _version.py will just call
    # get_keywords().
    git_refnames = " (HEAD, tag: v3.0.3, origin/3.0.x)"
    git_full = "72f2fea91530b5abb3cf2100cb22d84e504695c0"
    git_date = "2026-05-11 18:18:35 +0200"
    keywords = {"refnames": git_refnames, "full": git_full, "date": git_date}
    return keywords

