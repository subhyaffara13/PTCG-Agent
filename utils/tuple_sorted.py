
def tuple_sorted(x: tuple[_T, ...]) -> list[_T]:
    if len(x) == 0:
        return []

    def sort_func(elem: _T) -> str:
        if isinstance(elem, str):
            return elem

        from .scheduler import BaseSchedulerNode

        assert isinstance(elem, BaseSchedulerNode)
        return elem.get_name()

    return sorted(x, key=sort_func)

