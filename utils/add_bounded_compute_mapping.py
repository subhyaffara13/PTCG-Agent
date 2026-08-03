from typing import Callable

def add_bounded_compute_mapping(
    operator_schema: str, lower_bound_func: Callable, upper_bound_func: Callable
):
    # Adds a shape compute function for both upper and lower bounds
    fns = (process_func(lower_bound_func), process_func(upper_bound_func))
    bounded_compute_graph_mapping[operator_schema] = fns

