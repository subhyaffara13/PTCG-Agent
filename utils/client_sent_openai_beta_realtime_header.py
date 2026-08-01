
def client_sent_openai_beta_realtime_header(websocket: Any) -> bool:
    """True when the client WebSocket includes ``OpenAI-Beta: realtime=v1``."""
    return RealTimeStreaming._detect_beta_header(websocket)

