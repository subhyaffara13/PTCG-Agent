
def test_basic_codegen():
    numerical_tests = [
        ("test", (1.0, 6.0, 3.0), 21.0, 1e-15),
        ("test", (-1.0, 2.0, -2.5), -2.5, 1e-15),
    ]
    name_expr = [("test", (x + y)*z)]
    for lang, commands in valid_lang_commands:
        run_test("basic_codegen", name_expr, numerical_tests, lang, commands)

