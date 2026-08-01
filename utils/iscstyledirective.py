
def iscstyledirective(f2py_line):
    directives = {"callstatement", "callprotoargument", "pymethoddef"}
    return any(directive in f2py_line.lower() for directive in directives)

