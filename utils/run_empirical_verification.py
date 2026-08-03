import json
from pathlib import Path


def run_empirical_verification():
    print("=== Empirical Verification of Dynamic Configuration (Task 1) ===")
    
    # Paths
    project_dir = Path("C:/Users/subhy/.gemini/antigravity/scratch/ptcg-agent")
    skills_dir = project_dir / "skills"
    config_file = skills_dir / "strategy_thresholds.json"
    
    # Save original config
    original_config_content = config_file.read_text(encoding="utf-8")
    original_config = json.loads(original_config_content)
    
    try:
        # Clear SharedContext to start clean
        SharedContext._caches.clear()
        
        # Instantiate HandAnalyst and StrategyAgent
        analyst = HandAnalyst(log_dir=str(project_dir / "logs"), skills_dir=str(skills_dir))
        agent = StrategyAgent(log_dir=str(project_dir / "logs"), skills_dir=str(skills_dir))
        
        # Scenario 1: Initial configuration values
        # Let's check original trigger_rules in config
        orig_trigger_rules = original_config["strategy_agent"]["trigger_rules"]
        orig_prize_gap = orig_trigger_rules.get("prize_gap_threshold", 2)
        print(f"Original prize_gap_threshold: {orig_prize_gap}")
        
        # Send a packet where my_prizes = 6, opponent_prizes = 4 (gap = 2)
        packet_sa = StrategyPacket(trigger="turn_start", board_summary={
            "my_prizes_remaining": 6,
            "opponent_prizes_remaining": 4, # gap = 2
            "opponent_archetype_confidence": 0.1,
            "priority_profile": "aggro_push",
            "turn_number": 2
        })
        
        res_sa_1 = agent.receive(packet_sa)
        print(f"Scenario 1 (Original Config, gap=2): StrategyAgent triggered = {res_sa_1['triggered']}")
        
        # Scenario 2: Change config on disk (increase prize_gap_threshold to 5)
        modified_config = json.loads(original_config_content)
        modified_config["strategy_agent"]["trigger_rules"]["prize_gap_threshold"] = 5
        config_file.write_text(json.dumps(modified_config, indent=2), encoding="utf-8")
        print("\n[Disk Change] Modified strategy_thresholds.json: prize_gap_threshold set to 5")
        
        # Evaluate using the same existing agent instance (without clearing cache)
        res_sa_2 = agent.receive(packet_sa)
        print(f"Scenario 2 (Existing Instance, gap=2): StrategyAgent triggered = {res_sa_2['triggered']}")
        
        # Scenario 3: Create a new agent instance (without clearing cache)
        new_agent = StrategyAgent(log_dir=str(project_dir / "logs"), skills_dir=str(skills_dir))
        res_sa_3 = new_agent.receive(packet_sa)
        print(f"Scenario 3 (New Instance, same process, no cache clear): StrategyAgent triggered = {res_sa_3['triggered']}")
        
        # Scenario 4: Clear SharedContext cache and create a new agent
        SharedContext._caches.clear()
        fresh_agent = StrategyAgent(log_dir=str(project_dir / "logs"), skills_dir=str(skills_dir))
        res_sa_4 = fresh_agent.receive(packet_sa)
        print(f"Scenario 4 (Fresh Instance, cache cleared): StrategyAgent triggered = {res_sa_4['triggered']}")
        
        # Verify HandAnalyst dynamic thresholds
        # Let's check original hand_analyst bonuses/multipliers
        orig_ha = original_config["hand_analyst"]
        orig_search_bench = orig_ha["combo_multipliers"].get("search_and_bench", 0.1)
        print(f"\nOriginal HandAnalyst search_and_bench multiplier: {orig_search_bench}")
        
        # HandAnalystPacket with a search trainer and a basic pokemon
        # Card registry needs to be consulted or mocked. We can check actual registry to see what cards exist.
        # Let's inspect the cards in skills/card_scoring.json
        
    finally:
        # Restore original config
        config_file.write_text(original_config_content, encoding="utf-8")
        print("\nOriginal config file restored.")

