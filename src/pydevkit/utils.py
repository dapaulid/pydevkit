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
from timeit import default_timer as timer

import psutil


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
        status = "succeeded" if ret == 0 else "failed"
    except FileNotFoundError:
        print(f"[ {name} failed, command not found: {cmd[0]} ]")
        sys.exit(127)
    except KeyboardInterrupt:
        ret = 130  # Standard signal code for Ctrl-C
        status = "cancelled"
        print()  # newline after ^C
    elapsed = timer() - start_time
    cpu = psutil.cpu_percent()

    # print summary
    print(f"[ {name} {status}, took {elapsed:.3f}s at {cpu:.0f}% CPU ]")

    # TODO raise instead of exiting?
    if ret != 0:
        sys.exit(ret)


def remove_folder(path):
    if not os.path.exists(path):
        return
    def handle_exc(p, e):
        try:
            os.chmod(p, stat.S_IWRITE)
            if os.path.isdir(p):
                shutil.rmtree(p, ignore_errors=True)
            else:
                os.remove(p)
        except Exception:
            pass  # avoid recursion hell if something’s really locked
    shutil.rmtree(path, onexc=handle_exc)


# -------------------------------------------------------------------------------
# end of file
