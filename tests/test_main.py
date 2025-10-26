# -------------------------------------------------------------------------------
# imports
# -------------------------------------------------------------------------------
#
import shlex
from unittest.mock import patch

import pydevkit as pkg
from pydevkit.main import main


# -------------------------------------------------------------------------------
# helpers
# -------------------------------------------------------------------------------
#
def exec(capsys, command: str):
    argv = shlex.split(command)
    with patch("sys.argv", argv):
        try:
            main()
        except SystemExit as e:
            assert e.code == 0
    out, _ = capsys.readouterr()
    return out.strip()


# -------------------------------------------------------------------------------
# test functions
# -------------------------------------------------------------------------------
#
def test_help(capsys):
    out = exec(capsys, "pyd --help")
    assert "Examples:" in out, "help text must contain usage examples"


def test_version(capsys):
    out = exec(capsys, "pyd --version")
    assert out == pkg.__version__, "version output must match package version"


# -------------------------------------------------------------------------------
# end of file
