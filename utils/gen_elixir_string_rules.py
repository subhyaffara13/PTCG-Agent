
def gen_elixir_string_rules(name, symbol, token):
    states = {}
    states['string_' + name] = [
        (rf'[^#{symbol}\\]+', token),
        include('escapes'),
        (r'\\.', token),
        (rf'({symbol})', bygroups(token), "#pop"),
        include('interpol')
    ]
    return states

