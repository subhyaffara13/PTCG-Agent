from typing import Any, Callable

def shape_env_check_state_equal(
    env1: ShapeEnv,
    env2: ShapeEnv,
    non_state_variable_names: tuple[str, ...],
    map_value: Callable[[str, object], object],
) -> None:
    # Collect and remove variables that don't necessarily represent the state
    # of a ShapeEnv. Note: we copy the dictionary so that we don't modify the
    # instance itself.
    env1_vars = vars(env1).copy()
    env2_vars = vars(env2).copy()

    for v in non_state_variable_names:
        if v in env1_vars:
            env1_vars.pop(v)
        if v in env2_vars:
            env2_vars.pop(v)

    # Function for transforming the mismatched values into string.
    # Needed, since dict and set entries order might not be the same every time.
    def value_to_str(value: Any) -> str:
        if isinstance(value, dict):
            return (
                "{"
                + ", ".join(f"{k}: {value[k]}" for k in sorted(value.keys(), key=str))
                + "}"
            )
        if isinstance(value, set):
            return "{" + ", ".join(f"{v}" for v in sorted(value)) + "}"
        return str(value)

    # Compares env1_vars with env2_vars.
    # Here, we allow the value of each field to be mapped, so that we appropriately
    # compare the two values.
    def compare_vars(
        map_value: Callable[[str, object], object],
    ) -> list[tuple[str, str, str]]:
        env1_set, env2_set = set(env1_vars), set(env2_vars)

        # First, compare the set of keys in each vars dictionary.
        if env1_set != env2_set:
            raise NotEqualError(
                "field set mismatch:",
                [
                    (
                        "found unique fields:",
                        str(sorted(env1_set - env2_set)),
                        str(sorted(env2_set - env1_set)),
                    ),
                ],
            )

        # Then, sort the keys, and compare the mapped values of each key.
        sorted_keys = list(env1_set)
        sorted_keys.sort()

        mapped_dict = [
            (k, map_value(k, env1_vars[k]), map_value(k, env2_vars[k]))
            for k in sorted_keys
        ]

        # Return a list of tuples representing the fields that did not match
        # alongside their respective mapped values.
        return [
            (f"{k}: values don't match.", value_to_str(val1), value_to_str(val2))
            for k, val1, val2 in mapped_dict
            if val1 != val2
        ]

    # Accumulate the mismatching fields.
    errors = compare_vars(map_value)

    if len(errors) > 0:
        raise NotEqualError("field values don't match:", errors)

