
def disable_diag(diag_enum: Diagnostics) -> None:
    """
    Disable a global pyparsing diagnostic flag (see :class:`Diagnostics`).
    """
    __diag__.disable(diag_enum.name)

