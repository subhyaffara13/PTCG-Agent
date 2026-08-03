import os

def groups_target(tmp_path):
    """
    Set up some older sources, a target, and newer sources.

    Returns a simple namespace with these values.
    """
    filenames = ['older.c', 'older.h', 'target.o', 'newer.c', 'newer.h']
    paths = [tmp_path / name for name in filenames]

    for mtime, path in enumerate(paths):
        path.write_text('', encoding='utf-8')

        # make sure modification times are sequential
        os.utime(path, (mtime, mtime))

    return types.SimpleNamespace(older=paths[:2], target=paths[2], newer=paths[3:])

