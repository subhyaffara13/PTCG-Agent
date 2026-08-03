import random
import time

def stream_encode_multipart(
    data: t.Mapping[str, t.Any],
    use_tempfile: bool = True,
    threshold: int = 1024 * 500,
    boundary: str | None = None,
) -> tuple[t.IO[bytes], int, str]:
    """Encode a dict of values (either strings or file descriptors or
    :class:`FileStorage` objects.) into a multipart encoded string stored
    in a file descriptor.

    .. versionchanged:: 3.0
        The ``charset`` parameter was removed.
    """
    if boundary is None:
        boundary = f"---------------WerkzeugFormPart_{time()}{random()}"

    stream: t.IO[bytes] = BytesIO()
    total_length = 0
    on_disk = False
    write_binary: t.Callable[[bytes], int]

    if use_tempfile:

        def write_binary(s: bytes) -> int:
            nonlocal stream, total_length, on_disk

            if on_disk:
                return stream.write(s)
            else:
                length = len(s)

                if length + total_length <= threshold:
                    stream.write(s)
                else:
                    new_stream = t.cast(t.IO[bytes], TemporaryFile("wb+"))
                    new_stream.write(stream.getvalue())  # type: ignore
                    new_stream.write(s)
                    stream = new_stream
                    on_disk = True

                total_length += length
                return length

    else:
        write_binary = stream.write

    encoder = MultipartEncoder(boundary.encode())
    write_binary(encoder.send_event(Preamble(data=b"")))
    for key, value in _iter_data(data):
        reader = getattr(value, "read", None)
        if reader is not None:
            filename = getattr(value, "filename", getattr(value, "name", None))
            content_type = getattr(value, "content_type", None)
            if content_type is None:
                content_type = (
                    filename
                    and mimetypes.guess_type(filename)[0]
                    or "application/octet-stream"
                )
            headers = value.headers
            headers.update([("Content-Type", content_type)])
            if filename is None:
                write_binary(encoder.send_event(Field(name=key, headers=headers)))
            else:
                write_binary(
                    encoder.send_event(
                        File(name=key, filename=filename, headers=headers)
                    )
                )
            while True:
                chunk = reader(16384)

                if not chunk:
                    write_binary(encoder.send_event(Data(data=chunk, more_data=False)))
                    break

                write_binary(encoder.send_event(Data(data=chunk, more_data=True)))
        else:
            if not isinstance(value, str):
                value = str(value)
            write_binary(encoder.send_event(Field(name=key, headers=Headers())))
            write_binary(encoder.send_event(Data(data=value.encode(), more_data=False)))

    write_binary(encoder.send_event(Epilogue(data=b"")))

    length = stream.tell()
    stream.seek(0)
    return stream, length, boundary

