# CLI Example

This project is an example on how to develop CLI tools using Python.

## Prerequisites
- [Install uv](https://docs.astral.sh/uv/getting-started/installation/), e.g. for Windows: `winget install --id=astral-sh.uv  -e`

## Installation
```sh
uv tool install https://github.com/dapaulid/pydevkit.git
```

## Run
```sh
pydevkit
```

## Update
```sh
uv tool upgrade pydevkit
```

## Setup
```sh
# create initial project structure
uv init --app --package pydevkit
cd pydevkit
git add .
git commit -m "Origin."
# install launcher
uv tool install . -e
# install linter
uv add --dev ruff
git commit -am "Add ruff for linting."
# install testing
uv add --dev pytest
uv add --dev pytest-cov
# install task runner
uv add --dev taskipy
mkdir tests
# install type checker
uv add --dev mypy
```

## Workflow
```sh
# run linter, tests, coverage...
uv run task check
```

## Limitations
- The VSCode Test Explorer and Test Coverage (Testing view) will not update automatically when you hit Ctrl-B, you need to click "Run Tests with Coverage" instead.

## Further Reading
- https://mathspp.com/blog/using-uv-to-build-and-install-python-cli-apps
- https://pydevtools.com/handbook/tutorial/setting-up-testing-with-pytest-and-uv/
- https://nedbatchelder.com/blog/202008/you_should_include_your_tests_in_coverage.html
