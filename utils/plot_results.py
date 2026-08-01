
def plot_results(summary_data, output_dir):
    """
    Plots the results and saves them to files.
    """
    max_turns = sorted([int(k) for k in summary_data.keys()])
    metrics = ["total_cost", "total_tokens", "total_prompt_tokens", "total_completion_tokens"]

    for metric in metrics:
        means = [summary_data[str(t)][metric]["mean"] for t in max_turns]
        stds = [summary_data[str(t)][metric]["std"] for t in max_turns]

        plt.figure(figsize=(10, 6))
        plt.errorbar(max_turns, means, yerr=stds, fmt="-o", capsize=5, ecolor="red", markeredgecolor="black")
        plt.xlabel("Maximum Turns in Discussion")
        plt.ylabel(metric.replace("_", " ").title())
        plt.title(f"{metric.replace('_', ' ').title()} vs. Maximum Turns")
        plt.grid(True, which="both", linestyle="--", linewidth=0.5)
        plt.xticks(max_turns)

        plot_filename = os.path.join(output_dir, f"{metric}_vs_max_turns.png")
        plt.savefig(plot_filename)
        plt.close()
        logger.info(f"Saved plot: {plot_filename}")

