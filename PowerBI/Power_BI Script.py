import sys
import os
import pandas as pd

# ============================================================
# 1. POWER BI PROJECT DIRECTORY
# ============================================================

POWERBI_DIR = r"C:\Devashish\Projects\Heat_Treatment_Dashboard"

if POWERBI_DIR not in sys.path:
    sys.path.insert(0, POWERBI_DIR)

# PowerBI Python module directory
MODULE_DIR = os.path.join(
    POWERBI_DIR,
    "PowerBI"
)

if MODULE_DIR not in sys.path:
    sys.path.insert(0, MODULE_DIR)


# ============================================================
# 2. IMPORT INVERSE MODEL
# ============================================================

try:

    import inverse_model

    # ========================================================
    # 3. TEST TARGET PROPERTIES
    # ========================================================

    target_properties = {

        "hardness_HRC": 40.0,

        "UTS_MPa": 1300.0,

        "YS_MPa": 1100.0,

        "elongation_pct": 12.0,

        "reduction_of_area_pct": 40.0

    }

    # ========================================================
    # 4. TEST SECTION THICKNESS
    # ========================================================

    section_thickness = 50.0


    # ========================================================
    # 5. RUN INVERSE OPTIMIZATION
    # ========================================================

    results = inverse_model.find_heat_treatment(

        target_properties=target_properties,

        section_thickness=section_thickness,

        maxiter=20,

        popsize=5

    )


    # ========================================================
    # 6. RETURN RESULTS TO POWER BI
    # ========================================================

    dataset = results


except Exception as e:

    dataset = pd.DataFrame({

        "Status": ["ERROR"],

        "Message": [str(e)]

    })