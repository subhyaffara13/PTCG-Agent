
def _warn_for_string_literal(csource):
    if '"' not in csource:
        return
    for line in csource.splitlines():
        if '"' in line and not line.lstrip().startswith('#'):
            import warnings
            warnings.warn("String literal found in cdef() or type source. "
                          "String literals are ignored here, but you should "
                          "remove them anyway because some character sequences "
                          "confuse pre-parsing.")
            break

