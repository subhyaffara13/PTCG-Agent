
def test_opponent_model_archetype_predictor():
    om = OpponentModel(log_dir="logs", skills_dir="skills")
    
    # Mock signature cards for combo (e.g. charizard-ex-obs-125)
    packet = OpponentModelPacket(
        turn=1,
        newly_played_cards=["charizard-ex-obs-125", "pidgeot-ex-obs-164", "rare-candy-sv1-191"],
        revealed_active_pokemon="charmander-obs-023",
        revealed_bench_count=1,
        revealed_hand_size=5,
        revealed_prizes_remaining=6,
        revealed_discard=[],
        game_phase="early"
    )
    
    result = om.receive(packet)
    assert result["inferred_deck_type"] == "combo"
    assert result["archetype_confidence"] > 0.0

