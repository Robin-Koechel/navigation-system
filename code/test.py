import re
import numpy as np
import numpy
from matplotlib import image
from matplotlib import pyplot as plt
test = open('einlesen.txt', 'r')
line = test.read()
patternX  = re.compile(r'lon="(\d\.\d{7})"')
matchesX = patternX.finditer(line)




x = numpy.empty((1000), dtype=float, order='C')
y = numpy.empty((1000), dtype=float, order='C')

i = 0

for match in matchesX:
    print(match.group(1))
    x[i] = match.group(1)
    i += 1
i = 0
patternY  = re.compile(r'lat="(\d\d\.\d{7})"')
matchesY = patternY.finditer(line)
for match in matchesY:
    print(match.group(1))
    y[i] = match.group(1)
    i += 1

length = 600
width = 600




data = image.imread('weiß.png')
y2 =y[0]/50 * width
print (y2)
for b in range(i):
    x2 = x[b]-9.40
    y2 = y[b]- 48.76

    x2 = x2*100/1 * length


    y2 = y2*100/1 * width
    print(y2,x2)
    plt.plot(x2+100, y2, marker='v', color="black")


#x = [200, 500]
#y = [300, 100]
#plt.plot(x, y, color="black", linewidth=3)
plt.imshow(data)
plt.show()
