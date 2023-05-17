import click
import glob
import hashlib
import itertools
import logging
import os
from typing import Any, Callable, Dict, Union


# Supported hashing methods
METHODS: dict[str, Callable[[Union[bytes, bytearray, memoryview]], Any]] = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256,
    "sha512": hashlib.sha512,
}


class InvalidMethod(Exception):
    """Exception when an invalid hashing algorithm is found.

    Attributes
    ----------
    method: str
        The name of the invalid method
    """

    def __init__(self, method):
        self.method = method

        message = f"Unsupported hashing algorithm specified: {method}"
        super().__init__(message)


@click.command()
@click.option(
    "--method",
    default="sha256",
    help="Algorithm to use for calculating checksum",
)
@click.option(
    "--output",
    default="checksum.txt",
    help="File to output checksums to",
)
@click.option(
    "-v",
    "--verbose",
    help="Enable verbose output",
    is_flag=True,
)
@click.argument("patterns")
def main(
    method: str,
    output: str,
    verbose: bool,
    patterns: str,
):
    if verbose:
        logging.getLogger().setLevel(logging.INFO)

    patterns = patterns.split("\n")
    logging.info(f"Processing patterns: {patterns}")
    try:
        result = dict(  # {filename: checksum, ..}
            list(  # [(filename, checksum), ..]
                itertools.chain.from_iterable(
                    map(
                        checksums, [method] * len(patterns), patterns
                    )  # [[(filename, checksum)], ..]
                )
            )
        )
    except Exception as e:
        logging.error(f"Error calculating checksum: {e}")
        exit(1)

    write_file(result, output)


def checksums(method: str, pattern: str) -> list[(str, str)]:
    """Calculates checksums of files matched by the glob pattern.

    Parameters
    ----------
    method: str
        The hashing algorithm to use (i.e sha256)
    pattern: str
        The glob pattern to use for determining files to hash

    Returns
    -------
    list[(str, str)]
        A list of pairs in the format of (filename, checksum)

    """
    logging.info(f"Processing pattern `{pattern}` with method `{method}`")
    result: list[(str, str)] = []
    for filename in glob.glob(pattern):
        result.append(checksum(method, filename))

    return result


def checksum(method: str, filename: str) -> (str, str):
    """Calculates the checksum of a file.

    Parameters
    ----------
    method: str
        The hashing algorithm to use (i.e sha256)
    filename: str
        The file name to calculate the checksum for

    Returns
    -------
    (str, str)
        A pair in the format of (filename, checksum)

    Raises
    ------
    InvalidMethod
        If an unsupported or invalid hashing algorithm is supplied

    """
    logging.info(f"Processing file `{filename}` with method `{method}`")
    with open(filename, "rb") as f:
        try:
            return (filename, METHODS[method](f.read()).hexdigest())
        except KeyError:
            raise InvalidMethod(method)


def write_file(checksums: Dict[str, str], out_file: str):
    """Writes filename and checksum pairs to a file.

    Parameters
    ----------
    checksums: Dict[filename str, checksum str]
        Filename-checksum pairs.
    out_file: str
        The file name to write the output to.

    """
    # Output in format of "(checksum) (filename)"
    output_contents: str = ""
    for filename, checksum in checksums.items():
        short_name = format_filename(filename)
        output_contents += f"{checksum} {short_name}\n"

    logging.info(f"Writing output to {out_file}")
    try:
        with open(out_file, "w") as f:
            f.write(output_contents)
    except Exception as e:
        logging.error(f"Error writing checksum file: {e}")
        exit(1)


def format_filename(filename: str) -> str:
    return os.path.basename(filename)


if __name__ == "__main__":
    main()
