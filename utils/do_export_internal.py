
def do_export_internal(model: nn.Module, onnx_io_tuple: tuple, onnx_inputs: tuple, onnx_path: Path, opset: int):
    """do export with torch.onnx.export"""
    onnx_model_name = onnx_path.name
    onnx_inp_names, onnx_out_names, onnx_dynamic_axes = onnx_io_tuple
    # two step to export onnx
    # 1. export onnx with lots of pieces of weights
    # 2. save all weights to external data
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmp_onnx = os.path.join(tmpdirname, "tmp.onnx")

        torch.onnx.export(
            model=model,
            args=tuple(onnx_inputs),
            f=tmp_onnx,
            verbose=False,
            opset_version=opset,
            input_names=onnx_inp_names,
            output_names=onnx_out_names,
            dynamic_axes=onnx_dynamic_axes,
            dynamo=False,
        )

        onnx_path.unlink(missing_ok=True)
        (onnx_path.parent / f"{onnx_model_name}_ext.data").unlink(missing_ok=True)

        onnx_model = onnx.load(str(tmp_onnx))
        onnx.save_model(
            onnx_model,
            str(onnx_path),
            save_as_external_data=(len(os.listdir(tmpdirname)) > 1),
            all_tensors_to_one_file=True,
            location=f"{onnx_model_name}_ext.data",
            size_threshold=1024,
            convert_attribute=False,
        )

