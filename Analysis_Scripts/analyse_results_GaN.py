import os

from lobsterpy.cohp.analyze import Analysis
from lobsterpy.cohp.describe import Description

from pymatgen.io.lobster import MadelungEnergies
from pymatgen.io.vasp import Vasprun

# TODO: add code to get total energy

directories = [
    "/hpc-user/jgeorge/PycharmProjects/Scripts_for_Automation/LobsterAutomation/Results/GaN/mp-804/Spin_2/lobster_0",
    "/hpc-user/jgeorge/PycharmProjects/Scripts_for_Automation/LobsterAutomation/Results/GaN/mp-830/Spin_2/lobster_0/",
    "/hpc-user/jgeorge/PycharmProjects/Scripts_for_Automation/LobsterAutomation/Results/GaN/mp-1007824/Spin_2/lobster_0/",
    "/hpc-user/jgeorge/PycharmProjects/Scripts_for_Automation/LobsterAutomation/Results/GaN/mp-2853/Spin_2/lobster_0/",

    ]

icohps_sum=[]
icohps_mean=[]
total_energies=[]
madelung_energies=[]
charge_Ga=[]

for directory in directories:
    # Setup analysis dict
    analyse = Analysis(path_to_poscar=os.path.join(directory, "POSCAR.gz"),
                       path_to_icohplist=os.path.join(directory, "ICOHPLIST.lobster.gz"),
                       path_to_cohpcar=os.path.join(directory, "COHPCAR.lobster.gz"),
                       path_to_charge=os.path.join(directory, "CHARGE.lobster.gz"),
                       path_to_madelung=os.path.join(directory,"MadelungEnergies.lobster"))

    # Setup Desciption dict
    describe = Description(analysis_object=analyse)
    describe.write_description()

    # Automatic plots
    describe.plot_cohps(ylim=[-10, 2], xlim=[-4, 4])

    # different dicts that summarize the results
    print(analyse.condensed_bonding_analysis)
    print(analyse.final_dict_bonds)
    #TODO: has to be divided by number of symmetry indepenedent cations
    icohps_sum.append(analyse.final_dict_bonds["Ga-N"]["ICOHP_sum"]/len(analyse.final_dict_cations['Ga']))

    icohps_mean.append(analyse.final_dict_bonds["Ga-N"]["ICOHP_mean"])
    print(analyse.final_dict_cations)

    #madelung_energy=MadelungEnergies(filename=os.path.join(directory,"MadelungEnergies.lobster"))



    vasprun_here = Vasprun(filename=os.path.join(directory, "vasprun.xml.gz"))
    structure=vasprun_here.final_structure
    formula_units=structure.composition.num_atoms / structure.composition.reduced_composition.num_atoms
    final_energy=vasprun_here.final_energy/formula_units


    total_energies.append(final_energy)
    madelung_energies.append(analyse.condensed_bonding_analysis["madelung_energy"]/formula_units)

#TODO: add two plots correlating the Madelung energy with total energy
#TODO: add two plots correlating the sum_of_bond strength per Ga-N with total energy
# TODO: add this to a nice pandas frame that can be viszalized
print(icohps_sum)
print(icohps_mean)
print(total_energies)
print(madelung_energies)

import matplotlib as mpl

mpl.rcParams["savefig.directory"] = os.chdir(os.getcwd())
mpl.rcParams["savefig.format"] = 'pdf'
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['font.family'] = 'Arial'
#mpl.rcParams['text.usetex'] = True



import matplotlib.pyplot as plt

fix, ax = plt.subplots()
ax.scatter(total_energies, icohps_sum)
plt.xlabel("Total energy (eV)")
plt.ylabel("ICOHP (eV)")

plt.show()


fix, ax = plt.subplots()
ax.scatter(total_energies, madelung_energies)
plt.xlabel("Total energy (eV)")
plt.ylabel("ICOHP (eV)")

plt.show()
