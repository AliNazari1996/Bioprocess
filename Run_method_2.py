from biosteam.process_tools import BoundedNumericalSpecification
from biosteam import settings, Chemical, Stream, units, main_flowsheet

main_flowsheet.set_flowsheet('flash_specification_example')
settings.set_thermo(['Water', 'Ethanol', 'Propanol'])


mixture = Stream('mixture', T=340,Water=1000, Ethanol=1000, Propanol=1000,units='kg/hr')

F1 = units.Flash('F1',ins=mixture,outs=('vapor', 'liquid'),T=373, P=101325)

def f(T):
    F1.T = T
    F1._run() # IMPORTANT: This runs the mass and energy balance
    feed = F1.ins[0]
    vapor = F1.outs[0]
    V = vapor.F_mass / feed.F_mass
    return  V - 0.60

F1.specification = BoundedNumericalSpecification(f, 351.39, 373.15)

# Now create the system, simulate, and check results.
system = main_flowsheet.create_system()
system.simulate()
system.diagram()