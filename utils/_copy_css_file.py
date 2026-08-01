
def _copy_css_file(app, exc):
    if exc is None and app.builder.format == 'html':
        src = cbook._get_data_path('plot_directive/plot_directive.css')
        dst = app.outdir / Path('_static')
        dst.mkdir(exist_ok=True)
        # Use copyfile because we do not want to copy src's permissions.
        shutil.copyfile(src, dst / Path('plot_directive.css'))

