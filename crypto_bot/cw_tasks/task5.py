# https://www.codewars.com/kata/55fd2d567d94ac3bc9000064


def row_sum_odd_numbers(n):
    ans = 0
    a = 1
    k = 2
    for i in range(n - 1):
        a += k
        k += 2
    for j in range(n):
        ans += a
        a += 2
    return ans
