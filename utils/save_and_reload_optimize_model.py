
def save_and_reload_optimize_model(model: onnx.ModelProto, shape_infer: bool) -> onnx.ModelProto:
    with tempfile.TemporaryDirectory(prefix="ort.qnn_preproc.") as qnn_preproc_tmp_dir:
        model_in_path = Path(qnn_preproc_tmp_dir).joinpath("qnn_proc_input.onnx")
        onnx.save_model(model, model_in_path, save_as_external_data=True)
        if shape_infer:
            model_infer_path = Path(qnn_preproc_tmp_dir).joinpath("qnn_proc_infer.onnx")
            onnx.shape_inference.infer_shapes_path(str(model_in_path), str(model_infer_path))
            model_in_path = model_infer_path
        model_out_path = Path(qnn_preproc_tmp_dir).joinpath("qnn_proc_output.onnx")
        optimize_model(model_in_path, model_out_path)
        ret_model = onnx.load_model(model_out_path)
        ret_metaprops = {"onnx.infer": "onnxruntime.tools.qnn.preprocess"}
        if ret_model.metadata_props:
            ret_metaprops.update(ret_model.metadata_props)
        onnx.helper.set_model_props(ret_model, ret_metaprops)
        return ret_model

