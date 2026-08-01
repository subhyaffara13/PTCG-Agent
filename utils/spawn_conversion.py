
def spawn_conversion(token: str, private: bool, model_id: str):
    logger.info("Attempting to convert .bin model on the fly to safetensors.")

    safetensors_convert_space_url = "https://safetensors-convert.hf.space"
    sse_url = f"{safetensors_convert_space_url}/call/run"

    def start(_sse_connection):
        for line in _sse_connection.iter_lines():
            if not isinstance(line, str):
                line = line.decode()
            if line.startswith("event:"):
                status = line[7:]
                logger.debug(f"Safetensors conversion status: {status}")

                if status == "complete":
                    return
                elif status == "heartbeat":
                    logger.debug("Heartbeat")
                else:
                    logger.debug(f"Unknown status {status}")
            else:
                logger.debug(line)

    data = {"data": [model_id, private, token]}

    result = httpx.post(sse_url, follow_redirects=True, json=data).json()
    event_id = result["event_id"]

    with httpx.stream("GET", f"{sse_url}/{event_id}") as sse_connection:
        try:
            logger.debug("Spawning safetensors automatic conversion.")
            start(sse_connection)
        except Exception as e:
            logger.warning(f"Error during conversion: {repr(e)}")

