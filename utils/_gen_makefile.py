
def _gen_makefile(root, contents):
    jaraco.path.build({'Makefile': trim(contents)}, root)
    return root / 'Makefile'

