import numpy as np


def readdata(filename):
    d = np.loadtxt(filename, delimiter=",")
    n_steps = d.shape[0]
    n_partiles = int(d.shape[1]/3)
    x = np.zeros((n_partiles, n_steps))
    y = np.zeros((n_partiles, n_steps))
    z = np.zeros((n_partiles, n_steps))
    for i in range(n_partiles):
        x[i] = (d.T)[3*i]
        y[i] = (d.T)[3*i+1]
        z[i] = (d.T)[3*i+2]
    return x.T, y.T, z.T
    # return x, y, z
