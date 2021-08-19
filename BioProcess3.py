import biosteam as bst
from biosteam.units import Mixer, Splitter

# Set property pacakge
bst.settings.set_thermo(['Water'])

# Set feed stream and units
feed1 = bst.Stream('feed1')
M1 = Mixer('M1', outs='s1')
S1 = Splitter('S1', outs=('s2', 'product1'), split=0.5)

feed2 = bst.Stream('feed2')
M2 = Mixer('M2', outs='s3')
S2 = Splitter('S2', outs=('recycle', 'product2'), split=0.5)
bst.main_flowsheet.diagram()


(feed1, S2-0)-M1-S1
(feed2, S1-0)-M2-S2

# Without -pipe- notation:
# M1.ins[:] = (feed1, S2.outs[0])
# S1.ins[:] = M1.outs
# M2.ins[:] = (feed2, S1.outs[0])
# S2.ins[:] = M2.outs

bst.main_flowsheet.diagram(kind='cluster', file='ABC4.png')