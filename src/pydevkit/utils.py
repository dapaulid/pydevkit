# -------------------------------------------------------------------------------
# imports
# -------------------------------------------------------------------------------
#
import os
import shlex
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from timeit import default_timer as timer

import psutil
from rich.console import Console

console = Console()


# -------------------------------------------------------------------------------
# functions
# -------------------------------------------------------------------------------
#
def run_task(name: str, cmdline: str):
    # command line to list
    cmd = shlex.split(cmdline)

    psutil.cpu_percent()
    start_time = timer()
    try:
        ret = subprocess.call(cmd, shell=False)
        status = "[bold green]OK[/]" if ret == 0 else "[bold red]failed[/]"
    except FileNotFoundError:
        print(f"[ {name} [bold red]failed[/], command not found: {cmd[0]} ]")
        sys.exit(127)
    except KeyboardInterrupt:
        ret = 130  # Standard signal code for Ctrl-C
        status = "[bold yellow]cancelled[/]"
        print()  # newline after ^C
    elapsed = timer() - start_time
    cpu = psutil.cpu_percent()

    # print summary
    console.print(
        f"[ {name:<7} ] {status}  [black]took {elapsed:.3f}s at {cpu:.0f}% CPU[/]",
        highlight=False,
    )

    # TODO raise instead of exiting?
    if ret != 0:
        sys.exit(ret)


def remove_folder(path):
    # https://docs.python.org/3/library/shutil.html#shutil-rmtree-example

    if not os.path.exists(path):
        return

    def remove_readonly(func, path, _):
        # Clear the readonly bit and reattempt the removal
        os.chmod(path, stat.S_IWRITE)
        func(path)

    shutil.rmtree(path, onexc=remove_readonly)


def config_path(filename: str) -> str:
    root_dir = Path(__file__).resolve().parent.parent.parent
    cfg_path = root_dir / "config" / filename
    if not cfg_path.exists():
        raise FileNotFoundError(f"Config file not found: {cfg_path}")
    return cfg_path.as_posix()


# -------------------------------------------------------------------------------
# end of file
