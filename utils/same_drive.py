
def same_drive(*paths):
    return all_equal(pathlib.Path(path).drive for path in paths)

