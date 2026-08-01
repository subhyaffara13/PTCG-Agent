
def _pack_msg(msg_header: MsgHeader, job_id: int, length: int) -> bytes:
    return struct.pack("nnn", int(msg_header), job_id, length)

