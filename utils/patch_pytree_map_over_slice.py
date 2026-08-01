
def patch_pytree_map_over_slice() -> Generator[None]:
    if slice in pytree.SUPPORTED_NODES:
        yield
        return

    pytree._private_register_pytree_node(
        slice, lambda x: ([x.start, x.stop, x.step], None), lambda x, c: slice(*x)
    )

    try:
        yield
    finally:
        pytree._deregister_pytree_node(slice)

