import biosteam as bst
from biosteam import units
from biorefineries.lipidcane import chemicals
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

bst.settings.set_thermo(['Water', 'Methanol','OleicAcid','Methyl oleate'])
bst.settings.set_thermo(chemicals)
feed = bst.Stream('feed', Methanol=100, Water=450,OleicAcid=1,Biodiesel=1)

Mole_Flows = feed.imol['Water', 'Methanol','OleicAcid','Biodiesel']
Mass_flow = Vector_extract(feed.imass['Water', 'Methanol','OleicAcid','Biodiesel'])
Volumetric_flow = Vector_extract(feed.ivol['Water', 'Methanol','OleicAcid','Biodiesel'])


print(Mole_Flows)
print(Mass_flow)



M1 = units.Mixer('M1',ins=feed)
F1 = units.Flash('F1', V=0.5, P=101325)
S1 = units.Splitter('S1', outs=('liquid_recycle', 'liquid_product'),split=0.5)  # Split to 0th output stream

F1.outs[0].ID = 'vapor_product'
F1.outs[1].ID = 'liquid'

# Broken down -pipe- notation # For each operation unit there is a Mass Balance node
[S1-0, feed]-M1     # M1.ins[:] = [S1.outs[0], feed]
M1-F1               # F1.ins[:] = M1.outs
F1-1-S1             # S1.ins[:] = [F1.outs[1]]

#[S1-0, feed]-M1-F1-1-S1;

# All together
#[S1-0, feed]-M1-F1-1-S1; What ?!
#flowsheet_sys = bst.main_flowsheet.create_system('flowsheet_sys')
#flowsheet_sys.show()

sys = bst.System('sys', path=(M1, F1, S1), recycle=S1-0)
# recycle=S1.outs[0]

sys.simulate()
sys.show()

bst.main_flowsheet.diagram(kind='cluster', file='ABC2.png')

