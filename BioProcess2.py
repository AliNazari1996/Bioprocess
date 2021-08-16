import biosteam as bst
from biosteam import main_flowsheet, settings, units, Stream

settings.set_thermo(['Ethanol', 'Water'], cache=True)

s1 = Stream('s1', Water=20, T=350)
s2 = Stream('s2', Ethanol=20, T=300)
M1 = units.Mixer('M1', ins=(s1, s2), outs='s3')

M1.simulate()
M1.show()

F1 = units.Flash('F1', V=0.5, P=101325) # Unit operation
F1.ins[0] = M1.outs[0]

F1.simulate()
F1.show()

feed = F1.outs[1]
S1 = units.Splitter('S1', ins=feed, outs=('top', 'bot'), split=0.1) #Component split is thermodynamically infeasible!

S1.simulate()
S1.show()
file = bst.main_flowsheet.diagram()

#bst.settings.set_thermo(['Water', 'Methanol'])
#feed = bst.Stream(Water=50, Methanol=20) # kmol/hr Feed definition.

#F1 = units.Flash('F1', V=0.5, P=101325) # Unit operation
#F1.ins[0] = feed # feed assignment to unit operation.
# F1.ins the ingoing flows inside the unit, F1.outs: outgoing flows from the unit
#F1.simulate() # runs the system
#F1.results()  # shows the result ?? not working F1.results(with_units=False)
#F1.show()  # shows the result


