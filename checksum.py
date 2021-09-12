from typing import Callable
import base64
import glob
import hashlib
import itertools
import os
import sys


def main(method: str, patterns: str, output_path: str):
    patterns = patterns.split("\n")
    checksums = dict(  # {filename: checksum, ..}
        list(  # [(filename, checksum), ..]
            itertools.chain.from_iterable(
                map(
                    calculate_checksum, [method] * len(patterns), patterns
                )  # [[(filename, checksum)], ..]
            )
        )
    )

    # Output in format of "(checksum) (filename)"
    output: str = ""
    for filename, checksum in checksums.items():
        output += f"{checksum} {filename}\n"

    with open(output_path, "w") as f:
        f.write(output)


def calculate_checksum(method: str, pattern: str) -> list[(str, str)]:
    # Supported hashing methods
    methods: dict[
        str, Callable[[Union[bytes, bytearray, memoryview]], hashlib._Hash]
    ] = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512,
    }

    checksums: list[(str, str)] = []
    for filename in glob.glob(pattern):
        with open(filename, "rb") as f:
            try:
                checksums.append(
                    (filename, methods[method](f.read()).hexdigest())
                )
            except Exception as e:
                print(f"Error: {e}")
                exit(101)

    return checksums


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
