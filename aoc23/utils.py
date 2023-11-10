from typing import List, Optional


def read_input(
    day: int,
    example: bool = False,
    example_num: Optional[int] = None,
    strip: bool = False,
) -> List[str]:
    name = f"{day}" if not example else f"{day}_example"
    if example_num is not None:
        name += f"_{example_num}"
    f = open(f"./inputs/{name}.txt")
    lines = f.readlines()
    if strip:
        lines = [line.strip() for line in lines]
    return lines
