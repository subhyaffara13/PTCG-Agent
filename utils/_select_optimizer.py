
def _select_optimizer(
    optimization: Literal["random-cd", "lloyd"] | None, config: dict
) -> Callable | None:
    """A factory for optimization methods."""
    optimization_method: dict[str, Callable] = {
        "random-cd": _random_cd,
        "lloyd": _lloyd_centroidal_voronoi_tessellation
    }

    optimizer: partial | None
    if optimization is not None:
        try:
            optimizer_ = optimization_method[optimization.lower()]
        except KeyError as exc:
            message = (f"{optimization!r} is not a valid optimization"
                       f" method. It must be one of"
                       f" {set(optimization_method)!r}")
            raise ValueError(message) from exc

        # config
        optimizer = partial(optimizer_, **config)
    else:
        optimizer = None

    return optimizer

