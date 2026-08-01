
def get_redis_url_from_environment():
    if "REDIS_URL" in os.environ:
        return os.environ["REDIS_URL"]

    if "REDIS_HOST" not in os.environ or "REDIS_PORT" not in os.environ:
        raise ValueError(
            "Either 'REDIS_URL' or both 'REDIS_HOST' and 'REDIS_PORT' must be specified for Redis."
        )

    if "REDIS_SSL" in os.environ and os.environ["REDIS_SSL"].lower() == "true":
        redis_protocol = "rediss"
    else:
        redis_protocol = "redis"

    # Build authentication part of URL
    auth_part = ""
    if "REDIS_USERNAME" in os.environ and "REDIS_PASSWORD" in os.environ:
        auth_part = f"{os.environ['REDIS_USERNAME']}:{os.environ['REDIS_PASSWORD']}@"
    elif "REDIS_PASSWORD" in os.environ:
        auth_part = f"{os.environ['REDIS_PASSWORD']}@"

    return f"{redis_protocol}://{auth_part}{os.environ['REDIS_HOST']}:{os.environ['REDIS_PORT']}"

