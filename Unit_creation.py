import biosteam as bst
from math import ceil

class Boiler(bst.Unit):  #Inheritance from Unit function of biosteam library.
    """
    Create a Boiler object that partially boils the feed.

    Parameters
    ----------
    ins : stream
        Inlet fluid.
    outs : stream sequence
        * [0] vapor product
        * [1] liquid product
    V : float
        Molar vapor fraction.
    P : float
        Operating pressure [Pa].

    """
    # Note that the documentation does not include `ID` or `thermo` in the parameters.
    # This is OK, and most subclasses in BioSTEAM are documented this way too.
    # Documentation for all unit operations should include the inlet and outlet streams
    # listed by index. If there is only one stream in the inlets (or outlets), there is no
    # need to list out by index. The types for the `ins` and `outs` should be either
    # `stream sequence` for multiple streams, or `stream` for a single stream.
    # Any additional arguments to the unit should also be listed (e.g. V, and P).

    _N_ins = 1
    _N_outs = 2
    _N_heat_utilities = 1
    _units = {'Area': 'm^2'}

    def __init__(self, ID='', ins=None, outs=(), thermo=None, *, V, P):
        bst.Unit.__init__(self, ID, ins, outs, thermo)
        # Initialize MultiStream object to perform vapor-liquid equilibrium later
        # NOTE: ID is None to not register it in the flowsheet
        self._multistream = bst.MultiStream(None, thermo=self.thermo)
        self.V = V #: Molar vapor fraction.
        self.P = P #: Operating pressure [Pa].

    def _setup(self):
        super()._setup()
        gas, liq = self.outs

        # Initialize top stream as a gas
        gas.phase = 'g'

        # Initialize bottom stream as a liquid
        liq.phase = 'l'

    def _run(self):
        feed = self.ins[0]
        gas, liq = self.outs

        # Perform vapor-liquid equilibrium
        ms = self._multistream
        ms.imol['l'] = feed.mol
        ms.vle(V=self.V, P=self.P)

        # Update output streams
        gas.mol[:] = ms.imol['g']
        liq.mol[:] = ms.imol['l']
        gas.T = liq.T = ms.T
        gas.P = liq.P = ms.P

        # Reset flow to prevent accumulation in multiple simulations
        ms.empty()

    def _design(self):
        # Calculate heat utility requirement (please read docs for HeatUtility objects)
        T_operation = self._multistream.T
        duty = self.H_out - self.H_in
        if duty < 0:
            raise RuntimeError(f'{repr(self)} is cooling.')
        hu = self.heat_utilities[0]
        hu(duty, T_operation)

        # Temperature of utility at entrance
        T_utility = hu.inlet_utility_stream.T

        # Temeperature gradient
        dT = T_utility - T_operation

        # Heat transfer coefficient kJ/(hr*m2*K)
        U = 8176.699

        # Area requirement (m^2)
        A = duty/(U*dT)

        # Maximum area per unit
        A_max = 743.224

        # Number of units
        N = ceil(A/A_max)

        # Design requirements are stored here
        self.design_results['Area'] = A/N
        self.design_results['N'] = N

    def _cost(self):
        A = self.design_results['Area']
        N = self.design_results['N']

        # Long-tube vertical boiler cost correlation from
        # "Product process and design". Warren et. al. (2016) Table 22.32, pg 592
        purchase_cost = N*bst.CE*3.086*A**0.55

        # Itemized purchase costs are stored here
        self.baseline_purchase_costs['Boilers'] = purchase_cost # Not accounting for material factor

        # Assume design, pressure, and material factors are 1.
        self.F_D['Boilers'] = self.F_P['Boilers'] = self.F_M['Boilers'] = 1.

        # Set bare-module factor for boilers
        self.F_BM['Boilers'] = 2.45


bst.settings.set_thermo(['Water'])
water = bst.Stream('water', Water=300)
B1 = Boiler('B1', ins=water, outs=('gas', 'liq'),V=0.5, P=101325)

B1.show()