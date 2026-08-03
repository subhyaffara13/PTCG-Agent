import sys

def prepare_inputs(bsr, *dense_tensors):
    # Introduce fake batch dimension if not present for convenience.
    crow_indices = bsr.crow_indices().unsqueeze(0)
    col_indices = bsr.col_indices().unsqueeze(0)
    values = make_triton_contiguous(bsr.values().unsqueeze(0))
    tensors = [make_triton_contiguous(t.unsqueeze(0)) for t in dense_tensors]

    # Compute broadcasted batch dimension
    batch_dims_broadcasted = torch.broadcast_shapes(
        values.shape[:-3], *(t.shape[:-2] for t in tensors)
    )

    # Broadcast batch dimensions and squash.
    # The result can be either a view or a copy.
    def batch_broadcast_and_squash(t, batch_dims, invariant_dims):
        return t.broadcast_to(batch_dims + invariant_dims).flatten(
            0, len(batch_dims) - 1
        )

    crow_indices = batch_broadcast_and_squash(
        crow_indices, batch_dims_broadcasted, (-1,)
    )

    col_indices = batch_broadcast_and_squash(col_indices, batch_dims_broadcasted, (-1,))
    values = batch_broadcast_and_squash(
        values, batch_dims_broadcasted, values.shape[-3:]
    )
    tensors = [
        batch_broadcast_and_squash(t, batch_dims_broadcasted, t.shape[-2:])
        for t in tensors
    ]

    return crow_indices, col_indices, values, *tensors


def prepare_inputs(model, n_samples, dataloader, providers):
    """Prepare inputs for weight only quantization.

    Args:
        model (ModelProto or ONNXModel): onnx model
        n_samples (int, optional): calibration sample number. -1 means all samples.
        dataloader (object): dataloader for calibration.
        providers (list): providers to use

    Returns:
        inputs: prepared inputs.
        so: session options
    """
    from importlib.util import find_spec  # noqa: PLC0415

    from .util import to_numpy  # noqa: PLC0415

    so = ort.SessionOptions()
    if sys.version_info < (3, 11) and find_spec("onnxruntime_extensions"):  # pragma: no cover
        from onnxruntime_extensions import get_library_path  # noqa: PLC0415

        so.register_custom_ops_library(get_library_path())
    if model.is_large_model:
        onnx.save_model(
            model.model,
            model.model_path + "_augment.onnx",
            save_as_external_data=True,
            all_tensors_to_one_file=True,
            convert_attribute=False,
        )

    session = (
        ort.InferenceSession(model.model.SerializeToString(), so, providers=providers)
        if not model.is_large_model
        else ort.InferenceSession(model.model_path + "_augment.onnx", so, providers=providers)
    )
    inputs_names = [i.name for i in session.get_inputs()]
    del session

    inputs = []
    for i, data in enumerate(dataloader):
        if n_samples != -1 and ((i + 1) * dataloader.batch_size) > n_samples:
            break
        if len(inputs_names) != 1 or isinstance(data[0], dict):
            assert len(data[0]) == len(inputs_names), (
                f"Input number mismatch, require {len(inputs_names)} but get {len(data[0])}"
            )

        if isinstance(data[0], dict):
            inputs.append(dict([(name, to_numpy(inp_data)) for name, inp_data in data[0].items()]))  # noqa: C404
        elif isinstance(data[0], np.ndarray):  # pragma: no cover
            inputs.append(dict([(name, inp) for name, inp in zip(inputs_names, [data[0]], strict=False)]))  # noqa: C404
        else:  # pragma: no cover
            inputs.append(dict([(name, to_numpy(inp)) for name, inp in zip(inputs_names, data[0], strict=False)]))  # noqa: C404
    return inputs, so

