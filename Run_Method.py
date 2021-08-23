from biosteam import settings, Chemical, Stream, units, main_flowsheet

main_flowsheet.set_flowsheet('mix_ethanol_with_denaturant')
settings.set_thermo(['Water', 'Ethanol', 'Octane'])
dehydrated_ethanol = Stream('dehydrated_ethanol', T=340,
                            Water=0.1, Ethanol=99.9, units='kg/hr')

ADD = Stream('denaturant', Octane=1)
M1 = units.Mixer('M1', ins=(dehydrated_ethanol, ADD), outs='denatured_ethanol')

def adjust_denaturant_flow():

    ADD.imass['Octane'] = 0.02 / 0.98 * dehydrated_ethanol.F_mass # Vary input = SPEC
    M1._run() #Runs mass and energy for a specific unit.
    M1.specification = adjust_denaturant_flow #Specification is met for this unit.

adjust_denaturant_flow()

M1.simulate()
M1.show(composition=True, flow='kg/hr')
k=M1.specification

print(k)