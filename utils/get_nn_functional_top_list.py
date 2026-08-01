
def get_nn_functional_top_list() -> list[tuple[str, int]]:
    top_nn_functional_: dict[str, int] = dict(top_nn_functional)
    for _, count, functional_name in top_nn_module:
        if functional_name is None:
            continue
        if functional_name == "torch.flatten":
            continue
        if functional_name not in top_nn_functional_:
            top_nn_functional_[functional_name] = count
        else:
            top_nn_functional_[functional_name] += count

    top_nn_functional_list = list(top_nn_functional_.items())
    top_nn_functional_list.sort(key=operator.itemgetter(1), reverse=True)
    return top_nn_functional_list

