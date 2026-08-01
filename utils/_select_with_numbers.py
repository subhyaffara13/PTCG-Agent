
def _select_with_numbers(prompt: str, choices: list[str]) -> int:
    print(f"? {prompt}")
    for i, choice in enumerate(choices, start=1):
        print(f"  {i}. {choice}")
    while True:
        raw = input("Choice [1]: ").strip()
        if not raw:
            return 0
        if raw.isdecimal() and 1 <= int(raw) <= len(choices):
            return int(raw) - 1
        print(f"Invalid choice. Enter a number between 1 and {len(choices)}.")

