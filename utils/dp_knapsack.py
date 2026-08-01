
def dp_knapsack(
    memory: list[float], runtime: list[float], max_memory: float
) -> tuple[float, list[int], list[int]]:
    # Scaling factor to convert floating point weights to integers
    S = 10000

    # Quantize the memory weights
    quantized_memory = torch.tensor(
        [round(m * S) for m in memory], dtype=torch.long, device="cpu"
    )
    runtimes = torch.tensor(runtime, dtype=torch.float32, device="cpu")

    # Quantized pseudopolynomial DP for 0-1 Knapsack
    quantized_max_memory = round(max_memory * S)

    n = len(memory)

    # Initialize the DP table
    # TODO(chilli): I think if needed, this memory can be optimized with sliding
    # window trick + Hirschberg trick:
    # https://codeforces.com/blog/entry/47247?#comment-316200
    dp = torch.zeros(
        (n + 1, quantized_max_memory + 1), dtype=torch.float32, device="cpu"
    )

    for i in range(1, n + 1):
        current_memory = quantized_memory[i - 1]
        current_runtime = runtimes[i - 1]

        # Copy the previous row
        dp[i, :] = dp[i - 1, :]

        # Update dp[i, j] for all j >= current_memory
        if current_memory == 0:
            dp[i, :] = dp[i - 1, :] + current_runtime
        else:
            dp[i, current_memory:] = torch.maximum(
                dp[i - 1, current_memory:],
                dp[i - 1, :-current_memory] + current_runtime,
            )

    # Backtrack to find the items included in the knapsack
    saved_items = []
    recomputable_items = []
    j: int = quantized_max_memory
    for i in range(n, 0, -1):
        if dp[i][j] != dp[i - 1][j]:
            saved_items.append(i - 1)  # Include this item (indexing from 0)
            j -= int(quantized_memory[i - 1].item())
        else:
            recomputable_items.append(i - 1)

    saved_items.reverse()  # To get items in the order they were added

    # The maximum runtime that can be achieved within the max_memory constraint
    max_runtime = dp[n][quantized_max_memory].item()

    return max_runtime, saved_items, recomputable_items

