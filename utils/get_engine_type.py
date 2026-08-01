
def get_engine_type(name: str) -> EngineType:
    name_to_type = {
        "ORT_CUDA": EngineType.ORT_CUDA,
        "ORT_TRT": EngineType.ORT_TRT,
        "TRT": EngineType.TRT,
        "TORCH": EngineType.TORCH,
    }
    return name_to_type[name]

