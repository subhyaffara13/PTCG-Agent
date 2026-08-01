
def _filter_name(name):
    # ignoring the following utility ops
    filtered_out_names = [
        MEMORY_EVENT_NAME,  # used only for the top-level memory events
        OUT_OF_MEMORY_EVENT_NAME,
        "profiler::_record_function_enter",
        "profiler::_record_function_enter_new",
        "profiler::_record_function_exit",
        "aten::is_leaf",
        "aten::output_nr",
        "aten::_version",
    ]
    return name in filtered_out_names

