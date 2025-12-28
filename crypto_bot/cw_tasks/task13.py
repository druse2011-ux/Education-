# https://www.codewars.com/kata/555086d53eac039a2a000083


def lovefunc(a, b):
    return True if a % 2 == 0 and b % 2 != 0 or b % 2 == 0 and a % 2 != 0 else False
