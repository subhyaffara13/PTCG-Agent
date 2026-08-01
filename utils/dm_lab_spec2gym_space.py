
def dm_lab_spec2gym_space(spec) -> spaces.Space[Any]:
    """Converts a dm_lab spec to a gymnasium space."""
    if isinstance(spec, list):
        expanded = {}
        for desc in spec:
            assert (
                "name" in desc
            ), f"Can't find name for the description: {desc} in spec."

            # some observation spaces have a string description, we ignore those for now
            if "dtype" in desc:
                if desc["dtype"] == str:
                    continue

            expanded[desc["name"]] = dm_lab_spec2gym_space(desc)

        return spaces.Dict(expanded)
    if isinstance(spec, (OrderedDict, dict)):
        # this is an action space
        if "min" in spec and "max" in spec:
            return spaces.Box(low=spec["min"], high=spec["max"], dtype=np.float64)

        # we dk wtf it is here
        else:
            raise NotImplementedError(
                f"Unknown spec definition: {spec}, please report."
            )

    else:
        raise NotImplementedError(
            f"Cannot convert dm_spec to gymnasium space, unknown spec: {spec}, please report."
        )

