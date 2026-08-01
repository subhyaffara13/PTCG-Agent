
def find_integrator(name):
    for cl in IntegratorBase.integrator_classes:
        if re.match(name, cl.__name__, re.I):
            return cl
    return None

