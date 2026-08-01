
def encode_multipart_formdata(
    fields: _TYPE_FIELDS, boundary: str | None = None
) -> tuple[bytes, str]:
    """
    Encode a dictionary of ``fields`` using the multipart/form-data MIME format.

    :param fields:
        Dictionary of fields or list of (key, :class:`~urllib3.fields.RequestField`).
        Values are processed by :func:`urllib3.fields.RequestField.from_tuples`.

    :param boundary:
        If not specified, then a random boundary will be generated using
        :func:`urllib3.filepost.choose_boundary`.
    """
    body = BytesIO()
    if boundary is None:
        boundary = choose_boundary()

    for field in iter_field_objects(fields):
        body.write(f"--{boundary}\r\n".encode("latin-1"))

        writer(body).write(field.render_headers())
        data = field.data

        if isinstance(data, int):
            data = str(data)  # Backwards compatibility

        if isinstance(data, str):
            writer(body).write(data)
        else:
            body.write(data)

        body.write(b"\r\n")

    body.write(f"--{boundary}--\r\n".encode("latin-1"))

    content_type = f"multipart/form-data; boundary={boundary}"

    return body.getvalue(), content_type


def encode_multipart_formdata(
    fields: _TYPE_FIELDS, boundary: str | None = None
) -> tuple[bytes, str]:
    """
    Encode a dictionary of ``fields`` using the multipart/form-data MIME format.

    :param fields:
        Dictionary of fields or list of (key, :class:`~urllib3.fields.RequestField`).
        Values are processed by :func:`urllib3.fields.RequestField.from_tuples`.

    :param boundary:
        If not specified, then a random boundary will be generated using
        :func:`urllib3.filepost.choose_boundary`.
    """
    body = BytesIO()
    if boundary is None:
        boundary = choose_boundary()

    for field in iter_field_objects(fields):
        body.write(f"--{boundary}\r\n".encode("latin-1"))

        writer(body).write(field.render_headers())
        data = field.data

        if isinstance(data, int):
            data = str(data)  # Backwards compatibility

        if isinstance(data, str):
            writer(body).write(data)
        else:
            body.write(data)

        body.write(b"\r\n")

    body.write(f"--{boundary}--\r\n".encode("latin-1"))

    content_type = f"multipart/form-data; boundary={boundary}"

    return body.getvalue(), content_type

