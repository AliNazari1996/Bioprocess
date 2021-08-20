from biorefineries.lipidcane import chemicals
from biosteam.process_tools import BoundedNumericalSpecification
from biosteam import main_flowsheet, settings, units, Stream, System, Unit
import biosteam as bst

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

        self.outs[0] = bst.Stream('OUTFLOW', OleicAcid=Mole_Flows[0] * (1 - Conv), Methanol=Mole_Flows[0] * (1 - Conv),Water=Mole_Flows[0] * Conv, Biodiesel=Mole_Flows[0] * Conv, T=T, P=P)


settings.set_thermo(['OleicAcid','Methanol','Water','Methyl oleate'])
settings.set_thermo(chemicals)
s1 = Stream('s1',OleicAcid=100, Methanol=100, Water =0, Biodiesel=0, units='kmol/hr',T=350, phase='l')
CCC = CISTR('c1', ins=s1 ,Vol=100,)
CCC.simulate()
CCC.show()





