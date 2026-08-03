import os

def environ_setting_nodes(node_name_filter=None, node_type_filter=None):
    # Set I/O data as default
    os.environ["ORT_DEBUG_NODE_IO_DUMP_SHAPE_DATA"] = ZERO_VALUE
    os.environ["ORT_DEBUG_NODE_IO_DUMP_INPUT_DATA"] = NON_ZERO_VALUE
    os.environ["ORT_DEBUG_NODE_IO_DUMP_OUTPUT_DATA"] = NON_ZERO_VALUE
    if node_name_filter is not None:
        os.environ["ORT_DEBUG_NODE_IO_NAME_FILTER"] = node_name_filter
    elif node_type_filter is not None:
        os.environ["ORT_DEBUG_NODE_IO_OP_TYPE_FILTER"] = node_type_filter
    else:
        os.environ["ORT_DEBUG_NODE_IO_DUMPING_DATA_TO_FILES_FOR_ALL_NODES_IS_OK"] = NON_ZERO_VALUE

