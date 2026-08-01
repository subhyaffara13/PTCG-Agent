
def dontGenerateOpCheckTests(reason: str):
    def inner(fun):
        fun._torch_dont_generate_opcheck_tests = True
        return fun

    return inner

