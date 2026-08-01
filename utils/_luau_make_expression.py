
def _luau_make_expression(should_pop, _s, _s_la):
    temp_list = [
        (r'0[xX][\da-fA-F_]*', Number.Hex, '#pop'),
        (r'0[bB][\d_]*', Number.Bin, '#pop'),
        (r'\.?\d[\d_]*(?:\.[\d_]*)?(?:[eE][+-]?[\d_]+)?', Number.Float, '#pop'),

        (words((
            'true', 'false', 'nil'
        ), suffix=r'\b'), Keyword.Constant, '#pop'),

        (r'\[(=*)\[[.\n]*?\]\1\]', String, '#pop'),

        (r'(\.)([a-zA-Z_]\w*)(?=%s*[({"\'])', bygroups(Punctuation, Name.Function), '#pop'),
        (r'(\.)([a-zA-Z_]\w*)', bygroups(Punctuation, Name.Variable), '#pop'),

        (rf'[a-zA-Z_]\w*(?:\.[a-zA-Z_]\w*)*(?={_s_la}*[({{"\'])', Name.Other, '#pop'),
        (r'[a-zA-Z_]\w*(?:\.[a-zA-Z_]\w*)*', Name, '#pop'),
    ]
    if should_pop:
        return temp_list
    return [entry[:2] for entry in temp_list]

