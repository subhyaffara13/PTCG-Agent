
def get_acc_ops_name(k):
    if isinstance(k, str):
        return k
    elif k.__module__ and "acc_ops" in k.__module__:
        return f"acc_ops.{k.__name__}"
    else:
        module = k.__module__.replace(
            "torch._ops", "torch.ops"
        )  # WAR for bug in how torch.ops assigns module
        return f"{module if module else ''}.{k.__name__}"

