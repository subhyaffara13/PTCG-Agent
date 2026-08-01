
def pressure_network_fun_and_grad(flow_rates, Qtot, k):
    return (pressure_network(flow_rates, Qtot, k),
            pressure_network_jacobian(flow_rates, Qtot, k))

