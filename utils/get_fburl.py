import subprocess

def get_fburl(url: str) -> str:
    short_url = url
    # Attempt to shorten the URL
    try:
        result = subprocess.run(
            ["fburl", url], capture_output=True, stdin=subprocess.DEVNULL
        )
        if result.returncode == 0:
            short_url = result.stdout.decode("utf-8")
    except Exception as e:
        logger.warning("URL shortening failed: %s, using long URL", repr(e))
    return short_url

