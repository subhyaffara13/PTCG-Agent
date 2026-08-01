
def update_circle(im, _, state):
    """Updates the visualization for the circle environment.


    Args:
      im: The list of matplotlib artists to update.
      state: The state of the environment.


    Returns:
      A list of matplotlib artists to update during the episode.
    """
    anno_goal = im[0]
    anno_agent = im[1]
    anno_goal.center = (state.goal[0], state.goal[1])
    anno_agent.center = (state.pos[0], state.pos[1])
    return [anno_goal, anno_agent]

