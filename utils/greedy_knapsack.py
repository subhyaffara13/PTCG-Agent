
def greedy_knapsack(
    memory: list[float], runtimes: list[float], max_memory: float
) -> tuple[float, list[int], list[int]]:
    n = len(runtimes)
    items = list(range(n))

    # Sort items based on the ratio of runtime to memory in descending order
    items = sorted(items, key=lambda i: runtimes[i] / memory[i], reverse=True)

    total_memory = 0.0
    total_runtime = 0.0
    items_to_save = []
    items_to_allow_recomputing = []

    for i in items:
        if total_memory + memory[i] <= max_memory:
            total_memory += memory[i]
            total_runtime += runtimes[i]
            items_to_save.append(i)
        else:
            items_to_allow_recomputing.append(i)
    return total_runtime, items_to_save, items_to_allow_recomputing

