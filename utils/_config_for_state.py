
def _config_for_state(pyspiel_state: pyspiel.State) -> hh_utils.Config:
    """Build the hh_utils.Config the upstream agent hard-coded."""
    # TODO: extract small_blind / big_blind / starting_stacks from the state's
    # universal_poker game params. Upstream has the same TODO and hard-codes
    # these for HU NLHE 1/2 with 200/200 stacks; preserving for prompt parity.
    return hh_utils.Config(
        seats=pyspiel_state.num_players(),
        small_blind=1,
        big_blind=2,
        starting_stacks=[200] * pyspiel_state.num_players(),
    )

