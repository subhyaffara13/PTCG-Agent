
def is_storage_and_layout(x: IRNode) -> bool:
    try:
        as_storage_and_layout(x, freeze=False)
        return True
    except NotImplementedError:
        return False

