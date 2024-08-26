import streamlit as st
import time
from datetime import datetime

# ---------- UI + Sidebar -------------

# Set the Streamlit page configuration
st.set_page_config(page_title="PERC Rule for Pulmonary Embolism")

# HU Style Config
with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

# USCDI v4 Sidebar Toggle
USCDI = st.sidebar.toggle("**USCDI v4**", value = True, help = "Toggle on to view the [USCDI v4](https://www.healthit.gov/isp/sites/isp/files/2023-10/USCDI-Version-4-October-2023-Errata-Final.pdf) calculator.")

# Title - Center
if USCDI == True:
    st.markdown("# PERC Rule for Pulmonary Embolism <small>\n**(LOINC: 89544-1)**</small>", unsafe_allow_html=True)
else:
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
<p>This app is designed to help healthcare professionals evaluate a patient's risk for pulmonary embolism (PE) using the PERC (Pulmonary Embolism Rule-out Criteria) rule. The app asks 8 questions, including age, heart rate, oxygen saturation, and past medical history. Each question is binary, and an answer of "No" is assigned a score of 0, and an answer of "Yes" is assigned a score of 1. If the answers to all 8 questions are "No" (total score of 0), the patient is considered to be at low risk for PE. If one or more answers is "Yes" (total score of >= 1), then further testing is indicated.</p>
""", unsafe_allow_html=True)
st.sidebar.divider()

# Display the logo + feedback
st.sidebar.image("HU_Logo.svg", use_column_width="auto")
st.sidebar.write("**We value your feedback!** Please share your comments in our [discussions](https://www.healthuniverse.com/apps/PERC%20Rule%20for%20Pulmonary%20Embolism/discussions).")

# ---------- Code -------------

st.divider()

# Age - UI

# Function to calculate age based on birthdate
def calculate_age_range(birthdate):
    birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

# Input for Date of Birth
current_date = datetime.today().strftime('%Y-%m-%d')

if USCDI == True:
    # Inject custom CSS to reduce the gap
    st.markdown(
        """
        <style>
        .stTextInput { margin-top: -50px; }  /* Adjust this value as needed */
        </style>
        """,
        unsafe_allow_html=True
    )
    # Display the label with smaller (loinc) text
    st.markdown(
        """
        <h5>Date of Birth <span style="font-size: smaller;">YYYY-MM-DD</span> <span style="font-size: x-small;">(LOINC: 30525-0)</span></h5>
        """, help="Known or estimated year, month, and day of the patient's birth.",
        unsafe_allow_html=True
    )

    birthday = st.text_input("", value=current_date)
else:
    birthday = st.text_input("##### Date of Birth (YYYY-MM-DD)", value=current_date)
# Validate date input
try:
    age = calculate_age_range(birthday)
except ValueError:
    st.error("Please enter a valid date in the format YYYY-MM-DD")
    st.stop()

# Classification based on age
if age >= 50:
    age_score = 1
else:
    age_score = 0

# Pulse Rate - UI

if USCDI == True:
    # Inject custom CSS to reduce the gap
    st.markdown(
        """
        <style>
        .stNumberInput { margin-top: -50px; }  /* Adjust this value as needed */
        </style>
        """,
        unsafe_allow_html=True
    )
    # Display the label with smaller (loinc) text
    st.markdown(
        """
        <h5>Heart Rate <span style="font-size: smaller;">{beats}/min</span> <span style="font-size: x-small;">(LOINC: 8867-4)</span></h5>
        """, help="Measured off of the pulse oximetry device or ECG monitor.",
        unsafe_allow_html=True
    )
    pr = st.number_input("", value=60, min_value=0, max_value=250, step=1)
else:
    pr = st.number_input("##### Heart Rate (beats/minute):", value=60, min_value=0, max_value=250, step=1, help="Measured off of the pulse oximetry device or ECG monitor")
if pr >= 100: # Classification
    pr_score = 1
else:
    pr_score = 0

# O2 Saturation - UI
if USCDI == True:
    
    # Inject custom CSS to reduce the gap
    st.markdown(
        """
        <style>
        .stNumberInput { margin-top: -50px; }  /* Adjust this value as needed */
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Display the label with smaller (loinc) text
    st.markdown(
        """
        <h5>Oxygen Saturation <span style="font-size: smaller;">%</span> <span style="font-size: x-small;">(LOINC: 2708-6)</span></h5>
        """, help="Room air pulse oximetry (%). Oximetry derived from dual wavelength (680/805 nm) measurement; probe on the fingertip or earlobe.",
        unsafe_allow_html=True
    )
    o2_sat = st.number_input("", value=95, min_value=0, max_value=100, step=1)

else:
    o2_sat = st.number_input("##### Oxygen Saturation (%):", value=95, min_value=0, max_value=100, step=1, help="Room air pulse oximetry (%). Oximetry derived from dual wavelength (680/805 nm) measurement; probe on the fingertip or earlobe.")
if o2_sat < 95: # Classification
    o2_score = 1
else:
    o2_score = 0

# Checkbox Instructions
if USCDI == True:
    st.markdown(
        """
        <h5>Check all that apply: <span style="font-size: x-small;">(LOINC: 56865-9)</span></h5>
        """,
        unsafe_allow_html=True
    )
else:
    st.write("##### Check all that apply:")
    
# Unilateral Leg Swelling - UI
if USCDI==True:
    unilat_leg_swelling = st.checkbox("**Unilateral Leg Swelling** (SCTID: 248480008)", help="Asymmetrical calfs when the legs are raised by the heels off of the bed by the examiner.")
else:
    unilat_leg_swelling = st.checkbox("**Unilateral Leg Swelling**", help="Asymmetrical calfs when the legs are raised by the heels off of the bed by the examiner.")
if unilat_leg_swelling: # Classification
    UniLeg_score = 1
else:
    UniLeg_score = 0

# Hemoptysis - UI
if USCDI==True:
    hemoptysis = st.checkbox("**Hemoptysis** (SCTID: 66857006)", help="Patient report of coughing up any blood in past week.")
else:
    hemoptysis = st.checkbox("**Hemoptysis**", help="Patient report of coughing up any blood in past week.")
if hemoptysis: # Classification
    hemo_score = 1
else:
    hemo_score = 0

# Recent surgery/trauma - UI
if USCDI==True:
    recent_surgery = st.checkbox("**Recent surgery/trauma** (SCTID: 257556004 | 417746004)", help="Either surgery or trauma requiring treatment with general anesthesia in the previous 4 weeks")
else:
    recent_surgery = st.checkbox("**Recent surgery/trauma**", help="Either surgery or trauma requiring treatment with general anesthesia in the previous 4 weeks")
if recent_surgery: # Classification
    RecentSorT_score = 1
else:
    RecentSorT_score = 0

# Hormone Medication Use - UI
if USCDI==True:
    hormone_use = st.checkbox("**Hormone Medication Use** (LOINC: LA29586-7)", help="Oral contraceptives, hormone replacement, or estrogenic hormones use in males or female patients.")
else:
    hormone_use = st.checkbox("**Hormone Medication Use**", help="Oral contraceptives, hormone replacement, or estrogenic hormones use in males or female patients.")
if hormone_use: # Classification
    hormone_score = 1
else:
    hormone_score = 0

# Previous history of PE or DVT - UI SCTID: 59282003
if USCDI==True:
    prev_pe_dvt = st.checkbox("**Previous history of PE or DVT** (SCTID: 161512007 | 161508001)", help="Personal history of pulmonary embolism (PE) or deep vein thrombosis (DVT) requiring treatment.")
else:
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
