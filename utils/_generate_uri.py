
def _generate_uri(
    hotp: HOTP,
    type_name: str,
    account_name: str,
    issuer: str | None,
    extra_parameters: list[tuple[str, int]],
) -> str:
    parameters = [
        ("digits", hotp._length),
        ("secret", base64.b32encode(hotp._key)),
        ("algorithm", hotp._algorithm.name.upper()),
    ]

    if issuer is not None:
        parameters.append(("issuer", issuer))

    parameters.extend(extra_parameters)

    label = (
        f"{quote(issuer)}:{quote(account_name)}"
        if issuer
        else quote(account_name)
    )
    return f"otpauth://{type_name}/{label}?{urlencode(parameters)}"

