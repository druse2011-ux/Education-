str = "abcdefz"
shift = 4
list0 = []
list1 = []
for element in str:
    list0.append(ord(element) - ord("a"))
for i in range(len(list0)):
    list0[i] = chr(((list0[i] + shift) % 26 + ord("a")))

print("".join(list0))
