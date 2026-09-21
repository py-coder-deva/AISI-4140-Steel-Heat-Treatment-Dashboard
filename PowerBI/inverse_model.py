# ============================================================
# AISI 4140 Heat Treatment - Inverse ML Model
# Power BI Integration Module
# ============================================================

from pathlib import Path

import os
import sys
import joblib
import numpy as np
import pandas as pd

from scipy.optimize import differential_evolution


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from tempering_transformers import (
    TemperingParameterTransformer,
    YSTemperingParameterTransformer
)

# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(
    r"C:\Devashish\Projects\Heat_Treatment_Dashboard"
)

MODEL_DIR = PROJECT_DIR / "models"


# ============================================================
# 2. MODEL FILES
# ============================================================

MODEL_FILES = {

    "hardness_HRC":
        "aisi4140_hardness_HRC_pipeline.pkl",

    "UTS_MPa":
        "aisi4140_UTS_MPa_pipeline.pkl",

    "YS_MPa":
        "aisi4140_YS_MPa_pipeline.pkl",

    "elongation_pct":
        "aisi4140_elongation_pct_pipeline.pkl",

    "reduction_of_area_pct":
        "aisi4140_reduction_of_area_pct_pipeline.pkl",
}


# ============================================================
# 3. PROCESS VARIABLE RANGES
# ============================================================

AUSTENITIZING_RANGE = (
    828,
    872
)

TEMPERING_TEMP_RANGE = (
    200,
    815
)

TEMPERING_TIME_RANGE = (
    0.5,
    4.0
)


QUENCH_MEDIA = [
    "air",
    "oil",
    "water"
]


# ============================================================
# 4. LOAD TRAINED PIPELINES
# ============================================================

def load_pipelines():

    pipelines = {}

    for target, filename in MODEL_FILES.items():

        model_path = MODEL_DIR / filename

        if not model_path.exists():

            raise FileNotFoundError(
                f"Model file not found:\n{model_path}"
            )

        pipelines[target] = joblib.load(
            model_path
        )

    return pipelines


# Load all models when this module is imported
pipelines = load_pipelines()


# ============================================================
# 5. FEATURE ENGINEERING
# ============================================================

def prepare_features(input_data):

    """
    Create engineered features required by
    the trained ML pipelines.

    Engineered features:

    1. tempering_parameter
    2. temperature_temp_time

    Note:
    temperature_temp_time is only used by the
    YS model.
    """

    input_data = input_data.copy()

    # --------------------------------------------------------
    # Tempering Parameter
    # --------------------------------------------------------

    input_data["tempering_parameter"] = (

        (input_data["tempering_temp_C"] + 273.15)

        * (

            20
            + np.log10(
                input_data["tempering_time_hr"]
            )

        )

    )

    # --------------------------------------------------------
    # Tempering Temperature × Time
    # --------------------------------------------------------

    input_data["temperature_temp_time"] = (

        input_data["tempering_temp_C"]
        *
        input_data["tempering_time_hr"]

    )

    return input_data


# ============================================================
# 6. FORWARD PREDICTION
# ============================================================

def predict_properties(
    austenitizing_temp_C,
    section_thickness_mm,
    quench_medium,
    tempering_temp_C,
    tempering_time_hr
):

    """
    Predict all five mechanical properties
    for a given heat-treatment condition.
    """

    # --------------------------------------------------------
    # Create input DataFrame
    # --------------------------------------------------------

    input_data = pd.DataFrame({

        "austenitizing_temp_C": [
            austenitizing_temp_C
        ],

        "section_thickness_mm": [
            section_thickness_mm
        ],

        "quench_medium": [
            quench_medium
        ],

        "tempering_temp_C": [
            tempering_temp_C
        ],

        "tempering_time_hr": [
            tempering_time_hr
        ]

    })


    # --------------------------------------------------------
    # Feature Engineering
    # --------------------------------------------------------

    input_data = prepare_features(
        input_data
    )


    # --------------------------------------------------------
    # Predict Each Property
    # --------------------------------------------------------

    predictions = {}


    for target, pipeline in pipelines.items():

        # ----------------------------------------------------
        # YS model requires both engineered features
        # ----------------------------------------------------

        if target == "YS_MPa":

            model_input = input_data


        # ----------------------------------------------------
        # Other models only require tempering_parameter
        # and original input features
        # ----------------------------------------------------

        else:

            model_input = input_data.drop(
                columns=[
                    "temperature_temp_time"
                ]
            )


        # ----------------------------------------------------
        # Prediction
        # ----------------------------------------------------

        predictions[target] = pipeline.predict(
            model_input
        )[0]


    return predictions


# ============================================================
# 7. NORMALIZED ERROR FUNCTION
# ============================================================

def normalized_error(
    predictions,
    targets
):

    """
    Calculate normalized error between
    predicted and desired properties.

    Each property is normalized by the
    magnitude of its target value so that
    properties with different units can be
    compared in the optimization objective.
    """

    errors = []

    for key in targets:

        prediction = predictions[key]

        target = targets[key]

        error = (
            (prediction - target)
            / target
        )

        errors.append(
            error ** 2
        )


    return np.mean(errors)


# ============================================================
# 8. INVERSE OPTIMIZATION OBJECTIVE
# ============================================================

def inverse_objective(
    x,
    section_thickness,
    quench_medium,
    target_properties
):

    """
    Objective function used by the optimizer.

    Optimized variables:

    1. Austenitizing temperature
    2. Tempering temperature
    3. Tempering time

    Section thickness is kept fixed because
    it is a component/material input rather
    than a heat-treatment parameter.

    Quench medium is evaluated separately.
    """

    (
        austenitizing_temp,
        tempering_temp,
        tempering_time
    ) = x


    # --------------------------------------------------------
    # Forward prediction
    # --------------------------------------------------------

    predictions = predict_properties(

        austenitizing_temp_C=
            austenitizing_temp,

        section_thickness_mm=
            section_thickness,

        quench_medium=
            quench_medium,

        tempering_temp_C=
            tempering_temp,

        tempering_time_hr=
            tempering_time

    )


    # --------------------------------------------------------
    # Calculate normalized objective error
    # --------------------------------------------------------

    return normalized_error(
        predictions,
        target_properties
    )


# ============================================================
# 9. FIND OPTIMAL HEAT-TREATMENT CONDITIONS
# ============================================================

def find_heat_treatment(
    target_properties,
    section_thickness,
    maxiter=100,
    popsize=10
):

    """
    Find heat-treatment conditions that attempt
    to achieve the desired mechanical properties.

    The optimizer searches:

        Austenitizing Temperature
        Tempering Temperature
        Tempering Time

    for each quench medium:

        Air
        Oil
        Water

    Section thickness is fixed by the user.
    """

    results = []


    # --------------------------------------------------------
    # Optimization bounds
    # --------------------------------------------------------

    bounds = [

        AUSTENITIZING_RANGE,

        TEMPERING_TEMP_RANGE,

        TEMPERING_TIME_RANGE

    ]


    # ========================================================
    # Run Optimization for Each Quench Medium
    # ========================================================

    for quench_medium in QUENCH_MEDIA:

        print(
            f"Searching for quench medium: "
            f"{quench_medium}"
        )


        # ----------------------------------------------------
        # Differential Evolution
        # ----------------------------------------------------

        result = differential_evolution(

            inverse_objective,

            bounds=bounds,

            args=(

                section_thickness,

                quench_medium,

                target_properties

            ),

            maxiter=maxiter,

            popsize=popsize,

            seed=42,

            polish=True

        )


        # ----------------------------------------------------
        # Extract optimized variables
        # ----------------------------------------------------

        (
            austenitizing_temp,
            tempering_temp,
            tempering_time
        ) = result.x


        # ----------------------------------------------------
        # Predict properties using optimized condition
        # ----------------------------------------------------

        predictions = predict_properties(

            austenitizing_temp_C=
                austenitizing_temp,

            section_thickness_mm=
                section_thickness,

            quench_medium=
                quench_medium,

            tempering_temp_C=
                tempering_temp,

            tempering_time_hr=
                tempering_time

        )


        # ----------------------------------------------------
        # Store result
        # ----------------------------------------------------

        results.append({

            "austenitizing_temp_C":
                austenitizing_temp,

            "section_thickness_mm":
                section_thickness,

            "quench_medium":
                quench_medium,

            "tempering_temp_C":
                tempering_temp,

            "tempering_time_hr":
                tempering_time,

            "objective_error":
                result.fun,

            **predictions

        })


    # ========================================================
    # Convert Results to DataFrame
    # ========================================================

    results_df = pd.DataFrame(
        results
    )


    # ========================================================
    # Sort by Objective Error
    # ========================================================

    results_df = results_df.sort_values(

        "objective_error"

    ).reset_index(
        drop=True
    )


    return results_df


# ============================================================
# 10. POWER BI INPUT VALIDATION
# ============================================================

def validate_powerbi_input(
    dataset
):

    """
    Validate the input DataFrame received
    from Power BI.
    """

    required_columns = [

        "hardness_HRC",

        "UTS_MPa",

        "YS_MPa",

        "elongation_pct",

        "reduction_of_area_pct",

        "section_thickness_mm"

    ]


    # --------------------------------------------------------
    # Check required columns
    # --------------------------------------------------------

    missing_columns = [

        column

        for column in required_columns

        if column not in dataset.columns

    ]


    if missing_columns:

        raise ValueError(

            "Missing required Power BI columns: "

            + ", ".join(
                missing_columns
            )

        )


    # --------------------------------------------------------
    # Check that at least one row exists
    # --------------------------------------------------------

    if len(dataset) == 0:

        raise ValueError(
            "Power BI input table is empty."
        )


    # --------------------------------------------------------
    # Use first row
    # --------------------------------------------------------

    dataset = dataset.iloc[
        [0]
    ].copy()


    # --------------------------------------------------------
    # Convert numerical columns
    # --------------------------------------------------------

    numeric_columns = [

        "hardness_HRC",

        "UTS_MPa",

        "YS_MPa",

        "elongation_pct",

        "reduction_of_area_pct",

        "section_thickness_mm"

    ]


    for column in numeric_columns:

        dataset[column] = pd.to_numeric(

            dataset[column],

            errors="raise"

        )


    # --------------------------------------------------------
    # Check positive target values
    # --------------------------------------------------------

    target_columns = [

        "hardness_HRC",

        "UTS_MPa",

        "YS_MPa",

        "elongation_pct",

        "reduction_of_area_pct"

    ]


    for column in target_columns:

        if dataset[column].iloc[0] <= 0:

            raise ValueError(

                f"{column} must be greater than zero."

            )


    # --------------------------------------------------------
    # Check positive section thickness
    # --------------------------------------------------------

    if dataset[
        "section_thickness_mm"
    ].iloc[0] <= 0:

        raise ValueError(

            "section_thickness_mm "
            "must be greater than zero."

        )


    return dataset


# ============================================================
# END OF MODULE
# ============================================================