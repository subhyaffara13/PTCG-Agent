
def _new_private():
    return {
        "shed": {item: 0 for item in PRODUCTS + list(ANIMALS)},
        "seeds": {crop: 0 for crop in CROPS},
        # inventories[0] = main farmer; hands appended/removed each day.
        "inventories": [{}],
    }

