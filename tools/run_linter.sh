#!/bin/bash

# run linter to python scripts.
# This script requires:
#   pip install hacking flake8 flake8-import-order flake8-pep257

set -e

cwd=$(dirname "${0}")
expr "${0}" : "/.*" > /dev/null || cwd=$(cd "${cwd}" && pwd)

project_directory="${cwd}"/..

(cd "${project_directory}" && flake8 .)
