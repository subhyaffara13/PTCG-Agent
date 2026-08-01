
def uploaded_prior_to() -> Option:
    return Option(
        "--uploaded-prior-to",
        dest="uploaded_prior_to",
        metavar="datetime_or_duration",
        action="callback",
        callback=_handle_uploaded_prior_to,
        type="str",
        help=(
            "Only consider packages uploaded prior to the given value. "
            "Accepts an ISO 8601 datetime (e.g., '2023-01-01T00:00:00Z', "
            "uses local timezone if none specified) or a duration in days "
            "(e.g., 'P3D' for packages uploaded at least 3 days ago). "
            "Only effective when installing from indexes that provide "
            "upload-time metadata."
        ),
    )

