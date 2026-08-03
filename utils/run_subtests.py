import itertools
from typing import Any, Callable

def run_subtests(
    cls_inst,
    subtest_config: dict[str, list[Any]],
    test_fn: Callable,
    *test_args,
    **test_kwargs: Any,
):
    """
    Runs a test function given by ``test_fn`` as a subtest according to the
    configurations specified by ``subtest_config``. This amortizes the
    costly setup overhead (including process spawn and initializing the
    process group) over the subtests.

    Args:
        subtest_config (Dict[str, List[Any]]): A mapping from subtest
            keyword argument name to a list of its possible values.
        test_fn (Callable): A callable that runs the actual test.
        test_args: Positional arguments to pass to ``test_fn``.
        test_kwargs: Keyword arguments to pass to ``test_fn``.
    """
    # Convert the config mapping to a list to have a fixed order
    subtest_config_items: list[tuple[str, list[Any]]] = list(subtest_config.items())
    subtest_config_keys: list[str] = [item[0] for item in subtest_config_items]
    subtest_config_values: list[list[Any]] = [item[1] for item in subtest_config_items]
    for values in itertools.product(*subtest_config_values):
        # Map keyword to chosen value
        subtest_kwargs = dict(zip(subtest_config_keys, values, strict=True))
        with cls_inst.subTest(**subtest_kwargs):
            torch._dynamo.reset()
            test_fn(*test_args, **test_kwargs, **subtest_kwargs)
            torch._dynamo.reset()
        c10d.barrier()

