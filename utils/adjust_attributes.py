
def adjust_attributes(token, replacements):
    needs_adjustment = viewkeys(token['data']) & viewkeys(replacements)
    if needs_adjustment:
        token['data'] = type(token['data'])((replacements.get(k, k), v)
                                            for k, v in token['data'].items())

