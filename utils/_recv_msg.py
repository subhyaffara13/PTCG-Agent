
def _recv_msg(read_pipe: IO[bytes]) -> tuple[MsgHeader, int, bytes]:
    msg_header, job_id, length = _unpack_msg(read_pipe.read(msg_bytes))
    data = read_pipe.read(length) if length > 0 else b""
    return msg_header, job_id, data

