
def inference(model_path, dummy_inputs, outputs_path, use_gpu):
    environ_reset()
    environ_setting_nodes()
    environ_setting_paths(outputs_path)
    session = create_onnxruntime_session(model_path, use_gpu, enable_all_optimization=False)
    Gpt2Helper.onnxruntime_inference(session, dummy_inputs)

