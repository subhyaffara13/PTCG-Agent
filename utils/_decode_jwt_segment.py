
def _decode_jwt_segment(encoded_section):
    """Decodes a single JWT segment."""
    section_bytes = _helpers.padded_urlsafe_b64decode(encoded_section)
    try:
        return json.loads(section_bytes.decode("utf-8"))
    except ValueError as caught_exc:
        new_exc = exceptions.MalformedError(
            "Can't parse segment: {0}".format(section_bytes)
        )
        raise new_exc from caught_exc

