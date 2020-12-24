import random
import numpy as np
import os
import time
import concurrent.futures


class Particle():

    def __init__(self,  indx, E, H, tau, n_steps, charge=-1):
        self.charge = charge
        if self.charge == -1:
            self.m = 1.0
        else:
            self.m = 1836.0
        self.r = np.array(
            [random.random(), random.random(), random.random()])
        # self.r_prev = np.copy(self.r)
        self.v = np.array(
            [random.random(), random.random(), random.random()])
        self.v_prev = np.copy(self.v)
        self.v
        self.E = E
        self.H = H
        self.tau = tau
        self.indx = indx
        self.n_steps = n_steps

    def update_euler(self):  # , E=self.E, H=self.H, tau=self.tau):
        v = self.v
        # B = H(*self.r)
        self.v += 2*self.tau*np.cross(self.H(*self.r), v)
        self.r += self.v * 2 * self.tau
        self.v += (self.charge/self.m)*self.E(*self.r)*self.tau
        self.r += self.v*self.tau

    def update(self):
        H = self.H(*self.r)
        E = self.E(*self.r)
        omega = np.linalg.norm(H)*self.charge/self.m
        self.r += self.v * self.tau
        self.v = self.v*(1-0.5*omega**2*self.tau**2)+(self.charge*self.tau/self.m)*(
            E+np.cross(self.v, H))+(self.charge**2*self.tau*self.tau/(2*self.m**2))*(np.dot(self.v, H))*H


def E(x, y, z):
    return np.array([-10.0, 0.0, 0.0])


def H(x, y, z):
    return np.array([10.0, 0.0, 0.0])


def direct(n_particles, n_steps, filename, tau):
    particles = []
    pos = np.zeros((n_steps, 3*n_particles))
    for i in range(n_particles):
        p = Particle(i, E, H, tau, n_steps)
        particles.append(p)
        pos[0][3*i:3*i+3] = p.r

    for j in range(1, n_steps):
        for i in range(n_particles):
            p = particles[i]
            p.update()
            pos[j][3*i:3*i+3] = p.r

    with open(filename, 'w+') as f:
        np.savetxt(f, pos, delimiter=',')


def step(args):
    def _step(particles, n_steps, indx):
        p = particles[indx]
        pos = np.zeros((n_steps, 3))
        for j in range(n_steps):
            pos[j] = p.r
            p.update()
        return [indx, pos]
    return _step(*args)


def threads(n_particles, n_steps, filename, tau):
    particles = []
    # pos = np.zeros((n_steps, 3*n_particles))
    for i in range(n_particles):
        p = Particle(i, E, H, tau, n_steps)
        particles.append(p)

    args = [(particles, n_steps, i) for i in range(n_particles)]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(step, args)
    x = list(results)
    pos = np.zeros((3*n_particles, n_steps))
    for i in range(n_particles):
        j = x[i][0]
        pos[3*j:3*j+3] = (x[i][1]).T
    pos = pos.T
    with open(filename, 'w+') as f:
        np.savetxt(f, pos, delimiter=',')


def multiproc(n_particles, n_steps, filename, tau):
    particles = []
    # pos = np.zeros((n_steps, 3*n_particles))
    for i in range(n_particles):
        p = Particle(i, E, H, tau, n_steps)
        particles.append(p)

    args = [(particles, n_steps, i) for i in range(n_particles)]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(step, args)
    x = list(results)
    pos = np.zeros((3*n_particles, n_steps))
    for i in range(n_particles):
        j = x[i][0]
        pos[3*j:3*j+3] = (x[i][1]).T
    pos = pos.T
    with open(filename, 'w+') as f:
        np.savetxt(f, pos, delimiter=',')


if __name__ == '__main__':
    while True:
        print('1 - прямое вычиcление, 2- параллельное, 3 - многопоточное')
        meth = input()
        if meth == '1':
            method = direct
            break
        elif meth == '2':
            method = multiproc
            break
        elif meth == '3':
            method = threads
            break
    print('Введите название сохраняемого файла')
    filename = input()
    start = time.time()
    print('Введите число частиц')
    s = input()
    n_particles = int(s)
    print('Введите число шагов')
    s = input()
    n_steps = int(s)
    tau = 0.01

    method(n_particles, n_steps, filename, tau)
    print(f"Computation time {time.time()-start}")
