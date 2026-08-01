
def add_numeric_values_to_question(question):
    """Adds numeric value spans to a question."""
    original_text = question
    question = normalize_for_match(question)
    numeric_spans = parse_text(question)
    return Question(original_text=original_text, text=question, numeric_spans=numeric_spans)

