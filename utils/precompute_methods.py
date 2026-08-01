
def precompute_methods(obj: Any, methods: list[str]) -> None:
    """Replace methods with new methods that returns a precomputed constants."""
    for method in methods:
        precompute_method(obj, method)

