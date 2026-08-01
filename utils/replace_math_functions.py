
def replace_math_functions(input_string):
    """FIXME: Temporarily replace std:: invocations of math functions
        with non-std:: versions to prevent linker errors NOTE: This
        can lead to correctness issues when running tests, since the
        correct version of the math function (exp/expf) might not get
        called.  Plan is to remove this function once HIP supports
        std:: math function calls inside device code

    """
    output_string = input_string
    for func in MATH_TRANSPILATIONS:
        output_string = output_string.replace(fr'{func}(', f'{MATH_TRANSPILATIONS[func]}(')

    return output_string

