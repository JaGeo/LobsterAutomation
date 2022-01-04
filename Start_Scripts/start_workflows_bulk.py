from atomate.vasp.powerups import add_additional_fields_to_taskdocs
from atomate.vasp.workflows.base.lobster import get_wf_lobster_test_basis
from fireworks import LaunchPad
from pymatgen.ext.matproj import MPRester

# add standard settings for NaCl (mp-22862), ZnS (mp-10695), BaTiO3 (mp-5020), Yb14Mn1Sb11 (mp-568088/)
# add non-magnetic run for Yb14Mn1Sb11 (finger print for magnetism there?)
# TODO:  generate set of structures for BaTaO2N (maybe up to 2 unit cells)
# TODO:  generate set of structures for CaTaO2N (maybe up to 2 unit cells)
# TODO:  generate set of structures for SrTaO2N (maybe up to 2 unit cells)
# optimize structures well and create correlation plots!

# TODO: use ISMEAR=1 maybe?
#
# for ispin in [1]:
#     for mpid in [
#         "mp-568088"]:  # ["mp-830","mp-1007824"]:#["mp-804","mp-2853"]:#["mp-41", "mp-131"]:  # ["mp-22851","mp-560588", "mp-22862", "mp-10695", "mp-5020", "mp-568088"]:
#         with MPRester("1x3FJCaLIf2s6nRc") as a:
#             structure = a.get_structure_by_material_id(mpid)
#
#         wf = get_wf_lobster_test_basis(
#             structure=structure,
#             user_kpoints_settings={"grid_density": 6000},
#             user_incar_settings={"LCHARG": False, "ISPIN": ispin, "MAGMOM": None},
#             delete_all_wavecars=True,
#             additional_optimization=True,
#             user_incar_settings_optimization={"ISMEAR": 1, "EDIFFG": 1e-5, "EDIFF": 1e-6, "NELM": 3000, "ISPIN": ispin,
#                                               "MAGMOM": None},
#             user_kpoints_settings_optimization={"grid_density": 6000}
#         )
#
#         update_dict = {"material-id": mpid + '_' + str(ispin) + str("_ISMEAR_1")}
#         wf = add_additional_fields_to_taskdocs(wf, update_dict=update_dict, task_name_constraint='VaspToDb')
#         wf = add_additional_fields_to_taskdocs(wf, update_dict=update_dict, task_name_constraint='LobsterRunToDb')
#
#         lpad = LaunchPad.auto_load()  # loads this based on the FireWorks configuration
#         lpad.add_wf(wf)

# for ispin in [2]:
#     for mpid in [
#         "mp-568088"]:  # ["mp-568088","mp-830", "mp-1007824"]:#["mp-804","mp-2853"]:  # ["mp-22851","mp-560588","mp-22862", "mp-10695", "mp-5020", "mp-568088"]:
#         with MPRester("1x3FJCaLIf2s6nRc") as a:
#             structure = a.get_structure_by_material_id(mpid)
#
#         wf = get_wf_lobster_test_basis(
#             structure=structure,
#             user_kpoints_settings={"grid_density": 6000},
#             user_incar_settings={"LCHARG": False, "ISPIN": ispin},
#             delete_all_wavecars=True,
#             additional_optimization=True,
#             user_incar_settings_optimization={"ISMEAR": 1, "EDIFFG": 1e-5, "EDIFF": 1e-6, "NELM": 3000, "ISPIN": ispin},
#             user_kpoints_settings_optimization={"grid_density": 6000}
#         )
#
#         update_dict = {"material-id": mpid + '_' + str(ispin) + str("_ISMEAR_1")}
#         wf = add_additional_fields_to_taskdocs(wf, update_dict=update_dict, task_name_constraint='VaspToDb')
#         wf = add_additional_fields_to_taskdocs(wf, update_dict=update_dict, task_name_constraint='LobsterRunToDb')
#
#         lpad = LaunchPad.auto_load()  # loads this based on the FireWorks configuration
#         lpad.add_wf(wf)

for ispin in [2]:
    for mpid in [
        "mp-568088"]:  # ["mp-568088","mp-830", "mp-1007824"]:#["mp-804","mp-2853"]:  # ["mp-22851","mp-560588","mp-22862", "mp-10695", "mp-5020", "mp-568088"]:
        with MPRester("1x3FJCaLIf2s6nRc") as a:
            structure = a.get_structure_by_material_id(mpid)

        wf = get_wf_lobster_test_basis(
            structure=structure,
            user_kpoints_settings={"grid_density": 6000},
            user_incar_settings={"LCHARG": False, "ISPIN": ispin,},
            delete_all_wavecars=True,
            additional_optimization=True,
            user_incar_settings_optimization={"ISMEAR": 1, "EDIFFG": 1e-5, "EDIFF": 1e-6, "NELM": 3000, "ISPIN": ispin},
            user_kpoints_settings_optimization={"grid_density": 6000}
        )

        update_dict = {"material-id": mpid + '_' + str(ispin) + str("_ISMEAR_1")}
        wf = add_additional_fields_to_taskdocs(wf, update_dict=update_dict, task_name_constraint='VaspToDb')
        wf = add_additional_fields_to_taskdocs(wf, update_dict=update_dict, task_name_constraint='LobsterRunToDb')

        lpad = LaunchPad.auto_load()  # loads this based on the FireWorks configuration
        lpad.add_wf(wf)
# for ispin in [2]:
#     for mpid in [
#         "mp-568088"]:  # ["mp-568088","mp-830", "mp-1007824"]:#["mp-804","mp-2853"]:  # ["mp-22851","mp-560588","mp-22862", "mp-10695", "mp-5020", "mp-568088"]:
#         with MPRester("1x3FJCaLIf2s6nRc") as a:
#             structure = a.get_structure_by_material_id(mpid)
#
#         wf = get_wf_lobster_test_basis(
#             structure=structure,
#             user_kpoints_settings={"grid_density": 6000},
#             user_incar_settings={"LCHARG": False, "ISPIN": ispin, },
#             delete_all_wavecars=True,
#             additional_optimization=True,
#             user_incar_settings_optimization={"ISMEAR": 0, "EDIFFG": 1e-5, "EDIFF": 1e-6, "NELM": 3000, "ISPIN": ispin},
#             user_kpoints_settings_optimization={"grid_density": 6000}
#         )
#
#         update_dict = {"material-id": mpid + '_' + str(ispin) + str("_ISMEAR_1")}
#         wf = add_additional_fields_to_taskdocs(wf, update_dict=update_dict, task_name_constraint='VaspToDb')
#         wf = add_additional_fields_to_taskdocs(wf, update_dict=update_dict, task_name_constraint='LobsterRunToDb')
#
#         lpad = LaunchPad.auto_load()  # loads this based on the FireWorks configuration
#         lpad.add_wf(wf)


# for mpid in [
#     "mp-568088"]:  # ["mp-830","mp-1007824"]:#["mp-804","mp-2853"]:#["mp-41", "mp-131"]:  # ["mp-22851","mp-560588", "mp-22862", "mp-10695", "mp-5020", "mp-568088"]:
#     with MPRester("1x3FJCaLIf2s6nRc") as a:
#         structure = a.get_structure_by_material_id(mpid)
#
#     wf = get_wf_lobster_test_basis(
#         structure=structure,
#         user_kpoints_settings={"grid_density": 6000},
#         user_incar_settings={"LCHARG": False, "ISPIN": 1, "MAGMOM": None},
#         delete_all_wavecars=True,
#         additional_optimization=True,
#         user_incar_settings_optimization={"ISMEAR": 1, "EDIFFG": 1e-5, "EDIFF": 1e-6, "NELM": 3000},
#         user_kpoints_settings_optimization={"grid_density": 6000}
#     )
#
#     update_dict = {"material-id": mpid + '_' + "mixed" + str("_ISMEAR_1")}
#     wf = add_additional_fields_to_taskdocs(wf, update_dict=update_dict, task_name_constraint='VaspToDb')
#     wf = add_additional_fields_to_taskdocs(wf, update_dict=update_dict, task_name_constraint='LobsterRunToDb')
#
#     lpad = LaunchPad.auto_load()  # loads this based on the FireWorks configuration
#     lpad.add_wf(wf)
