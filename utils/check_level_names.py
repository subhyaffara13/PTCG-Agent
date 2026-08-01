
def check_level_names(index, names):
    assert [level.name for level in index.levels] == list(names)

