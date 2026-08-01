
def _optimization_suffix(optimization_level_str: str, optimization_style: OptimizationStyle, suffix: str):
    return "{}{}{}".format(
        f".{optimization_level_str}" if optimization_level_str != "all" else "",
        ".with_runtime_opt" if optimization_style == OptimizationStyle.Runtime else "",
        suffix,
    )

