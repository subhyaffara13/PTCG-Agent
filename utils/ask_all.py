
def ask_all(*queries, assumptions):
    return fuzzy_and(
        (ask(query, assumptions) for query in queries))

