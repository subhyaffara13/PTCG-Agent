
def patch_testing_methods_to_collect_info():
    """
    Patch some methods (`torch.testing.assert_close`, `unittest.case.TestCase.assertEqual`, etc).

    This will allow us to collect the call information, e.g. the argument names and values, also the literal expressions
    passed as the arguments.
    """
    p = os.path.join(os.environ.get("_PATCHED_TESTING_METHODS_OUTPUT_DIR", ""), "captured_info.txt")
    Path(p).unlink(missing_ok=True)

    if is_torch_available():
        import torch

        _patch_with_call_info(torch.testing, "assert_close", _parse_call_info, target_args=("actual", "expected"))

    _patch_with_call_info(unittest.case.TestCase, "assertEqual", _parse_call_info, target_args=("first", "second"))
    _patch_with_call_info(unittest.case.TestCase, "assertListEqual", _parse_call_info, target_args=("list1", "list2"))
    _patch_with_call_info(
        unittest.case.TestCase, "assertTupleEqual", _parse_call_info, target_args=("tuple1", "tuple2")
    )
    _patch_with_call_info(unittest.case.TestCase, "assertSetEqual", _parse_call_info, target_args=("set1", "set1"))
    _patch_with_call_info(unittest.case.TestCase, "assertDictEqual", _parse_call_info, target_args=("d1", "d2"))
    _patch_with_call_info(unittest.case.TestCase, "assertIn", _parse_call_info, target_args=("member", "container"))
    _patch_with_call_info(unittest.case.TestCase, "assertNotIn", _parse_call_info, target_args=("member", "container"))
    _patch_with_call_info(unittest.case.TestCase, "assertLess", _parse_call_info, target_args=("a", "b"))
    _patch_with_call_info(unittest.case.TestCase, "assertLessEqual", _parse_call_info, target_args=("a", "b"))
    _patch_with_call_info(unittest.case.TestCase, "assertGreater", _parse_call_info, target_args=("a", "b"))
    _patch_with_call_info(unittest.case.TestCase, "assertGreaterEqual", _parse_call_info, target_args=("a", "b"))

