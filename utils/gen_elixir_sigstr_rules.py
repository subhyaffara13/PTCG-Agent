
def gen_elixir_sigstr_rules(term, term_class, token, interpol=True):
    if interpol:
        return [
            (rf'[^#{term_class}\\]+', token),
            include('escapes'),
            (r'\\.', token),
            (rf'{term}[a-zA-Z]*', token, '#pop'),
            include('interpol')
        ]
    else:
        return [
            (rf'[^{term_class}\\]+', token),
            (r'\\.', token),
            (rf'{term}[a-zA-Z]*', token, '#pop'),
        ]

