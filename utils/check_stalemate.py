
def check_stalemate(logs):
    rt = logs.get("reasoning_test", {}).get("game_data", {})
    if rt.get("prizes_taken_b", 0) == 0 and rt.get("prizes_taken_a", 0) == 0:
        if rt.get("turns_taken", 0) >= 90:
            logger.error("CRITICAL_STALEMATE_ERROR: reasoning_test match ended in timeout with 0 prizes taken!")
            return True
    return False

