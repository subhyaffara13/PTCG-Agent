
def unpack_callback_protocol(t: Instance) -> ProperType | None:
    assert t.type.is_protocol
    if t.type.protocol_members == ["__call__"]:
        return get_proper_type(find_member("__call__", t, t, is_operator=True))
    return None

