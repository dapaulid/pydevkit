# -------------------------------------------------------------------------------
# imports
# -------------------------------------------------------------------------------
#
import argparse

import rich_argparse

import pydevkit as pkg

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

    # example command
    greet_parser = subparsers.add_parser(
        "lint", formatter_class=parser.formatter_class, help="analyse code for potential errors"
    )
    greet_parser.set_defaults(func=cmd_lint)

    # parse and execute command line
    args = parser.parse_args()
    args.func(args)


# -------------------------------------------------------------------------------
# commands
# -------------------------------------------------------------------------------
#
def cmd_lint(args):
    print("hello from linter")


# -------------------------------------------------------------------------------
# end of file
