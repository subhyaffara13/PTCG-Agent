
def _no_nodes_error(arg: Argument) -> Never:
    raise RuntimeError(
        "Keys for dictionaries used as an argument cannot contain a "
        f"Node. Got key: {arg}"
    )

