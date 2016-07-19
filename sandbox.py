import os, math, random
from neat.config import Config
from src.cellGenome import CellGenome

# from src.simulation2 import Simulation
from src.hexSimulation import HexSimulation
from src.hexVisualize import HexRenderer as Renderer

local_dir = os.path.dirname(__file__)
config  = Config(os.path.join(local_dir, 'config.txt'))
config.genome_config = {
    'inputs': ['derp'],
    'outputs':['foo'],
    'num_morphogens': 1,
    'morphogen_thresholds': 4
}
dummy_genome = CellGenome.create_unconnected(1, config)

class Sandbox(HexSimulation):
    """Extend the simualtion to inject arbitrary cell behavior."""
    # def __init__(self, *args, **kwargs):
    #     super(Sandbox, self).__init__(*args, **kwargs)
        # self.renderer._viewZoom = .2
    def create_inputs(self, cell):
        return [0]

    def handle_outputs(self, cell, outputs):
        pass

    def set_up(self):
        # for coords in self.hmap.neighbor_coords((4,4)):
        #     print(coords)
        #     self.create_cell(coords)

        # self.create_cell((4,4))
        # self.create_cell((1,4))
        # self.create_cell((1,5))
        # self.create_cell((1,5))
        # for i in range(7):
        #     self.create_cell((i,0))
        #     self.create_cell((i,1))

        # for i in range(2,7):
        #     self.create_cell((7,i))

        # for i in range(8):
        #     for j in range(8):
        #         self.create_cell((i,j))

    # def Step(self, *args):
    #     super(Sandbox, self).Step(*args)

        # if self.stepCount%2 == 0:
        # pygame.image.save(self.screen, './out_temp/' + str(self.stepCount)+'.jpg')
        # print('saved')

renderer = Renderer()
simulation = Sandbox(dummy_genome, max_steps=200, verbose=False, bounds=(8,8))
simulation.verbose = True
simulation.set_up()
simulation.run(renderer)
renderer.hold()
