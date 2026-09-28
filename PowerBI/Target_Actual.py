from pathlib import Path
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(r"C:\Devashish\Projects\Heat_Treatment_Dashboard")

DATA_PATH = (
    PROJECT_DIR
    / "data"
    / "aisi_4140_heat_treatment_dataset.csv"
)

MODEL_DIR = PROJECT_DIR / "models"

OUTPUT_PATH = (
    PROJECT_DIR
    / "results"
    / "ML_Actual_vs_Predicted.csv"
)

# Create results folder if it doesn't exist
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. LOAD DATA
# ============================================================

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)


# ============================================================
# 3. DEFINE INPUTS AND TARGETS
# ============================================================

INPUT_FEATURES = [
    "austenitizing_temp_C",
    "section_thickness_mm",
    "quench_medium",
    "tempering_temp_C",
    "tempering_time_hr"
]

TARGETS = [
    "hardness_HRC",
    "UTS_MPa",
    "YS_MPa",
    "elongation_pct",
    "reduction_of_area_pct"
]


# ============================================================
# 4. REMOVE MISSING VALUES
# ============================================================

required_columns = INPUT_FEATURES + TARGETS

df = df.dropna(subset=required_columns).copy()

print("Dataset after removing missing values:", df.shape)


# ============================================================
# 5. CREATE THE SAME TRAIN/TEST SPLIT
# ============================================================

X = df[INPUT_FEATURES]
y = df[TARGETS]

# IMPORTANT:
# Use the same random_state and test_size that you used
# during model evaluation.
#
# If your original training code used different values,
# change these two values accordingly.

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("Test set size:", len(X_test))


# ============================================================
# 6. LOAD TRAINED MODELS
# ============================================================

model_files = {
    "Hardness": "aisi4140_hardness_HRC_pipeline.pkl",
    "UTS": "aisi4140_UTS_MPa_pipeline.pkl",
    "Yield Strength": "aisi4140_YS_MPa_pipeline.pkl",
    "Elongation": "aisi4140_elongation_pct_pipeline.pkl",
    "Reduction of Area": "aisi4140_reduction_of_area_pct_pipeline.pkl"
}


# ============================================================
# 7. GENERATE ACTUAL VS PREDICTED VALUES
# ============================================================

results = []

for property_name, model_file in model_files.items():

    print(f"\nProcessing: {property_name}")

    model_path = MODEL_DIR / model_file

    # Load pipeline
    model = joblib.load(model_path)

    # --------------------------------------------------------
    # Select corresponding target
    # --------------------------------------------------------

    if property_name == "Hardness":
        target_column = "hardness_HRC"

    elif property_name == "UTS":
        target_column = "UTS_MPa"

    elif property_name == "Yield Strength":
        target_column = "YS_MPa"

    elif property_name == "Elongation":
        target_column = "elongation_pct"

    elif property_name == "Reduction of Area":
        target_column = "reduction_of_area_pct"

    # --------------------------------------------------------
    # Actual values
    # --------------------------------------------------------

    actual_values = y_test[target_column].values

    # --------------------------------------------------------
    # Predicted values
    # --------------------------------------------------------

    predicted_values = model.predict(X_test)

    # --------------------------------------------------------
    # Store results
    # --------------------------------------------------------

    for i in range(len(X_test)):

        results.append({
            "Sample_ID": i + 1,
            "Property": property_name,
            "Actual": actual_values[i],
            "Predicted": predicted_values[i]
        })


# ============================================================
# 8. CREATE FINAL DATAFRAME
# ============================================================

results_df = pd.DataFrame(results)


# ============================================================
# 9. SAVE CSV
# ============================================================

results_df.to_csv(
    OUTPUT_PATH,
    index=False
)


# ============================================================
# 10. DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 60)
print("ACTUAL VS PREDICTED DATASET CREATED")
print("=" * 60)

print("\nShape:")
print(results_df.shape)

print("\nRows per property:")
print(results_df["Property"].value_counts())

print("\nFirst 15 rows:")
print(results_df.head(15))

print("\nSaved to:")
print(OUTPUT_PATH)