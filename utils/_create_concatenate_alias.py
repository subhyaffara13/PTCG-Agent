import sys

def _create_concatenate_alias(origin, parameters):
    if parameters[-1] is ... and sys.version_info < (3, 9, 2):
        # Hack: Arguments must be types, replace it with one.
        parameters = (*parameters[:-1], _EllipsisDummy)
    if sys.version_info >= (3, 10, 3):
        concatenate = _ConcatenateGenericAlias(origin, parameters,
                                        _typevar_types=(TypeVar, ParamSpec),
                                        _paramspec_tvars=True)
    else:
        concatenate = _ConcatenateGenericAlias(origin, parameters)
    if parameters[-1] is not _EllipsisDummy:
        return concatenate
    # Remove dummy again
    concatenate.__args__ = tuple(p if p is not _EllipsisDummy else ...
                                    for p in concatenate.__args__)
    if sys.version_info < (3, 10):
        # backport needs __args__ adjustment only
        return concatenate
    concatenate.__parameters__ = tuple(p for p in concatenate.__parameters__
                                        if p is not _EllipsisDummy)
    return concatenate

