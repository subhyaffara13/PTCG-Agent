import os

def environ_setting_paths(output_path):
    # Set dumping values to files as default
    os.environ["ORT_DEBUG_NODE_IO_DUMP_DATA_DESTINATION"] = "files"
    os.environ["ORT_DEBUG_NODE_IO_OUTPUT_DIR"] = output_path

