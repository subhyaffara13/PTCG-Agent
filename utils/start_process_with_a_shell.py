
def start_process_with_a_shell(context, config):
    """**B605: Test for starting a process with a shell**

    Python possesses many mechanisms to invoke an external executable. However,
    doing so may present a security issue if appropriate care is not taken to
    sanitize any user provided or variable input.

    This plugin test is part of a family of tests built to check for process
    spawning and warn appropriately. Specifically, this test looks for the
    spawning of a subprocess using a command shell. This type of subprocess
    invocation is dangerous as it is vulnerable to various shell injection
    attacks. Great care should be taken to sanitize all input in order to
    mitigate this risk. Calls of this type are identified by the use of certain
    commands which are known to use shells. Bandit will report a LOW
    severity warning.

    See also:

    - :doc:`../plugins/linux_commands_wildcard_injection`
    - :doc:`../plugins/subprocess_without_shell_equals_true`
    - :doc:`../plugins/start_process_with_no_shell`
    - :doc:`../plugins/start_process_with_partial_path`
    - :doc:`../plugins/subprocess_popen_with_shell_equals_true`

    **Config Options:**

    This plugin test shares a configuration with others in the same family,
    namely `shell_injection`. This configuration is divided up into three
    sections, `subprocess`, `shell` and `no_shell`. They each list Python calls
    that spawn subprocesses, invoke commands within a shell, or invoke commands
    without a shell (by replacing the calling process) respectively.

    This plugin specifically scans for methods listed in `shell` section.

    .. code-block:: yaml

        shell_injection:
            shell:
                - os.system
                - os.popen
                - os.popen2
                - os.popen3
                - os.popen4
                - popen2.popen2
                - popen2.popen3
                - popen2.popen4
                - popen2.Popen3
                - popen2.Popen4
                - commands.getoutput
                - commands.getstatusoutput
                - subprocess.getoutput
                - subprocess.getstatusoutput

    :Example:

    .. code-block:: none

        >> Issue: Starting a process with a shell: check for injection.
           Severity: Low   Confidence: Medium
           CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
           Location: examples/os_system.py:3
        2
        3   os.system('/bin/echo hi')

    .. seealso::

     - https://security.openstack.org
     - https://docs.python.org/3/library/os.html#os.system
     - https://docs.python.org/3/library/subprocess.html#frequently-used-arguments
     - https://security.openstack.org/guidelines/dg_use-subprocess-securely.html
     - https://cwe.mitre.org/data/definitions/78.html

    .. versionadded:: 0.10.0

    .. versionchanged:: 1.7.3
        CWE information added

    """  # noqa: E501
    if config and context.call_function_name_qual in config["shell"]:
        if len(context.call_args) > 0:
            sev = _evaluate_shell_call(context)
            if sev == bandit.LOW:
                return bandit.Issue(
                    severity=bandit.LOW,
                    confidence=bandit.HIGH,
                    cwe=issue.Cwe.OS_COMMAND_INJECTION,
                    text="Starting a process with a shell: "
                    "Seems safe, but may be changed in the future, "
                    "consider rewriting without shell",
                )
            else:
                return bandit.Issue(
                    severity=bandit.HIGH,
                    confidence=bandit.HIGH,
                    cwe=issue.Cwe.OS_COMMAND_INJECTION,
                    text="Starting a process with a shell, possible injection"
                    " detected, security issue.",
                )

