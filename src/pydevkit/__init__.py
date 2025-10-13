# -------------------------------------------------------------------------------
# imports
# -------------------------------------------------------------------------------
#
from importlib import metadata as meta

# -------------------------------------------------------------------------------
# variables
# -------------------------------------------------------------------------------
#
# load package metadata from pyproject.toml
pkginfo: meta.PackageMetadata | dict
try:
    pkginfo = meta.metadata(__package__)
except meta.PackageNotFoundError:
    pkginfo = {}

# set module metadata
# https://peps.python.org/pep-0008/#module-level-dunder-names
__version__ = pkginfo.get("Version", "(version missing)")
__summary__ = pkginfo.get("Summary", "(summary missing)")
__homepage__ = pkginfo.get("Project-URL", "").split(" ")[-1]

# -------------------------------------------------------------------------------
# end of file
