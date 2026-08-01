
def _expand_text_props(props):
    props = cbook.normalize_kwargs(props, mtext.Text)
    return cycler(**props)() if props else itertools.repeat({})

