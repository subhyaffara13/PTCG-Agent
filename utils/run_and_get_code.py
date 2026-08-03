from typing import Callable

def run_and_get_code(
    fn: Callable[P, _T],
    *args: P.args,
    **kwargs: P.kwargs,
) -> tuple[_T, list[str]]:
    from .graph import GraphLowering

    source_codes: OrderedSet[str] = OrderedSet()

    def save_output_code(code: str) -> None:
        source_codes.add(code)

    with mock.patch.object(GraphLowering, "save_output_code", save_output_code):
        torch._dynamo.reset()
        result = fn(*args, **kwargs)
    return result, list(source_codes)

