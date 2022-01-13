import os

import pandas as pd
from lobsterpy.cohp.analyze import Analysis
from lobsterpy.cohp.describe import Description
from pymatgen.io.vasp import Vasprun

directories = [
    "../Results/GaN/mp-804/Spin_2/lobster_0",
    "../Results/GaN/mp-830/Spin_2/lobster_0/",
    "../Results/GaN/mp-1007824/Spin_2/lobster_0/",
    "../Results/GaN/mp-2853/Spin_2/lobster_0/",

]

names = ["mp-804", "mp-830", "mp-1007824", "mp-2853"]
icohps_sum = []
icohps_mean = []
total_energies = []
madelung_energies = []
charge_Ga = []

for directory in directories:
    # Setup analysis dict
    analyse = Analysis(path_to_poscar=os.path.join(directory, "POSCAR.gz"),
                       path_to_icohplist=os.path.join(directory, "ICOHPLIST.lobster.gz"),
                       path_to_cohpcar=os.path.join(directory, "COHPCAR.lobster.gz"),
                       path_to_charge=os.path.join(directory, "CHARGE.lobster.gz"),
                       path_to_madelung=os.path.join(directory, "MadelungEnergies.lobster.gz"))

    # Setup Desciption dict
    describe = Description(analysis_object=analyse)
    describe.write_description()

    # Automatic plots
    describe.plot_cohps(ylim=[-10, 2], xlim=[-5, 5])

    # different dicts that summarize the results
    print("Dicts including informations on bonds")
    print(analyse.condensed_bonding_analysis)
    print(analyse.final_dict_bonds)

    print(analyse.final_dict_cations)

    vasprun_here = Vasprun(filename=os.path.join(directory, "vasprun.xml.gz"))
    structure = vasprun_here.final_structure
    formula_units = structure.composition.num_atoms / structure.composition.reduced_composition.num_atoms
    final_energy = vasprun_here.final_energy / formula_units

    total_energies.append(final_energy)
    madelung_energies.append(analyse.condensed_bonding_analysis["madelung_energy"] / formula_units)
    icohps_sum.append(analyse.final_dict_bonds["Ga-N"]["ICOHP_sum"] / len(analyse.final_dict_cations['Ga']))
    icohps_mean.append(analyse.final_dict_bonds["Ga-N"]["ICOHP_mean"])

# make a pandas dataframe

df = pd.DataFrame(list(zip(names, total_energies, madelung_energies, icohps_sum, icohps_mean)),
                  columns=["Name", "Total Energy (eV)", "Madelung Energy (eV)", "Sum ICOHP (eV)", "Mean ICOHP (eV)"])
print("Data Frame:")
print(df.to_string())
