
def _make_run_options(self: Run) -> Options:
    """Return the options used in a Run class."""
    return (
        (
            "rcfile",
            {
                "action": _DoNothingAction,
                "kwargs": {},
                "group": "Commands",
                "help": "Specify a configuration file to load.",
                "hide_from_config_file": True,
            },
        ),
        (
            "output",
            {
                "action": _DoNothingAction,
                "kwargs": {},
                "group": "Commands",
                "help": "Specify an output file.",
                "hide_from_config_file": True,
            },
        ),
        (
            "init-hook",
            {
                "action": _DoNothingAction,
                "kwargs": {},
                "help": "Python code to execute, usually for sys.path "
                "manipulation such as pygtk.require().",
            },
        ),
        (
            "help-msg",
            {
                "action": _MessageHelpAction,
                "kwargs": {"Run": self},
                "group": "Commands",
                "help": "Display a help message for the given message id and "
                "exit. The value may be a comma separated list of message ids.",
                "hide_from_config_file": True,
            },
        ),
        (
            "list-msgs",
            {
                "action": _ListMessagesAction,
                "kwargs": {"Run": self},
                "group": "Commands",
                "help": "Display a list of all pylint's messages divided by whether "
                "they are emittable with the given interpreter.",
                "hide_from_config_file": True,
            },
        ),
        (
            "list-msgs-enabled",
            {
                "action": _ListMessagesEnabledAction,
                "kwargs": {"Run": self},
                "group": "Commands",
                "help": "Display a list of what messages are enabled, "
                "disabled and non-emittable with the given configuration.",
                "hide_from_config_file": True,
            },
        ),
        (
            "list-groups",
            {
                "action": _ListCheckGroupsAction,
                "kwargs": {"Run": self},
                "group": "Commands",
                "help": "List pylint's message groups.",
                "hide_from_config_file": True,
            },
        ),
        (
            "list-conf-levels",
            {
                "action": _ListConfidenceLevelsAction,
                "kwargs": {"Run": self},
                "group": "Commands",
                "help": "Generate pylint's confidence levels.",
                "hide_from_config_file": True,
            },
        ),
        (
            "list-extensions",
            {
                "action": _ListExtensionsAction,
                "kwargs": {"Run": self},
                "group": "Commands",
                "help": "List available extensions.",
                "hide_from_config_file": True,
            },
        ),
        (
            "full-documentation",
            {
                "action": _FullDocumentationAction,
                "kwargs": {"Run": self},
                "group": "Commands",
                "help": "Generate pylint's full documentation.",
                "hide_from_config_file": True,
            },
        ),
        (
            "generate-rcfile",
            {
                "action": _GenerateRCFileAction,
                "kwargs": {"Run": self},
                "group": "Commands",
                "help": "Generate a sample configuration file according to "
                "the current configuration. You can put other options "
                "before this one to get them in the generated "
                "configuration.",
                "hide_from_config_file": True,
            },
        ),
        (
            "generate-toml-config",
            {
                "action": _GenerateConfigFileAction,
                "kwargs": {"Run": self},
                "group": "Commands",
                "help": "Generate a sample configuration file according to "
                "the current configuration. You can put other options "
                "before this one to get them in the generated "
                "configuration. The config is in the .toml format.",
                "hide_from_config_file": True,
            },
        ),
        (
            "errors-only",
            {
                "action": _ErrorsOnlyModeAction,
                "kwargs": {"Run": self},
                "short": "E",
                "help": "In error mode, messages with a category besides "
                "ERROR or FATAL are suppressed, and no reports are done by default. "
                "Error mode is compatible with disabling specific errors. ",
                "hide_from_config_file": True,
            },
        ),
        (
            "verbose",
            {
                "action": _DoNothingAction,
                "kwargs": {},
                "short": "v",
                "help": "In verbose mode, extra non-checker-related info "
                "will be displayed.",
                "hide_from_config_file": True,
                "metavar": "",
            },
        ),
        (
            "enable-all-extensions",
            {
                "action": _DoNothingAction,
                "kwargs": {},
                "help": "Load and enable all available extensions. "
                "Use --list-extensions to see a list all available extensions.",
                "hide_from_config_file": True,
                "metavar": "",
            },
        ),
        (
            "long-help",
            {
                "action": _LongHelpAction,
                "kwargs": {"Run": self},
                "help": "Show more verbose help.",
                "group": "Commands",
                "hide_from_config_file": True,
            },
        ),
    )

