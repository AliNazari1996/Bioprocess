from biorefineries.lipidcane import chemicals
from biosteam.process_tools import BoundedNumericalSpecification
from biosteam import main_flowsheet, settings, units, Stream, System, Unit
import biosteam as bst
from biosteam.units import HXutility

# How to incorporate the defined functions to operate on the intermediate variable ms ?

class CISTR(bst.Unit):
    """
    Creates a CSTR reactor that calculates the conversion according to a specific first order
    reaction kinetics and residance time.

    Parameters
    ----------
    ins : stream
        Inlet fluid.
    outs : stream
        Outlet fluid
    Vol : float
        Volume

    P and T taken as the inlet (Isobaric & Isothermal)
    """
    _N_ins = 1
    _N_outs = 1                                                          #Gas phase and liquid phase outlets
    #_N_heat_utilities = 1
    _units = {'Conversion': '%'}

    def __init__(self, ID='', ins=None, outs=(), thermo=None, *, Vol):
        bst.Unit.__init__(self, ID, ins, outs, thermo)
        self._multistream = bst.MultiStream(None, thermo=self.thermo)
        self.Vol = Vol                                                   #Reactor volume

    def _setup(self):
        super()._setup()
        outlet = self.outs[0]

    def _run(self):

        inlet = self.ins[0]

        A = inlet.imass['OleicAcid', 'Methanol', 'Water', 'Biodiesel']

        LIST = []
        LIST_extract = ['' for x in range(len(A))]

        for i in range(len(A)):
            LIST.append(str(A[i]))

        ENGAGE = 1

        for k in range(len(LIST)):
            for i in LIST[k]:
                for j in i:
                    if j == ' ':
                        ENGAGE = ENGAGE * (-1)
                    if ENGAGE == -1:
                        LIST_extract[k] = str(LIST_extract[k]) + j

        AA = [0 for x in range(len(A))]
        for i in range(len(LIST_extract)):
            AA[i] = float(LIST_extract[i][1:len(LIST_extract[i])])

        Mole_Flows = inlet.imol['OleicAcid', 'Methanol', 'Water', 'Biodiesel']

        rho = inlet.rho
        T = inlet.T
        P = inlet.P
        Phi_tot = sum(AA) / rho
        tau = self.Vol / Phi_tot

        # First order reaction kinetics for a continuously ideally stirred tank reactor. [CISTR(1,0)]
        # k = 10^(-1) is assumed. (WARNING: Artificial kinetics)

        K = 10 ** (-1)
        Conv = K * tau / (1 + (K * tau))

        self.outs[0] = bst.Stream('s2', OleicAcid=Mole_Flows[0] * (1 - Conv), Methanol=Mole_Flows[0] * (1 - Conv),Water=Mole_Flows[0] * Conv, Biodiesel=Mole_Flows[0] * Conv, T=T, P=P)
def adjust_s1_flow_Methanol():

    s1.imol['Methanol'] = 100 - s2.imol['Methanol']          # VARIABLE parameter = Specification
    M1._run()                                    # Runs the mass and energy balances around this
    M1.specification = adjust_s1_flow_Methanol        # Specification related to M1
def f(T):
    F1.T = T
    F1._run()
    liquid = F1.outs[1]
    RES = liquid.imol['Methanol']
    return  RES - 0.5

# Oleic acid + methanol --> water + Methyl oleate (Reaction pathway)
# Methyl oleate = Biodiesel

settings.set_thermo(['OleicAcid','Methanol','Water','Methyl oleate'])
settings.set_thermo(chemicals)

s1 = Stream('Feed',OleicAcid=100, Methanol=100, Water =0, Biodiesel=0, units='kmol/hr',T=350, phase='l')
s2 = Stream('Recycle',OleicAcid=0, Methanol=0, Water =0, Biodiesel=0, units='kmol/hr',T=350, phase='l')

error = 10
K = 0
while error >= 0.1 :

    M1 = units.Mixer('M1', ins=(s1, s2), outs='s1')
    M1.simulate()
    adjust_s1_flow_Methanol()  # The spec function is called after the unit definition.

    R1 = CISTR('R1', ins=M1.outs[0], Vol=100,outs='s2')
    R1.simulate()

    F1 = units.Flash('F1', ins=R1.outs[0], P=101325, T=400,outs=('s3','product'))
    F1.specification = BoundedNumericalSpecification(f, 300, 500)  # reducing the methanol in the upgraded fuel!
    F1.simulate()

    HX1 = HXutility(ID='HX1', ins=F1.outs[0], T=350,outs='Recycle')
    HX1.simulate()

    S_previous = s2.imol['OleicAcid', 'Methanol', 'Water', 'Biodiesel']
    print(S_previous)
    s2 = HX1.outs[0]
    S_new = s2.imol['OleicAcid', 'Methanol', 'Water', 'Biodiesel']
    print(s2)
    error = abs(sum(S_new) - sum(S_previous))
    print(error)
    K = K + 1

M1.show()
R1.show()
F1.show()
HX1.show()

print(K)
bst.main_flowsheet.diagram(kind='cluster', file='FlowSheet.png')