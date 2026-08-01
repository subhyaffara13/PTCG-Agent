
def _is_gm_meta_like_dict(d: dict, o: typing.Any) -> bool:
    # Hope gm.meta was a custom dict we can assert on
    return d.get("val") is o

