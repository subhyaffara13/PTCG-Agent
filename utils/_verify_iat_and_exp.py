
def _verify_iat_and_exp(payload, clock_skew_in_seconds=0):
    """Verifies the ``iat`` (Issued At) and ``exp`` (Expires) claims in a token
    payload.

    Args:
        payload (Mapping[str, str]): The JWT payload.
        clock_skew_in_seconds (int): The clock skew used for `iat` and `exp`
            validation.

    Raises:
        google.auth.exceptions.InvalidValue: if value validation failed.
        google.auth.exceptions.MalformedError: if schema validation failed.
    """
    now = _helpers.datetime_to_secs(_helpers.utcnow())

    # Make sure the iat and exp claims are present.
    for key in ("iat", "exp"):
        if key not in payload:
            raise exceptions.MalformedError(
                "Token does not contain required claim {}".format(key)
            )

    # Make sure the token wasn't issued in the future.
    iat = payload["iat"]
    # Err on the side of accepting a token that is slightly early to account
    # for clock skew.
    earliest = iat - clock_skew_in_seconds
    if now < earliest:
        raise exceptions.InvalidValue(
            "Token used too early, {} < {}. Check that your computer's clock is set correctly.".format(
                now, iat
            )
        )

    # Make sure the token wasn't issued in the past.
    exp = payload["exp"]
    # Err on the side of accepting a token that is slightly out of date
    # to account for clow skew.
    latest = exp + clock_skew_in_seconds
    if latest < now:
        raise exceptions.InvalidValue("Token expired, {} < {}".format(latest, now))

