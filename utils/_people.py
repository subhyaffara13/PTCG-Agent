
def _people(dist: Distribution, val: list[dict], _root_dir: StrPath | None, kind: str):
    field = []
    email_field = []
    for person in val:
        if "name" not in person:
            email_field.append(person["email"])
        elif "email" not in person:
            field.append(person["name"])
        else:
            addr = Address(display_name=person["name"], addr_spec=person["email"])
            email_field.append(str(addr))

    if field:
        _set_config(dist, kind, _static.Str(", ".join(field)))
    if email_field:
        _set_config(dist, f"{kind}_email", _static.Str(", ".join(email_field)))

