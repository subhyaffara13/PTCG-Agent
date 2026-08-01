
def normalise_package_base(root: str) -> str:
    if not root:
        root = os.curdir
    root = os.path.abspath(root)
    if root.endswith(os.sep):
        root = root[:-1]
    return root

