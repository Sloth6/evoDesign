import os
from os import path
import sys
import argparse
import pickle
from pprint import pprint

from neat.parallel import ParallelEvaluator
from neat import population, visualize
from neat.config import Config
from .cellGenome import CellGenome

from .simulation import Simulation
from .physics.softPhysics import SoftPhysics

class Experiment(object):
    def __init__(self, cores, generations, population, out_dir='./out/derp'):
        # Run options
        self.cores = cores
        self.out_dir = out_dir
        self.generations = generations
        self.population = population

        # Simulation
        self.simulation_config = {
            'max_steps': 100,
            'bounds' : 100
        }

        # Genome
        self.genome_config = {
            'num_morphogens': 0,
            'morphogen_thresholds': 4,
            'inputs': [
            ],

            'outputs': [
            ]

        }

        # Physics
        self.physics = SoftPhysics
        self.physics.render = True
        self.physics_config = {
            'max_steps': 200,
        }

        if path.exists(out_dir):
            print('"%s" already exists'% out_dir)
            # erase = raw_input('Delete existing out folder? (y/n) :')
            if True:#erase.lower() in ['y', 'yes']:
              os.system("rm -rf " + out_dir)
            else:
              sys.exit(0)
        os.makedirs(out_dir)

    def evaluate_genome(self, genome):
        physics = self.physics(**self.physics_config)
        sim = Simulation(genome, physics, **self.simulation_config)
        self.set_up(sim)
        sim.run()
        return self.fitness(sim)

    def evaluate_genomes(self, genomes):
        for g in genomes:
          g.fitness = self.evaluate_genome(g)

    def pre_draw(self, screen):
        pass

    def post_draw(self, screen):
        pass

    def report(self, pop):
        winner = pop.statistics.best_genome()

        #Save the winner.
        with open(path.join(self.out_dir,'population.p'), 'wb') as f:
            pickle.dump(pop, f)

        genome_text = open(path.join(self.out_dir,'genome.txt'), 'w+')
        genome_text.write('fitness: %f\n' % winner.fitness)
        genome_text.write(str(winner))

        # Plot the evolution of the best/average fitness.
        visualize.plot_stats(pop.statistics, ylog=True,
                            filename=path.join(self.out_dir,"nn_fitness.svg"))

        # Visualizes speciation
        visualize.plot_species(pop.statistics,
                            filename=path.join(self.out_dir,"nn_speciation.svg"))

        # Visualize the best network.
        node_names = dict()
        for i, name in enumerate(winner.inputs + winner.outputs):
            node_names[i] = name

        visualize.draw_net(winner, view=True, node_names=node_names,
                        filename=path.join(self.out_dir,"nn_winner.gv"))

        if self.physicsVisual:
            physics = self.physicsVisual(**self.physics_config)
            sim = Simulation(winner, physics, **self.simulation_config)
            self.set_up(sim)
            sim.run()

        print('Report finished.')

    def set_up(self, sim):
        raise NotImplementedError

    def run(self):
        print('Running:')
        print(pprint(vars(self)))

        # Change the Genome used.
        local_dir = path.dirname(__file__)
        config = Config(path.join(local_dir, '../config.txt'))
        config.genotype = CellGenome
        config.genome_config = self.genome_config
        config.pop_size = self.population

        # Create a population.
        pop = population.Population(config)

        # Run single or multi core.
        if self.cores > 1:
            pe = ParallelEvaluator(self.cores, self.evaluate_genome)
            pop.run(pe.evaluate, self.generations)
        else:
            pop.run(self.evaluate_genomes, self.generations)
        print('Experiment finished.')
        self.report(pop)