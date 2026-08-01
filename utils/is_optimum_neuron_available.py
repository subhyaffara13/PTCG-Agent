
def is_optimum_neuron_available() -> bool:
    return is_optimum_available() and _is_package_available("optimum.neuron")[0]

