#!/usr/bin/env python
print 'hello, world'
name = raw_input('please enter your name: ')
print 'hello,', name

a = 100
if a >= 0:
    print a
else:
    print -a

print 'I\'m ok.'
print r'\\\t\\'

x = abs(100)
y = abs(-20)
print(x, y)
print('max(1, 2, 3) =', max(1, 2, 3))
print('min(1, 2, 3) =', min(1, 2, 3))
print('sum([1, 2, 3]) =', sum([1, 2, 3]))

def my_abs(x):
    if x >= 0:
        return x
    else:
        return -x