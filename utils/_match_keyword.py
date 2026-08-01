
def _match_keyword(keyword):

    def matcher(value):
        if keyword in value:
            yield value

    return matcher

