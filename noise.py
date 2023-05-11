from itertools import cycle

import numpy as np

from PIL import Image

def remap(t, type_):
    # remap t using the function selected by type_

    def linear(t):

        return t

    def cosine(t):

        return (1-np.cos(t*np.pi))/2

    def cubic(t):

        return t**2 * (3 - 2*t)

    def quintic(t):

        return 6*t**5 - 15*t**4 + 10*t**3

    remap_functions = {'linear': linear,
                       'cosine': cosine,
                       'cubic': cubic,
                       'quintic': quintic}

    return remap_functions[type_](t)


def noise_line(length, vertices, octave=0, seed=None, remap_type='quintic'):

    #TODO move randomness out of this function
    try:
        random_values = vertices
        vertices = len(vertices)
    except:
        if seed is None:
            seed = np.random.randint(0, 4294967295)
            # print('generating seed')
        # print('seed_ = {}'.format(seed))
        np.random.seed(seed)
        random_values = np.random.rand(vertices)


    def make_noise(frequency):
        node = cycle(random_values)
        y0 = next(node)
        y1 = next(node)
        # how many points between vertices
        # the higher the frequency, the shorter the line (less points)
        points = int(length / vertices / frequency)

        # if there is less than one point per vertex return none
        if points < 1:
            return None
        x_values = np.linspace(0, 1, endpoint=False, num=points)
        line = []

        for vertex in range(vertices):
            for x in x_values:
                t = remap(x, remap_type)
                y = y0*(1-t) + y1*t
                line.append(y)
            y0 = y1
            y1 = next(node)
        return line

    frequency = 2**octave
    line = make_noise(frequency)
    # If the number of vertices is not a factor of length,
    # the length of the noise line will be smaller than length.
    # The following pads the noise line to the proper length
    try:
        while len(line) < length:
            line += line

        return np.array(line[0:length])
    except TypeError:
        print('Not enough points. Reduce vertices or octaves.')

def value_noise_1D(length, vertices, octaves=0, seed=None):

    lines = []
    for octave in range(octaves+1):
        x = noise_line(length, vertices, octave, seed)
        lines.append(x/(2**octave))

    return sum(lines)

def value_noise_2D(size, grid, octaves=0, seed=None):

    img_width, img_height = size
    grid_rows, grid_columns = grid

    if seed is None:
        seed = np.random.randint(0, 4294967295)
        print('seed: ', seed)

    np.random.seed(seed)

    # build random values with seed
    grid_columns =[]
    for row in range(grid_rows):
        grid_columns.append(np.random.rand(grid[1]))

    def make_plane(octave):
        lines = []
        for row in range(grid_rows):
            line = noise_line(length=img_width,
                              vertices=grid_columns[row],
                              octave=octave)
            lines.append(line)

        lines = np.array(lines)
        image = []
        for column in range(img_width):
            line = noise_line(length=img_height,
                              vertices=lines[:,column],
                              octave=octave)
            image.append(line)


        return np.array(image)

    planes = []
    for octave in range(octaves+1):
        planes.append(make_plane(octave)/(2**octave))

    return sum(planes)/len(planes)


# noise = value_noise_2D(size=(400,400), grid=(8,5),octaves=4, seed=1507300730)
# Image.fromarray(noise*255).convert('RGB').show()