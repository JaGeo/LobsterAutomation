import os
from pathlib import Path
import matplotlib.pyplot as plt
import argparse

from lobsterpy.cohp.analyze import Analysis
from lobsterpy.cohp.describe import Description

# The computations have to be downloaded from zenodo.org as they too large for a github repository
outputs = Path(__file__).parent / "Outputs"

parser = argparse.ArgumentParser()
parser.add_argument(
    "--style",
    type=str,
    default=Path(__file__).parent / "Styles" / "pub.mplstyle-14-1-11",
    nargs="+",
    help="Matplotlib style for plotting",
)
parser.add_argument(
    "--sigma",
    type=float,
    default=0.1,
    help="sigma for gaussian broadening",
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

# First folder contains spin-polarized computation, second one the one without.
for spin in ["Spin_2", "Spin_mixed"]:
    directory = (
        Path(__file__).parent.parent / f"Results/Yb14MnSb11/mp-568088/{spin}/lobster_1"
    )

    # Setup analysis dict
    analyse = Analysis(
        path_to_poscar=os.path.join(directory, "POSCAR.gz"),
        path_to_icohplist=os.path.join(directory, "ICOHPLIST.lobster.gz"),
        path_to_cohpcar=os.path.join(directory, "COHPCAR.lobster.gz"),
        path_to_charge=os.path.join(directory, "CHARGE.lobster.gz"),
        summed_spins=False,
    )

    # Setup Desciption dict
    describe = Description(analysis_object=analyse)
    describe.write_description()

    if args.style:
        plt.style.use(args.style)
    # Automatic plots
    describe.plot_cohps(
        ylim=[-4, 2],
        xlim=[-10, 10],
        integrated=False,
        save=(True if args.save else False),
        filename=(args.save / f"14-1-11-{spin}_large_basis.pdf") if args.save else None,
        sigma=args.sigma,
    )

    # different dicts that summarize the results

    print(analyse.condensed_bonding_analysis)
    print(analyse.final_dict_bonds)
    print(analyse.final_dict_ions)
