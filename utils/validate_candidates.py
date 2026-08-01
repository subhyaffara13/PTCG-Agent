
def validate_candidates(validator, deck_candidate, logic_candidate, eval_report):
    valid = True
    if deck_candidate:
        val_res = validator.validate(deck_candidate, eval_report)
        if not val_res.get("promoted"):
            valid = False
    if logic_candidate:
        val_res = validator.validate(logic_candidate, eval_report)
        if not val_res.get("promoted"):
            valid = False
    return valid

