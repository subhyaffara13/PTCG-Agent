
def _reverse_repeat_padding(padding: list[int]) -> list[int]:
    _reversed_padding_repeated_twice: list[int] = []
    N = len(padding)
    for idx in range(N):
        _reversed_padding_repeated_twice.extend(padding[N - idx - 1] for _ in range(2))
    return _reversed_padding_repeated_twice

