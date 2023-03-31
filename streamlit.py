import streamlit as st

def calculate_perc(age, hr, o2_sat, unilat_leg_swelling, hemoptysis, recent_surgery, hormone_use, prev_pe_dvt):
    # Criteria for PERC
    criteria = [
        age <= 50,
        hr < 100,
        o2_sat >= 95,
        not unilat_leg_swelling,
        not hemoptysis,
        not recent_surgery,
        not hormone_use,
        not prev_pe_dvt
    ]
    # If all criteria are met, then PERC rule is negative
    return all(criteria)


st.title("PERC Rule for Pulmonary Embolism")

age = st.number_input("Age (years):", min_value=0, max_value=150, step=1)
hr = st.number_input("Heart Rate (beats per minute):", min_value=0, max_value=250, step=1)
o2_sat = st.number_input("Oxygen Saturation (%):", min_value=0, max_value=100, step=1)
unilat_leg_swelling = st.checkbox("Unilateral leg swelling?")
hemoptysis = st.checkbox("Hemoptysis (coughing up blood)?")
recent_surgery = st.checkbox("Recent surgery or trauma?")
hormone_use = st.checkbox("Hormone use (oral contraceptives, hormone replacement therapy)?")
prev_pe_dvt = st.checkbox("Previous history of PE or DVT?")

if st.button("Calculate PERC Rule"):
    result = calculate_perc(age, hr, o2_sat, unilat_leg_swelling, hemoptysis, recent_surgery, hormone_use, prev_pe_dvt)
    if result:
        st.success("PERC rule is negative. Low risk for pulmonary embolism.")
    else:
        st.warning("PERC rule is positive. Further evaluation may be needed.")

