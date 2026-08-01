
def subtest_name(test_name_mapping, *args):
    return "_".join(
        [test_name_mapping[str(s)] if s is not None else "none" for s in args]
    )

