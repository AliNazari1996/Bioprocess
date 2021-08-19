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
    rho = inflow.rho

    Phi_tot = sum(Mass_flow)/rho
    tau = Volume/Phi_tot

    # First order reaction kinetics for a continuously ideally stirred tank reactor. [CISTR(1,0)]
    # k = 10^(-1) is assumed. (WARNING: Artificial kinetics)

    K = 10**(-1)
    Conv = K*tau /(1+(K*tau))

    outflow = Stream('OUTFLOW',OleicAcid=Mole_Flows[0]*(1-Conv),Methanol=Mole_Flows[0]*(1-Conv),Water=Mole_Flows[0]*Conv,Biodiesel=Mole_Flows[0]*Conv,T=T,P=P)
    U = Unit(ID=ID, ins=inflow, outs=outflow)
    U.show()
    return outflow

def adjust_s2_flow():
    s2.imol['Methanol']= s1.F_mol            # VARIABLE parameter = Specification
    M1._run()                                # Only runs the mass and energy balances around this
    M1.specification = adjust_s2_flow        # Specification related to M1

# Oleic acid + methanol --> water + Methyl oleate (Reaction pathway)

settings.set_thermo(['OleicAcid','Methanol','Water','Methyl oleate'])
settings.set_thermo(chemicals)

# Methyl oleate = Biodiesel

s1 = Stream('s1',OleicAcid=100, Methanol=0, Water =0, Biodiesel=0, units='kmol/hr',T=350, phase='l')
s2 = Stream('s2',OleicAcid=0, Methanol=50, Water =0, Biodiesel=0, units='kmol/hr',T=350, phase='l')

s1.show()
s2.show()

M1 = units.Mixer('M1', ins=(s1, s2), outs='s3')

adjust_s2_flow() # The spec function is called after the unit definition.


M1.simulate()
M1 = main_flowsheet('M1')
M1.show()

feed = M1.outs[0]

ID = 'R1'
V = 100 # m^3
feed = CSTR_REACTOR(ID,feed,V)
feed.show()

F1 = units.Flash('F1', ins=feed, P=101325,T=400)
F1.simulate()
F1 = main_flowsheet('F1')
F1.show()

main_flowsheet.diagram(kind='cluster', file='ABC.png')

