import random
totalCount = 0
iterations = 10000
for j in range(iterations):
    lst = [i for i in range(100)]
    random.shuffle(lst)

    max = lst[0]
    for element in lst:
        if element > max:
            max = element
            totalCount += 1

print(totalCount/iterations)
