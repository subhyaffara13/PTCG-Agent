
def _hangman_state_to_string(state: HangmanState, show_word: bool = True):
  if state.word:
    assert state.letters_revealed
    letters_revealed_str = "".join(state.letters_revealed)
    assert state.letters_guessed is not None
    letters_guessed_str = "".join(state.letters_guessed)
    word_line = f"Word:             {state.word}\n" if show_word else ""
    return (word_line + f"Letters Revealed: {letters_revealed_str}\n" +
                        f"Letters Guessed:  {letters_guessed_str}\n" +
                        f"Num guesses: {state.num_guesses}\n")
  else:
    return "Not started yet"

