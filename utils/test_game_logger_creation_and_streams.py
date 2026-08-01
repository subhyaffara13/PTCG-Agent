
def test_game_logger_creation_and_streams(tmp_path):
    logger = GameLogger(log_dir=str(tmp_path))
    assert logger.perspective_flag == "player"
    assert len(logger.action_logs) == 0
    assert len(logger.reasoning_logs) == 0
    assert len(logger.variance_logs) == 0

