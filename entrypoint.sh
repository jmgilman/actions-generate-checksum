#!/bin/bash

set -e
set -o pipefail

poetry run python /run/src/checksum.py -v --method "$1" --output "$2" "$3"
