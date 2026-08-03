import logging
import os
import sys
from typing import Any

def setup(app):
    # Add hook for building doxygen xml when needed
    app.connect("builder-inited", generate_doxygen_xml)

    # Copy the readme in
    app.connect("builder-inited", prepare)

    # Clean up the generated readme
    app.connect("build-finished", clean_up)


def setup(app):
    app.add_directive('pygmentsdoc', PygmentsDoc)


def setup(**attrs) -> Distribution:
    logging.configure()
    # Make sure we have any requirements needed to interpret 'attrs'.
    _install_setup_requires(attrs)
    # Override return type of distutils.core.Distribution with setuptools.dist.Distribution
    # (implicitly implemented via `setuptools.monkey.patch_all`).
    return distutils.core.setup(**attrs)  # type: ignore[return-value]


def setup(app: Sphinx) -> dict[str, Any]:
    LOG.info('loading stevedore.sphinxext')
    app.add_directive('list-plugins', ListPluginsDirective)
    return {'parallel_read_safe': True, 'parallel_write_safe': True}


def setup(app: t.Any) -> dict[str, t.Any]:
    """Registers the Sphinx extension.

    You shouldn't need to call this directly; configure Sphinx to use this
    module instead.
    """
    app.add_object_type("configtrait", "configtrait", objname="Config option")
    return {"parallel_read_safe": True, "parallel_write_safe": True}


def setup(key, value=None):
    """Assign a value to (or reset) a configuration item. """
    key = key.upper()

    if value is not None:
        _current_config[key] = value
    else:
        _current_config[key] = _default_config[key]


def setup(**attrs):  # noqa: C901
    """The gateway to the Distutils: do everything your setup script needs
    to do, in a highly flexible and user-driven way.  Briefly: create a
    Distribution instance; find and parse config files; parse the command
    line; run each Distutils command found there, customized by the options
    supplied to 'setup()' (as keyword arguments), in config files, and on
    the command line.

    The Distribution instance might be an instance of a class supplied via
    the 'distclass' keyword argument to 'setup'; if no such class is
    supplied, then the Distribution class (in dist.py) is instantiated.
    All other arguments to 'setup' (except for 'cmdclass') are used to set
    attributes of the Distribution instance.

    The 'cmdclass' argument, if supplied, is a dictionary mapping command
    names to command classes.  Each command encountered on the command line
    will be turned into a command class, which is in turn instantiated; any
    class found in 'cmdclass' is used in place of the default, which is
    (for command 'foo_bar') class 'foo_bar' in module
    'distutils.command.foo_bar'.  The command class must provide a
    'user_options' attribute which is a list of option specifiers for
    'distutils.fancy_getopt'.  Any command-line options between the current
    and the next command are used to set attributes of the current command
    object.

    When the entire command-line has been successfully parsed, calls the
    'run()' method on each command object in turn.  This method will be
    driven entirely by the Distribution object (which each command object
    has a reference to, thanks to its constructor), and the
    command-specific options that became attributes of each command
    object.
    """

    global _setup_stop_after, _setup_distribution

    # Determine the distribution class -- either caller-supplied or
    # our Distribution (see below).
    klass = attrs.get('distclass')
    if klass:
        attrs.pop('distclass')
    else:
        klass = Distribution

    if 'script_name' not in attrs:
        attrs['script_name'] = os.path.basename(sys.argv[0])
    if 'script_args' not in attrs:
        attrs['script_args'] = sys.argv[1:]

    # Create the Distribution instance, using the remaining arguments
    # (ie. everything except distclass) to initialize it
    try:
        _setup_distribution = dist = klass(attrs)
    except DistutilsSetupError as msg:
        if 'name' not in attrs:
            raise SystemExit(f"error in setup command: {msg}")
        else:
            raise SystemExit("error in {} setup command: {}".format(attrs['name'], msg))

    if _setup_stop_after == "init":
        return dist

    # Find and parse the config file(s): they will override options from
    # the setup script, but be overridden by the command line.
    dist.parse_config_files()

    if DEBUG:
        print("options (after parsing config files):")
        dist.dump_option_dicts()

    if _setup_stop_after == "config":
        return dist

    # Parse the command line and override config files; any
    # command-line errors are the end user's fault, so turn them into
    # SystemExit to suppress tracebacks.
    try:
        ok = dist.parse_command_line()
    except DistutilsArgError as msg:
        raise SystemExit(gen_usage(dist.script_name) + f"\nerror: {msg}")

    if DEBUG:
        print("options (after parsing command line):")
        dist.dump_option_dicts()

    if _setup_stop_after == "commandline":
        return dist

    # And finally, run all the commands found on the command line.
    if ok:
        return run_commands(dist)

    return dist


def setup(app):
    app.add_directive('pygmentsdoc', PygmentsDoc)


def setup(app):
    app.add_directive("figure-mpl", FigureMpl)
    figurempl_addnode(app)
    metadata = {'parallel_read_safe': True, 'parallel_write_safe': True,
                'version': matplotlib.__version__}
    return metadata


def setup(app):
    setup.app = app
    app.add_config_value('mathmpl_fontsize', 10.0, True)
    app.add_config_value('mathmpl_srcset', [], True)
    try:
        app.connect('config-inited', _config_inited)  # Sphinx 1.8+
    except ExtensionError:
        app.connect('env-updated', lambda app, env: _config_inited(app, None))

    # Add visit/depart methods to HTML-Translator:
    def visit_latex_math_html(self, node):
        source = self.document.attributes['source']
        self.body.append(latex2html(node, source))

    def depart_latex_math_html(self, node):
        pass

    # Add visit/depart methods to LaTeX-Translator:
    def visit_latex_math_latex(self, node):
        inline = isinstance(node.parent, nodes.TextElement)
        if inline:
            self.body.append('$%s$' % node['latex'])
        else:
            self.body.extend(['\\begin{equation}',
                              node['latex'],
                              '\\end{equation}'])

    def depart_latex_math_latex(self, node):
        pass

    app.add_node(latex_math,
                 html=(visit_latex_math_html, depart_latex_math_html),
                 latex=(visit_latex_math_latex, depart_latex_math_latex))
    app.add_role('mathmpl', math_role)
    app.add_directive('mathmpl', MathDirective)
    if sphinx.version_info < (1, 8):
        app.add_role('math', math_role)
        app.add_directive('math', MathDirective)

    metadata = {'parallel_read_safe': True, 'parallel_write_safe': True}
    return metadata


def setup(app):
    setup.app = app
    setup.config = app.config
    setup.confdir = app.confdir
    app.add_directive('plot', PlotDirective)
    app.add_config_value('plot_pre_code', None, True)
    app.add_config_value('plot_include_source', False, True)
    app.add_config_value('plot_html_show_source_link', True, True)
    app.add_config_value('plot_formats', ['png', 'hires.png', 'pdf'], True)
    app.add_config_value('plot_basedir', None, True)
    app.add_config_value('plot_html_show_formats', True, True)
    app.add_config_value('plot_rcparams', {}, True)
    app.add_config_value('plot_apply_rcparams', False, True)
    app.add_config_value('plot_working_directory', None, True)
    app.add_config_value('plot_template', None, True)
    app.add_config_value('plot_srcset', [], True)
    app.connect('doctree-read', mark_plot_labels)
    app.add_css_file('plot_directive.css')
    app.connect('build-finished', _copy_css_file)
    metadata = {'parallel_read_safe': True, 'parallel_write_safe': True,
                'version': matplotlib.__version__}
    app.connect('builder-inited', init_filename_registry)
    app.add_env_collector(_FilenameCollector)
    return metadata


def setup(app):
    app.add_role("rc", _rcparam_role)
    app.add_role("mpltype", _mpltype_role)
    app.add_node(
        _QueryReference,
        html=(_visit_query_reference_node, _depart_query_reference_node),
        latex=(_visit_query_reference_node, _depart_query_reference_node),
        text=(_visit_query_reference_node, _depart_query_reference_node),
    )
    return {"version": matplotlib.__version__,
            "parallel_read_safe": True, "parallel_write_safe": True}


def setup():
    # The baseline images are created in this locale, so we should use
    # it during all of the tests.

    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'English_United States.1252')
        except locale.Error:
            _log.warning(
                "Could not set locale to English/United States. "
                "Some date-related tests may fail.")

    mpl.use('Agg')

    with _api.suppress_matplotlib_deprecation_warning():
        mpl.rcdefaults()  # Start with all defaults

    # These settings *must* be hardcoded for running the comparison tests and
    # are not necessarily the default values as specified in rcsetup.py.
    set_font_settings_for_testing()
    set_reproducibility_for_testing()

