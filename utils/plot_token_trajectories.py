
def plot_token_trajectories(trajectories_data, output_dir):
    """
    Plots token usage trajectories, grouped by max_turns, and saves them to files.
    """
    for metric, trajectories_by_turns in trajectories_data.items():
        if not trajectories_by_turns:
            continue

        plt.figure(figsize=(12, 8))

        # Create a color map for the different turn settings
        turn_keys = sorted(trajectories_by_turns.keys(), key=int)
        colors = plt.cm.viridis(np.linspace(0, 1, len(turn_keys)))
        color_map = {turns: color for turns, color in zip(turn_keys, colors)}

        for turns, trajectories in sorted(trajectories_by_turns.items(), key=lambda item: int(item[0])):
            for i, traj in enumerate(trajectories):
                # Only add a label to the first trajectory of each group for a clean legend
                label = f"Max Turns: {turns}" if i == 0 else None
                plt.plot(np.arange(len(traj)), traj, linestyle="-", alpha=0.4, color=color_map[turns], label=label)

        plt.title(f"{metric.replace('_', ' ').title()} per Query Step Trajectories")
        plt.xlabel("Query Step")
        plt.ylabel(f"{metric.replace('_', ' ').title()} per Query Step")
        plt.grid(True, which="both", linestyle="--", linewidth=0.5)
        plt.legend()

        plot_filename = os.path.join(output_dir, f"{metric}_trajectories.png")
        plt.savefig(plot_filename)
        plt.close()
        logger.info(f"Saved trajectory plot: {plot_filename}")


def plot_token_trajectories(trajectories_data, output_dir):
    """
    Plots token usage trajectories, grouped by max_turns, and saves them to files.
    """
    for metric, trajectories_by_turns in trajectories_data.items():
        if not trajectories_by_turns:
            logger.warning(f"No data found for metric '{metric}'. Skipping plot.")
            continue

        plt.figure(figsize=(12, 8))

        # Create a color map for the different turn settings
        turn_keys = sorted(trajectories_by_turns.keys(), key=int)
        colors = plt.cm.viridis(np.linspace(0, 1, len(turn_keys)))
        color_map = {turns: color for turns, color in zip(turn_keys, colors)}

        for turns, trajectories in sorted(trajectories_by_turns.items(), key=lambda item: int(item[0])):
            for i, traj in enumerate(trajectories):
                if not all(isinstance(x, (int, float)) for x in traj):
                    logger.error(
                        f"Trajectory for metric '{metric}' (turns={turns}) contains non-numeric data. Skipping."
                    )
                    continue
                # Only add a label to the first trajectory of each group for a clean legend
                label = f"Max Turns: {turns}" if i == 0 else None
                plt.plot(np.arange(len(traj)), traj, linestyle="-", alpha=0.4, color=color_map[turns], label=label)

        plt.title(f"{metric.replace('_', ' ').title()} per Query Step Trajectories")
        plt.xlabel("Query Step")
        plt.ylabel(f"{metric.replace('_', ' ').title()} per Query Step")
        plt.grid(True, which="both", linestyle="--", linewidth=0.5)
        plt.legend()

        plot_filename = os.path.join(output_dir, f"{metric}_trajectories.png")
        plt.savefig(plot_filename)
        plt.close()
        logger.info(f"Saved trajectory plot: {plot_filename}")

