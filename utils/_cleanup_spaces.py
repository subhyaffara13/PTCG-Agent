
def _cleanup_spaces(text, entities):
    """Remove the spaces around the text and the entities in it."""
    new_text = text.strip()
    leading_spaces = len(text) - len(text.lstrip())

    new_entities = []
    for entity_name, (start, end), bboxes in entities:
        entity_name_leading_spaces = len(entity_name) - len(entity_name.lstrip())
        entity_name_trailing_spaces = len(entity_name) - len(entity_name.rstrip())

        start = start - leading_spaces + entity_name_leading_spaces
        end = end - leading_spaces - entity_name_trailing_spaces
        entity_name = entity_name.strip()

        new_entities.append((entity_name, (start, end), bboxes))

    return new_text, new_entities

