import sortedcontainers

L = sortedcontainers.SortedList()
L.add(2)
L.add(6)
L.add(1)
L.add(0)
for value in L:
    print(value)