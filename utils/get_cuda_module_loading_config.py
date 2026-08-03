import os

def get_cuda_module_loading_config():
    if TORCH_AVAILABLE and torch.cuda.is_available():
        torch.cuda.init()
        config = os.environ.get("CUDA_MODULE_LOADING", "")
        return config
    else:
        return "N/A"

