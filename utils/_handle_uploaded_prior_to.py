
def _handle_uploaded_prior_to(
    option: Option, opt: str, value: str, parser: OptionParser
) -> None:
    """
    This is an optparse.Option callback for the --uploaded-prior-to option.

    Accepts either an ISO 8601 datetime string (e.g., '2023-01-01T00:00:00Z')
    or a strict subset of ISO 8601 durations: PnD where n is a number of days
    (e.g., 'P7D' for 7 days ago).

    Note: This option only works with indexes that provide upload-time metadata
    as specified in the simple repository API:
    https://packaging.python.org/en/latest/specifications/simple-repository-api/
    """
    if value is None:
        return None

    # Try ISO 8601 duration in PnD format. The leading 'P' disambiguates
    # from absolute datetimes. Only whole days are supported; the format may
    # be extended to more of the ISO 8601 duration syntax in the future if
    # a real need is presented.
    match = re.match(r"^P(\d+)D$", value, re.ASCII)
    if match:
        days = int(match.group(1))
        parser.values.uploaded_prior_to = datetime.now(timezone.utc) - timedelta(
            days=days
        )
        return

    try:
        uploaded_prior_to = parse_iso_datetime(value)
        # Use local timezone if no offset is given in the ISO string.
        if uploaded_prior_to.tzinfo is None:
            uploaded_prior_to = uploaded_prior_to.astimezone()
        parser.values.uploaded_prior_to = uploaded_prior_to
    except ValueError as exc:
        msg = (
            f"invalid value: {value!r}: {exc}. "
            f"Expected an ISO 8601 datetime string "
            f"(e.g., '2023-01-01' or '2023-01-01T00:00:00Z') "
            f"or a duration in days (e.g., 'P3D')"
        )
        raise_option_error(parser, option=option, msg=msg)

