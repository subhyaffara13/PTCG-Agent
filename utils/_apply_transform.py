
def _apply_transform(
    s: cs.CoreSchema | None, func: Callable[[Any], Any], handler: GetCoreSchemaHandler
) -> cs.CoreSchema:
    if s is None:
        return cs.no_info_plain_validator_function(func)

    if s['type'] == 'str':
        if func is str.strip:
            s = s.copy()
            s['strip_whitespace'] = True
            return s
        elif func is str.lower:
            s = s.copy()
            s['to_lower'] = True
            return s
        elif func is str.upper:
            s = s.copy()
            s['to_upper'] = True
            return s

    return cs.no_info_after_validator_function(func, s)

