
def _convert_to_stringdtype_kwargs(coerce, na_object=_NoValue):
    if na_object is _NoValue:
        return StringDType(coerce=coerce)
    return StringDType(coerce=coerce, na_object=na_object)

