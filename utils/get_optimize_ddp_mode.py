
def get_optimize_ddp_mode() -> str:
    optimize_ddp = config.optimize_ddp
    if isinstance(optimize_ddp, bool):
        mode = "ddp_optimizer" if optimize_ddp else "no_optimization"
    elif isinstance(optimize_ddp, str):
        mode = optimize_ddp
    else:
        raise ValueError(
            f"Invalid dynamo config optimize_ddp type {type(optimize_ddp)=}"
        )

    assert mode in _ddp_optimization_mode, (
        f"Invalid dynamo config optimize_ddp value {mode=}"
    )
    return mode

