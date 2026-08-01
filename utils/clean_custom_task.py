
def clean_custom_task(task_info):
    import transformers

    if "impl" not in task_info:
        raise RuntimeError("This model introduces a custom pipeline without specifying its implementation.")
    pt_class_names = task_info.get("pt", ())
    if isinstance(pt_class_names, str):
        pt_class_names = [pt_class_names]
    task_info["pt"] = tuple(getattr(transformers, c) for c in pt_class_names)
    return task_info, None

