
def _relax_type_check_only_type(typ: mypy.types.ProperType) -> mypy.types.ProperType:
    return mypy.types.get_proper_type(typ.accept(_TYPE_CHECK_ONLY_BASE_MAPPER))

