
def compute_stats(stats) -> None:
    unsupported_calls = {cuda_call for (cuda_call, _filepath) in stats["unsupported_calls"]}

    # Print the number of unsupported calls
    print(f"Total number of unsupported CUDA function calls: {len(unsupported_calls):d}")

    # Print the list of unsupported calls
    print(", ".join(unsupported_calls))

    # Print the number of kernel launches
    print(f"\nTotal number of replaced kernel launches: {len(stats['kernel_launches']):d}")

