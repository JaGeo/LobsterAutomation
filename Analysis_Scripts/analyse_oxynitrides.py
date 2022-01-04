import os

import numpy as np
import pandas as pd
import plotly.express as px
from pymatgen.core.composition import Composition
from pymatgen.core.structure import Structure
from pymatgen.io.lobster import Lobsterout
from pymatgen.io.vasp.outputs import Vasprun
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

from lobsterpy.cohp.analyze import Analysis
from lobsterpy.cohp.describe import Description

exclude_distorted = False

# for foldername in range(0, 28):

correlation_dict = {}

directories = ["/hpc-user/jgeorge/PycharmProjects/Scripts_for_Automation/LobsterAutomation/Results/Ca1Ta1O2N1",
               "/hpc-user/jgeorge/PycharmProjects/Scripts_for_Automation/LobsterAutomation/Results/Ba1Ta1O2N1",
               "/hpc-user/jgeorge/PycharmProjects/Scripts_for_Automation/LobsterAutomation/Results/Sr1Ta1O2N1",
               "/hpc-user/jgeorge/PycharmProjects/Scripts_for_Automation/LobsterAutomation/Results/La1Ta1O2N1"]

#directories = ["/hpc-user/jgeorge/PycharmProjects/Scripts_for_Automation/LobsterAutomation/Results/La1Ta1O2N1"]

for idir, dir in enumerate(directories, 0):
    print("number dir: " + str(idir))
    okay = False
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

        for lobdiriter in lobdirs:
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
        formula_units = structure.composition.num_atoms / structure.composition.reduced_composition.num_atoms
        energy = vasprun.final_energy / formula_units
        analyse = Analysis(path_to_poscar=os.path.join(dir, dir2, lobdir, "POSCAR.gz"),
                           path_to_icohplist=os.path.join(dir, dir2, lobdir, "ICOHPLIST.lobster.gz"),
                           path_to_cohpcar=os.path.join(dir, dir2, lobdir, "COHPCAR.lobster.gz"),
                           path_to_charge=os.path.join(dir, dir2, lobdir, "CHARGE.lobster.gz"),
                           path_to_madelung=os.path.join(dir, dir2, lobdir, "MadelungEnergies.lobster"))

        describe = Description(analysis_object=analyse)
        describe.write_description()

        for bond in analyse.final_dict_bonds.keys():
            if not bond in ICOHP:
                ICOHP[bond] = [analyse.final_dict_bonds[bond]["ICOHP_mean"]]

                ICOHP_sum[bond] = [
                    analyse.final_dict_bonds[bond]["ICOHP_sum"] / len(analyse.final_dict_cations[bond.split('-')[0]])]
                # TODO: add ICOHP[bond]/len(number of different cations in structure)

                antibdg_dict[bond] = [analyse.final_dict_bonds[bond]["has_antbdg"]]

                CE_dict[bond] = [analyse.final_dict_cations[bond.split("-")[0]]]
                # addd number of bonds but maybe normalize for number of cations
            else:
                ICOHP[bond].append(analyse.final_dict_bonds[bond]["ICOHP_mean"])
                ICOHP_sum[bond].append(
                    analyse.final_dict_bonds[bond]["ICOHP_sum"] / len(analyse.final_dict_cations[bond.split('-')[0]]))

                antibdg_dict[bond].append(analyse.final_dict_bonds[bond]["has_antbdg"])
                CE_dict[bond].append(analyse.final_dict_cations[bond.split("-")[0]])
            # print(CE_dict)
        total_energy.append(energy)
        madelung_list.append(analyse.condensed_bonding_analysis["madelung_energy"] / formula_units)

        # CE_list.append(describe.final_dict_cations)
        print(analyse.final_dict_cations)
        print(analyse.final_dict_bonds)

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
            # add info on antibonding interactions

        data = {"ICOHP": all_ICOHPs, "total_energy": all_totale_energy, "env": all_CE_list, "spa": all_spa_list,
                "key": all_keys, "has_antibdg": all_antibdg, "structure_id": all_structure_list,
                "madelung": all_madelung_list}

        df = pd.DataFrame(data)

    print(df)
    fig = px.scatter(df, x="total_energy", y="ICOHP", color="key",
                     hover_data=["env", "spa", "has_antibdg", "structure_id", "madelung"])
    # TODO: include this again
    import matplotlib as mpl

    mpl.rcParams["savefig.directory"] = os.chdir(os.getcwd())
    mpl.rcParams["savefig.format"] = 'pdf'
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['ps.fonttype'] = 42
    mpl.rcParams['font.family'] = 'Arial'
    # mpl.rcParams['text.usetex'] = True

    fig.show()

    import matplotlib.pyplot as plt
    import matplotlib.style as style
    import scipy

    style.use('ggplot')

    fix, ax = plt.subplots()

    for k, d in df.groupby("key"):
        if "Ta" in k:
            if "N" in k:
                color = "xkcd:lightish blue"
            elif "O" in k:
                color = "xkcd:lightish red"

            ax.scatter(d["total_energy"], d["ICOHP"], label=k, color=color)
            slope, intercept, r, p, stderr = scipy.stats.linregress(d["total_energy"], d["ICOHP"])
            # line = f'Regression line: y={intercept:.2f}+{slope:.2f}x, r={r:.2f}'
            line = "Pearson correlation coefficient: " + str(r)
            ax.plot(d["total_energy"], intercept + slope * d["total_energy"], label=line, color=color)

    plt.xlabel("Total energy (eV)")
    plt.ylabel("ICOHP (eV)")
    plt.legend(loc=2)
    plt.title(dir)
    plt.show()

#     #fig.show()
#     #Add another type of plot here to export to the manuscript
#     # Use BaTaO2N, CaTaO2N, SrTaO2N as an example.
#
#     print(dir)
#
#     # fix, ax = plt.subplots()
#     correlation_dict[dir] = {}
#     for k, d in df.groupby("key"):
#
#             # ax.scatter(d["total_energy"], d["ICOHP"], label=k)
#             # save a correlation for each k
#             my_rho = np.corrcoef(d["ICOHP"], d["total_energy"])
#             #taken from https://www.freecodecamp.org/news/how-machines-make-predictions-finding-correlations-in-complex-data-dfd9f0d87889/
#             r = my_rho[0][1]
#             import math
#             z = math.atanh(r)
#             SD_z = 1 / math.sqrt(len(d["ICOHP"]) - 3)
#             z_upper = z + 1.96 * SD_z
#             z_lower = z - 1.96 * SD_z
#             r_upper = math.tanh(z_upper)
#             r_lower = math.tanh(z_lower)
#             correlation_dict[dir][k] = {"coeff": my_rho[0][1], "minICOHP": float(str(np.min(d["ICOHP"])))}
#             print(str(k) + ': ' + str(my_rho[0][1]) + ' ' + str(len(d["ICOHP"])) + ' ' + str(np.min(d["ICOHP"])))
#
#
# # plot correlation plot
#
# print(correlation_dict)
# #TODO: you might have to exclude more compounds from the overall plots!
#
# def get_heatmap_data(list_compounds, correlation_dict, anions={"N":2, "O":1}):
#     O2N_dict = {}
#
#     # O2N
#     cationAlist_O2N = []
#     cationBlist_O2N = []
#     for compound, bonds in correlation_dict.items():
#         print(compound)
#         if compound in list_compounds:
#             # finde Bindung, mit der ich Korrelation zeigen möchte?
#             # oder finde Bindung mit höchster Korrelation?
#             maxvalue = 0.0
#             maxname = None
#             for bondname, bondinfo in bonds.items():
#                 print(bondinfo)
#                 print(bondname)
#                 #input()
#                 if abs(bondinfo["minICOHP"]) > maxvalue:
#                     maxname = bondname
#                     maxvalue = abs(bondinfo["minICOHP"])
#                     print(abs(bondinfo["coeff"]))
#                     print(abs(bondinfo["minICOHP"]))
#             print(bondname)
#             print(bonds[maxname]["coeff"])
#             # O2N_dict[compound] = bonds[maxname]["coeff"]
#             # transfer compound name to
#             composition = Composition(compound)
#             print(composition.reduced_formula)
#             cations = [el for el in composition.elements if str(el) not in ["N", "O", "F"]]
#             cationA = str(cations[0])
#             cationB = str(cations[1])
#
#             skip=False
#             for label, number in anions.items():
#                 print(composition[label])
#                 print(number)
#
#                 if not np.isclose(composition[label],number):
#                     skip=True
#
#             if not skip:
#                 # TODO: fix bug
#                 if not cationA in O2N_dict:
#                     O2N_dict[cationA] = {}
#                     O2N_dict[cationA][cationB] = bonds[maxname]["coeff"]
#                 else:
#                     O2N_dict[cationA][cationB] = bonds[maxname]["coeff"]
#
#             cationAlist_O2N.append(cationA)
#             cationBlist_O2N.append(cationB)
#     print(O2N_dict)
#     setA_O2N = list(set(cationAlist_O2N))
#     setB_O2N = list(set(cationBlist_O2N))
#
#     return O2N_dict, setA_O2N, setB_O2N
#
# #TODO: update this list of compounds
# #generate all possible compounds here:
#
# #TODO: sort out combinations that will end up as metals
# list_cationA = ["Na", "K", "Rb", "Cs", "Mg", "Ca", "Sr", "Ba", "Ag", "La"]
# list_cationB = ["Ti", "V", "Nb", "Ta", "Cu", "Zn", "Al", "Pb", "Bi"]
#
#
# O2N_dict, setA_O2N, setB_O2N = get_heatmap_data(
#     list_compounds=directories, correlation_dict=correlation_dict, anions={"O":2, "N":1})
# N2O_dict, setA_N2O, setB_N2O = get_heatmap_data(list_compounds=directories,
#                                                 correlation_dict=correlation_dict, anions={"O":1, "N":2})
# F2O_dict, setA_F2O, setB_F2O = get_heatmap_data(list_compounds=directories,
#                                                 correlation_dict=correlation_dict, anions={"F":2, "O":1})
#
# O2F_dict, setA_O2F, setB_O2F = get_heatmap_data(
#     list_compounds=directories,
#     correlation_dict=correlation_dict, anions={"O":2, "F":1})
#
# # TODO: combine the generation of the heat maps in a better way:
#
#
# # setA_list = [list(set(setA_O2N+setA_N2O+setA_O2F+setA_F2O)), list(set(setA_O2N+setA_N2O+setA_O2F+setA_F2O)), list(set(setA_O2N+setA_N2O+setA_O2F+setA_F2O)), list(set(setA_O2N+setA_N2O+setA_O2F+setA_F2O))]
# # setB_list = [list(set(setB_O2N+setB_N2O+setB_O2F+setB_F2O)), list(set(setB_O2N+setB_N2O+setB_O2F+setB_F2O)), list(set(setB_O2N+setB_N2O+setB_O2F+setB_F2O)), list(set(setB_O2N+setB_N2O+setB_O2F+setB_F2O))]
#
# # TODO: how to extend?
#
# setA_list = [list_cationA, list_cationA, list_cationA, list_cationA]
# setB_list = [list_cationB, list_cationB, list_cationB, list_cationB]
#
# dict_list = [O2N_dict, N2O_dict, F2O_dict, O2F_dict]
# name_list = ["O2N", "N2O", "F2O", "O2F"]
# # heatmap O2N
# has_to_be_computed = []
# for setA, setB, dict_here, name in zip(setA_list, setB_list, dict_list, name_list):
#     print(setA)
#     print(setB)
#     array_here = np.zeros([len(setA), len(setB)])
#
#     for icationA, cationA in enumerate(setA):
#         for icationB, cationB in enumerate(setB):
#             try:
#                 array_here[icationA][icationB] = dict_here[cationA][cationB]
#             except:
#                 print("No entry")
#                 has_to_be_computed.append(str(cationA) + str(cationB) + name)
#
#     print(array_here)
#     print(setA)
#     print(setB)
#     import matplotlib.pyplot as plt
#
#     fig, ax = plt.subplots()
#     im = ax.imshow(array_here)
#     # TODO: check labels
#     ax.set_yticks(np.arange(len(setA)))
#     ax.set_xticks(np.arange(len(setB)))
#     ax.set_yticklabels(setA)
#     ax.set_xticklabels(setB)
#     # TODO: figure out what is wrong here?
#     plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
#              rotation_mode="anchor")
#     for i in range(len(setA)):
#         for j in range(len(setB)):
#             text = ax.text(j, i, np.round(array_here[i, j], 2),
#                            ha="center", va="center", color="w")
#
#     ax.set_title(name)
#     fig.tight_layout()
#     plt.show()
#
# print(has_to_be_computed)
