
def construct_loss_function(m, loss, f_scale):
    if loss == 'linear':
        return None

    if not callable(loss):
        loss = IMPLEMENTED_LOSSES[loss]
        rho = np.empty((3, m))

        def loss_function(f, cost_only=False):
            z = (f / f_scale) ** 2
            loss(z, rho, cost_only=cost_only)
            if cost_only:
                return 0.5 * f_scale ** 2 * np.sum(rho[0])
            rho[0] *= f_scale ** 2
            rho[2] /= f_scale ** 2
            return rho
    else:
        def loss_function(f, cost_only=False):
            z = (f / f_scale) ** 2
            rho = loss(z)
            if cost_only:
                return 0.5 * f_scale ** 2 * np.sum(rho[0])
            rho[0] *= f_scale ** 2
            rho[2] /= f_scale ** 2
            return rho

    return loss_function

