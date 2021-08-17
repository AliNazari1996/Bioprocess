from biorefineries.lipidcane import chemicals
from biosteam.units import Fermentation
from biosteam import main_flowsheet, settings, units, Stream

settings.set_thermo(chemicals)
s1 = Stream('feed',Water=1.20e+05,Glucose=1.89e+03,Sucrose=2.14e+04,DryYeast=1.03e+04,units='kg/hr',T=32+273.15)

# Stream one definition (stream assignment)
#s1.vle(P=101325, V=0.75), Vapour fraction indication at a certain Pressure.
# In stream function is adjustable (Pressure Temperature, Mole flows)
#lle also (sle) not sure though.

s2 = Stream('s2', water=10000, T=32+273.15, P=101325,units='kg/hr', phase='l')

#(Pressure Temperature, Mole flows)
s1.show()
s2.show()

M1 = units.Mixer('M1', ins=(s1, s2), outs='s3')                         #Mixer function
M1.simulate()                                                           #Simulation
M1 = main_flowsheet('M1')                                               #Inclusion into the flowsheet
M1.show()                                                               #shows the results of a unit or a stream.

feed = M1.outs[0]
R1 = Fermentation('R1',ins=feed, outs=('CO2', 'product'),tau=8, efficiency=0.90, N=8) #Fermentation function
R1.simulate()
R1.show()

F1 = units.Flash('F1', V=0.5, P=101325)                                 #Flash operation
F1.ins[0] = R1.outs[1]                                                  #(stream assignment)
F1.simulate()
F1 = main_flowsheet('F1')
F1.show()

feed = F1.outs[1]
S1 = units.Splitter('S1', ins=feed, outs=('top', 'bot'), split=0.1) #Component split is thermodynamically infeasible!
S1.simulate()
s1 = main_flowsheet('S1')
S1.show()

main_flowsheet.diagram(kind='cluster', file='ABC.png')              #flowsheet display function.

