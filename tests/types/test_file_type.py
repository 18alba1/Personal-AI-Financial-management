from pathlib import Path

from money_mate.types.file_type import FileType


def test_from_filename():
  first_path = Path("/foo/bar/baz.pdf")
  assert FileType.from_filename(first_path) == FileType.PDF

  second_path = Path("/foo/bar/baz.txt")
  assert FileType.from_filename(second_path) == FileType.OTHER
