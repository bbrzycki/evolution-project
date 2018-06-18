import parameter_file_storage.DatasetLoad as dl
import parameter_file_storage.ParameterLoad as pl
import fields
import sys
import os
import glob
import world
import species
import organism

class Universe(object):
    """
    Create the universe of the simulation.
    """

    def __init__(self,
                 world_fn=None,
                 organism_fns=None,
                 world_param_fn=None,
                 species_param_fs=None,
                 current_time=0,
                 end_time=10):
        self.world_param_fn = world_param_fn
        self.species_param_fns = species_param_fns
        self.world_fn = world_fn
        self.organism_fns = organism_fns
        self.current_time = current_time
        self.end_time = end_time

        # world is a World object
        self.world = initialize_world(world_fns, world_param_fn)
        # organisms is a list of Organism objects
        self.organism_list = initialize_organisms(organism_fns, species_param_fs)
        self.intent_list = []

    # return World object
    def initialize_world(self, world_fn=None, world_param_fn=None):
        # world = world.World()
        if world_fn is not None:
            world = dl.load_datasets(world_fn, fields.world_field_names.keys())
            # TODO: set up entire world based on world records
        elif world_param_fn is not None:
            world = pl.load_world_params(world_param_fn)
            # TODO: set up entire world based on parameter file
            pass
        else:
            sys.exit('No files specified for initialization!')
        return world

    def initialize_organisms(self, organism_fns=None, species_param_fs=None):
        # organisms is a list of Organism objects
        # organisms = []
        if organism_fns is not None:
            organism_list = dl.load_datasets(organism_fns,
                                            fields.organism_field_names.keys())
            # TODO: set up all organisms based on organism records
        elif species_param_fs is not None:
            organism_list = pl.load_species_params(species_param_fns)
            # TODO: set up all organisms based on species specifications
            pass
        else:
            sys.exit('No files specified for initialization!')
        return organism_list

    def step(self):
        self.organism_list = self.intent_list
        self.intent_list = []
        for organism in organism_list:
            self.intent_list.append(organism.act(self.organism_list, self.world))
        # Somehow parse whether the intent_list makes sense, otherwise revise it
        self.current_time += 1

# the entire executable could just be written like this
# and everything happens under the hood
# well, we have to include parameter input options,
# but these can go straight into Universe initialization
if __name__ == '__main__':
    universe = Universe()
    while universe.current_time < universe.end_time:
        universe.step()
