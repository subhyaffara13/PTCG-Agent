import os

def _addsitedirs(new_dirs):
    """To use this function, it is necessary to insert new_dir in front of sys.path.
    The Python process will try to import a ``sitecustomize`` module on startup.
    If we manipulate sys.path/PYTHONPATH, we can force it to run our code,
    which invokes ``addsitedir`` and ensure ``.pth`` files are loaded.
    """
    content = '\n'.join(
        ("import site",)
        + tuple(f"site.addsitedir({os.fspath(new_dir)!r})" for new_dir in new_dirs)
    )
    (new_dirs[0] / "sitecustomize.py").write_text(content, encoding="utf-8")

