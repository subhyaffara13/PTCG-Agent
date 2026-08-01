
def _using_accelerate():
    config = np.show_config('dicts')
    return config['Build Dependencies']['blas']['name'].lower() == 'accelerate'

