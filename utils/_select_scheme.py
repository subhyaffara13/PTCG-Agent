
def _select_scheme(ob, name):
    scheme = _inject_headers(name, _load_scheme(_resolve_scheme(name)))
    vars(ob).update(_remove_set(ob, _scheme_attrs(scheme)))

