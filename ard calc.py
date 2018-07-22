

def calc(t):
    total = 0
    for c in range(0, t):
        add = 100 * (c+1)
        sum = 1300 + add
        total += sum
        print(total)

calc(47)
