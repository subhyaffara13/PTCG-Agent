import os

def to_string(s, encoding: str = "utf-8"):
    if isinstance(s, str):
        return s
    elif isinstance(s, bytes):
        return s.decode(encoding, "ignore")
    else:
        return s  # Not a string we care about


def to_string(model_path, session, test_setting):
    sess_options = session.get_session_options()
    option = f"model={os.path.basename(model_path)},"
    option += f"graph_optimization_level={sess_options.graph_optimization_level},intra_op_num_threads={sess_options.intra_op_num_threads},".replace(
        "GraphOptimizationLevel.ORT_", ""
    )

    option += f"batch_size={test_setting.batch_size},sequence_length={test_setting.sequence_length},"
    option += f"test_cases={test_setting.test_cases},test_times={test_setting.test_times},"
    option += f"use_gpu={test_setting.use_gpu},use_io_binding={test_setting.use_io_binding},"
    option += f"average_sequence_length={test_setting.average_sequence_length},"
    option += f"random_sequence_length={test_setting.random_sequence_length}"
    return option

