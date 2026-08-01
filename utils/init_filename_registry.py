
def init_filename_registry(app):
    env = app.builder.env
    if not hasattr(env, 'mpl_plot_image_basenames'):
        env.mpl_plot_image_basenames = defaultdict(set)

