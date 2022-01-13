from atomate.vasp.powerups import add_additional_fields_to_taskdocs
from atomate.vasp.workflows.base.lobster import get_wf_lobster_test_basis
from fireworks import LaunchPad
from pymatgen.ext.matproj import MPRester


for mpid in ["mp-568088", "mp-22851", "mp-22862", "mp-804", "mp-83", "mp-2853", "mp-1007824"]:
    with MPRester() as a:
        structure = a.get_structure_by_material_id(mpid)

    wf = get_wf_lobster_test_basis(
        structure=structure,
        user_kpoints_settings={"grid_density": 6000},
        user_incar_settings={"LCHARG": False, "ISPIN": 0, "MAGMOM": None},
        delete_all_wavecars=True,
        additional_optimization=True,
        user_incar_settings_optimization={"ISMEAR": 0, "EDIFFG": 1e-5, "EDIFF": 1e-6, "NELM": 3000, "ISPIN": 1,
                                          "MAGMOM": None},
        user_kpoints_settings_optimization={"grid_density": 6000}
    )

    update_dict = {"material-id": mpid + '_' + str(1) }
    wf = add_additional_fields_to_taskdocs(wf, update_dict=update_dict, task_name_constraint='VaspToDb')
    wf = add_additional_fields_to_taskdocs(wf, update_dict=update_dict, task_name_constraint='LobsterRunToDb')

    lpad = LaunchPad.auto_load()  # loads this based on the FireWorks configuration
    lpad.add_wf(wf)

for mpid in [
    "mp-568088", "mp-22851", "mp-22862", "mp-804", "mp-83", "mp-2853", "mp-1007824"]:
    with MPRester() as a:
        structure = a.get_structure_by_material_id(mpid)

    wf = get_wf_lobster_test_basis(
        structure=structure,
        user_kpoints_settings={"grid_density": 6000},
        user_incar_settings={"LCHARG": False, "ISPIN": 2},
        delete_all_wavecars=True,
        additional_optimization=True,
        user_incar_settings_optimization={"ISMEAR": 0, "EDIFFG": 1e-5, "EDIFF": 1e-6, "NELM": 3000, "ISPIN": 2},
        user_kpoints_settings_optimization={"grid_density": 6000}
    )

    update_dict = {"material-id": mpid + '_' + str(2) }
    wf = add_additional_fields_to_taskdocs(wf, update_dict=update_dict, task_name_constraint='VaspToDb')
    wf = add_additional_fields_to_taskdocs(wf, update_dict=update_dict, task_name_constraint='LobsterRunToDb')

    lpad = LaunchPad.auto_load()  # loads this based on the FireWorks configuration
    lpad.add_wf(wf)

# start mixed spin calculation for 14-1-11
for mpid in ["mp-568088"]:
    with MPRester("1x3FJCaLIf2s6nRc") as a:
        structure = a.get_structure_by_material_id(mpid)

    wf = get_wf_lobster_test_basis(
        structure=structure,
        user_kpoints_settings={"grid_density": 6000},
        user_incar_settings={"LCHARG": False, "ISPIN": 1, "MAGMOM": None},
        delete_all_wavecars=True,
        additional_optimization=True,
        user_incar_settings_optimization={"ISMEAR": 0, "EDIFFG": 1e-5, "EDIFF": 1e-6, "NELM": 3000},
        user_kpoints_settings_optimization={"grid_density": 6000}
    )

    update_dict = {"material-id": mpid + '_' + "mixed"}
    wf = add_additional_fields_to_taskdocs(wf, update_dict=update_dict, task_name_constraint='VaspToDb')
    wf = add_additional_fields_to_taskdocs(wf, update_dict=update_dict, task_name_constraint='LobsterRunToDb')

    lpad = LaunchPad.auto_load()  # loads this based on the FireWorks configuration
    lpad.add_wf(wf)

