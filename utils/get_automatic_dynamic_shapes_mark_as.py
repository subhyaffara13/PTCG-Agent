
def get_automatic_dynamic_shapes_mark_as() -> DimDynamic:
    if config.automatic_dynamic_shapes_mark_as == "dynamic":
        return DimDynamic.DYNAMIC
    elif config.automatic_dynamic_shapes_mark_as == "unbacked":
        return DimDynamic.UNBACKED
    else:
        raise ValueError(
            f"invalid automatic_dynamic_shapes_mark_as = {config.automatic_dynamic_shapes_mark_as}"
        )

