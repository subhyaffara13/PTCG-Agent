
def deprecate_fun_eval():
    sympy_deprecation_warning(
        """
        The Tensor.fun_eval() method is deprecated. Use
        Tensor.substitute_indices() instead.
        """,
        deprecated_since_version="1.5",
        active_deprecations_target="deprecated-tensor-fun-eval",
        stacklevel=4,
    )

