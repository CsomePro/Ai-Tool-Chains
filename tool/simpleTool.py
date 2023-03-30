from toolchains.tool.base import *
import re
import sys
from io import StringIO


@ToolsManager.register
class PythonRepl(ToolFactory):
    class _Tool(ToolModel):
        def func(self, code: str):
            code = code.strip().strip('`')
            """Run command with own globals/locals and returns anything printed."""
            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()
            try:
                exec(code)
                sys.stdout = old_stdout
                output = mystdout.getvalue()
            except Exception as e:
                sys.stdout = old_stdout
                output = str(e)
            return {"output": output}

    tool = _Tool(
        uuid=get_tool_uuid_by_name(locals()['__qualname__']),
        in_vars=['code'],
        out_vars=['output'], tag={},
        name='Python_REPL', dec="A Python shell. Use this to execute python commands. "
        "Input should be a valid python command. "
        "If you want to see the output of a value, you should print it out "
        "with `print(...)`." )


@ToolsManager.register
class RegexRepl(ToolFactory):
    class _Tool(ToolModel):
        def func(self, string: str):
            assert 'exp' in self._args
            exp = re.compile(self._args.get('exp'))
            match = exp.search(string)
            return match.groupdict()

    tool = _Tool(
        uuid=get_tool_uuid_by_name(locals()['__qualname__']),
        in_vars=['string'],
        out_vars=["num1", "num2"], tag={}, param={'exp': r'(?P<num1>[0-9]+),(?P<num2>[0-9]+)'},
        name="Regex", dec='using to test')
