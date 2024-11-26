from enum import StrEnum
from pathlib import Path


class FileType(StrEnum):
  JPG = "jpg"
  PNG = "png"
  PDF = "pdf"
  OTHER = "other"

  @classmethod
  def from_filename(cls, filename: Path):
    match filename.suffix.lower():
      case ".jpg" | ".jpeg":
        return cls.JPG
      case ".png":
        return cls.PNG
      case ".pdf":
        return cls.PDF
      case _:
        return cls.OTHER
