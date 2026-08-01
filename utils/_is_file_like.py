
def _is_file_like(maybefile):
    # compare to xml.etree.ElementTree._get_writer
    return hasattr(maybefile, 'write')


def _is_file_like(value: t.Any) -> te.TypeIs[t.IO[t.Any]]:
    return hasattr(value, "read") or hasattr(value, "write")

