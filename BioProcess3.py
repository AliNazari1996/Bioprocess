from biorefineries.lipidcane import chemicals
from biosteam.units import Fermentation
from biosteam import Stream, settings
settings.set_thermo(chemicals)
feed = Stream('feed',Water=1.20e+05,Glucose=1.89e+03,Sucrose=2.14e+04,DryYeast=1.03e+04,units='kg/hr',T=32+273.15)
>>> F1 = Fermentation('F1',
...                   ins=feed, outs=('CO2', 'product'),
...                   tau=8, efficiency=0.90, N=8)
>>> F1.simulate()
>>> F1.show()