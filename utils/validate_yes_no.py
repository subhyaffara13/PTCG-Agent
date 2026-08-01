
def validate_yes_no(question: str, default: Literal["yes", "no"] | None) -> bool:
    """Validate that a yes or no answer is correct."""
    question = f"{question} (y)es or (n)o "
    if default:
        question += f" (default={default}) "
    # pylint: disable-next=bad-builtin
    answer = input(question).lower()

    if not answer and default:
        answer = default

    if answer not in YES_NO_ANSWERS:
        raise InvalidUserInput(", ".join(sorted(YES_NO_ANSWERS)), answer)

    return answer.startswith("y")

