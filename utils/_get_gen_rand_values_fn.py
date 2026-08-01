
def _get_gen_rand_values_fn(random_calls: Any) -> Callable[[], list[Any]]:
    def _gen_rand_values() -> list[Any]:
        return [fn(*args, **kwargs) for fn, args, kwargs in random_calls]

    return _gen_rand_values

