
def init_maze(ax, env, state, _):
    """Initializes the maze visualization."""
    _ = ax.imshow(env.occupied_map, cmap="Greys")
    anno_pos = ax.annotate(
        "A",
        fontsize=20,
        xy=(state.pos[1], state.pos[0]),
        xycoords="data",
        xytext=(state.pos[1] - 0.3, state.pos[0] + 0.25),
    )
    _ = ax.annotate(
        "G",
        fontsize=20,
        xy=(state.goal[1], state.goal[0]),
        xycoords="data",
        xytext=(state.goal[1] - 0.3, state.goal[0] + 0.25),
    )
    ax.set_xticks([])
    ax.set_yticks([])
    return anno_pos

