import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def score(eD, iV, eA, aP):

    demandOut = eD - iV
    demandIn = eA - aP

    if demandOut > demandIn:
        evaluation = 2 * demandOut
    else:
        evaluation = 2 * demandIn

    if evaluation >= 10:
        s = 10
    elif evaluation <= 0:
        s = 0
    else:
        s = evaluation

    return s

imageWidth = 640
imageHeight = 480

data = pd.read_csv('stations_state.csv')

I = [0, 1, 2, 4, 6, 7]

data2 = data.iloc[:, I]
locations = data2.iloc[:, [4, 5]].values
# print(locations)
data3 = data2.values
env = np.zeros((len(data3), imageWidth, imageHeight))

points = []


def degsToPixels(long, lat, max_width, max_height):

    rangelat = np.max(locations[:,0]) - np.min(locations[:,0])
    rangelong = np.max(locations[:,1]) - np.min(locations[:,1])

    width = max_width / rangelong
    length = max_height / rangelat

    x = width * (long - np.min(locations[:, 1]))
    y = length * (lat - np.min(locations[:, 0]))
    points.append([x,y])
    return np.array([x,y])

pix = np.zeros((imageWidth, imageHeight,2))
for j in range(imageWidth):
    for k in range(imageHeight):
        pix[j][k][1] = k
        pix[j][k][0] = j


for i, value in enumerate(data3):
    s = score(value[2], value[3], value[0], value[1])
    coordinates = degsToPixels(value[5], value[4], imageWidth, imageHeight)
    env[i,:,:] = -.005*((pix[:,:,0] - coordinates[0])**2 + (pix[:,:,1] - coordinates[1])**2)
    env[i, :, :] = s*np.exp(env[i,:,:])

points = np.array(points)
print(points)

grayscale = np.sum(env, axis=0)

plt.imshow(grayscale.T, cmap='jet')
plt.gca().invert_yaxis()
X = locations[:,1] - np.min(locations[:,1])
X = imageWidth*X/np.max(X)
Y = locations[:,0] - np.min(locations[:,0])
Y = imageHeight*Y/np.max(Y)

plt.scatter(X,Y, c = 'w')
plt.show()

