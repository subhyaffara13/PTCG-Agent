
def _gemma4_json_to_json(text: str) -> str:
    """Convert Gemma4 tool call format (unquoted keys, ``<|"|>`` string delimiters) to valid JSON."""
    strings = []

    def _capture(m):
        strings.append(m.group(1))
        return f"\x00{len(strings) - 1}\x00"

    # Grab the inside of gemma-quotes and store them for later
    text = re.sub(r'<\|"\|>(.*?)<\|"\|>', _capture, text, flags=re.DOTALL)
    # Add quotes to the bare keys elsewhere
    text = re.sub(r"(?<=[{,])(\w+):", r'"\1":', text)

    # Put the inside of the quotes back afterwards
    for i, s in enumerate(strings):
        text = text.replace(f"\x00{i}\x00", json.dumps(s))

    return text

