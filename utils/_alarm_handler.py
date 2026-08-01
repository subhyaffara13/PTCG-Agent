
def _alarm_handler(signum, frame):
    raise _AblationTimeout("game exceeded --game-timeout")

