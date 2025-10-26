# -------------------------------------------------------------------------------
# imports
# -------------------------------------------------------------------------------
#
import argparse
import os

import rich_argparse
from rich import print

import pydevkit as pkg

from . import utils

# -------------------------------------------------------------------------------
# constants
# -------------------------------------------------------------------------------
#
USAGE_EXAMPLES = """
  {0} --version
  {0} greet Alice
  {0} greet Bob --excited
"""

# path to monkeytype sqlite3 database file
# NOTE: it's not easy to put this into the 'build' output directory,
# since monkeytype has no param for passing a path, and changing
# working directory messes with running module paths
AUTOTYPE_CACHE = "monkeytype.sqlite3"


# -------------------------------------------------------------------------------
# main
# -------------------------------------------------------------------------------
#
def main():
    # setup command line parser
    parser = argparse.ArgumentParser(
        # format program description
        description=f"%(prog)s v{pkg.__version__} - {pkg.__summary__}\n"
        f"  [argparse.prog]{pkg.__homepage__}[/]",
        # format usage examples
        epilog="[argparse.groups]Examples:[/]"
        + USAGE_EXAMPLES.format("[argparse.prog]%(prog)s[/]"),
        # use colored help formatter
        formatter_class=rich_argparse.RawDescriptionRichHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")
    parser.set_defaults(func=lambda args: parser.print_help())

    # general options
    parser.add_argument("--version", action="version", version=pkg.__version__)

    # 'init' command
    sp = subparsers.add_parser(
        "init",
        formatter_class=parser.formatter_class,
        help="generate project files",
    )
    sp.set_defaults(func=cmd_init)

    # 'run' command
    sp = subparsers.add_parser(
        "run",
        formatter_class=parser.formatter_class,
        help="run main script",
    )
    sp.set_defaults(func=cmd_run)
    sp.add_argument("params", nargs=argparse.REMAINDER)

    # 'lint' command
    sp = subparsers.add_parser(
        "lint",
        formatter_class=parser.formatter_class,
        help="analyse code for potential errors",
    )
    sp.set_defaults(func=cmd_lint)

    # 'typing' command
    sp = subparsers.add_parser(
        "typing",
        formatter_class=parser.formatter_class,
        help="run static type checker",
    )
    sp.set_defaults(func=cmd_typing)

    # 'format' command
    sp = subparsers.add_parser(
        "format",
        formatter_class=parser.formatter_class,
        help="format code to style guide",
    )
    sp.set_defaults(func=cmd_format)

    # 'test' command
    sp = subparsers.add_parser(
        "test",
        formatter_class=parser.formatter_class,
        help="run tests including coverage",
    )
    sp.set_defaults(func=cmd_test)

    # 'build' command
    sp = subparsers.add_parser(
        "build",
        formatter_class=parser.formatter_class,
        help="runs lint, typecheck, format",
    )
    sp.set_defaults(func=cmd_build)

    # 'clean' command
    sp = subparsers.add_parser(
        "clean", formatter_class=parser.formatter_class, help="delete build artifacts"
    )
    sp.set_defaults(func=cmd_clean)

    # 'autotype' command
    sp = subparsers.add_parser(
        "autotype", formatter_class=parser.formatter_class, help="add type annotations"
    )
    sp.add_argument(
        "subcommand", nargs="?", choices=["apply", "enable", "disable"], default="apply"
    )

    sp.set_defaults(func=cmd_autotype)

    # parse and execute command line
    args = parser.parse_args()
    args.func(args)


# -------------------------------------------------------------------------------
# commands
# -------------------------------------------------------------------------------
#
def cmd_init(args):
    utils.copy_dir_contents("templates/project", ".")


def cmd_run(args):
    with utils.run_task("run"):
        cmd = utils.tool_wrapper()
        if (
            is_autotype_enabled()
            and "autotype" not in args.params  # avoid self-referential problem
        ):
            print("[ autotype ] collecting type data...")
            cmd += ["monkeytype", "run", "-m", "pydevkit.main"]
        else:
            cmd += ["pyd"]
        cmd += args.params
        utils.exec(cmd)


def cmd_lint(args):
    with utils.run_task("lint"):
        cmd = utils.tool_wrapper()
        cmd += ["ruff"]
        cmd += ["-q", "--config", utils.config_path("ruff.toml")]
        cmd += ["check", "--fix"]
        utils.exec(cmd)


def cmd_typing(args):
    with utils.run_task("typing"):
        cmd = utils.tool_wrapper()
        cmd += ["mypy"]
        cmd += ["--config-file", utils.config_path("mypy.ini")]
        cmd += ["."]
        utils.exec(cmd)


def cmd_format(args):
    with utils.run_task("format"):
        cmd = utils.tool_wrapper()
        cmd += ["ruff"]
        cmd += ["-q", "--config", utils.config_path("ruff.toml")]
        cmd += ["format"]
        utils.exec(cmd)


def cmd_test(args):
    with utils.run_task("test"):
        cmd = utils.tool_wrapper()
        cmd += ["pytest"]
        cmd += ["-c", utils.config_path("pytest.ini")]
        cmd += ["--rootdir", "."]
        cmd += ["--cov", "--cov-config", utils.config_path(".coveragerc")]
        utils.exec(cmd)


def cmd_build(args):
    with utils.run_task("build", output_header=True):
        cmd_lint(args)
        cmd_typing(args)
        cmd_format(args)
        cmd_test(args)


def cmd_clean(args):
    with utils.run_task("clean"):
        utils.remove_folder("build")


def cmd_autotype(args):
    with utils.run_task("autotype"):
        # check if type collection is enabled
        enabled = is_autotype_enabled()

        cmd = utils.tool_wrapper()
        cmd += ["monkeytype"]

        if args.subcommand == "apply":
            # get modules with type data
            modules = utils.eval(cmd + ["list-modules"]).splitlines()
            if not modules:
                utils.die("no modules with type data found")
            # apply types to each module
            for module in modules:
                print(f"applying types: '{module}'")
                utils.exec(cmd + ["apply", module], silent=True)
            if not enabled:
                # remove cache to avoid inadvertent data collection
                os.remove(AUTOTYPE_CACHE)
                assert not is_autotype_enabled()

        elif args.subcommand == "enable":
            if not enabled:
                # dummy operation to create the sqlite3 db file
                utils.exec(cmd + ["list-modules"], silent=True)
                print("type collection enabled")
            assert is_autotype_enabled()

        elif args.subcommand == "disable":
            if enabled:
                os.remove(AUTOTYPE_CACHE)
                print("type collection disabled")
            assert not is_autotype_enabled()

        else:
            utils.die(f"unknown autotype subcommand: '{args.subcommand}'")


def is_autotype_enabled() -> bool:
    return os.path.exists(AUTOTYPE_CACHE)


# entry point
if __name__ == "__main__":
    main()

# -------------------------------------------------------------------------------
# end of file
