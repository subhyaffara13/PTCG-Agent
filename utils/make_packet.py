from router.packets import OpponentModelPacket


def make_packet(**overrides) -> OpponentModelPacket:
    defaults = dict(
        turn=1,
        newly_played_cards=[],
        revealed_active_pokemon=None,
        revealed_bench_count=0,
        revealed_hand_size=5,
        revealed_prizes_remaining=6,
        revealed_discard=[],
        game_phase="early",
    )
    defaults.update(overrides)
    return OpponentModelPacket(**defaults)

