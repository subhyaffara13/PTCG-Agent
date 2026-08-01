
def _warn_complex_not_supported():
    warnings.warn(
        "Torchinductor does not support code generation for complex operators. Performance may be worse than eager."
    )

