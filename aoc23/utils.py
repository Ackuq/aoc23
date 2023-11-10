import os
from typing import List, Optional


def get_directory(file: str) -> str:
    return os.path.dirname(os.path.realpath(file))


def get_input(
    directory: str,
    example: Optional[int] = None,
    strip: bool = True,
) -> List[str]:
    filename = (
        f"{directory}/example{example}.txt"
        if example is not None
        else f"{directory}/problem.txt"
    )
    file = open(filename)
    lines = file.readlines()
    if strip:
        lines = [line.strip() for line in lines]
    return lines
