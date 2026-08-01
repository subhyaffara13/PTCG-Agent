
def create_io_binding(sess, input_tensors, output_tensors):
    io_binding = sess.io_binding()
    for name, tensor in input_tensors.items():
        io_binding.bind_input(
            name,
            tensor.device.type,
            0,
            numpy_type(tensor.dtype),
            tensor.shape,
            tensor.data_ptr(),
        )
    for name, tensor in output_tensors.items():
        io_binding.bind_output(
            name,
            tensor.device.type,
            0,
            numpy_type(tensor.dtype),
            tensor.shape,
            tensor.data_ptr(),
        )
    return io_binding

