
def test_ccode_codegen_ast():
    # Note that C only allows comments of the form /* ... */, double forward
    # slash is not standard C, and some C compilers will grind to a halt upon
    # encountering them.
    assert ccode(Comment("this is a comment")) == "/* this is a comment */"  # not //
    assert ccode(While(abs(x) > 1, [aug_assign(x, '-', 1)])) == (
        'while (fabs(x) > 1) {\n'
        '   x -= 1;\n'
        '}'
    )
    assert ccode(Scope([AddAugmentedAssignment(x, 1)])) == (
        '{\n'
        '   x += 1;\n'
        '}'
    )
    inp_x = Declaration(Variable(x, type=real))
    assert ccode(FunctionPrototype(real, 'pwer', [inp_x])) == 'double pwer(double x)'
    assert ccode(FunctionDefinition(real, 'pwer', [inp_x], [Assignment(x, x**2)])) == (
        'double pwer(double x){\n'
        '   x = pow(x, 2);\n'
        '}'
    )

    # Elements of CodeBlock are formatted as statements:
    block = CodeBlock(
        x,
        Print([x, y], "%d %d"),
        Print([QuotedString('hello'), y], "%s %d", file=stderr),
        FunctionCall('pwer', [x]),
        Return(x),
    )
    assert ccode(block) == '\n'.join([
        'x;',
        'printf("%d %d", x, y);',
        'fprintf(stderr, "%s %d", "hello", y);',
        'pwer(x);',
        'return x;',
    ])

