
def _set_stream_by_id(stream_id, device_index, device_type):
    r"""set stream specified by the stream id, device index and
        device type

    Args: stream_id (int): stream id in stream pool
          device_index (int): device index in topo
          device_type (int): enum device type
    """
    torch._C._cuda_setStream(
        stream_id=stream_id,
        device_index=device_index,
        device_type=device_type,
    )


def _set_stream_by_id(stream_id, device_index, device_type):
    r"""set stream specified by the stream id, device index and
        device type

    Args: stream_id (int): stream id in stream pool
          device_index (int): device index in topo
          device_type (int): enum device type
    """
    torch._C._mtia_setStream(stream_id, device_index, device_type)


def _set_stream_by_id(stream_id, device_index, device_type) -> None:
    r"""set stream specified by the stream id, device index and device type

    Args: stream_id (int): not visible to the user, used to assigned to the specific stream.
          device_index (int): selected device index.
          device_type (int): selected device type.
    """
    torch._C._xpu_setStream(
        stream_id=stream_id,
        device_index=device_index,
        device_type=device_type,
    )

