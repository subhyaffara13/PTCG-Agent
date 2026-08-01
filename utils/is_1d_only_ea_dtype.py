
def is_1d_only_ea_dtype(dtype: DtypeObj | None) -> bool:
    """
    Analogue to is_extension_array_dtype but excluding DatetimeTZDtype.
    """
    return isinstance(dtype, ExtensionDtype) and not dtype._supports_2d

