
def adjust_entity_positions(entity, text):
    """Adjust the positions of the entities in `text` to be relative to the text with special fields removed."""
    entity_name, (start, end) = entity
    # computed the length of strings with special fields (tag tokens, patch index tokens, etc.) removed
    adjusted_start = len(re.sub("<.*?>", "", text[:start]))
    adjusted_end = len(re.sub("<.*?>", "", text[:end]))
    adjusted_entity = (entity_name, (adjusted_start, adjusted_end))
    return adjusted_entity

