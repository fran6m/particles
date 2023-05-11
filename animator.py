import os

from datetime import datetime

import pygame
import numpy as np

from PIL import Image

# Some colors
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
ANTIQUEWHITE = (250,235,215)
GREY = (50,50,50)

class Animator(object):
    # TODO: clearly define the ways one can start recording frames

    def __init__(self, frames, name, fps=15, fade_out=False, fade_in=False,
                 from_start=False, build_on_quit=False):

        self.frames = frames
        self.frame = 0
        self.fps = fps
        self.skip_frames = 1

        self.count = 0

        self.done = False

        self.temp_files = []
        if self.frame == self.frames:
            self.done = True
            self.temp_files = []

        if not os.path.exists('frames'):
            os.makedirs('frames')

        self.name = name

        self.fade_out = fade_out
        self.fade_in = fade_in

        self.from_start = from_start
        self.build_on_quit = build_on_quit
        self.recording = False


    def record(self):
        ''' toggles recording on/off '''

        self.recording = not self.recording 
        if self.recording:
            print('start recording frames')
        else:
            print('stop recording frames')


    def setup(self, world_fps, bkg):
        ''' TODO '''
        self.skip_frames = world_fps // self.fps # ???
        self.bkg_color = bkg

    def rename_frames(self):
        ''' Pad file number with zeros to help with ffmpeg
            TODO give example
        '''

        # find how many digits in the filename of the last frame
        last_file = '1'
        for f in self.temp_files:
            file_number = f.split('_')[1].split('.')[0]
            if int(file_number) > int(last_file):
                last_file = file_number
        digits = len(last_file) + 1 # add one digit for the first zero

        # rename all the files with proper padding
        for old in self.temp_files:
            prefix = old.split('_')[0]
            number = old.split('_')[1].split('.')[0]
            suffix = '.' + old.split('_')[1].split('.')[1]
            if len(number) < digits:
                number = '0' * (digits - len(number)) + number
            new = prefix + number + suffix
            os.rename(old, new)

    def save_frame(self, surface):
        ''' TODO explain '''

        if self.count % self.skip_frames == 0:
            frame_name = 'frames/temp_' + str(self.frame + 1) + '.bmp'
            pygame.image.save(surface, frame_name)
            self.temp_files.append(frame_name)

            self.frame += 1
            if self.frame == self.frames:
                self.done = True

        self.count += 1


    def snapshot(self, surface):
        now = datetime.now()
        name = 'snapshot' + '_' \
        + now.strftime("%Y-%m-%d_%H:%M:%S") \
        + '.png'
        print('saving snapshot: ' + name)
        pygame.image.save(surface, name)


    def build(self):

        if self.temp_files == []:
            return

        # build the gif
        now = datetime.now()
        name = self.name.split('.')[0] + '_' \
               + now.strftime("%Y-%m-%d_%H:%M:%S") \
               + '.gif'

        print('creating ' + name)
        sequence = []
        for file in self.temp_files:
            sequence.append(Image.open(file)) # load png files as Pillow images

        if self.fade_in:
            fade_in_frames = []
            blank = Image.new('RGB',sequence[0].size, self.bkg_color)
            for i in range(0, self.fps):
                alpha = self.fps - i
                fade_in_frames.append(Image.blend(sequence[i], blank, alpha))
            sequence = fade_in_frames + sequence

        if self.fade_out:
            blank = Image.new('RGB',sequence[0].size, self.bkg_color)
            for i in range(1, self.fps):
                alpha = 1/i
                sequence[-i] = Image.blend(sequence[-i], blank, alpha)
            sequence.append(blank)
        sequence[0].save(name, save_all=True,
                         append_images=sequence[1:],
                         duration=1000/self.fps, loop=0)

        # clean up our temporary png files
        print('cleaning up')
        for file in self.temp_files:
            os.remove(file)

        self.temp_files = []

        print('done')



class World(object):

    def __init__(self,size, sprites, fade=0, fps=30, bkg=BLACK,
                 animator=None, g=None, field=None, drag=1, G=-0.03,
                 attraction=False, offscreen='kill'):

        pygame.init()

        self.clock = pygame.time.Clock()
        self.fps = fps

        self.size = size # size of world ex: (1920,1080)
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption('My World')
        self.screen.fill(bkg)
        self.bkg = bkg

        self.sprites = sprites
        self.G = G

        if g is not None:
            for s in self.sprites:
                s.g = g
        if field is None:
            self.field = np.zeros((size[0],size[1],2))
        else:
            self.field = field
        self.drag = drag
        self.attraction = attraction

        #TODO Doesn't work right with GREY (50,50,50)
        self.fade = fade
        self.apply_mask = 0
        if fade > 0:
            self.mask = pygame.Surface(size)
            self.mask.fill(bkg)
            if fade < 1:
                self.mask.set_alpha(1)
            else:
                self.mask.set_alpha(fade)

        self.animator = animator

        if offscreen == 'bounce':
            self.check_boundaries = self.bounce
        elif offscreen == 'kill':
            self.check_boundaries = self.kill
        elif offscreen == 'wrap':
            self.check_boundaries = self.wrap

        self.count = len(sprites)

        self.frame_count = 0

    def wrap(self, sprite):
        if  sprite.xy[0] < 0:
            sprite.xy[0] = self.size[0] -1

        elif sprite.xy[0] >= self.size[0]:
            sprite.xy[0] = 0

        if sprite.xy[1] < 0:
            sprite.xy[1] = self.size[1] -1

        elif sprite.xy[1] >= self.size[1]:
            sprite.xy[1] = 0


    def bounce(self, sprite):

        if  sprite.xy[0] < 0:
            sprite.velocity[0] *= -1
            sprite.xy[0] = 0

        elif sprite.xy[0] >= self.size[0]:
            sprite.velocity[0] *= -1
            sprite.xy[0] = self.size[0] -1

        if sprite.xy[1] < 0:
            sprite.velocity[1] *= -1
            sprite.xy[1] = 0

        elif sprite.xy[1] >= self.size[1]:
            sprite.velocity[1] *= -1
            sprite.xy[1] = self.size[1] -1


    def kill(self, sprite):
        a =  sprite.xy[0] < 0
        b = sprite.xy[0] >= self.size[0]
        c = sprite.xy[1] < 0
        d = sprite.xy[1] >= self.size[1]

        if a or b or c or d:
            sprite.dead = True


    def run(self):

        if self.animator is not None:
            self.animator.setup(self.fps, self.bkg)
            if self.animator.from_start:
                self.animator.record()

        while True:

            self.frame_count += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.animator is not None and self.animator.build_on_quit:
                        self.animator.build()
                    else:
                        self.animator.rename_frames()
                    os.sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if self.animator is not None:
                        if event.key == pygame.K_p:
                            self.animator.snapshot(self.screen)
                        if event.key == pygame.K_s:
                            self.animator.record()
                        if event.key == pygame.K_b:
                            self.animator.build()

            [self.check_boundaries(s) for s in self.sprites]
            [self.sprites.remove(s) for s in list(self.sprites) if s.dead]

            if self.attraction:
                field = np.copy(self.field)
                for i, s1 in enumerate(self.sprites[:-1]):
                    for s2 in self.sprites[i+1:]:
                        r = np.linalg.norm(s1.xy-s2.xy)
                        force = self.G*(s1.mass*s2.mass/ r**2) * (s1.xy-s2.xy)
                        try:
                            field[int(s1.xy[0]), int(s1.xy[1])] += force
                            field[int(s2.xy[0]), int(s2.xy[1])] += -force
                        except:
                            print(s1.xy, s2.xy, field.shape)
            else:
                field = self.field
            for s in self.sprites:
                x = int(s.xy[0])
                y = int(s.xy[1])
                s.draw(self.screen)

                force = field[x,y]
                s.update(force=force, drag=self.drag)


            pygame.display.update()

            if self.animator is not None:

                if not self.animator.done:
                    self.animator.save_frame(self.screen)
                    if self.animator.done:
                        print('saved {} frames'.format(self.animator.frame))
                elif self.animator.recording:
                    self.animator.save_frame(self.screen)


            if self.fade > 0:
                self.apply_mask += self.fade
                if self.apply_mask >= 1:
                    self.screen.blit(self.mask,(0,0))
                    self.apply_mask = 0

            self.clock.tick(self.fps)

