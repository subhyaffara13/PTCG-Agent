import os

def is_project_root(test_dir='.'):
    makefile = os.path.join(test_dir, MAKEFILE)
    include = os.path.join(test_dir, INCLUDE)
    single_include = os.path.join(test_dir, SINGLE_INCLUDE)

    return (os.path.exists(makefile)
            and os.path.isfile(makefile)
            and os.path.exists(include)
            and os.path.exists(single_include))

