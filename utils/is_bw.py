
def is_bw() -> bool:
    return torch._C._current_graph_task_id() != -1

