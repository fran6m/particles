from itertools import cycle

import numpy as np
import pygame

from noise import value_noise_1D


class Particle(object):

    def __init__(self, xy=(0.,0.), v=(0.,0.), a=(0.,0.), mass=0,
                 size=2, color=(0,0,255)):

        self.xy = np.array(xy, dtype='float64')
        self.velocity = np.array(v)
        self.acceleration = np.array(a)
        self.mass = mass
        self.size = size
        self.color = color

        self.g = 0

        self.dead = False

        # used to track this sprite
        self.trace = False

        # used to track how many times the sprite was drawn
        self.steps = 0


    def update(self, force=0, drag=1):

        self.xy += self.velocity
        self.velocity += self.acceleration
        self.velocity += self.g
        self.velocity *= drag
        if self.mass != 0:
            self.acceleration = force / self.mass


    def draw(self, surface):

        xy = self.xy.astype(int)
        if self.size >= 2:
            pygame.draw.circle(surface, self.color, xy, self.size)
        else:
            surface.set_at(xy, self.color)


class RandomWalker(Particle):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def update(self, **kwargs):

        self.xy += np.random.randint(-3, 4, 2)



class Forward(Particle):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


    def update(self, **kwargs):

        self.xy += self.velocity



class PulsingFish(Particle):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def update(self, **kwargs):

        self.xy += self.velocity
        self.velocity += self.acceleration

        self.steps += 1
        if self.steps == 60:
            self.acceleration *= -1
            self.steps = -60


class PulsingFish2(Particle):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.change = np.random.randint(30,90)
        self.steps = np.random.randint(0, self.change)

        if np.linalg.norm(self.velocity) > 1:
            self.velocity *= 1.5

        if np.absolute(self.velocity[0]) < 0.5:
            self.velocity[0] *= 1.5
        if np.absolute(self.velocity[1]) < 0.5:
            self.velocity[1] *= 1.5

    def update(self, **kwargs):

        self.xy += self.velocity
        self.velocity += self.acceleration

        if np.linalg.norm(self.velocity) > 1.5:
            if np.absolute(self.velocity[0]) > np.absolute(self.velocity[1]):
                self.velocity *= [0.8, 1.2]

            else:
                self.velocity *= [1.2, 0.8]

        self.steps += 1
        if self.steps == self.change:
            self.acceleration *= -1
            self.steps = -self.change



class Ant(object):

    def __init__(self, xy=(0.,0.), color=(0,0,255)):

        # draw the ant on a surface
        # create a copy of that surface to work with (rotations)
        self.width = 4
        self.height = 10
        self.color = color
        rect = (0, 0, self.width, self.height)
        self.original_image = pygame.Surface((self.width, self.height))
        self.original_image.set_colorkey((0,0,0))
        self.original_center = self.original_image.get_rect().center
        pygame.draw.rect(self.original_image, self.color, rect)
        self.working_copy = self.original_image

        # set the position of the ant
        self.xy = np.array(xy, dtype='float64')

        # set the behavior of the ant
        _ = value_noise_1D(length=500, vertices=50)
        _ -= _.mean()
        _ *= 2
        self.vx = cycle(_) # a list of pseudorandom x axis velocities

        _ = value_noise_1D(length=400, vertices=50)
        _ -= _.mean()
        _ *= 2
        self.vy = cycle(_) # a list of pseudorandom y axis velocities

        self.velocity = np.array((next(self.vx), next(self.vy)))

        # track how many times the sprite was drawn
        self.step = 0
        # a list of scheduled changes in velocity
        self.changes = cycle(np.random.randint(2,10,200))
        # how many steps before velocity changes
        self.change = next(self.changes)

        self.dead = False # is the ant alive?

    def update(self, force=0, drag=1):

        self.xy += self.velocity # move the ant

        # orient the ant in the direction of movement
        self.angle = np.arctan2(self.velocity[0], self.velocity[1])*180/np.pi
        self.working_copy = pygame.transform.rotate(self.original_image,
                                                    self.angle)


        self.step +=1
        if self.step == self.change:
            self.step = 0
            self.change = next(self.changes)
            self.velocity = np.array((next(self.vx), next(self.vy)))

    def draw(self, surface):

        # When an image is rotated the size of its surface will change
        # If you draw using the top left corner as reference the rotated image
        # will wobble around. You need to set the center of the rotated image
        # on the same spot as the center of the original image
        rect = self.working_copy.get_rect()
        rect.center = self.original_center
        rect.left += self.xy[0]
        rect.top += self.xy[1]

        surface.blit(self.working_copy, rect)
