
def count_meta_path(venv, env=None):
    py_cmd = textwrap.dedent(
        """
        import sys
        is_distutils = lambda finder: finder.__class__.__name__ == "DistutilsMetaFinder"
        print(len(list(filter(is_distutils, sys.meta_path))))
        """
    )
    cmd = ['python', '-c', py_cmd]
    return int(venv.run(cmd, env=win_sr(env), **_TEXT_KWARGS))

