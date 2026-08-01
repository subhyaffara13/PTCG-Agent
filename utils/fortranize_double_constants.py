
def fortranize_double_constants(code_string):
    """
    Replaces every literal float with literal doubles
    """
    import re
    pattern_exp = re.compile(r'\d+(\.)?\d*[eE]-?\d+')
    pattern_float = re.compile(r'\d+\.\d*(?!\d*d)')

    def subs_exp(matchobj):
        return re.sub('[eE]', 'd', matchobj.group(0))

    def subs_float(matchobj):
        return "%sd0" % matchobj.group(0)

    code_string = pattern_exp.sub(subs_exp, code_string)
    code_string = pattern_float.sub(subs_float, code_string)

    return code_string

