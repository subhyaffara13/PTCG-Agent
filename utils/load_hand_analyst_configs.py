
def load_hand_analyst_configs(agent, shared_context):
    """Loads strategic thresholds and tip overrides."""
    agent.strategy_tips = {"priority_modifiers": {}}
    tips_path = agent.skills_dir / "strategy_tips.json"
    if tips_path.exists():
        try:
            agent.strategy_tips = json.loads(tips_path.read_text(encoding="utf-8"))
        except Exception as e:
            logger.error(f"Failed strategy_tips load: {e}")

    agent.strategy_thresholds = {}
    if shared_context:
        agent.strategy_thresholds = shared_context.get_config(str(agent.skills_dir), "strategy_thresholds.json")
    else:
        try:
            from cb_agents.context import SharedContext
            agent.strategy_thresholds = SharedContext().get_config(str(agent.skills_dir), "strategy_thresholds.json")
        except:
            pass


def load_hand_analyst_configs(agent, shared_context):
    """Loads strategic thresholds and tip overrides."""
    agent.strategy_tips = {"priority_modifiers": {}}
    tips_path = agent.skills_dir / "strategy_tips.json"
    if tips_path.exists():
        try:
            agent.strategy_tips = json.loads(tips_path.read_text(encoding="utf-8"))
        except Exception as e:
            logger.error(f"Failed strategy_tips load: {e}")

    agent.strategy_thresholds = {}
    if shared_context:
        agent.strategy_thresholds = shared_context.get_config(str(agent.skills_dir), "strategy_thresholds.json")
    else:
        try:
            from cb_agents.context import SharedContext
            agent.strategy_thresholds = SharedContext().get_config(str(agent.skills_dir), "strategy_thresholds.json")
        except Exception as e:
            logger.debug(f"Failed to load strategy_thresholds from context fallback: {e}")


def load_hand_analyst_configs(agent, shared_context):
    """Loads strategic thresholds and tip overrides."""
    agent.strategy_tips = {"priority_modifiers": {}}
    tips_path = agent.skills_dir / "strategy_tips.json"
    if tips_path.exists():
        try:
            agent.strategy_tips = json.loads(tips_path.read_text(encoding="utf-8"))
        except Exception as e:
            logger.error(f"Failed strategy_tips load: {e}")

    agent.strategy_thresholds = {}
    if shared_context:
        agent.strategy_thresholds = shared_context.get_config(str(agent.skills_dir), "strategy_thresholds.json")
    else:
        try:
            from cb_agents.context import SharedContext
            agent.strategy_thresholds = SharedContext().get_config(str(agent.skills_dir), "strategy_thresholds.json")
        except Exception as e:
            logger.debug(f"Failed to load strategy_thresholds from context fallback: {e}")

