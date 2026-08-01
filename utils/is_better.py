
def is_better(t: Type, s: Type) -> bool:
    # Given two possible results from join_instances_via_supertype(),
    # indicate whether t is the better one.
    t = get_proper_type(t)
    s = get_proper_type(s)

    if isinstance(t, Instance):
        if not isinstance(s, Instance):
            return True
        if t.type.is_protocol != s.type.is_protocol:
            if t.type.fullname != "builtins.object" and s.type.fullname != "builtins.object":
                # mro of protocol is not really relevant
                return not t.type.is_protocol
        # Use len(mro) as a proxy for the better choice.
        if len(t.type.mro) > len(s.type.mro):
            return True
    return False

