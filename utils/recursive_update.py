
def recursive_update(target, update, overwrite=True):
    """Update recursively a (nested) dictionary with the content of another.
    Inspired from https://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth
    """
    for key in update:
        value = update[key]
        if value is None:
            del target[key]
        elif isinstance(value, dict):
            target[key] = recursive_update(
                target.get(key, {}),
                value,
                overwrite=overwrite,
            )
        elif overwrite:
            target[key] = value
        else:
            target.setdefault(key, value)
    return target


def recursive_update(target: dict[Any, Any], new: dict[Any, Any]) -> None:
    """Recursively update one dictionary using another.

    None values will delete their keys.
    """
    for k, v in new.items():
        if isinstance(v, dict):
            if k not in target:
                target[k] = {}
            recursive_update(target[k], v)
            if not target[k]:
                # Prune empty subdicts
                del target[k]

        elif v is None:
            target.pop(k, None)

        else:
            target[k] = v

