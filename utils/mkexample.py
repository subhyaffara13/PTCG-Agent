
def mkexample(tmp_path_factory, name):
    basedir = tmp_path_factory.mktemp(name)
    jaraco.path.build(EXAMPLES[name], prefix=str(basedir))
    return basedir

