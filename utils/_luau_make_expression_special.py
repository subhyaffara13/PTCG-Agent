
def _luau_make_expression_special(should_pop):
    temp_list = [
        (r'\{', Punctuation, ('#pop', 'closing_brace_base', 'expression')),
        (r'\(', Punctuation, ('#pop', 'closing_parenthesis_base', 'expression')),

        (r'::?', Punctuation, ('#pop', 'type_end', 'type_start')),

        (r"'", String.Single, ('#pop', 'string_single')),
        (r'"', String.Double, ('#pop', 'string_double')),
        (r'`', String.Backtick, ('#pop', 'string_interpolated')),
    ]
    if should_pop:
        return temp_list
    return [(entry[0], entry[1], entry[2][1:]) for entry in temp_list]

