
def test_card_registry_behavioral_parsing():
    registry = CardRegistry()
    # Check that attributes exist on CardRegistry
    assert hasattr(registry, "target_setup_duration")
    assert hasattr(registry, "target_bench_density")
    assert hasattr(registry, "target_deck_stats")
    assert hasattr(registry, "behavior_donts_rules")

