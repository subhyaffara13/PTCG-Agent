
def can_be_keyword(param: Parameter) -> bool:
    return param.kind in (Parameter.POSITIONAL_OR_KEYWORD, Parameter.KEYWORD_ONLY)

