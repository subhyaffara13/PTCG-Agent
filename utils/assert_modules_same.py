
def assert_modules_same(ir1: ModuleIR, ir2: ModuleIR) -> None:
    """Assert that two module IRs are the same (*).

    * Or rather, as much as we care about preserving across
    serialization.  We drop the actual IR bodies of functions but try
    to preserve everything else.
    """
    assert ir1.fullname == ir2.fullname

    assert ir1.imports == ir2.imports

    for cls1, cls2 in zip(ir1.classes, ir2.classes):
        assert_blobs_same(get_dict(cls1), get_dict(cls2), (ir1.fullname, cls1.fullname))

    for fn1, fn2 in zip(ir1.functions, ir2.functions):
        assert_blobs_same(
            get_function_dict(fn1), get_function_dict(fn2), (ir1.fullname, fn1.fullname)
        )
        assert_blobs_same(get_dict(fn1.decl), get_dict(fn2.decl), (ir1.fullname, fn1.fullname))

    assert_blobs_same(ir1.final_names, ir2.final_names, (ir1.fullname, "final_names"))

    assert ir1.dependencies == ir2.dependencies

