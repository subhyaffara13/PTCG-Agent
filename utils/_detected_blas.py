
def _detected_blas():
    blas = np.show_config('dicts').get('Build Dependencies', {}).get('blas', {})
    return blas.get('name', 'unknown'), blas.get('version', 'unknown')

