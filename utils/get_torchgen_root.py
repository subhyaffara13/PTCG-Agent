
def get_torchgen_root() -> Path:
    """
    If you're depending on torchgen out-of-tree, you can use the root to figure
    out the path to native_functions.yaml
    """
    return Path(__file__).parent.resolve()

