from typing import Any, Callable

def argument(
    *param_decls: str, cls: type[Argument] | None = None, **attrs: t.Any
) -> t.Callable[[FC], FC]:
    """Attaches an argument to the command.  All positional arguments are
    passed as parameter declarations to :class:`Argument`; all keyword
    arguments are forwarded unchanged (except ``cls``).
    This is equivalent to creating an :class:`Argument` instance manually
    and attaching it to the :attr:`Command.params` list.

    For the default argument class, refer to :class:`Argument` and
    :class:`Parameter` for descriptions of parameters.

    :param cls: the argument class to instantiate.  This defaults to
                :class:`Argument`.
    :param param_decls: Passed as positional arguments to the constructor of
        ``cls``.
    :param attrs: Passed as keyword arguments to the constructor of ``cls``.
    """
    if cls is None:
        cls = Argument

    def decorator(f: FC) -> FC:
        _param_memo(f, cls(param_decls, **attrs))
        return f

    return decorator


def Argument(
    # Parameter
    default: Any | None = ...,
    *,
    callback: Callable[..., Any] | None = None,
    metavar: str | None = None,
    expose_value: bool = True,
    is_eager: bool = False,
    envvar: str | list[str] | None = None,
    # Note that shell_complete is not fully supported and will be removed in future versions
    # TODO: Remove shell_complete in a future version (after 0.16.0)
    shell_complete: Callable[
        [click.Context, click.Parameter, str],
        list["click.shell_completion.CompletionItem"] | list[str],
    ]
    | None = None,
    autocompletion: Callable[..., Any] | None = None,
    default_factory: Callable[[], Any] | None = None,
    # Custom type
    parser: Callable[[str], Any] | None = None,
    # TyperArgument
    show_default: bool | str = True,
    show_choices: bool = True,
    show_envvar: bool = True,
    help: str | None = None,
    hidden: bool = False,
    # Choice
    case_sensitive: bool = True,
    # Numbers
    min: int | float | None = None,
    max: int | float | None = None,
    clamp: bool = False,
    # DateTime
    formats: list[str] | None = None,
    # File
    mode: str | None = None,
    encoding: str | None = None,
    errors: str | None = "strict",
    lazy: bool | None = None,
    atomic: bool = False,
    # Path
    exists: bool = False,
    file_okay: bool = True,
    dir_okay: bool = True,
    writable: bool = False,
    readable: bool = True,
    resolve_path: bool = False,
    allow_dash: bool = False,
    path_type: None | type[str] | type[bytes] = None,
    # Rich settings
    rich_help_panel: str | None = None,
) -> Any: ...


def Argument(
    # Parameter
    default: Any | None = ...,
    *,
    callback: Callable[..., Any] | None = None,
    metavar: str | None = None,
    expose_value: bool = True,
    is_eager: bool = False,
    envvar: str | list[str] | None = None,
    # Note that shell_complete is not fully supported and will be removed in future versions
    # TODO: Remove shell_complete in a future version (after 0.16.0)
    shell_complete: Callable[
        [click.Context, click.Parameter, str],
        list["click.shell_completion.CompletionItem"] | list[str],
    ]
    | None = None,
    autocompletion: Callable[..., Any] | None = None,
    default_factory: Callable[[], Any] | None = None,
    # Custom type
    click_type: click.ParamType | None = None,
    # TyperArgument
    show_default: bool | str = True,
    show_choices: bool = True,
    show_envvar: bool = True,
    help: str | None = None,
    hidden: bool = False,
    # Choice
    case_sensitive: bool = True,
    # Numbers
    min: int | float | None = None,
    max: int | float | None = None,
    clamp: bool = False,
    # DateTime
    formats: list[str] | None = None,
    # File
    mode: str | None = None,
    encoding: str | None = None,
    errors: str | None = "strict",
    lazy: bool | None = None,
    atomic: bool = False,
    # Path
    exists: bool = False,
    file_okay: bool = True,
    dir_okay: bool = True,
    writable: bool = False,
    readable: bool = True,
    resolve_path: bool = False,
    allow_dash: bool = False,
    path_type: None | type[str] | type[bytes] = None,
    # Rich settings
    rich_help_panel: str | None = None,
) -> Any: ...


def Argument(
    # Parameter
    default: Annotated[
        Any | None,
        Doc(
            """
            By default, CLI arguments are required. However, by giving them a default value they become [optional](https://typer.tiangolo.com/tutorial/arguments/optional):

            **Example**

            ```python
            @app.command()
            def main(name: str = typer.Argument("World")):
                print(f"Hello {name}!")
            ```

            Note that this usage is deprecated, and we recommend to use `Annotated` instead:
            ```python
            @app.command()
            def main(name: Annotated[str, typer.Argument()] = "World"):
                print(f"Hello {name}!")
            ```
            """
        ),
    ] = ...,
    *,
    callback: Annotated[
        Callable[..., Any] | None,
        Doc(
            """
            Add a callback to this CLI Argument, to execute additional logic with the value received from the terminal.
            See [the tutorial about callbacks](https://typer.tiangolo.com/tutorial/options/callback-and-context/) for more details.

            **Example**

            ```python
            def name_callback(value: str):
                if value != "Deadpool":
                    raise typer.BadParameter("Only Deadpool is allowed")
                return value

            @app.command()
            def main(name: Annotated[str, typer.Argument(callback=name_callback)]):
                print(f"Hello {name}")
            ```
            """
        ),
    ] = None,
    metavar: Annotated[
        str | None,
        Doc(
            """
            Customize the name displayed in the help text to represent this CLI Argument.
            By default, it will be the same name you declared, in uppercase.
            See [the tutorial about CLI Arguments with Help](https://typer.tiangolo.com/tutorial/arguments/help/#custom-help-name-metavar) for more details.

            **Example**

            ```python
            @app.command()
            def main(name: Annotated[str, typer.Argument(metavar="✨username✨")]):
                print(f"Hello {name}")
            ```
            """
        ),
    ] = None,
    expose_value: Annotated[
        bool,
        Doc(
            """
            **Note**: you probably shouldn't use this parameter, it is inherited from Click and supported for compatibility.

            ---

            If this is `True` then the value is passed onwards to the command callback and stored on the context, otherwise it’s skipped.
            """
        ),
    ] = True,
    is_eager: Annotated[
        bool,
        Doc(
            """
            Set an argument to "eager" to ensure it gets processed before other CLI parameters. This could be relevant when there are other parameters with callbacks that could exit the program early.
            For more information and an extended example, see the documentation [here](https://typer.tiangolo.com/tutorial/options/version/#fix-with-is_eager).
            """
        ),
    ] = False,
    envvar: Annotated[
        str | list[str] | None,
        Doc(
            """
            Configure an argument to read a value from an environment variable if it is not provided in the command line as a CLI argument.
            For more information, see the [documentation on Environment Variables](https://typer.tiangolo.com/tutorial/arguments/envvar/).

            **Example**

            ```python
            @app.command()
            def main(name: Annotated[str, typer.Argument(envvar="ME")]):
                print(f"Hello Mr. {name}")
            ```
            """
        ),
    ] = None,
    # TODO: Remove shell_complete in a future version (after 0.16.0)
    shell_complete: Annotated[
        Callable[
            [click.Context, click.Parameter, str],
            list["click.shell_completion.CompletionItem"] | list[str],
        ]
        | None,
        Doc(
            """
            **Note**: you probably shouldn't use this parameter, it is inherited from Click and supported for compatibility.
            It is however not fully functional, and will likely be removed in future versions.
            """
        ),
    ] = None,
    autocompletion: Annotated[
        Callable[..., Any] | None,
        Doc(
            """
            Provide a custom function that helps to autocomplete the values of this CLI Argument.
            See [the tutorial on parameter autocompletion](https://typer.tiangolo.com/tutorial/options-autocompletion) for more details.

            **Example**

            ```python
            def complete():
                return ["Me", "Myself", "I"]

            @app.command()
            def main(name: Annotated[str, typer.Argument(autocompletion=complete)]):
                print(f"Hello {name}")
            ```
            """
        ),
    ] = None,
    default_factory: Annotated[
        Callable[[], Any] | None,
        Doc(
            """
            Provide a custom function that dynamically generates a [default](https://typer.tiangolo.com/tutorial/arguments/default) for this CLI Argument.

            **Example**

            ```python
            def get_name():
                return random.choice(["Me", "Myself", "I"])

            @app.command()
            def main(name: Annotated[str, typer.Argument(default_factory=get_name)]):
                print(f"Hello {name}")
            ```
            """
        ),
    ] = None,
    # Custom type
    parser: Annotated[
        Callable[[str], Any] | None,
        Doc(
            """
            Use your own custom types in Typer applications by defining a `parser` function that parses input into your own types:

            **Example**

            ```python
            class CustomClass:
                def __init__(self, value: str):
                    self.value = value

                def __str__(self):
                    return f"<CustomClass: value={self.value}>"

            def my_parser(value: str):
                return CustomClass(value * 2)

            @app.command()
            def main(arg: Annotated[CustomClass, typer.Argument(parser=my_parser):
                print(f"arg is {arg}")
            ```
            """
        ),
    ] = None,
    click_type: Annotated[
        click.ParamType | None,
        Doc(
            """
            Define this parameter to use a [custom Click type](https://click.palletsprojects.com/en/stable/parameters/#implementing-custom-types) in your Typer applications.

            **Example**

            ```python
            class MyClass:
                def __init__(self, value: str):
                    self.value = value

                def __str__(self):
                    return f"<MyClass: value={self.value}>"

            class MyParser(click.ParamType):
                name = "MyClass"

                def convert(self, value, param, ctx):
                    return MyClass(value * 3)

            @app.command()
            def main(arg: Annotated[MyClass, typer.Argument(click_type=MyParser())]):
                print(f"arg is {arg}")
            ```
            """
        ),
    ] = None,
    # TyperArgument
    show_default: Annotated[
        bool | str,
        Doc(
            """
            When set to `False`, don't show the default value of this CLI Argument in the [help text](https://typer.tiangolo.com/tutorial/arguments/help/).

            **Example**

            ```python
            @app.command()
            def main(name: Annotated[str, typer.Argument(show_default=False)] = "Rick"):
                print(f"Hello {name}")
            ```
            """
        ),
    ] = True,
    show_choices: Annotated[
        bool,
        Doc(
            """
            **Note**: you probably shouldn't use this parameter, it is inherited from Click and supported for compatibility.

            ---

            When set to `False`, this suppresses choices from being displayed inline when `prompt` is used.
            """
        ),
    ] = True,
    show_envvar: Annotated[
        bool,
        Doc(
            """
            When an ["envvar"](https://typer.tiangolo.com/tutorial/arguments/envvar) is defined, prevent it from showing up in the help text:

            **Example**

            ```python
            @app.command()
            def main(name: Annotated[str, typer.Argument(envvar="ME", show_envvar=False)]):
                print(f"Hello Mr. {name}")
            ```
            """
        ),
    ] = True,
    help: Annotated[
        str | None,
        Doc(
            """
            Help text for this CLI Argument.
            See [the tutorial about CLI Arguments with help](https://typer.tiangolo.com/tutorial/arguments/help/) for more dedails.

            **Example**

            ```python
            @app.command()
            def greet(name: Annotated[str, typer.Argument(help="Person to greet")]):
                print(f"Hello {name}")
            ```
            """
        ),
    ] = None,
    hidden: Annotated[
        bool,
        Doc(
            """
            Hide this CLI Argument from [help outputs](https://typer.tiangolo.com/tutorial/arguments/help). `False` by default.

            **Example**

            ```python
            @app.command()
            def main(name: Annotated[str, typer.Argument(hidden=True)] = "World"):
                print(f"Hello {name}")
            ```
            """
        ),
    ] = False,
    # Choice
    case_sensitive: Annotated[
        bool,
        Doc(
            """
            For a CLI Argument representing an [Enum (choice)](https://typer.tiangolo.com/tutorial/parameter-types/enum),
            you can allow case-insensitive matching with this parameter:

            **Example**

            ```python
            from enum import Enum

            class NeuralNetwork(str, Enum):
                simple = "simple"
                conv = "conv"
                lstm = "lstm"

            @app.command()
            def main(
                network: Annotated[NeuralNetwork, typer.Argument(case_sensitive=False)]):
                print(f"Training neural network of type: {network.value}")
            ```

            With this setting, "LSTM" or "lstm" will both be valid values that will be resolved to `NeuralNetwork.lstm`.
            """
        ),
    ] = True,
    # Numbers
    min: Annotated[
        int | float | None,
        Doc(
            """
            For a CLI Argument representing a [number](https://typer.tiangolo.com/tutorial/parameter-types/number/) (`int` or `float`),
            you can define numeric validations with `min` and `max` values:

            **Example**

            ```python
            @app.command()
            def main(
                user: Annotated[str, typer.Argument()],
                user_id: Annotated[int, typer.Argument(min=1, max=1000)],
            ):
                print(f"ID for {user} is {user_id}")
            ```

            If the user attempts to input an invalid number, an error will be shown, explaining why the value is invalid.
            """
        ),
    ] = None,
    max: Annotated[
        int | float | None,
        Doc(
            """
            For a CLI Argument representing a [number](https://typer.tiangolo.com/tutorial/parameter-types/number/) (`int` or `float`),
            you can define numeric validations with `min` and `max` values:

            **Example**

            ```python
            @app.command()
            def main(
                user: Annotated[str, typer.Argument()],
                user_id: Annotated[int, typer.Argument(min=1, max=1000)],
            ):
                print(f"ID for {user} is {user_id}")
            ```

            If the user attempts to input an invalid number, an error will be shown, explaining why the value is invalid.
            """
        ),
    ] = None,
    clamp: Annotated[
        bool,
        Doc(
            """
            For a CLI Argument representing a [number](https://typer.tiangolo.com/tutorial/parameter-types/number/) and that is bounded by using `min` and/or `max`,
            you can opt to use the closest minimum or maximum value instead of raising an error. This is done by setting `clamp` to `True`.

            **Example**

            ```python
            @app.command()
            def main(
                user: Annotated[str, typer.Argument()],
                user_id: Annotated[int, typer.Argument(min=1, max=1000, clamp=True)],
            ):
                print(f"ID for {user} is {user_id}")
            ```

            If the user attempts to input 3420 for `user_id`, this will internally be converted to `1000`.
            """
        ),
    ] = False,
    # DateTime
    formats: Annotated[
        list[str] | None,
        Doc(
            """
            For a CLI Argument representing a [DateTime object](https://typer.tiangolo.com/tutorial/parameter-types/datetime),
            you can customize the formats that can be parsed automatically:

            **Example**

            ```python
            from datetime import datetime

            @app.command()
            def main(
                birthday: Annotated[
                    datetime,
                    typer.Argument(
                        formats=["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%m/%d/%Y"]
                    ),
                ],
            ):
                print(f"Birthday defined at: {birthday}")
            ```
            """
        ),
    ] = None,
    # File
    mode: Annotated[
        str | None,
        Doc(
            """
            For a CLI Argument representing a [File object](https://typer.tiangolo.com/tutorial/parameter-types/file/),
            you can customize the mode to open the file with. If unset, Typer will set a [sensible value by default](https://typer.tiangolo.com/tutorial/parameter-types/file/#advanced-mode).

            **Example**

            ```python
            @app.command()
            def main(config: Annotated[typer.FileText, typer.Argument(mode="a")]):
                config.write("This is a single line\\n")
                print("Config line written")
            ```
            """
        ),
    ] = None,
    encoding: Annotated[
        str | None,
        Doc(
            """
            Customize the encoding of this CLI Argument represented by a [File object](https://typer.tiangolo.com/tutorial/parameter-types/file/).

            **Example**

            ```python
            @app.command()
            def main(config: Annotated[typer.FileText, typer.Argument(encoding="utf-8")]):
                config.write("All the text gets written\\n")
            ```
            """
        ),
    ] = None,
    errors: Annotated[
        str | None,
        Doc(
            """
            **Note**: you probably shouldn't use this parameter, it is inherited from Click and supported for compatibility.

            ---

            The error handling mode.
            """
        ),
    ] = "strict",
    lazy: Annotated[
        bool | None,
        Doc(
            """
            For a CLI Argument representing a [File object](https://typer.tiangolo.com/tutorial/parameter-types/file/),
            by default the file will not be created until you actually start writing to it.
            You can change this behaviour by setting this parameter.
            By default, it's set to `True` for writing and to `False` for reading.

            **Example**

            ```python
            @app.command()
            def main(config: Annotated[typer.FileText, typer.Argument(mode="a", lazy=False)]):
                config.write("This is a single line\\n")
                print("Config line written")
            ```
            """
        ),
    ] = None,
    atomic: Annotated[
        bool,
        Doc(
            """
            For a CLI Argument representing a [File object](https://typer.tiangolo.com/tutorial/parameter-types/file/),
            you can ensure that all write instructions first go into a temporal file, and are only moved to the final destination after completing
            by setting `atomic` to `True`. This can be useful for files with potential concurrent access.

            **Example**

            ```python
            @app.command()
            def main(config: Annotated[typer.FileText, typer.Argument(mode="a", atomic=True)]):
                config.write("All the text")
            ```
            """
        ),
    ] = False,
    # Path
    exists: Annotated[
        bool,
        Doc(
            """
            When set to `True` for a [`Path` argument](https://typer.tiangolo.com/tutorial/parameter-types/path/),
            additional validation is performed to check that the file or directory exists. If not, the value will be invalid.

            **Example**

            ```python
            from pathlib import Path

            @app.command()
            def main(config: Annotated[Path, typer.Argument(exists=True)]):
                text = config.read_text()
                print(f"Config file contents: {text}")
            ```
            """
        ),
    ] = False,
    file_okay: Annotated[
        bool,
        Doc(
            """
            Determine whether or not a [`Path` argument](https://typer.tiangolo.com/tutorial/parameter-types/path/)
            is allowed to refer to a file. When this is set to `False`, the application will raise a validation error when a path to a file is given.

            **Example**

            ```python
            from pathlib import Path

            @app.command()
            def main(config: Annotated[Path, typer.Argument(exists=True, file_okay=False)]):
                print(f"Directory listing: {[x.name for x in config.iterdir()]}")
            ```
            """
        ),
    ] = True,
    dir_okay: Annotated[
        bool,
        Doc(
            """
            Determine whether or not a [`Path` argument](https://typer.tiangolo.com/tutorial/parameter-types/path/)
            is allowed to refer to a directory. When this is set to `False`, the application will raise a validation error when a path to a directory is given.

            **Example**

            ```python
            from pathlib import Path

            @app.command()
            def main(config: Annotated[Path, typer.Argument(exists=True, dir_okay=False)]):
                text = config.read_text()
                print(f"Config file contents: {text}")
            ```
            """
        ),
    ] = True,
    writable: Annotated[
        bool,
        Doc(
            """
            Whether or not to perform a writable check for this [`Path` argument](https://typer.tiangolo.com/tutorial/parameter-types/path/).

            **Example**

            ```python
            from pathlib import Path

            @app.command()
            def main(config: Annotated[Path, typer.Argument(writable=True)]):
                config.write_text("All the text")
            ```
            """
        ),
    ] = False,
    readable: Annotated[
        bool,
        Doc(
            """
            Whether or not to perform a readable check for this [`Path` argument](https://typer.tiangolo.com/tutorial/parameter-types/path/).

            **Example**

            ```python
            from pathlib import Path

            @app.command()
            def main(config: Annotated[Path, typer.Argument(readable=True)]):
                config.read_text("All the text")
            ```
            """
        ),
    ] = True,
    resolve_path: Annotated[
        bool,
        Doc(
            """
            Whether or not to fully resolve the path of this [`Path` argument](https://typer.tiangolo.com/tutorial/parameter-types/path/),
            meaning that the path becomes absolute and symlinks are resolved.

            **Example**

            ```python
            from pathlib import Path

            @app.command()
            def main(config: Annotated[Path, typer.Argument(resolve_path=True)]):
                config.read_text("All the text")
            ```
            """
        ),
    ] = False,
    allow_dash: Annotated[
        bool,
        Doc(
            """
            When set to `True`, a single dash for this [`Path` argument](https://typer.tiangolo.com/tutorial/parameter-types/path/)
            would be a valid value, indicating standard streams. This is a more advanced use-case.
            """
        ),
    ] = False,
    path_type: Annotated[
        None | type[str] | type[bytes],
        Doc(
            """
            A string type that will be used to represent this [`Path` argument](https://typer.tiangolo.com/tutorial/parameter-types/path/).
            The default is `None` which means the return value will be either bytes or unicode, depending on what makes most sense given the input data.
            This is a more advanced use-case.
            """
        ),
    ] = None,
    # Rich settings
    rich_help_panel: Annotated[
        str | None,
        Doc(
            """
            Set the panel name where you want this CLI Argument to be shown in the [help text](https://typer.tiangolo.com/tutorial/arguments/help).

            **Example**

            ```python
            @app.command()
            def main(
                name: Annotated[str, typer.Argument(help="Who to greet")],
                age: Annotated[str, typer.Option(help="Their age", rich_help_panel="Data")],
            ):
                print(f"Hello {name} of age {age}")
            ```
            """
        ),
    ] = None,
) -> Any:
    """
    A [CLI Argument](https://typer.tiangolo.com/tutorial/arguments) is a positional parameter to your command line application.

    Often, CLI Arguments are required, meaning that users have to specify them. However, you can set them to be optional by defining a default value:

    ## Example

    ```python
    @app.command()
    def main(name: Annotated[str, typer.Argument()] = "World"):
        print(f"Hello {name}!")
    ```

    Note how in this example, if `name` is not specified on the command line, the application will still execute normally and print "Hello World!".
    """
    return ArgumentInfo(
        # Parameter
        default=default,
        # Arguments can only have one param declaration
        # it will be generated from the param name
        param_decls=None,
        callback=callback,
        metavar=metavar,
        expose_value=expose_value,
        is_eager=is_eager,
        envvar=envvar,
        shell_complete=shell_complete,
        autocompletion=autocompletion,
        default_factory=default_factory,
        # Custom type
        parser=parser,
        click_type=click_type,
        # TyperArgument
        show_default=show_default,
        show_choices=show_choices,
        show_envvar=show_envvar,
        help=help,
        hidden=hidden,
        # Choice
        case_sensitive=case_sensitive,
        # Numbers
        min=min,
        max=max,
        clamp=clamp,
        # DateTime
        formats=formats,
        # File
        mode=mode,
        encoding=encoding,
        errors=errors,
        lazy=lazy,
        atomic=atomic,
        # Path
        exists=exists,
        file_okay=file_okay,
        dir_okay=dir_okay,
        writable=writable,
        readable=readable,
        resolve_path=resolve_path,
        allow_dash=allow_dash,
        path_type=path_type,
        # Rich settings
        rich_help_panel=rich_help_panel,
    )


def argument(
    a: Argument | TensorOptionsArguments | SelfArgument,
    *,
    cpp_no_default_args: set[str],
    method: bool,
    faithful: bool,
    symint: bool = False,
    has_tensor_options: bool,
) -> list[Binding]:
    def sub_argument(
        a: Argument | TensorOptionsArguments | SelfArgument,
    ) -> list[Binding]:
        return argument(
            a,
            cpp_no_default_args=cpp_no_default_args,
            method=method,
            faithful=faithful,
            symint=symint,
            has_tensor_options=has_tensor_options,
        )

    if isinstance(a, Argument):
        binds: ArgName
        if a.name == "memory_format" and has_tensor_options:
            binds = SpecialArgName.possibly_redundant_memory_format
        else:
            binds = a.name
        default: str | None = None
        if a.name not in cpp_no_default_args and a.default is not None:
            default = default_expr(a.default, a.type, symint=symint)
        return [
            Binding(
                nctype=argument_type(a, binds=binds, symint=symint),
                name=a.name,
                default=default,
                argument=a,
            )
        ]
    elif isinstance(a, TensorOptionsArguments):
        if faithful:
            return (
                sub_argument(a.dtype)
                + sub_argument(a.layout)
                + sub_argument(a.device)
                + sub_argument(a.pin_memory)
            )
        else:
            default = None
            # Enforced by NativeFunction.__post_init__
            if "options" in cpp_no_default_args:
                raise AssertionError("'options' should not be in cpp_no_default_args")
            if all(x.default == "None" for x in a.all()):
                default = "{}"
            elif a.dtype.default == "long":
                default = "at::kLong"  # TODO: this is wrong
            return [
                Binding(
                    nctype=NamedCType("options", BaseCType(tensorOptionsT)),
                    name="options",
                    default=default,
                    argument=a,
                )
            ]
    elif isinstance(a, SelfArgument):
        if method:
            # Caller is responsible for installing implicit this in context!
            return []
        else:
            return sub_argument(a.argument)
    else:
        assert_never(a)


def argument(
    a: Argument, *, remove_non_owning_ref_types: bool = False, symint: bool = True
) -> Binding:
    return Binding(
        nctype=argument_type(
            a,
            binds=a.name,
            remove_non_owning_ref_types=remove_non_owning_ref_types,
            symint=symint,
        ),
        name=a.name,
        argument=a,
    )


def argument(
    a: Argument | SelfArgument | TensorOptionsArguments,
    *,
    is_out: bool,
    symint: bool,
) -> list[Binding]:
    # Ideally, we NEVER default native functions.  However, there are a number
    # of functions that call native:: directly and rely on the defaulting
    # existing.  So for BC, we generate defaults for non-out variants (but not
    # for out variants, where it is impossible to generate an appropriate
    # default)
    should_default = not is_out
    if isinstance(a, Argument):
        default: str | None = None
        if should_default and a.default is not None:
            default = cpp.default_expr(a.default, a.type, symint=symint)
        return [
            Binding(
                nctype=argument_type(a, binds=a.name, symint=symint),
                name=a.name,
                default=default,
                argument=a,
            )
        ]
    elif isinstance(a, SelfArgument):
        # Erase SelfArgument from the distinction
        return argument(a.argument, is_out=is_out, symint=symint)
    elif isinstance(a, TensorOptionsArguments):
        default = None
        if should_default:
            default = "{}"
        # TODO: Not sure why the arguments assigned here are for
        # TensorOptionsArguments and not the constituent pieces.  It seems
        # to matter
        return [
            Binding(
                nctype=NamedCType("dtype", OptionalCType(BaseCType(scalarTypeT))),
                name="dtype",
                default=default,
                argument=a,
            ),
            Binding(
                nctype=NamedCType("layout", OptionalCType(BaseCType(layoutT))),
                name="layout",
                default=default,
                argument=a,
            ),
            Binding(
                nctype=NamedCType("device", OptionalCType(BaseCType(deviceT))),
                name="device",
                default=default,
                argument=a,
            ),
            Binding(
                nctype=NamedCType("pin_memory", OptionalCType(BaseCType(boolT))),
                name="pin_memory",
                default=default,
                argument=a,
            ),
        ]
    else:
        assert_never(a)


def argument(a: Argument) -> PythonArgument:
    return PythonArgument(
        name=a.name,
        type=a.type,
        # TODO: directly translate a.default to python default
        default=(
            str(pythonify_default(cpp.default_expr(a.default, a.type, symint=False)))
            if a.default is not None
            else None
        ),
        default_init=None,
    )


def argument(a: Argument | SelfArgument | TensorOptionsArguments) -> list[Binding]:
    if isinstance(a, Argument):
        return [
            Binding(
                nctype=argument_type(a, binds=a.name),
                name=a.name,
                default=None,
                argument=a,
            )
        ]
    elif isinstance(a, SelfArgument):
        return argument(a.argument)
    elif isinstance(a, TensorOptionsArguments):
        raise AssertionError("structured kernels don't support TensorOptions yet")
    else:
        assert_never(a)

