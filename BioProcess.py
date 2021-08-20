
def __init__(self, ID='', ins=None, outs=(), thermo=None, *, Vol):
    bst.Unit.__init__(self, ID, ins, outs, thermo)

    # Initialize MultiStream object to perform vapor-liquid equilibrium later
    # NOTE: ID is None to not register it in the flowsheet

    self._multistream = bst.MultiStream(None, thermo=self.thermo)
    self.Vol = Vol  # volume

def _setup(self):
    super()._setup()
    gas, liq = self.outs

    # Initialize top stream as a gas
    gas.phase = 'g'

    # Initialize bottom stream as a liquid
    liq.phase = 'l'



