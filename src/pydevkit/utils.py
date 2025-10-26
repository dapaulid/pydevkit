# -------------------------------------------------------------------------------
# imports
# -------------------------------------------------------------------------------
#
import os
import shutil
import stat
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from timeit import default_timer as timer
from typing import Iterator

import psutil
from rich.console import Console

console = Console()


# -------------------------------------------------------------------------------
# context managers
# -------------------------------------------------------------------------------
#
# context manager to run a task with timing and error handling
@contextmanager
def run_task(name: str, output_header: bool = False) -> Iterator[None]:
    depth = run_task.depth  # type: ignore
    indent = "  " * depth
    if output_header:
        console.print(f"{indent}[ {name:<7} ] started")

    # task preparation
    if depth == 0:
        # only for outermost task, since the nesting cpu_percent does not work
        psutil.cpu_percent()
    run_task.depth += 1  # type: ignore
    start_time = timer()

    # task execution with error handling
    try:
        yield  # run the task contained in the 'with' block
        ret = 0
        status = "[bold green]OK[/]"
    except KeyboardInterrupt:
        ret = 130  # Standard signal code for Ctrl-C
        status = "[bold yellow]cancelled[/]"
        print()  # newline after ^C
    except SystemExit as e:
        ret = e.code if isinstance(e.code, int) else 1
        status = "[bold yellow]cancelled[/]" if ret == 130 else "[bold red]failed[/]"
    except subprocess.CalledProcessError:
        ret = 1
        status = "[bold red]failed[/]"
    except Exception as e:
        ret = 1
        status = "[bold red]failed[/]: %s" % e

    # task finalization
    elapsed = timer() - start_time
    run_task.depth -= 1  # type: ignore
    if depth == 0:
        cpu = psutil.cpu_percent()

    # print summary
    details = f"took {elapsed:.3f}s"
    if depth == 0:
        details += f" at {cpu:.0f}% CPU"
    console.print(f"{indent}[ {name:<7} ] {status}  [black]{details}[/]")

    # TODO raise instead of exiting?
    if ret != 0:
        sys.exit(ret)


# 'static' variable to track depth of nested tasks
run_task.depth = 0  # type: ignore


# -------------------------------------------------------------------------------
# functions
# -------------------------------------------------------------------------------
#
def die(msg: str):
    console.print(f"[bold red]error:[/] {msg}")
    sys.exit(1)


def exec(cmd, silent: bool = False):
    stdout = subprocess.DEVNULL if silent else None
    try:
        subprocess.check_call(cmd, shell=False, stdout=stdout)
    except FileNotFoundError as e:
        raise RuntimeError("command not found: '%s'" % cmd[0] if cmd else "") from e


def eval(cmd) -> str:
    try:
        return subprocess.check_output(cmd, shell=False, encoding="utf-8").strip()
    except FileNotFoundError as e:
        raise RuntimeError("command not found: '%s'" % cmd[0] if cmd else "") from e


def remove_folder(path: str):
    # https://docs.python.org/3/library/shutil.html#shutil-rmtree-example

    if not os.path.exists(path):
        return

    def remove_readonly(func, path, _):
        # Clear the readonly bit and reattempt the removal
        os.chmod(path, stat.S_IWRITE)
        func(path)

    shutil.rmtree(path, onexc=remove_readonly)


def copy_dir_contents(source_dir: str, target_dir: str):
    for root, dirs, files in os.walk(source_dir):
        # Compute the relative path from the source
        relative_path = os.path.relpath(root, source_dir)
        # Create the corresponding path in the target directory
        target_path = os.path.join(target_dir, relative_path)
        os.makedirs(target_path, exist_ok=True)

        for file in files:
            source_file = os.path.normpath(os.path.join(root, file))
            target_file = os.path.normpath(os.path.join(target_path, file))
            print(f"writing {target_file}")
            shutil.copy2(source_file, target_file)


def config_path(filename: str) -> str:
    root_dir = Path(__file__).resolve().parent.parent.parent
    cfg_path = root_dir / "config" / filename
    if not cfg_path.exists():
        raise FileNotFoundError(f"Config file not found: {cfg_path}")
    return cfg_path.as_posix()


def tool_wrapper():
    if is_local_venv():
        return []  # no wrapper needed
    else:
        return ["uv", "run"]  # venv wrapper


def is_local_venv() -> bool:
    return sys.prefix.endswith(".venv")  # TODO verify


# -------------------------------------------------------------------------------
# end of file
