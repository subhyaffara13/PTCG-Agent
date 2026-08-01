
def _remove_participant_epilogue(
    state: _RendezvousState, settings: RendezvousSettings
) -> None:
    if state.complete:
        # If we do not have any participants left, move to the next round.
        if not state.participants:
            msg = "No participants left in the rendezvous, marking rendezvous as incomplete"
            logger.debug(msg)
            state.complete = False

            state.round += 1
    else:
        if len(state.participants) < settings.min_nodes:
            msg = (
                f"Number of participants {len(state.participants)}) less than"
                f"min_nodes {settings.min_nodes}, clearning deadline in state"
            )
            logger.debug(msg)
            state.deadline = None

