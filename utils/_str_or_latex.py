
def _str_or_latex(label):
    if isinstance(label, Basic):
        return latex(label, mode='inline')
    return str(label)

