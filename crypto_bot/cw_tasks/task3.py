# https://www.codewars.com/kata/5949481f86420f59480000e7


def odd_or_even(arr):
    count = 0
    count += sum(arr)
    return "even" if count % 2 == 0 else "odd"
