
def _send_msg(
    write_pipe: IO[bytes], msg_header: MsgHeader, job_id: int = -1, data: bytes = b""
) -> None:
    length = len(data)
    write_pipe.write(_pack_msg(msg_header, job_id, length))
    if length > 0:
        write_pipe.write(data)
    write_pipe.flush()

