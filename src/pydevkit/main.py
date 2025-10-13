# -------------------------------------------------------------------------------
# imports
# -------------------------------------------------------------------------------
#
import argparse

import rich_argparse

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

    # 'lint' command
    sp = subparsers.add_parser(
        "lint",
        formatter_class=parser.formatter_class,
        help="analyse code for potential errors",
    )
    sp.set_defaults(func=cmd_lint)

    # 'typecheck' command
    sp = subparsers.add_parser(
        "typecheck",
        formatter_class=parser.formatter_class,
        help="run static type checker",
    )
    sp.set_defaults(func=cmd_typecheck)    

    # 'format' command
    sp = subparsers.add_parser(
        "format", formatter_class=parser.formatter_class, help="format code to style guide"
    )
    sp.set_defaults(func=cmd_format)

    # 'clean' command
    sp = subparsers.add_parser(
        "clean", formatter_class=parser.formatter_class, help="delete build artifacts"
    )
    sp.set_defaults(func=cmd_clean)

    # parse and execute command line
    args = parser.parse_args()
    args.func(args)


# -------------------------------------------------------------------------------
# commands
# -------------------------------------------------------------------------------
#
def cmd_lint(args):
    utils.run_task("lint", "ruff --config config/ruff.toml check --fix")

def cmd_typecheck(args):
    utils.run_task("typecheck", "mypy --config-file config/mypy.ini .")

def cmd_format(args):
    utils.run_task("format", "ruff --config config/ruff.toml format")

def cmd_clean(args):
    utils.remove_folder("build")

# -------------------------------------------------------------------------------
# end of file
