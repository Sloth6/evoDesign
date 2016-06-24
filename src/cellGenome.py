from neat.genome import Genome
from neat_custom.genes import AttributeGene, MorphogenGene

class CellType(object):
    """docstring for CellType"""
    def __init__(self, id, shape=[2], area_divide=8,
                density=10, friction=0.3):
        self.shape = shape # One dimension to be a circle.
        self.area_divide = area_divide # None to use an output node.
        self.density = density
        self.friction = friction

class CellGenome(Genome):
    """Extend the default genome with more behavior."""
    def __init__(self, *args, **kwargs):
        super(CellGenome, self).__init__(*args, **kwargs)

        # Start with one cell type with default params.
        self.cell_types = [CellType(0)]

        self.num_morphogens = 1
        self.morphogen_thresholds = 4

        self.morphogen_genes = dict()
        self.attribute_genes = dict()

        self.inputs = [
            'stress'
        ]

        self.outputs = [
            ('apoptosis', 'sigmoid', True),
            ('divide_sin', 'tanh', False),
            ('divide_cos', 'tanh', False),
            ('grow', 'tanh', False)
            # ('grow0', 'identity'),
            # ('grow1', 'identity')
        ]

        for i in range(self.num_morphogens):
            # Create the morphogen gene with ranodm values.
            self.morphogen_genes[i] = MorphogenGene(i)

            # Create the inputs and outputs for this morphogen.
            for t in range(self.morphogen_thresholds):
                self.inputs.append('a%it%i' % (i, t))

            self.outputs.append(('a'+str(i), 'sigmoid', False))
            self.outputs.append(('h'+str(i), 'sigmoid', False))

        # print self.inputs
        self.num_inputs  = len(self.inputs)
        self.num_outputs = len(self.outputs)
        self.config.input_nodes = self.num_inputs
        self.config.output_nodes = self.num_outputs

    def mutate(self, innovation_indexer):
        super(CellGenome, self).mutate(innovation_indexer)

        # if condition:
        #   add or subtract morphogen

        for mg in self.morphogen_genes.values():
            mg.mutate(self.config)

        for ag in self.attribute_genes.values():
            ag.mutate(self.config)

        return self

    # Override create_unconnected function. to take custom activation_types.
    @classmethod
    def create_unconnected(cls, ID, config):
        '''Create a genome for a network with no hidden nodes and no connections.'''
        c = cls(ID, config, None, None)
        node_id = 0
        # Create input node genes.
        for i in range(c.num_inputs):
            assert node_id not in c.node_genes
            c.node_genes[node_id] = config.node_gene_type(node_id, 'INPUT')
            node_id += 1

        # Create output node genes.
        # print(c.outputs)
        for (name, act_func, _) in c.outputs:
            node_gene = config.node_gene_type(node_id,
                                              node_type='OUTPUT',
                                              activation_type=act_func)
            assert node_gene.ID not in c.node_genes
            c.node_genes[node_gene.ID] = node_gene
            node_id += 1

        assert node_id == len(c.node_genes)
        return c

    def __str__(self):
        s = super(CellGenome, self).__str__()
        s += '\n'
        for mid, m in self.morphogen_genes.items():
            s += 'Morphogen %i:' % mid
            for k, v in m.values().items():
                s += '\n\t%s:%s' % (k,v)
        return s
