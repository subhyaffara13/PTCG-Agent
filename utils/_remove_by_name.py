
def _remove_by_name(saved_values: list[fx.Node], name: str) -> None:
    for saved_value in saved_values:
        if saved_value.name == name:
            saved_values.remove(saved_value)
            break

