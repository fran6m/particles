import systems
from animator import Animator

HD = (1890, 1070)

########
# TypeError: 'float' object cannot be interpreted as an integer
#########

# name = 'orbits.gif'
# a = Animator(frames=0, name=name, fade_out=False, fade_in=False,
#               from_start=False, build_on_quit=False, fps=30)
# sim = systems.orbits(size=HD, pop=5)
# # sprite size of 3 is nice
# sim.animator=a
# sim.run()

# name = 'fishes.gif'
# a = Animator(frames=0, name=name, fade_out=False, fade_in=False,
#               from_start=False, build_on_quit=False, fps=30)
# sim = systems.fishes(size=HD, pop=500)
# # sprite size of 3 is nice
# sim.animator=a
# sim.run()


# name = 'fishes2.gif'
# a = Animator(frames=0, name=name, fade_out=False, fade_in=False,
#               from_start=False, build_on_quit=False, fps=30)
# sim = systems.fishes2(size=HD, pop=500)
# # sprite size of 3 is nice
# sim.animator=a
# sim.run()


# name = 'forcefield.gif'
# a = Animator(frames=0, name=name, fade_out=False, fade_in=False,
#               from_start=False, build_on_quit=False, fps=30)
# sim = systems.force_field(size=HD, pop=1500)
# # sprite size of 3 is nice
# sim.animator=a
# sim.run()


name = 'forcefield.gif'
a = Animator(frames=0, name=name, fade_out=False, fade_in=False,
              from_start=False, build_on_quit=False, fps=30)
sim = systems.repulsion(size=HD, pop= 20)
# sprite size of 3 is nice
sim.animator=a
sim.run()

# name = 'noise_field.gif'
# a = Animator(frames=0, name=name, fade_out=False, fade_in=False,
#               from_start=False, build_on_quit=False, fps=30)
# sim = systems.noise_field(size=(1000,1000), ratio=0.35)
# sim.animator=a
# sim.run()

# name = 'value_noise_field.gif'
# a = Animator(frames=0, name=name, fade_out=False, fade_in=False,
#               from_start=False, build_on_quit=False, fps=30)
# sim = systems.value_noise_field(size=HD, ratio=0.2)
# sim.animator=a
# sim.run()

# name = 'colony.gif'
# a = Animator(frames=0, name=name, fade_out=False, fade_in=False,
#               from_start=False, build_on_quit=False, fps=30)
# sim = systems.colony(HD)
# # sprite size of 3 is nice
# sim.animator=a
# sim.run()