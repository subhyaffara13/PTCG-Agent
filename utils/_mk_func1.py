
def _mk_func1():
    declars = n, inp, out = Variable('n', integer), Pointer('inp', real), Pointer('out', real)
    i = Variable('i', integer)
    whl = While(i<n, [Assignment(out[i], inp[i]), PreIncrement(i)])
    body = CodeBlock(i.as_Declaration(value=0), whl)
    return FunctionDefinition(void, 'our_test_function', declars, body)

