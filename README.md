# Machine Learning-Based Inverse Heat Treatment Design for AISI 4140 Steel

An integrated **Machine Learning + Metallurgical Engineering + Power BI** project that uses inverse optimization to identify suitable heat-treatment parameters for AISI 4140 steel based on desired mechanical properties.

---

## 1. Project Overview

Heat treatment plays a critical role in determining the mechanical properties and performance of steel components. Parameters such as austenitizing temperature, quenching medium, tempering temperature and tempering duration directly influence the resulting mechanical properties.

In conventional heat-treatment design, engineers generally select process parameters and then evaluate the resulting material properties.

This project explores the reverse approach.

A user specifies the desired mechanical properties of AISI 4140 steel, and the system uses machine learning models and gradient-descent-based inverse optimization to identify suitable heat-treatment process parameters.

The optimized parameters are subsequently used to generate a temperature-time heat-treatment cycle, which is visualized through an interactive Power BI dashboard.

## 2. Project Objectives

- Develop machine learning models to establish process-property relationships for AISI 4140 steel.
- Implement inverse optimization to identify heat-treatment conditions corresponding to desired mechanical properties.
- Apply gradient descent to optimize process parameters against target mechanical properties.
- Generate heat-treatment process cycles using the optimized parameters.
- Integrate Python-based machine learning with Microsoft Power BI.
- Evaluate model performance using regression metrics and actual-versus-predicted visualizations.

## 3. System Architecture and Methodology

The project consists of two interconnected stages.

### Stage 1: Machine Learning Model Development

A synthetic dataset containing approximately 1,100 observations and 11 variables is used to develop regression models.

The models establish relationships between heat-treatment parameters and mechanical properties.

**Input process parameters:**
- Austenitizing temperature (°C)
- Section thickness (mm)
- Quenching medium
- Tempering temperature (°C)
- Tempering time (hours)

**Predicted mechanical properties:**
- Hardness (HRC)
- Ultimate Tensile Strength (MPa)
- Yield Strength (MPa)
- Elongation (%)
- Reduction of Area (%)

### Stage 2: Inverse Heat Treatment Optimization

Instead of directly predicting mechanical properties from process parameters, the system uses the trained predictive models within an inverse optimization framework.

The workflow is:

1. User specifies the desired mechanical properties.
2. Initial heat-treatment parameters are selected.
3. The trained machine learning models estimate the resulting mechanical properties.
4. Prediction errors relative to the target properties are evaluated.
5. Gradient descent iteratively updates the process parameters.
6. The optimized parameters are used to construct a heat-treatment process cycle.

The objective is to minimize the difference between desired and model-predicted mechanical properties.

## 4. Machine Learning Models and Performance

Gradient Boosting and tuned Gradient Boosting regression models are used for predicting the mechanical properties.

### Model Evaluation Results

| Property | Model | MAE | RMSE | R² |
|---|---|---:|---:|---:|
| Hardness (HRC) | Gradient Boosting | 0.6309 | 0.8241 | 0.9945 |
| UTS (MPa) | Gradient Boosting | 31.4622 | 40.9953 | 0.9854 |
| Elongation (%) | Tuned Gradient Boosting | 0.9471 | 1.2141 | 0.9411 |
| Reduction of Area (%) | Tuned Gradient Boosting | 1.9396 | 2.5020 | 0.9308 |
| Yield Strength (MPa) | Tuned Gradient Boosting | 27.3791 | 37.7089 | 0.9890 |

**Evaluation metrics:**
- MAE: Mean Absolute Error
- RMSE: Root Mean Squared Error
- R²: Coefficient of Determination

The results indicate strong predictive performance across the five mechanical properties within the synthetic dataset.

## 5. Power BI Dashboard

The project includes two interactive Power BI dashboards.

### A. Inverse Heat Treatment Process Cycle Dashboard

The dashboard allows users to specify target mechanical properties and section thickness.

The system displays:
- Target mechanical properties.
- Selected quenching medium (Air, Oil or Water).
- Optimized austenitizing temperature.
- Optimized tempering temperature.
- Optimized tempering duration.
- Generated temperature-time process cycle.
- Target-versus-predicted mechanical property comparison.

### B. Machine Learning Model Performance Dashboard

This dashboard provides an overview of model performance and the inverse optimization workflow.

It includes:
- R² comparison across mechanical properties.
- MAE and RMSE comparisons.
- Model evaluation metrics.
- Actual-versus-predicted scatter plots.
- Machine learning and inverse optimization workflow.

## 6. Example Heat Treatment Design

An example dashboard configuration uses the following target properties:

| Target property | Value |
|---|---:|
| Elongation | 12% |
| Hardness | 40 HRC |
| Section Thickness | 50 mm |
| Reduction of Area | 35% |
| UTS | 1300 MPa |
| Yield Strength | 1100 MPa |

The displayed optimized process parameters are:

| Process parameter | Optimized value |
|---|---:|
| Austenitizing Temperature | 828.07 °C |
| Tempering Temperature | 350.87 °C |
| Tempering Time | 1.50 hours |
| Quenching Medium | Water |

The dashboard subsequently generates the corresponding temperature-time heat-treatment cycle.

*These values are an illustrative model-generated design, not experimentally validated production recommendations.*

## 7. Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Data Processing | NumPy, Pandas |
| Machine Learning | Scikit-learn |
| Optimization | Gradient Descent |
| Data Visualization | Matplotlib |
| Business Intelligence | Microsoft Power BI |
| Data Transformation | Power Query |

## 8. Project Workflow

```text
       Synthetic Dataset
               |
               v
       Data Preprocessing
               |
               v
        Feature Engineering
               |
               v
      ML Regression Models
               |
               v
       Model Evaluation
               |
               v
       User Target Properties
               |
               v
      Inverse Optimization
        (Gradient Descent)
               |
               v
    Optimized Process Parameters
               |
               v
     Heat Treatment Cycle
               |
               v
       Power BI Dashboard
```

## 9. Engineering Significance

This project demonstrates an application of machine learning in metallurgical process design.

The primary focus is on connecting material-property requirements with manufacturing process parameters.

By combining regression models, inverse optimization and interactive visualization, the project explores a data-driven approach to heat-treatment design.

It also demonstrates how machine learning can complement conventional metallurgical engineering workflows by helping engineers explore possible processing conditions before experimental validation.

## 10. Limitations

- The current dataset is synthetic and does not replace experimental or industrial validation.
- Model performance on synthetic data does not guarantee equivalent performance on real steel components.
- Optimized parameters should be checked against metallurgical constraints, phase transformations, component geometry and industrial processing limitations.
- The generated process cycles represent model-based recommendations rather than certified industrial heat-treatment procedures.

## 11. Future Scope

- Incorporate experimental heat-treatment datasets.
- Integrate physical metallurgy constraints into the optimization framework.
- Explore physics-informed machine learning.
- Incorporate microstructural characteristics such as martensite fraction and carbide distribution.
- Extend the framework to other alloy steel grades.
- Develop a more comprehensive multi-objective optimization framework.

## 12. Author

**Devashish Prasad**

Metallurgical Engineering | Machine Learning | Computational Materials Science

GitHub: [py-coder-deva](https://github.com/py-coder-deva)

---

*This project explores the integration of machine learning and inverse optimization for metallurgical process design.*
