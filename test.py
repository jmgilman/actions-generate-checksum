import unittest
from unittest.mock import patch, mock_open

from src.checksum import checksum, checksums, InvalidMethod, format_filename


@patch(
    "builtins.open", new_callable=mock_open, read_data="data".encode("utf-8")
)
class TestChecksum(unittest.TestCase):
    def test_checksum(self, mock_file):
        """
        Test that is calculates the hash of the file data
        """
        import hashlib

        result = checksum("sha256", "test.txt")
        self.assertEqual(
            result,
            ("test.txt", hashlib.sha256("data".encode("utf-8")).hexdigest()),
        )

    def test_invalid_checksum(self, mock_file):
        """
        Test that an invalid hashing algorith is rejected
        """
        with self.assertRaises(InvalidMethod):
            checksum("sha652", "test.txt")


@patch(
    "builtins.open", new_callable=mock_open, read_data="data".encode("utf-8")
)
@patch("glob.glob", return_value=["archive/test1.txt", "test2.txt"])
class TestChecksums(unittest.TestCase):
    def test_checksums(self, mock_file, mock_glob):
        """
        Test that it iterates the glob pattern and returns a list of checksum
        pairs
        """
        import hashlib

        expected_checksum = hashlib.sha256("data".encode("utf-8")).hexdigest()
        result = checksums("sha256", "*")
        self.assertEqual(
            result,
            [
                ("archive/test1.txt", expected_checksum),
                ("test2.txt", expected_checksum),
            ],
        )


class TestFilenameFormatter(unittest.TestCase):
    def test_format_filename(self):
        input = "archive/test.txt"
        expected = "test.txt"
        self.assertEqual(format_filename(input), expected)


if __name__ == "__main__":
    unittest.main()
