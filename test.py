from time import sleep

for x in range(75):
    print('*' * (75 - x), x, end='\x1b[1K\r')
print()