import math


def exact2018(exact):
    # SI base constants
    c = exact['speed of light in vacuum']
    h = exact['Planck constant']
    e = exact['elementary charge']
    k = exact['Boltzmann constant']
    N_A = exact['Avogadro constant']

    # Other useful constants
    R = N_A * k
    hbar = h / (2*math.pi)
    G_0 = 2 * e**2 / h

    # Wien law numerical constants: https://en.wikipedia.org/wiki/Wien%27s_displacement_law
    # (alpha - 3)*exp(alpha) + 3 = 0
    # (x - 5)*exp(x) + 5 = 0
    alpha_W = 2.821439372122078893403  # 3 + lambertw(-3 * exp(-3))
    x_W = 4.965114231744276303699  # 5 + lambertw(-5 * exp(-5))

    # Conventional electrical unit
    # See https://en.wikipedia.org/wiki/Conventional_electrical_unit
    K_J90 = exact['conventional value of Josephson constant']
    K_J = 2 * e / h
    R_K90 = exact['conventional value of von Klitzing constant']
    R_K = h / e**2
    V_90 = K_J90 / K_J
    ohm_90 = R_K / R_K90
    A_90 = V_90 / ohm_90

    replace = {
        'atomic unit of action': hbar,
        'Boltzmann constant in eV/K': k / e,
        'Boltzmann constant in Hz/K': k / h,
        'Boltzmann constant in inverse meter per kelvin': k / (h * c),
        'conductance quantum': G_0,
        'conventional value of ampere-90': A_90,
        'conventional value of coulomb-90': A_90,
        'conventional value of farad-90': 1 / ohm_90,
        'conventional value of henry-90': ohm_90,
        'conventional value of ohm-90': ohm_90,
        'conventional value of volt-90': V_90,
        'conventional value of watt-90': V_90**2 / ohm_90,
        'electron volt-hertz relationship': e / h,
        'electron volt-inverse meter relationship': e / (h * c),
        'electron volt-kelvin relationship': e / k,
        'electron volt-kilogram relationship': e / c**2,
        'elementary charge over h-bar': e / hbar,
        'Faraday constant': e * N_A,
        'first radiation constant': 2 * math.pi * h * c**2,
        'first radiation constant for spectral radiance': 2 * h * c**2,
        'hertz-electron volt relationship': h / e,
        'hertz-inverse meter relationship': 1 / c,
        'hertz-kelvin relationship': h / k,
        'hertz-kilogram relationship': h / c**2,
        'inverse meter-electron volt relationship': (h * c) / e,
        'inverse meter-joule relationship': h * c,
        'inverse meter-kelvin relationship': h * c / k,
        'inverse meter-kilogram relationship': h / c,
        'inverse of conductance quantum': 1 / G_0,
        'Josephson constant': K_J,
        'joule-electron volt relationship': 1 / e,
        'joule-hertz relationship': 1 / h,
        'joule-inverse meter relationship': 1 / (h * c),
        'joule-kelvin relationship': 1 / k,
        'joule-kilogram relationship': 1 / c**2,
        'kelvin-electron volt relationship': k / e,
        'kelvin-hertz relationship': k / h,
        'kelvin-inverse meter relationship': k / (h * c),
        'kelvin-kilogram relationship': k / c**2,
        'kilogram-electron volt relationship': c**2 / e,
        'kilogram-hertz relationship': c**2 / h,
        'kilogram-inverse meter relationship': c / h,
        'kilogram-joule relationship': c**2,
        'kilogram-kelvin relationship': c**2 / k,
        'Loschmidt constant (273.15 K, 100 kPa)': 100e3 / 273.15 / k,
        'Loschmidt constant (273.15 K, 101.325 kPa)': 101.325e3 / 273.15 / k,
        'mag. flux quantum': h / (2 * e),
        'molar gas constant': R,
        'molar Planck constant': h * N_A,
        'molar volume of ideal gas (273.15 K, 100 kPa)': R * 273.15 / 100e3,
        'molar volume of ideal gas (273.15 K, 101.325 kPa)': R * 273.15 / 101.325e3,
        'natural unit of action': hbar,
        'natural unit of action in eV s': hbar / e,
        'Planck constant in eV/Hz': h / e,
        'reduced Planck constant': hbar,
        'reduced Planck constant in eV s': hbar / e,
        'reduced Planck constant times c in MeV fm': hbar * c / (e * 1e6 * 1e-15),
        'second radiation constant': h * c / k,
        'Stefan-Boltzmann constant': 2 * math.pi**5 * k**4 / (15 * h**3 * c**2),
        'von Klitzing constant': R_K,
        'Wien frequency displacement law constant': alpha_W * k / h,
        'Wien wavelength displacement law constant': h * c / (x_W * k),
    }
    return replace

