import numpy as np

import sprites as sp

from animator import World
from colour import Color

import noise as nz

def _color_palette_rgb(starting_color='red', ending_color='blue', palette_size=1):

    # Create a pallette of colors
    palette = []
    s = Color(starting_color)
    e = Color(ending_color)
    values = list(s.range_to(e,palette_size))

    for v in values:
        color = []
        for i in v.get_rgb():
            color.append(i*255)
        palette.append(color)

    return palette

def orbits(size=(400,400), pop=5, fade=3):
    ''' size = size of world
        pop = sprite population
        fade = sprite trail fade rate
        
        This system creates sprites, each having a position, velocity
        and mass. 
        
        The world's attraction is set to True, with a value of G =-0.03
    '''

    colors = _color_palette_rgb(palette_size=pop+2)

    # a list of random coordinates roughly centered in the view
    xy = (np.random.rand(pop,2)*50) + [size[0]/2-75, size[1]/2-75]
    # a list of random velocities
    v = np.random.rand(pop,2)*5

    m = [50]*pop # a list of masses
    sprites =[]
    for i in range(pop):
        sprite = sp.Particle(xy=xy[i],v=v[i], mass=m[i], size=3, color=colors[i+1])
        sprites.append(sprite)

    w = World(size, sprites, fade=fade, fps=60, drag=.99,
              attraction=True, offscreen='bounce')
    return w

def random_walk(size=(400,400), pop=55, fade=3):

    # TODO: animator.py:230:
    #       RuntimeWarning: invalid value encountered in double_scalars
    #       force = self.G*(s1.mass*s2.mass/ r**2) * (s1.xy-s2.xy)
    size = np.array(size)
    colors = [np.random.randint(0,256,3) for _ in range (pop)]
    sprites = [sp.RandomWalker(xy=size/2,color=colors[i]) for i in range(pop)]
    w = World(size, sprites, fade=fade, offscreen='bounce')
    return w


def forward(size=(400,400), pop=25, fade=10):

    size = np.array(size)
    xy = np.tile(size/2, (pop,1))

    c = _color_palette_rgb(palette_size=pop)
    v = np.random.uniform(-1, 1, (pop, 2))/1.2
    for s in v:
        if s[1] < 0: s[1] *= -1
    sprites = [sp.Forward(xy=xy[i], v=v[i], color=c[i]) for i in range(pop)]

    w = World(size, sprites, fade=fade, fps=60, offscreen='bounce')
    return w


def fishes(size=(400,400), pop=30, fade=24):

    size = np.array(size)
    xy = np.tile(size/2, (pop,1))
    xy = (np.random.rand(pop,2)*50) + [size[0]/2, size[1]/2]
    colors = _color_palette_rgb(palette_size=pop)
    v = np.random.uniform(-1.5, 1.2, (pop, 2))/3
    a = np.random.uniform(-0.03, 0.03, (pop,2))

    sprites = []
    for i in range(pop):
        sprite = sp.PulsingFish(xy=xy[i],v=v[i], a=a[i], color=colors[i])
        sprites.append(sprite)


    w = World(size, sprites, fade=fade, fps=60, offscreen='bounce')

    return w


def fishes2(size=(400,400), pop=30, fade=24):

    size = np.array(size)
    xy = (np.random.rand(pop,2)*200) + [size[0]/2-100, size[1]/2-100]
    colors = _color_palette_rgb(palette_size=pop)
    v = np.random.uniform(-1.5, 1.2, (pop, 2))/10
    a = np.random.uniform(-0.03, 0.03, (pop,2))

    sprites = []
    for i in range(pop):
        sprite = sp.PulsingFish2(xy=xy[i],v=v[i], a=a[i],color=colors[i])
        sprites.append(sprite)


    w = World(size, sprites, fade=fade, fps=60, offscreen='bounce')

    return w

def falling(size=(400,400), pop=100, fade=24, g=[0,0.009]):

    size = np.array(size)

    xy = np.tile([size[0]/2, size[1]/2-25], (pop,1))

    colors = _color_palette_rgb(palette_size=pop)

    v = np.random.uniform(-1, 1, (pop, 2))
    for s in v:
        if np.sqrt(s[0]**2 + s[1]**2) < 1:
            s *= 1.1
    for s in v:
        if np.sqrt(s[0]**2 + s[1]**2) < 1:
            s *= 1.1
    # for s in v:
    #     if np.sqrt(s[0]**2 + s[1]**2) < 1:
    #         s *= 3
    # # for s in v:
    #     if np.sqrt(s[0]**2 + s[1]**2) < 1:
    #         s *= 3

    sprites = [sp.Particle(xy=xy[i],v=v[i], color=colors[i]) for i in range(pop)]

    w = World(size, sprites, fade=fade, fps=60, g=g, offscreen='kill')

    return w



def force_field(size=(400,400), pop=100, fade=24):

    colors = _color_palette_rgb(palette_size=pop)

    xy = (np.random.rand(pop,2)*300) + [size[0]/2-800, size[1]/2-200]

    v = [[-0.5,2.]]*pop

    m = np.random.rand(pop)*5 + 5

    sprites = []
    for i in range(pop):
        sprite = sp.Particle(xy=xy[i],v=v[i], mass=m[i], color=colors[i])
        sprites.append(sprite)

    # note: to draw field:
    # g = np.sqrt(field[:,:,0]**2 + field[:,:,1]**2)
    # h = g/g.max()*255
    # PIL.Image.fromarray(h.astype('uint8')).show()

    vx = 0
    vy = 0
    field = np.zeros((size[0],size[1],2))
    for x in range(size[0]):
        vx = size[0]/2 - x
        for y in range(size[1]):
            vy = size[1]/2 - y
            field[x,y] = np.array([vx/5000,vy/5000])
    w = World(size, sprites, fade=fade, fps=60, field=field, drag=.9996,
              attraction=False, offscreen='bounce')

    return w



def repulsion(size=(400,400), pop=12, fade=12):

    colors = _color_palette_rgb(palette_size=pop)

    xy = (np.random.rand(pop,2)*50) + [size[0]/2-75, size[1]/2-75]
    v = np.random.rand(pop,2)*2

    m = [50]*pop
    m = (np.random.rand(pop)*5 )+ 10
    sprites =[]
    for i in range(pop):
        sprite = sp.Particle(xy=xy[i],v=v[i], mass=m[i], color=colors[i])
        sprites.append(sprite)

    xy = (np.random.rand(pop,2)*50) + [size[0]/2+75, size[1]/2+75]
    v = np.random.rand(pop,2)*2

    m = [-50]*pop
    m = (np.random.rand(pop)*(-5)) - 10
    for i in range(pop):
        sprite = sp.Particle(xy=xy[i],v=v[i], mass=m[i], color=colors[i])
        sprites.append(sprite)

    vx = 0
    vy = 0
    field = np.zeros((size[0],size[1],2))
    for x in range(size[0]):
        vx = size[0]/2 - x
        for y in range(size[1]):
            vy = size[1]/2 - y
            field[x,y] = np.array([vx/12000,vy/12000])

    w = World(size, sprites, fade=fade, fps=60, drag=.98,
              field=field, attraction=True, offscreen='wrap')
    return w

def burst(size=(400,400), pop=300, fade=12):

    size = np.array(size)
    xy = np.tile(size/2, (pop,1))

    colors = _color_palette_rgb(palette_size=pop)
    v = np.random.uniform(-1, 1, (pop, 2)) * 1.5
    for s in v:
        if np.sqrt(s[0]**2 + s[1]**2) < 1:
            s *= 1.5
    for s in v:
        if np.sqrt(s[0]**2 + s[1]**2) < 1:
            s *= 2
    for s in v:
        if np.sqrt(s[0]**2 + s[1]**2) < 1:
            s *= 3
    for s in v:
        if np.sqrt(s[0]**2 + s[1]**2) < 1:
            s *= 3

    m = [50]*pop
    sprites = []
    for i in range(pop):
        sprite = sp.Particle(xy=xy[i],v=v[i], mass=m[i], color=colors[i])
        sprites.append(sprite)

    w = World(size, sprites, fade=fade, fps=60, offscreen='kill')

    return w

def colony(size=(400,400), pop=500):

    size = np.array(size)
    xy = np.random.randint(175,225, (pop,2))
    colors = (255,0,0)

    sprites = []
    for i in range(pop):
        sprite = sp.Ant(xy=xy[i], color=colors)
        sprites.append(sprite)

    w = World(size, sprites, fade=100, fps=60, offscreen='bounce')

    return w


def noise_field(size=(400,400), pop=100, ratio=0):

    #size = np.array(size)
    pixels = size[0] * size[1]
    width = size[0]
    height = size[1]
    center = np.array(size).mean()/2
    if ratio > 0:
        pop = int(pixels * (ratio / 100))

    # colors = _color_palette_rgb(palette_size=pop)
    colors = [(12,45,200)]*pop

    print(pixels, "pixels -- ", pop, 'sprites')
    x = np.random.randint(0, width, pop)
    y = np.random.randint(0, height, pop)
    xy = np.column_stack((x,y))

    # Vertices = 2, octaves = 0
    seed = 3421
    seed=56
    seed = 188780121 # Tres lent
    seed = 2363552696 # Pressque carre
    seed = 2221433200 # Champ d'etoiles
    # Vertices,octaves: 5,6;7,0
    seed = 3606892633
    seed = 2645929104
    seed = 1256733691
    seed = None
    seed = np.random.randint(0, 4294967295)
    print(seed)
    seed = 1048040730
    x = nz.value_noise_1D(length=width, vertices=5  , octaves=6, seed=seed)
    y = nz.value_noise_1D(length=height, vertices=7, octaves=0, seed=seed)
    x -= x.mean()
    y -= y.mean()
    # y *= 2

    x = np.tile(x, height).reshape(width,height, 1)
    y = np.repeat(y, width).reshape(width, height, 1)
    field = np.concatenate((x,y), axis=2)
    # import pylab as plt
    # plt.style.use('dark_background')
    # plt.axes().set_aspect('equal')
    X = np.linspace(0,size[0]-1,size[1])
    Y = np.linspace(0,size[1]-1,size[0])
    # plt.streamplot(X, Y, field[:,:,1], -field[:,:,0], color='r')
    # plt.show()

    vx = np.random.rand(pop) * np.random.choice((-1,1), pop)
    vy = np.random.rand(pop) * np.random.choice((-1,1), pop)
    v = np.column_stack((vx,vy))

    m = ([2]*(pop//2) + [-2]*(pop//2)) 
    # m = [4]*pop 
    sprites = []
    for i in range(pop):
        try:
            sprite = sp.Particle(xy=xy[i],v=v[i], mass=m[i], size=1, color=colors[i])
            sprites.append(sprite)
        except:
            print("Error, index out of range, population = ", i)

    # sprites[0].trace = True
    fade = 1
    w = World(size, sprites, fade=fade, fps=60, field=field, drag=0.95,offscreen='wrap')
    return w


def value_noise_field(size=(400,400), pop=100, ratio=0):

    #size = np.array(size)
    pixels = size[0] * size[1]
    width = size[0]
    height = size[1]
    center = np.array(size).mean()/2
    if ratio > 0:
        pop = int(pixels * (ratio / 100))

    # colors = [(12,45,200)]*pop
    colors = _color_palette_rgb(palette_size=pop)

    print(pixels, "pixels -- ", pop, 'sprites')
    x = np.random.randint(0, width, pop)
    y = np.random.randint(0, height, pop)
    xy = np.column_stack((x,y))

    seed_x = None
    seed_y = None
    # seed_x = 3306022396
    # seed_y = 819314637

    # octave = 0, grid (8,8)
    # seed_x = 3504105030
    # seed_y = 1623095843
    # seed_x = 1949969566
    # seed_y = seed_x
    #
    # Tres joli
    # 2073600 pixels --  4147 sprites
    # seed:  3075241342
    # seed:  1108814207

    x = nz.value_noise_2D(size=size, octaves=0, grid=(16,16), seed=seed_x)
    x -= x.mean()
    x = x.reshape(size[0],size[1],1)
    y = nz.value_noise_2D(size=size, octaves=0, grid=(8,8), seed=seed_y)
    y -= y.mean()
    y = y.reshape(size[0],size[1],1)

    field = np.concatenate((x,y), axis=2)

    # import pylab as plt
    # plt.style.use('dark_background')
    # plt.axes().set_aspect('equal')
    # X = np.linspace(0,399,400)
    # Y = np.linspace(0,399,400)
    # plt.streamplot(X, Y, field[:,:,1], field[:,:,0], color='r')
    # plt.show()

    vx = np.random.rand(pop) * np.random.choice((-1,1), pop)
    vy = np.random.rand(pop) * np.random.choice((-1,1), pop)
    v = np.column_stack((vx,vy))

    m = [4] * (pop//2) + [4]*(pop//2)

    m = np.random.rand(pop) * 100
    # m[m.size//2:] *= -1
    # m = [4]*pop
    sprites = []
    for i in range(pop):
        sprite = sp.Particle(xy=xy[i],v=v[i], mass=m[i], size=1, color=colors[i])
        sprites.append(sprite)

    # sprites[0].trace = True
    fade = 1
    w = World(size, sprites, fade=fade, fps=60, field=field, drag=0.95,offscreen='wrap')
    return w

# 160000 pixels --  3200 sprites
# seed:  1949969566
# seed:  1844350572

# seed:  652400134
# seed:  2127904008