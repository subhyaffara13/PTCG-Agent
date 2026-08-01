
def _read_line(conn):
    buf = bytearray()
    while True:
        try:
            chunk = conn.recv(65536)
            if not chunk:
                return None
            buf.extend(chunk)
            if b'\n' in chunk:
                break
        except Exception:
            return None
    return buf.decode('utf-8')


def _read_line(conn):
    buf = bytearray()
    while True:
        try:
            chunk = conn.recv(65536)
            if not chunk:
                return None
            buf.extend(chunk)
            if b'\n' in chunk:
                break
        except Exception:
            return None
    return buf.decode('utf-8')

