
def get_stream_from_external(data_ptr: int, device: Device = None) -> Stream:
    r"""Return a :class:`Stream` from an externally allocated CUDA stream.

    This function is used to wrap streams allocated in other libraries in order
    to facilitate data exchange and multi-library interactions.

    .. note:: This function doesn't manage the stream life-cycle, it is the user
       responsibility to keep the referenced stream alive while this returned
       stream is being used.

    Args:
        data_ptr(int): Integer representation of the `cudaStream_t` value that
            is allocated externally.
        device(torch.device or int, optional): the device where the stream
            was originally allocated. If device is specified incorrectly,
            subsequent launches using this stream may fail.
    """
    _lazy_init()
    streamdata = torch._C._cuda_getStreamFromExternal(
        data_ptr, _get_device_index(device, optional=True)
    )
    return Stream(
        stream_id=streamdata[0], device_index=streamdata[1], device_type=streamdata[2]
    )


def get_stream_from_external(data_ptr: int, device: Device = None) -> Stream:
    r"""Return a :class:`Stream` from an external SYCL queue.

    This function is used to wrap SYCL queue created in other libraries in order
    to facilitate data exchange and multi-library interactions.

    .. note:: This function doesn't manage the queue life-cycle, it is the user
       responsibility to keep the referenced queue alive while this returned stream is
       being used. The different SYCL queue pointers will result in distinct
       :class:`Stream` objects, even if the SYCL queues they dereference are equivalent.

    Args:
        data_ptr(int): Integer representation of the `sycl::queue*` value passed externally.
        device(torch.device or int, optional): the device where the queue was originally created.
            It is the user responsibility to ensure the device is specified correctly.
    """
    _lazy_init()
    streamdata = torch._C._xpu_getStreamFromExternal(
        data_ptr, _get_device_index(device, optional=True)
    )
    return Stream(
        stream_id=streamdata[0], device_index=streamdata[1], device_type=streamdata[2]
    )

