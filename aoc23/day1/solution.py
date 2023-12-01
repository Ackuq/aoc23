from typing import List


def main(input: List[str]) -> None:
    print(part1(input))
    print(part2(input))


def part1(input: List[str]) -> int:
    result = 0
    for row in input:
        numbers = [char for char in row if char.isdigit()]
        if len(numbers) == 0:
            continue
        number = numbers[0] + numbers[-1]
        result += int(number)
    return result


string_digits = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def part2(input: List[str]) -> int:
    result = 0

    for row in input:
        number = ""
        left = 0
        right = len(row) - 1
        while left < len(row):
            found = False
            for key in string_digits:
                if row[left:].startswith(key):
                    number += string_digits[key]
                    found = True
                    break
            if found:
                break
            if row[left].isdigit():
                number += row[left]
                break
            left += 1

        while right >= 0:
            found = False
            for key in string_digits:
                if row[right:].startswith(key):
                    number += string_digits[key]
                    found = True
                    break
            if found:
                break
            if row[right].isdigit():
                number += row[right]
                break
            right -= 1
        result += int(number)
    return result
