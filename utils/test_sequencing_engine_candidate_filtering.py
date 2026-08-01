
def test_sequencing_engine_candidate_filtering():
    candidates = [
        "play_trainer:Ultra Ball",      # search phase
        "play_trainer:Professor's Research", # draw phase
        "bench:1",                      # board phase
        "attack:Punch",                 # attack phase
        "pass"                          # attack phase
    ]
    
    seq_engine = SequencingEngine()
    groups = seq_engine.group_actions(candidates)
    assert "search" in groups
    assert "play_trainer:Ultra Ball" in groups["search"]

