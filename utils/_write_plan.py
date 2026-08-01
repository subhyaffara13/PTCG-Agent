
def _write_plan(plan: SyncPlan, f) -> None:
    """Write a sync plan as JSONL to a file-like object."""
    # Write header
    header = {
        "type": "header",
        "source": plan.source,
        "dest": plan.dest,
        "timestamp": plan.timestamp,
        "summary": plan.summary(),
    }
    f.write(json.dumps(header) + "\n")

    # Write operations
    for op in plan.operations:
        op_dict: dict[str, Any] = {
            "type": "operation",
            "action": op.action,
            "path": op.path,
            "reason": op.reason,
        }
        if op.size is not None:
            op_dict["size"] = op.size
        if op.local_mtime is not None:
            op_dict["local_mtime"] = op.local_mtime
        if op.remote_mtime is not None:
            op_dict["remote_mtime"] = op.remote_mtime
        f.write(json.dumps(op_dict) + "\n")

