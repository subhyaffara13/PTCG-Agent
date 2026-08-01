
def _populate() -> None:
    for k, v in _tags_v2.items():
        # Populate legacy structure.
        TAGS[k] = v[0]
        if len(v) == 4:
            for sk, sv in v[3].items():
                TAGS[(k, sv)] = sk

        TAGS_V2[k] = TagInfo(k, *v)

    for group, tags in _tags_v2_groups.items():
        TAGS_V2_GROUPS[group] = {k: TagInfo(k, *v) for k, v in tags.items()}


def _populate() -> None:
    for name, value in VariableTracker.__dict__.items():
        if name not in LazyVariableTracker.__dict__:
            if callable(value):
                setattr(LazyVariableTracker, name, _create_realize_and_forward(name))

