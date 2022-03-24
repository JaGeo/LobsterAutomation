import argparse
import os
import matplotlib.pyplot as plt
from pathlib import Path

import pandas as pd
from lobsterpy.cohp.analyze import Analysis
from lobsterpy.cohp.describe import Description
from pymatgen.io.vasp import Vasprun

outputs = Path(__file__).parent / "Outputs"

parser = argparse.ArgumentParser()
parser.add_argument(
    "--style",
    type=str,
    default=Path(__file__).parent / "Styles" / "pub.mplstyle",
    nargs="+",
    help="Matplotlib style for plotting",
)
parser.add_argument(
    "--save",
    type=Path,
    nargs="?",
    const=outputs,
    default=None,
    help=("Save plots to files. If no path provided, " "will save to ./Outputs"),
)
args = parser.parse_args()

# We will analyze the results with Gaussian Smearing as VASP 6.* does not correctly determine the Fermi level with tetrahedron smearing
names = ["mp-804", "mp-830", "mp-1007824", "mp-2853"]

icohps_sum = []
icohps_mean = []
total_energies = []
madelung_energies = []
charge_Ga = []

for name in names:
    directory = (
        Path(__file__).parent.parent
        / f"Results/GaN_Gaussian_Smearing/{name}/Spin1_ISMEAR_0/lobster_0"
    )
    # Setup analysis dict
    analyse = Analysis(
        path_to_poscar=os.path.join(directory, "POSCAR.gz"),
        path_to_icohplist=os.path.join(directory, "ICOHPLIST.lobster.gz"),
        path_to_cohpcar=os.path.join(directory, "COHPCAR.lobster.gz"),
        path_to_charge=os.path.join(directory, "CHARGE.lobster.gz"),
        path_to_madelung=os.path.join(directory, "MadelungEnergies.lobster.gz"),
    )

    # Setup Desciption dict
    describe = Description(analysis_object=analyse)
    describe.write_description()

    # Automatic plots
    if args.style:
        plt.style.use(args.style)

    describe.plot_cohps(
        ylim=[-20, 2],
        xlim=[-10, 30],
        save=(True if args.save else False),
        filename=(args.save / f"GaN-{name}.pdf") if args.save else None,
    )

    # different dicts that summarize the results
    print("Dicts including informations on bonds")
    print(analyse.condensed_bonding_analysis)
    print(analyse.final_dict_bonds)

    print(analyse.final_dict_ions)

    vasprun_here = Vasprun(filename=os.path.join(directory, "vasprun.xml.gz"))
    structure = vasprun_here.final_structure
    formula_units = (
        structure.composition.num_atoms
        / structure.composition.reduced_composition.num_atoms
    )
    final_energy = vasprun_here.final_energy / formula_units

    total_energies.append(final_energy)
    madelung_energies.append(
        analyse.condensed_bonding_analysis["madelung_energy"] / formula_units
    )
    number_of_bonds = [
        key.split(":")[1] for key in analyse.final_dict_ions["Ga"].keys()
    ][0]
    icohps_sum.append(
        analyse.final_dict_bonds["Ga-N"]["ICOHP_mean"] * int(number_of_bonds)
    )
    icohps_mean.append(analyse.final_dict_bonds["Ga-N"]["ICOHP_mean"])

# make a pandas dataframe

df = pd.DataFrame(
    list(zip(names, total_energies, madelung_energies, icohps_sum, icohps_mean)),
    columns=[
        "Name",
        "Total Energy (eV)",
        "Madelung Energy (eV)",
        "Sum ICOHP (eV)",
        "Mean ICOHP (eV)",
    ],
)
print("Data Frame:")
print(df.to_string())
