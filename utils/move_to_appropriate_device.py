
def move_to_appropriate_device(model: nn.Module, sample_inputs_tp: tuple) -> nn.Module:
    """
    According to the model size, we will upload it to
    CPU if has no GPU or enough GPU memory,
    Single GPU if has only one GPU in local or model size is enough to fit one GPU
    Multiple GPU if there is more than one gpu in local and model is too large
    """
    total_mem_per_cpu = torch.cuda.get_device_properties(0).total_memory / 1024 / 1024

    print(f"Model_Size = {get_model_parameter_size(model) / 1024} GB")
    print(f"total_mem_per_cpu = {total_mem_per_cpu / 1024} GB")
    if get_model_parameter_size(model) > total_mem_per_cpu * 0.45:
        device_collection = [torch.device(i) for i in range(torch.cuda.device_count())]
        if len(device_collection) > 1:
            print(
                f"{len(device_collection)} GPUs are used to export onnx, \
                   Please set CUDA_VISIBLE_DEVICES to use specific GPU group"
            )
            model = auto_pipeline_parallel(model, device_collection, sample_inputs_tp)
        else:
            print("!!!! convert model to float and export onnx using CPU")
            model = model.cpu().float()
    else:
        print("Export model on a single GPU")
        model = model.cuda().half()
    return model

