
def ask_any(*queries, assumptions):
    return fuzzy_or(
        (ask(query, assumptions) for query in queries))

