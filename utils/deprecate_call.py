
def deprecate_call():
    sympy_deprecation_warning(
        """
        Calling a tensor like Tensor(*indices) is deprecated. Use
        Tensor.substitute_indices() instead.
        """,
        deprecated_since_version="1.5",
        active_deprecations_target="deprecated-tensor-fun-eval",
        stacklevel=4,
    )

