from biorefineries.lipidcane import chemicals
from biosteam.units import Fermentation
from biosteam import main_flowsheet, settings, units, Stream, System,Unit

def Vector_extract(Mass_flow):

    LIST = []
    LIST_extract = ['' for x in range(len(Mass_flow))]

    for i in range(len(Mass_flow)):
        LIST.append(str(Mass_flow[i]))

    ENGAGE = 1

    for k in range(len(LIST)):
        for i in LIST[k]:
            for j in i:
                if j == ' ':
                    ENGAGE = ENGAGE * (-1)
                if ENGAGE == -1:
                    LIST_extract[k] = str(LIST_extract[k]) + j

    Mass_flow_extract = [0 for x in range(len(Mass_flow))]
    for i in range(len(LIST_extract)):
        Mass_flow_extract[i] = float(LIST_extract[i][1:len(LIST_extract[i])])

    return Mass_flow_extract
def CSTR_REACTOR(ID,inflow):

    Mole_Flows = inflow.imol['Water', 'Glucose', 'Sucrose', 'DryYeast']                          #Vectorise the mole flows
    Mass_flow = Vector_extract(inflow.imass['Water','Glucose','Sucrose','DryYeast'])
    Volumetric_flow = Vector_extract(inflow.ivol['Water','Glucose','Sucrose','DryYeast'])
    T = inflow.T
    P = inflow.P
    Phase =  inflow.phase

    Mole_Flows =[i*0.8 for i in Mole_Flows]
    outflow = Stream('OUTFLOW',Water=Mole_Flows[0],Glucose=Mole_Flows[1],Sucrose=Mole_Flows[2],DryYeast=Mole_Flows[3],T=T,P=P)
    U = Unit(ID='ID', ins=inflow, outs=outflow)
    U.show()

settings.set_thermo(chemicals)

settings.set_thermo(['Benzoic acid','ethanol','ethyl benzoate','water'], cache=True)

print('ALOHA')


s1 = Stream('s1',Water=1.20e+05,Glucose=1.89e+03,Sucrose=2.14e+04,DryYeast=1.03e+04,units='kmol/hr',T=32+273.15)

#s1.vle(P=101325, V=0.75), Vapour fraction indication at a certain Pressure. Also (lle & sle)

s2 = Stream('s2', water=10000, T=32+273.15, P=101325,units='kmol/hr', phase='l')

s1.show()
s2.show()

M1 = units.Mixer('M1', ins=(s1, s2), outs='s3')
M1.simulate()
M1 = main_flowsheet('M1')
M1.show()

feed = M1.outs[0]

ID = 'R11'
CSTR_REACTOR(ID,feed)

#R1 = Fermentation('R1', ins=feed, outs=('CO2', 'product'), tau=8, efficiency=0.90, N=8)
R1.simulate()
R1.show()

feed = R1.outs[1]
F1 = units.Flash('F1', ins=feed,V=0.5, P=101325)

F1.simulate()
F1 = main_flowsheet('F1')
F1.show()

feed = F1.outs[1]
S1 = units.Splitter('S1', ins=feed, outs=('top', 'bot'), split=0.1)
S1.simulate()
s1 = main_flowsheet('S1')
S1.show()

Mole_Flows = S1.outs[0].mol




main_flowsheet.diagram(kind='cluster', file='ABC.png')

