
def is_serve_available() -> bool:
    return is_pydantic_available() and is_fastapi_available() and is_uvicorn_available() and is_openai_available()

