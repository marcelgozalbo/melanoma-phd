import os
import sys

import streamlit as st

# workaround for Streamlit Cloud for importing `melanoma_phd` module correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from streamlit_app.AppLoader import AppLoader, create_database_section, select_filters, select_variables, download_statistics, plot_figures, plot_statistics  # isort: skip <- Force to be after workaround
from melanoma_phd.database.Correlationer import Correlationer
from melanoma_phd.database.filter.PatientDataFilterer import \
    PatientDataFilterer  # isort: skip <- Force to be after workaround
from melanoma_phd.database.IndependenceTester import IndependenceTester
from melanoma_phd.database.variable.BooleanVariable import BooleanVariable
from melanoma_phd.database.variable.CategoricalVariable import CategoricalVariable
from melanoma_phd.database.variable.ScalarVariable import ScalarVariable

if __name__ == "__main__":
    st.set_page_config(page_title="Melanoma PHD Statistics", layout="wide")
    st.title("Correlation and Independence Tests")
    with AppLoader() as app:
        create_database_section(app)

        filters = select_filters(app)
        st.subheader("Filtered data")
        with st.expander(f"Filtered dataframe"):
            df_result = PatientDataFilterer().filter(app.database, filters)
            st.text(f"{len(df_result.index)} patients match with selected filters")
            st.dataframe(df_result)

        st.subheader("Variable selection")
        selected_variables = select_variables(
            app,
            variable_types=[
                ScalarVariable,
                CategoricalVariable,
                BooleanVariable,
            ],
        )

        normality_null_hypothesis = st.number_input(
            "Normality null hypotesis", min_value=0, max_value=1, step=0.01, value=0.05
        )
        homogeneity_null_hypothesis = st.number_input(
            "Homogeneity null hypotesis", min_value=0, max_value=1, step=0.01, value=0.05
        )
        if selected_variables:
            st.header("Independence Tests (p-value)")
            independence_tester = IndependenceTester(normality_null_hypothesis=normality_null_hypothesis, homogeneity_null_hypothesis=homogeneity_null_hypothesis)
            independence_table = independence_tester.table(df_result, selected_variables)
            st.dataframe(independence_table)

            correlationer = Correlationer(normality_null_hypothesis=normality_null_hypothesis, homogeneity_null_hypothesis=homogeneity_null_hypothesis)
            correlation_table = correlationer.table(df_result, selected_variables)
            st.dataframe(correlation_table)
        else:
            st.text("Select variables to analyze :)")