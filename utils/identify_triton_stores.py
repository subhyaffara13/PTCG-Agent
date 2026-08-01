
def identify_triton_stores(source_code: str) -> TritonStores:
    """
    Parse Python source code of triton kernel and find all tl.store calls.
    Returns a TritonStores object containing information about pointer, value, and mask.

    tl.store signature: store(pointer, value, mask=None, boundary_check=(), ...)
    """
    return identify_triton_stores_from_ast(ast.parse(source_code))

