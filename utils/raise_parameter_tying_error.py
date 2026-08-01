
def raise_parameter_tying_error() -> NoReturn:
    raise RuntimeError(
        "make_functional(module): we don't yet support models that "
        "do parameter tying (also sometimes known as weight sharing). "
        "Please try to rewrite your model by replacing all instances of the "
        "tied parameter with another and/or comment your support in "
        "https://github.com/pytorch/functorch/issues/446"
    )

