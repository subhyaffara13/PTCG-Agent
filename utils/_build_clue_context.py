
def _build_clue_context(observation: Mapping[str, Any]) -> str:
    """Build the clue / guess-progress context string for Guesser turns."""
    clue = observation.get("clue", "")
    clue_number = observation.get("clue_number", 0)
    remaining = observation.get("guesses_remaining", 0)

    parts: list[str] = []

    # Clarify the last entry in current_game_turns for the guesser.
    if observation.get("current_game_turns"):
        parts.append(
            "Note: The last entry in the 'Clues and guesses in this game so "
            "far' list above represents your current turn, showing the guesses "
            "you have already made for the current clue.\n\n",
        )

    parts.append(
        f"The clue from your Cluemaster is: '{clue}' for {clue_number} "
        f"words. (You have {remaining} guesses remaining this turn.)\n\n",
    )

    if clue_number > 0:
        parts.append(
            f"If you correctly guess {clue_number} words based on this clue, "
            "you may make a bonus guess based on all information you've "
            "received so far.\n\n",
        )

        correct_guesses = (clue_number + 1) - remaining
        words_remaining = remaining - 1

        if correct_guesses > 0:
            current_guesses: list[str] = []
            game_turns = observation.get("current_game_turns")
            if game_turns:
                current_guesses = game_turns[-1].get("guesses", [])
            guesses_str = ", ".join(current_guesses)

            if words_remaining == 0:
                parts.append(
                    f"You have correctly guessed all {clue_number} words for "
                    f"this clue (Guessed: {guesses_str}). You are now on your "
                    "bonus guess!\n\n",
                )
            else:
                parts.append(
                    f"You have correctly guessed {correct_guesses} times for "
                    f"this clue already (Guessed: {guesses_str}), meaning "
                    f"there are {words_remaining} words related to the clue "
                    "remaining.\n\n",
                )
    elif clue_number == 0:
        parts.append(
            "A clue number of 0 means NONE of your remaining words relate to "
            "this clue (often used to point out the trap). You get unlimited "
            "guesses, but you MUST still make at least one guess.\n\n",
        )
    elif clue_number == -1:
        parts.append(
            "A clue number of -1 means 'Infinity'. You get unlimited guesses "
            "based on this clue and previous clues. You must make at least one "
            "guess.\n\n",
        )

    return "".join(parts)

