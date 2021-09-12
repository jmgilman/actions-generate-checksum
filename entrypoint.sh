#!/bin/bash

set -e
set -o pipefail

python3 /checksum.py "$1" "$2" "$3"