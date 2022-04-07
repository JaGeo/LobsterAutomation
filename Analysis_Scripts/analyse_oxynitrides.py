import os

import pandas as pd
from lobsterpy.cohp.analyze import Analysis
from lobsterpy.cohp.describe import Description
from pymatgen.core.structure import Structure
from pymatgen.io.lobster import Lobsterout
from pymatgen.io.vasp.outputs import Vasprun
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer


correlation_dict = {}

directories = [
    "/hpc-user/jgeorge/PycharmProjects/Scripts_for_Automation/LobsterAutomation/Results/Ca1Ta1O2N1",
    "/hpc-user/jgeorge/PycharmProjects/Scripts_for_Automation/LobsterAutomation/Results/Ba1Ta1O2N1",
    "/hpc-user/jgeorge/PycharmProjects/Scripts_for_Automation/LobsterAutomation/Results/Sr1Ta1O2N1",
]

for dir in directories:
    print(str(dir.split("/")[-1]))

    directories2 = os.listdir(os.path.join(dir))
    ICOHP = {}
    ICOHP_sum = {}
    total_energy = []
    CE_list = []
    CE_dict = {}
    spa_list = []
    madelung_list = []
    antibdg_dict = {}
    number_of_bonds_dict = {}
    structure_list = []

    for dir2 in directories2:
        lobdirs = os.listdir(os.path.join(dir, dir2))
        min = 10000.0

        # will only look at the lobster outputs and identify the one with the smalles charge spilling
        for lobdiriter in [dir for dir in lobdirs if dir not in ["optimization"]]:
            lobster0 = Lobsterout(os.path.join(dir, dir2, lobdiriter, "lobsterout.gz"))
            csp0 = float(lobster0.chargespilling[0]) + float(lobster0.chargespilling[1])
            if csp0 < min:
                min = csp0
                lobdir = lobdiriter
                lobster_final_0 = lobster0

        structure = Structure.from_file(os.path.join(dir, dir2, lobdir, "POSCAR.gz"))
        sga = SpacegroupAnalyzer(structure)

        symm_struct = sga.get_symmetrized_structure()
        vasprun = Vasprun(filename=os.path.join(dir, dir2, lobdir, "vasprun.xml.gz"))
        formula_units = (
            structure.composition.num_atoms
            / structure.composition.reduced_composition.num_atoms
        )
        energy = vasprun.final_energy / formula_units

        import contextlib

        # this cleans up the screen output. Otherwise, there will be too many references visible
        with contextlib.redirect_stdout(None):
            with contextlib.redirect_stderr(None):
                analyse = Analysis(
                    path_to_poscar=os.path.join(dir, dir2, lobdir, "POSCAR.gz"),
                    path_to_icohplist=os.path.join(
                        dir, dir2, lobdir, "ICOHPLIST.lobster.gz"
                    ),
                    path_to_cohpcar=os.path.join(
                        dir, dir2, lobdir, "COHPCAR.lobster.gz"
                    ),
                    path_to_charge=os.path.join(dir, dir2, lobdir, "CHARGE.lobster.gz"),
                    path_to_madelung=os.path.join(
                        dir, dir2, lobdir, "MadelungEnergies.lobster.gz"
                    ),
                )

                describe = Description(analysis_object=analyse)
        describe.write_description()

        for bond in analyse.final_dict_bonds.keys():
            if not bond in ICOHP:
                ICOHP[bond] = [analyse.final_dict_bonds[bond]["ICOHP_mean"]]
                antibdg_dict[bond] = [analyse.final_dict_bonds[bond]["has_antbdg"]]
                CE_dict[bond] = [analyse.final_dict_ions[bond.split("-")[1]]]
            else:
                ICOHP[bond].append(analyse.final_dict_bonds[bond]["ICOHP_mean"])
                antibdg_dict[bond].append(analyse.final_dict_bonds[bond]["has_antbdg"])
                CE_dict[bond].append(analyse.final_dict_ions[bond.split("-")[1]])
        total_energy.append(energy)
        madelung_list.append(
            analyse.condensed_bonding_analysis["madelung_energy"] / formula_units
        )

        structure_list.append(dir2)
        spa_list.append(sga.get_space_group_symbol())

        # add madelung energies
        all_ICOHPs = []
        all_totale_energy = []
        all_CE_list = []
        all_spa_list = []
        all_keys = []
        all_antibdg = []
        all_structure_list = []
        all_madelung_list = []
        for key, item in ICOHP.items():
            all_ICOHPs.extend(item)
            all_totale_energy.extend(total_energy)
            all_CE_list.extend(CE_dict[key])
            all_spa_list.extend(spa_list)
            all_madelung_list.extend(madelung_list)
            all_keys.extend(len(item) * [key])
            all_antibdg.extend(antibdg_dict[key])
            all_structure_list.extend(structure_list)

        data = {
            "ICOHP": all_ICOHPs,
            "total_energy": all_totale_energy,
            "env": all_CE_list,
            "spa": all_spa_list,
            "key": all_keys,
            "has_antibdg": all_antibdg,
            "structure_id": all_structure_list,
            "madelung": all_madelung_list,
        }

        df = pd.DataFrame(data)

    print(df.to_string())

    # Plot the results
    import matplotlib as mpl

    mpl.rcParams["savefig.directory"] = os.chdir(os.getcwd())
    mpl.rcParams["savefig.format"] = "pdf"
    mpl.rcParams["pdf.fonttype"] = 42
    mpl.rcParams["ps.fonttype"] = 42

    import matplotlib.pyplot as plt
    import matplotlib.style as style
    import scipy

    style.use("ggplot")

    fix, ax = plt.subplots()

    for k, d in df.groupby("key"):
        if "Ta" in k:
            if "N" in k:
                color = "xkcd:lightish blue"
            elif "O" in k:
                color = "xkcd:lightish red"

            ax.scatter(d["total_energy"], d["ICOHP"], label=k, color=color)
            slope, intercept, r, p, stderr = scipy.stats.linregress(
                d["total_energy"], d["ICOHP"]
            )
            line = "Pearson correlation coefficient: " + str(r)
            ax.plot(
                d["total_energy"],
                intercept + slope * d["total_energy"],
                label=line,
                color=color,
            )

    plt.xlabel("Total energy (eV)")
    plt.ylabel("ICOHP (eV)")
    plt.legend(loc=2)
    plt.title(str(dir.split("/")[-1]))
    plt.show()
