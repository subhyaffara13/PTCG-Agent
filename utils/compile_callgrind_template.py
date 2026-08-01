
def compile_callgrind_template(*, stmt: str, setup: str, global_setup: str) -> str:
    template_path: str = os.path.join(SOURCE_ROOT, "valgrind_wrapper", "timer_callgrind_template.cpp")
    with open(template_path) as f:
        src: str = f.read()

    target = _compile_template(stmt=stmt, setup=setup, global_setup=global_setup, src=src, is_standalone=True)
    if not isinstance(target, str):
        raise AssertionError("compiled target path is not a string")
    return target

