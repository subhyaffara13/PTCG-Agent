
def _unpack_msg(data: bytes) -> tuple[MsgHeader, int, int]:
    if not data:
        return MsgHeader.ERROR, -1, -1
    msg_header, job_id, length = struct.unpack("nnn", data)
    return MsgHeader(msg_header), job_id, length

