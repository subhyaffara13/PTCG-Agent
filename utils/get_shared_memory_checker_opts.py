
def get_shared_memory_checker_opts(op_name: str, dtype_size: int):
    return {
        "has_sm_layout_conversion": True,
        # addmm requires the acc dtype for layout conversion due to adding bias
        # mm just input dtype
        "layout_conversion_byte_size": 4 if op_name == "addmm" else dtype_size,
    }

