
def _same_path(path1: pathops.Path, path2: pathops.Path) -> bool:
    return {tuple(c) for c in path1.contours} == {tuple(c) for c in path2.contours}

