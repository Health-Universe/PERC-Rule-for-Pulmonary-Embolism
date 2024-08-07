import streamlit as st
import time

# ---------- UI + Sidebar -------------

# Set the Streamlit page configuration
st.set_page_config(page_title="PERC Rule for Pulmonary Embolism")

# HU Style Config
with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

# Title - Center
st.title("PERC Rule for Pulmonary Embolism")

# Expanders for instructions + disclaimer
with st.expander("**Instructions**"):
    st.write("""This app is designed to calculate if a patient meets the PERC criteria. Please provide the requested information below to determine if the PERC rule can be used to rule out a pulmonary embolism (PE).""")

with st.expander("**Disclaimer**"):
    st.write("""
    This tool is for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified healthcare provider with any questions you may have regarding a medical condition.
    """)

# Paper + Evaluation + Sidebar Overview Info
st.sidebar.markdown("""
<h2 style='color: black; margin-bottom: 0; font-size: 1em;'>Overview</h2>
<a href="https://pubmed.ncbi.nlm.nih.gov/15304025/" target="_blank";"><strong>Paper</strong></a> |
<a href="https://pubmed.ncbi.nlm.nih.gov/18318689/" target="_blank";"><strong>Validation</strong></a>
<p>   </p>
<p>This app is designed to help healthcare professionals evaluate a patient's risk for pulmonary embolism (PE) using the PERC (Pulmonary Embolism Rule-out Criteria) rule. By inputting specific patient data such as age, pulse rate, oxygen saturation, and checking for relevant clinical conditions, the app calculates whether the patient meets the PERC criteria, indicating whether further evaluation for PE is necessary.</p>
""", unsafe_allow_html=True)
st.sidebar.divider()

# Display the logo + feedback
st.sidebar.image("HU_Logo.svg", use_column_width="auto")
st.sidebar.write("**We value your feedback!** Please share your comments in our [discussions](https://healthuniverse.com).")

# ---------- Code -------------

st.divider()

# Age - UI
age = st.number_input("##### Age (years):", min_value=0, max_value=150, step=1)
if age >= 50: # Classification
    age_score = 1
else:
    age_score = 0

# Pulse Rate - UI
pr = st.number_input("##### Pulse Rate (beats/minute):", min_value=0, max_value=250, step=1, help="Measured off of the pulse oximetry device or ECG monitor")
if pr >= 100: # Classification
    pr_score = 1
else:
    pr_score = 0

# O2 Saturation - UI
o2_sat = st.number_input("##### Oxygen Saturation (%):", min_value=0, max_value=100, step=1, help="Room air pulse oximetry (%). Oximetry derived from dual wavelength (680/805 nm) measurement; probe on the fingertip or earlobe.")
if o2_sat < 95: # Classification
    o2_score = 1
else:
    o2_score = 0

# Checkbox Instructions
st.write("##### Check all that apply:")

# Unilateral Leg Swelling - UI
unilat_leg_swelling = st.checkbox("**Unilateral Leg Swelling**", help="Asymmetrical calfs when the legs are raised by the heels off of the bed by the examiner.")
if unilat_leg_swelling: # Classification
    UniLeg_score = 1
else:
    UniLeg_score = 0

# Hemoptysis - UI
hemoptysis = st.checkbox("**Hemoptysis**", help="Patient report of coughing up any blood in past week.")
if hemoptysis: # Classification
    hemo_score = 1
else:
    hemo_score = 0

# Recent surgery/trauma - UI
recent_surgery = st.checkbox("**Recent surgery/trauma**", help="Either surgery or trauma requiring treatment with general anesthesia in the previous 4 weeks")
if recent_surgery: # Classification
    RecentSorT_score = 1
else:
    RecentSorT_score = 0

# Hormone Medication Use - UI
hormone_use = st.checkbox("**Hormone Medication Use**", help="Oral contraceptives, hormone replacement, or estrogenic hormones use in males or female patients.")
if hormone_use: # Classification
    hormone_score = 1
else:
    hormone_score = 0

# Previous history of PE or DVT - UI
prev_pe_dvt = st.checkbox("**Previous history of PE or DVT**", help="Personal history of pulmonary embolism (PE) or deep vein thrombosis (DVT) requiring treatment.")
if prev_pe_dvt: # Classification
    PEorDVT_score = 1
else:
    PEorDVT_score = 0

# Calculator
total_score = age_score + pr_score + o2_score + UniLeg_score + hemo_score + RecentSorT_score + hormone_score + PEorDVT_score

if st.button("Calculate"):
    # Spinner to delay
    with st.spinner("Calculating..."):
        time.sleep(1)  # Simulate a delay
    st.divider()
    st.write("##### Results:")
    if total_score == 0:
        risk=("PERC rule is **negative**. No criteria met, indicating low risk for pulmonary embolism.")
        final = f"""**Criteria Met:** {total_score}

        \n {risk}"""
        st.success(final)
    else:
        risk=("PERC rule is **positive**. PERC cannot be used to rule out pulmonary embolism. Further evaluation may be necessary.".format(total_score))
        final = f"""**Criteria Met:** {total_score}

        \n {risk}"""
        st.warning(final)
