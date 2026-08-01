
def get_required_header(headers: HeadersLike, header: str) -> str:
    lower_header = header.lower()
    if is_mapping_t(headers):
        # mypy doesn't understand the type narrowing here
        for k, v in headers.items():  # type: ignore
            if k.lower() == lower_header and isinstance(v, str):
                return v

    # to deal with the case where the header looks like Stainless-Event-Id
    intercaps_header = re.sub(r"([^\w])(\w)", lambda pat: pat.group(1) + pat.group(2).upper(), header.capitalize())

    for normalized_header in [header, lower_header, header.upper(), intercaps_header]:
        value = headers.get(normalized_header)
        if value:
            return value

    raise ValueError(f"Could not find {header} header")

