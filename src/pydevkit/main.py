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

    # 'init' command
    sp = subparsers.add_parser(
        "init",
        formatter_class=parser.formatter_class,
        help="generate project files",
    )
    sp.set_defaults(func=cmd_init)

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

    # parse and execute command line
    args = parser.parse_args()
    args.func(args)


# -------------------------------------------------------------------------------
# commands
# -------------------------------------------------------------------------------
#
def cmd_init(args):
    utils.copy_dir_contents("templates/project", ".")


def cmd_lint(args):
    utils.run_task(
        "lint", f"ruff -q --config {utils.config_path('ruff.toml')} check --fix"
    )


def cmd_typing(args):
    utils.run_task("typing", f"mypy --config-file {utils.config_path('mypy.ini')} .")


def cmd_format(args):
    utils.run_task(
        "format", f"ruff -q --config {utils.config_path('ruff.toml')} format"
    )


def cmd_test(args):
    utils.run_task(
        "test",
        f"pytest -c {utils.config_path('pytest.ini')} --rootdir . --cov --cov-config {utils.config_path('.coveragerc')}",
    )


def cmd_build(args):
    cmd_lint(args)
    cmd_typing(args)
    cmd_format(args)
    cmd_test(args)


def cmd_clean(args):
    utils.remove_folder("build")


# -------------------------------------------------------------------------------
# end of file
