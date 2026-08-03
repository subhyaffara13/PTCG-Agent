from typing import Any

def update_storage_options(
    options: dict[str, Any], inherited: dict[str, Any] | None = None
) -> None:
    if not inherited:
        inherited = {}
    collisions = set(options) & set(inherited)
    if collisions:
        for collision in collisions:
            if options.get(collision) != inherited.get(collision):
                raise KeyError(
                    f"Collision between inferred and specified storage "
                    f"option:\n{collision}"
                )
    options.update(inherited)

