
def notake(env_state):
    """This function is called if the player has decided to not take a card.

    Calling this function ends the active portion
    of the game and turns control over to the dealer.
    """
    state, key = env_state
    dealer_hand = state.dealer_hand
    player_hand = state.player_hand
    dealer_cards = state.dealer_cards
    player_cards = state.player_cards

    key, dealer_hand, dealer_cards = jax.lax.while_loop(
        dealer_stop,
        draw_card_wrapper,
        (key, dealer_hand, dealer_cards),
    )

    return (
        EnvState(
            dealer_hand=dealer_hand,
            player_hand=player_hand,
            dealer_cards=dealer_cards,
            player_cards=player_cards,
            done=1,
        ),
        key,
    )

