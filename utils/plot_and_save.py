
def plot_and_save(expr, *args, name='', dir=None, **kwargs):
    p = plot_implicit(expr, *args, **kwargs)
    p.save(tmp_file(dir=dir, name=name))
    # Close the plot to avoid a warning from matplotlib
    p._backend.close()

