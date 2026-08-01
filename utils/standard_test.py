
def standard_test(
    self: Any,
    fn: Callable[..., Any],
    nargs: int,
    expected_ops: int | None = None,
    expected_ops_dynamic: int | None = None,
    expected_frame_count: int = 1,
) -> None:
    if not config.assume_static_by_default and expected_ops_dynamic is not None:
        expected_ops = expected_ops_dynamic

    actual = CompileCounter()

    args1 = [torch.randn(10, 10) for _ in range(nargs)]
    args2 = [torch.randn(10, 10) for _ in range(nargs)]
    correct1 = fn(*args1)
    correct2 = fn(*args2)
    reset()
    opt_fn = optimize_assert(actual)(fn)
    val1a = opt_fn(*args1)
    val2a = opt_fn(*args2)
    val1b = opt_fn(*args1)
    val2b = opt_fn(*args2)
    reset()
    self.assertTrue(same(val1a, correct1))
    self.assertTrue(same(val1b, correct1))
    self.assertTrue(same(val2a, correct2))
    self.assertTrue(same(val2b, correct2))
    self.assertEqual(actual.frame_count, expected_frame_count)
    if expected_ops is not None:
        self.assertEqual(actual.op_count, expected_ops)

