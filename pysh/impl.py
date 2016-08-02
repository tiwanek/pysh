import os
import subprocess

THROW_AT_ERROR = "throw_at_error"
IGNORE_OUTPUT = "ignore_output"


class PyShException(Exception):
    def __init__(self, result):
        super(PyShException, self).__init__()
        self.result = result


class PyShResult:
    def __init__(self, command, exit_code, out):
        self.command = command
        self.exit_code = exit_code
        self.out = out

    def __bool__(self):
        return self.exit_code == 0

    def __nonzero__(self):
        return self.__bool__()


class PyShBinding:
    def __init__(self, name, config, subcommands=None):
        self.name = name.replace('__', '-')
        self.config = config
        self.subcommands = subcommands or []

    def __getattr__(self, name):
        return PyShBinding(self.name, self.config, subcommands=self.subcommands + [name.replace('__', '-')])

    def __call__(self, *args, **kwargs):
        command = self._create_command(*args, **kwargs)
        stdout_mode = subprocess.PIPE
        fnull = None
        if self.config[IGNORE_OUTPUT]:
            if hasattr(subprocess, "DEVNULL"):
                stdout_mode = subprocess.DEVNULL
            else:
                fnull = open(os.devnull, 'w')
                stdout_mode = fnull
        sub = subprocess.Popen(command, stdout=stdout_mode, stderr=subprocess.STDOUT)
        code = sub.wait()
        r = PyShResult(command, code, sub.stdout.read() if sub.stdout else None)
        if sub.stdout:
            sub.stdout.close()
        if fnull:
            fnull.close()
        if self.config[THROW_AT_ERROR]:
            if r.exit_code:
                raise PyShException(r)
        return r

    def _create_command(self, *args, **kwargs):
        cmd = [self.name]
        cmd += self.subcommands
        for k, v in kwargs.items():
            key = k.replace('__', '-')
            if len(key) == 1:
                key = '-' + key
            else:
                key = '--' + key
            if type(v) == bool:
                if v:
                    cmd.append(key)
            elif type(v) == str:
                cmd.append(key)
                cmd.append(v)
            elif hasattr(v, "__iter__"):
                for value in v:
                    cmd.append(key)
                    cmd.append(value)
            else:
                pass
        for arg in args:
            cmd.append(arg)
        return cmd


class PySh:
    def __init__(self):
        self.config = {}
        self.config[THROW_AT_ERROR] = False
        self.config[IGNORE_OUTPUT] = False

    def __getattr__(self, name):
        return PyShBinding(name, self.config)

    def __getitem__(self, key):
        return self.config[key]

    def __setitem__(self, key, value):
        self.config[key] = value


pysh = PySh()


if __name__ == "__main__":
    import unittest

    class PyShSuite(unittest.TestCase):
        def test_simple_run_check_output(self):
            r = pysh.echo("test")
            self.assertEqual(r.out.decode(), "test\n")

        def test_simple_run_check_success(self):
            r = pysh.true()
            self.assertEqual(r.exit_code, 0)

        def test_simple_run_check_fail(self):
            r = pysh.false()
            self.assertNotEqual(r.exit_code, 0)

        def test_short_option_run(self):
            r = pysh.echo("test", n=True)
            self.assertEqual(r.out.decode(), "test")

        def test_command_empty(self):
            r = pysh.true()
            self.assertEqual(r.command, ["true"])

        def test_command_positional(self):
            r = pysh.true("pos1", "pos2")
            self.assertEqual(r.command, ["true", "pos1", "pos2"])

        def test_command_short_option_binary_absent(self):
            r = pysh.true(a=False)
            self.assertEqual(r.command, ["true"])

        def test_command_short_option_binary_present(self):
            r = pysh.true(a=True)
            self.assertEqual(r.command, ["true", "-a"])

        def test_command_short_option_string(self):
            r = pysh.true(a="a_value")
            self.assertEqual(r.command, ["true", "-a", "a_value"])

        def test_command_short_option_list_one(self):
            r = pysh.true(a=["a_value"])
            self.assertEqual(r.command, ["true", "-a", "a_value"])

        def test_command_short_option_list_many(self):
            r = pysh.true(a=["a_value", "a_value2", "a_value3"])
            self.assertEqual(r.command, ["true", "-a", "a_value", "-a", "a_value2", "-a", "a_value3"])

        def test_command_long_option_binary_absent(self):
            r = pysh.true(long=False)
            self.assertEqual(r.command, ["true"])

        def test_command_long_option_binary_present(self):
            r = pysh.true(long=True)
            self.assertEqual(r.command, ["true", "--long"])

        def test_command_long_option_string(self):
            r = pysh.true(long="a_value")
            self.assertEqual(r.command, ["true", "--long", "a_value"])

        def test_command_long_option_list_one(self):
            r = pysh.true(long=["a_value"])
            self.assertEqual(r.command, ["true", "--long", "a_value"])

        def test_command_long_option_list_many(self):
            r = pysh.true(long=["a_value", "a_value2", "a_value3"])
            self.assertEqual(r.command, ["true", "--long", "a_value", "--long", "a_value2", "--long", "a_value3"])

        def test_command_mixed_options(self):
            r = pysh.true(long=["a_value", "a_value2", "a_value3"], s=True, app="app")
            self.assertIn("-s", r.command)
            self.assertIn("--app", r.command)
            self.assertIn("app", r.command)
            self.assertEqual(r.command.count("--long"), 3)

        def test_command_long_option_list_many(self):
            r = pysh.true.subcommand("param1", "param2", option=True, o=True)
            self.assertEqual(r.command[0], "true")
            self.assertEqual(r.command[1], "subcommand")
            self.assertIn("-o", r.command)
            self.assertIn("--option", r.command)
            self.assertEqual(r.command[4], "param1")
            self.assertEqual(r.command[5], "param2")

        def test_config_throw_exception(self):
            mysh = PySh()
            mysh[THROW_AT_ERROR] = True
            with self.assertRaises(PyShException):
                mysh.false()
            mysh.true()

        def test_config_ignore_output(self):
            mysh = PySh()
            mysh[IGNORE_OUTPUT] = True
            r = mysh.echo("test")
            self.assertEqual(r.out, None)

        def test_escape_hyphen_in_subcommand(self):
            r = pysh.true.sub__command(long=True)
            self.assertEqual(r.command, ["true", "sub-command", "--long"])

        def test_escape_hyphen_in_argument(self):
            r = pysh.true(long__option=True)
            self.assertEqual(r.command, ["true", "--long-option"])

    unittest.main()