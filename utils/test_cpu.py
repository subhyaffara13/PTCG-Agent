
def test_cpu():
    try:
        CppCodeCache.load("")
        return True
    except (
        CalledProcessError,
        OSError,
        torch._inductor.exc.InvalidCxxCompiler,
        torch._inductor.exc.CppCompileError,
    ):
        return False

