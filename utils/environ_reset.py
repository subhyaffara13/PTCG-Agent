
def environ_reset():
    for flag in [
        "ORT_DEBUG_NODE_IO_DUMP_SHAPE_DATA",
        "ORT_DEBUG_NODE_IO_DUMP_INPUT_DATA",
        "ORT_DEBUG_NODE_IO_DUMP_OUTPUT_DATA",
        "ORT_DEBUG_NODE_IO_NAME_FILTER",
        "ORT_DEBUG_NODE_IO_OP_TYPE_FILTER",
        "ORT_DEBUG_NODE_IO_DUMP_DATA_TO_FILES",
        "ORT_DEBUG_NODE_IO_OUTPUT_DIR",
        "ORT_DEBUG_NODE_IO_DUMPING_DATA_TO_FILES_FOR_ALL_NODES_IS_OK",
    ]:
        if flag in os.environ:
            del os.environ[flag]

