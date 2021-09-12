#!/bin/bash

set -e
set -o pipefail

python /run/src/checksum.py --method "$1" --output "$2" $3