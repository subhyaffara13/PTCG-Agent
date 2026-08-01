
def save_chat(filename: str, chat: list[dict], settings: dict) -> str:
    """Saves the chat history to a file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        json.dump({"settings": settings, "chat_history": chat}, f, indent=4)
    return os.path.abspath(filename)

