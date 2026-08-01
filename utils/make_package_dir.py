
def make_package_dir(name, base_dir, ns=False):
    dir_package = base_dir
    for dir_name in name.split('/'):
        dir_package = dir_package.mkdir(dir_name)
    init_file = None
    if not ns:
        init_file = dir_package.join('__init__.py')
        init_file.write('')
    return dir_package, init_file

