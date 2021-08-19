from biorefineries.lipidcane import chemicals
from biosteam import main_flowsheet, settings, units, Stream, System, Unit

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
def CSTR_REACTOR(ID,inflow,Volume):

    Mole_Flows = inflow.imol['OleicAcid', 'Methanol','Water','Biodiesel']
    Mass_flow = Vector_extract(inflow.imass['OleicAcid', 'Methanol','Water','Biodiesel'])
    Volumetric_flow = Vector_extract(inflow.ivol['OleicAcid', 'Methanol','Water','Biodiesel'])

    T = inflow.T
    P = inflow.P
    Phase = inflow.phase

    if sum(Mass_flow) ==0:
        rho = 1
        tau = 0

    if sum(Mass_flow) !=0:
        rho = inflow.rho
        Phi_tot = sum(Mass_flow) / rho
        tau = Volume / Phi_tot

    # First order reaction kinetics for a continuously ideally stirred tank reactor. [CISTR(1,0)]
    # A k = 10^(-2) is assumed. (WARNING: Artificial kinetics)

    K = 10**(-1)
    Conv = K*tau /(1+(K*tau))

    outflow = Stream('OUTFLOW',OleicAcid=Mole_Flows[0]*(1-Conv),Methanol=Mole_Flows[0]*(1-Conv),Water=Mole_Flows[0]*Conv,Biodiesel=Mole_Flows[0]*Conv,T=T,P=P)
    return outflow

# Oleic acid + methanol --> water + Methyl oleate (Reaction pathway)

settings.set_thermo(['OleicAcid','Methanol','Water','Methyl oleate'])
settings.set_thermo(chemicals)

# Methyl oleate = Biodiesel

s1 = Stream('s1',OleicAcid=100, Methanol=0, Water =0, Biodiesel=0, units='kmol/hr',T=350, phase='l')
s2 = Stream('s2',OleicAcid=0, Methanol=100, Water =0, Biodiesel=0, units='kmol/hr',T=350, phase='l')

s1.show()
s2.show()

M1 = units.Mixer('M1', ins=(s1, s2), outs='s3')

M1 = main_flowsheet('M1')
M1.show()

feed = M1.outs[0]

ID = 'RRR'
V = 100 # m^3

outflow = CSTR_REACTOR(ID,feed,V)
RRR = Unit(ID =ID,ins=feed, outs=outflow)
RRR.show()


F1 = units.Flash('F1', ins=outflow,T=400, P=101325)




main_flowsheet.diagram(kind='cluster', file='ABC.png')

[s1, s2] - M1
M1-RRR
RRR-F1

sys = System('sys', path=(M1, RRR, F1))

sys.simulate()
sys.show()



