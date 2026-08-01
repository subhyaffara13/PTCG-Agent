
def _fitstart_S1(data):
    # We follow McCullock 1986 method - Simple Consistent Estimators
    # of Stable Distribution Parameters

    # fmt: off
    # Table III and IV
    nu_alpha_range = [2.439, 2.5, 2.6, 2.7, 2.8, 3, 3.2, 3.5, 4,
                      5, 6, 8, 10, 15, 25]
    nu_beta_range = [0, 0.1, 0.2, 0.3, 0.5, 0.7, 1]

    # table III - alpha = psi_1(nu_alpha, nu_beta)
    alpha_table = np.array([
        [2.000, 2.000, 2.000, 2.000, 2.000, 2.000, 2.000],
        [1.916, 1.924, 1.924, 1.924, 1.924, 1.924, 1.924],
        [1.808, 1.813, 1.829, 1.829, 1.829, 1.829, 1.829],
        [1.729, 1.730, 1.737, 1.745, 1.745, 1.745, 1.745],
        [1.664, 1.663, 1.663, 1.668, 1.676, 1.676, 1.676],
        [1.563, 1.560, 1.553, 1.548, 1.547, 1.547, 1.547],
        [1.484, 1.480, 1.471, 1.460, 1.448, 1.438, 1.438],
        [1.391, 1.386, 1.378, 1.364, 1.337, 1.318, 1.318],
        [1.279, 1.273, 1.266, 1.250, 1.210, 1.184, 1.150],
        [1.128, 1.121, 1.114, 1.101, 1.067, 1.027, 0.973],
        [1.029, 1.021, 1.014, 1.004, 0.974, 0.935, 0.874],
        [0.896, 0.892, 0.884, 0.883, 0.855, 0.823, 0.769],
        [0.818, 0.812, 0.806, 0.801, 0.780, 0.756, 0.691],
        [0.698, 0.695, 0.692, 0.689, 0.676, 0.656, 0.597],
        [0.593, 0.590, 0.588, 0.586, 0.579, 0.563, 0.513]]).T
    # transpose because interpolation with `RectBivariateSpline` is with
    # `nu_beta` as `x` and `nu_alpha` as `y`

    # table IV - beta = psi_2(nu_alpha, nu_beta)
    beta_table = np.array([
        [0, 2.160, 1.000, 1.000, 1.000, 1.000, 1.000],
        [0, 1.592, 3.390, 1.000, 1.000, 1.000, 1.000],
        [0, 0.759, 1.800, 1.000, 1.000, 1.000, 1.000],
        [0, 0.482, 1.048, 1.694, 1.000, 1.000, 1.000],
        [0, 0.360, 0.760, 1.232, 2.229, 1.000, 1.000],
        [0, 0.253, 0.518, 0.823, 1.575, 1.000, 1.000],
        [0, 0.203, 0.410, 0.632, 1.244, 1.906, 1.000],
        [0, 0.165, 0.332, 0.499, 0.943, 1.560, 1.000],
        [0, 0.136, 0.271, 0.404, 0.689, 1.230, 2.195],
        [0, 0.109, 0.216, 0.323, 0.539, 0.827, 1.917],
        [0, 0.096, 0.190, 0.284, 0.472, 0.693, 1.759],
        [0, 0.082, 0.163, 0.243, 0.412, 0.601, 1.596],
        [0, 0.074, 0.147, 0.220, 0.377, 0.546, 1.482],
        [0, 0.064, 0.128, 0.191, 0.330, 0.478, 1.362],
        [0, 0.056, 0.112, 0.167, 0.285, 0.428, 1.274]]).T

    # Table V and VII
    # These are ordered with decreasing `alpha_range`; so we will need to
    # reverse them as required by RectBivariateSpline.
    alpha_range = [2, 1.9, 1.8, 1.7, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1,
                   1, 0.9, 0.8, 0.7, 0.6, 0.5][::-1]
    beta_range = [0, 0.25, 0.5, 0.75, 1]

    # Table V - nu_c = psi_3(alpha, beta)
    nu_c_table = np.array([
        [1.908, 1.908, 1.908, 1.908, 1.908],
        [1.914, 1.915, 1.916, 1.918, 1.921],
        [1.921, 1.922, 1.927, 1.936, 1.947],
        [1.927, 1.930, 1.943, 1.961, 1.987],
        [1.933, 1.940, 1.962, 1.997, 2.043],
        [1.939, 1.952, 1.988, 2.045, 2.116],
        [1.946, 1.967, 2.022, 2.106, 2.211],
        [1.955, 1.984, 2.067, 2.188, 2.333],
        [1.965, 2.007, 2.125, 2.294, 2.491],
        [1.980, 2.040, 2.205, 2.435, 2.696],
        [2.000, 2.085, 2.311, 2.624, 2.973],
        [2.040, 2.149, 2.461, 2.886, 3.356],
        [2.098, 2.244, 2.676, 3.265, 3.912],
        [2.189, 2.392, 3.004, 3.844, 4.775],
        [2.337, 2.634, 3.542, 4.808, 6.247],
        [2.588, 3.073, 4.534, 6.636, 9.144]])[::-1].T
    # transpose because interpolation with `RectBivariateSpline` is with
    # `beta` as `x` and `alpha` as `y`

    # Table VII - nu_zeta = psi_5(alpha, beta)
    nu_zeta_table = np.array([
        [0, 0.000, 0.000, 0.000, 0.000],
        [0, -0.017, -0.032, -0.049, -0.064],
        [0, -0.030, -0.061, -0.092, -0.123],
        [0, -0.043, -0.088, -0.132, -0.179],
        [0, -0.056, -0.111, -0.170, -0.232],
        [0, -0.066, -0.134, -0.206, -0.283],
        [0, -0.075, -0.154, -0.241, -0.335],
        [0, -0.084, -0.173, -0.276, -0.390],
        [0, -0.090, -0.192, -0.310, -0.447],
        [0, -0.095, -0.208, -0.346, -0.508],
        [0, -0.098, -0.223, -0.380, -0.576],
        [0, -0.099, -0.237, -0.424, -0.652],
        [0, -0.096, -0.250, -0.469, -0.742],
        [0, -0.089, -0.262, -0.520, -0.853],
        [0, -0.078, -0.272, -0.581, -0.997],
        [0, -0.061, -0.279, -0.659, -1.198]])[::-1].T
    # fmt: on

    psi_1 = RectBivariateSpline(nu_beta_range, nu_alpha_range,
                                alpha_table, kx=1, ky=1, s=0)

    def psi_1_1(nu_beta, nu_alpha):
        return psi_1(nu_beta, nu_alpha) \
            if nu_beta > 0 else psi_1(-nu_beta, nu_alpha)

    psi_2 = RectBivariateSpline(nu_beta_range, nu_alpha_range,
                                beta_table, kx=1, ky=1, s=0)

    def psi_2_1(nu_beta, nu_alpha):
        return psi_2(nu_beta, nu_alpha) \
            if nu_beta > 0 else -psi_2(-nu_beta, nu_alpha)

    phi_3 = RectBivariateSpline(beta_range, alpha_range, nu_c_table,
                                kx=1, ky=1, s=0)

    def phi_3_1(beta, alpha):
        return phi_3(beta, alpha) if beta > 0 else phi_3(-beta, alpha)

    phi_5 = RectBivariateSpline(beta_range, alpha_range, nu_zeta_table,
                                kx=1, ky=1, s=0)

    def phi_5_1(beta, alpha):
        return phi_5(beta, alpha) if beta > 0 else -phi_5(-beta, alpha)

    # quantiles
    p05 = np.percentile(data, 5)
    p50 = np.percentile(data, 50)
    p95 = np.percentile(data, 95)
    p25 = np.percentile(data, 25)
    p75 = np.percentile(data, 75)

    nu_alpha = (p95 - p05) / (p75 - p25)
    nu_beta = (p95 + p05 - 2 * p50) / (p95 - p05)

    if nu_alpha >= 2.439:
        eps = np.finfo(float).eps
        alpha = np.clip(psi_1_1(nu_beta, nu_alpha)[0, 0], eps, 2.)
        beta = np.clip(psi_2_1(nu_beta, nu_alpha)[0, 0], -1.0, 1.0)
    else:
        alpha = 2.0
        beta = np.sign(nu_beta)
    c = (p75 - p25) / phi_3_1(beta, alpha)[0, 0]
    zeta = p50 + c * phi_5_1(beta, alpha)[0, 0]
    delta = zeta-beta*c*np.tan(np.pi*alpha/2.) if alpha != 1. else zeta

    return (alpha, beta, delta, c)

