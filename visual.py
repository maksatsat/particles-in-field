from IPython.display import HTML
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from read_data import readdata
from matplotlib import animation
import numpy as np

filename = input('Введите название файла\n')
x, y, z = readdata(filename)
xlim = [np.min(x), np.max(x)]
ylim = [np.min(y), np.max(y)]
zlim = [np.min(z), np.max(z)]


FRAMES = x.shape[0]
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


def init():
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.axes.set_xlim3d(left=xlim[0], right=xlim[1])
    ax.axes.set_ylim3d(bottom=ylim[0], top=ylim[1])
    ax.axes.set_zlim3d(bottom=zlim[0], top=zlim[1])


def animate(i):
    j = i
    ax.cla()
    ax.scatter(x[j], y[j], z[j], marker='o', s=5.5)
    ax.axes.set_xlim3d(left=xlim[0], right=xlim[1])
    ax.axes.set_ylim3d(bottom=ylim[0], top=ylim[1])
    ax.axes.set_zlim3d(bottom=zlim[0], top=zlim[1])

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')


anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=FRAMES, interval=100)

plt.show()
