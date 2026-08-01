
def test_game_logger_auto_hook_router(tmp_path):
    delegation = {"on_trigger": "strategy_agent"}
    bus = RouterBus(delegation, log_dir=str(tmp_path))
    bus.register_agent("strategy_agent", lambda p: {"result": "success"})
    
    gl = GameLogger(log_dir=str(tmp_path))
    gl.register_with_bus(bus)
    
    packet = StrategyPacket(trigger="turn_draw", board_summary={})
    res = bus.dispatch("on_trigger", packet)
    
    assert res == {"result": "success"}
    assert len(gl.action_logs) == 1
    assert gl.action_logs[0]["action_taken"] == "on_trigger"
    assert gl.action_logs[0]["agent_called"] == "strategy_agent"

