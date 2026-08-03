from typing import Any

def set_head_dim_values(
    kernel_options: dict[str, Any], qk_head_dim, v_head_dim, graph_sizevars
):
    """
    Mutates kernel options, adding head dimension calculations.

    Args:
        kernel_options: Dictionary to populate with options
        qk_head_dim: Query/Key head dimension
        v_head_dim: Value head dimension
        graph_sizevars: Graph size variables object with guard_int method

    """
    # QK dimensions
    qk_head_dim_static = graph_sizevars.guard_int(qk_head_dim)
    kernel_options.setdefault("QK_HEAD_DIM", qk_head_dim_static)
    kernel_options.setdefault(
        "QK_HEAD_DIM_ROUNDED", next_power_of_two(qk_head_dim_static)
    )

    # V dimensions
    v_head_dim_static = graph_sizevars.guard_int(v_head_dim)
    kernel_options.setdefault("V_HEAD_DIM", v_head_dim_static)
    kernel_options.setdefault(
        "V_HEAD_DIM_ROUNDED", next_power_of_two(v_head_dim_static)
    )

    # Safety flag
    kernel_options.setdefault(
        "SAFE_HEAD_DIM",
        is_power_of_2(qk_head_dim_static) and is_power_of_2(v_head_dim_static),
    )

