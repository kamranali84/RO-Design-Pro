##############################################################
#Top of File
# ###################################################
import streamlit as st
import math
import pandas as pd
import numpy as np

from io import BytesIO
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


st.set_page_config(
    page_title="RO Design Pro",
    page_icon="💧",
    layout="wide"
)
####################################################
#Box size reduction
##########################################
st.markdown("""
<style>

/* Reduce width of Number Inputs */

div[data-testid="stNumberInput"] {
    max-width: 180px !important;
}

/* Reduce width of Select Boxes */

div[data-testid="stSelectbox"] {
    max-width: 180px !important;
}

/* Center value */

div[data-testid="stNumberInput"] input {
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

###########################################################################
#box closer
###########################################################################

st.markdown("""
<style>

.main .block-container {
    max-width: 1100px;
    padding-top: 1rem;
    padding-bottom: 1rem;
}

</style>
""", unsafe_allow_html=True)
#################################################################################################################
# =====================================================
# SESSION DEFAULTS
# =====================================================


defaults = {

    # Feed Water Analysis

    "ca": 0.0,
    "mg": 0.0,
    "na": 0.0,
    "k": 0.0,

    "ba": 0.0,
    "sr": 0.0,

    "hco3": 0.0,
    "co3": 0.0,
    "so4": 0.0,
    "cl": 0.0,
    "no3": 0.0,

    "fluoride": 0.0,

    "silica": 0.0,
    "boron": 0.0,

    "iron": 0.0,
    "manganese": 0.0,
    "co2":0.0,


    "temperature": 25.0,
    "feed_ph": 7.0,

    # Calculated Values
    "calculated_tds": 0.0,
    "hardness": 0.0,
    "conductivity": 0.0,
    "feed_op": 0.0,
    "alkalinity": 0.0,

    # ==================================
    # RO DESIGN
    # ==================================

    "ro_feed": 50.0,
    "ro_permeate": 37.5,
    "ro_concentrate": 12.5,

    "pass1_recovery": 75.0,
    "pass1_permeate_flow": 50.0,

    "passes": 1,

    "pass1_stages": 3,
    "pass2_stages": 2,

    # Stage 1
    "stage1_elements": 6,
    "stage1_vessels": 6,

    # Stage 2
    "stage2_elements": 6,
    "stage2_vessels": 3,

    # Stage 3
    "stage3_elements": 6,
    "stage3_vessels": 2,

    # Pass 2
    "pass2_recovery": 85.0,

    "pass2_stage1_elements": 6,
    "pass2_stage1_vessels": 4,

    "pass2_stage2_elements": 6,
    "pass2_stage2_vessels": 2,

    "pass2_stage3_elements": 6,
    "pass2_stage3_vessels": 1,

    # ==================================
    # WATER TYPE
    # ==================================

    "water_type": "Municipal Water",

    # ==================================
    # MEMBRANE
    # ==================================
    "membrane_model": "BW30-400",
    "membrane_area": 400.0,
    "membrane_flow": 10500.0,
    "membrane_rejection": 99.5,

    "pass1_feed_ph": 7.0,
    "pass2_feed_ph": 8.2,

    "smbs_free_chlorine": 1.0,
    "smbs_dose": 0.0,
    "smbs_kg_day": 0.0,

    "acid_dose": 0.0,
    "naoh_dose": 0.0,
    "boron_rejection": 0.0,
    "permeate_boron": 0.0,
    "naoh_kg_day": 0.0,


    "selected_chemical": "H2SO4",
    "chemical_strength": 98.0,
    "target_ph": 6.5,
    "chemical_dose": 0.0,
    "chemical_kg_hr": 0.0,
    "chemical_kg_day": 0.0,
    "chemical_lph": 0.0,
    "chemical_day_tank": 0.0,

    #Antiscalant

    "selected_antiscalant": "Vitec 3000",
    "antiscalant_vendor": "",
    "antiscalant_application": "",
    "antiscalant_dose": 0.0,
    "antiscalant_kg_day": 0.0,




}

for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value
######################################################################################################################
#if "ca" not in st.session_state:
    #st.session_state["ca"] = 0.0

#if "mg" not in st.session_state:
    #st.session_state["mg"] = 0.0

#if "na" not in st.session_state:
    #st.session_state["na"] = 0.0

#if "pass1_feed_flow" not in st.session_state:
    #st.session_state["pass1_feed_flow"] = 50.0

#if "pass1_recovery" not in st.session_state:
    #st.session_state["pass1_recovery"] = 75.0#

####################################################################
#SIDE BAR
####################################################################

page = st.sidebar.selectbox(
    "Select Module",
    [
        "🏠 Dashboard",
        "💧 Feed Water Analysis",
        "⚡ Conductivity",
        "📈 RO Design",
        "🧪 Chemical Dosing",
        "🌊 Hydraulic & Energy",
        "✅ Treated Water Quality",
        "📄 PDF Report"
    ]
)

####################################################################
#Dashboard
##################################################################

####################################################################
#Dashboard
##################################################################

if page == "🏠 Dashboard":

    feed_flow = st.session_state.get(
        "ro_feed",
        50.0
    )

    permeate_flow = st.session_state.get(
        "ro_permeate",
        37.5
    )

    concentrate_flow = st.session_state.get(
        "ro_concentrate",
        12.5
    )

    ########################################################
    #Flow diagram
    ######################################################


    st.components.v1.html(
        f"""
    <style>

    .flow-container {{
        position: relative;
        height: 350px;
        width: 100%;
        background: #f5f5f5;
        border: 1px solid #cccccc;
        border-radius: 10px;
    }}

    .box {{
        position: absolute;
        background: #dff4f3;
        border: 1px solid #90c8c5;
        border-radius: 6px;
        padding: 10px;
        width: 170px;
        text-align: center;
        font-weight: bold;
    }}

    .feed {{
        left: 20px;
        top: 120px;
    }}

    .ro {{
        left: 420px;
        top: 120px;
    }}

    .product {{
        right: 500px;
        top: 120px;
    }}

    .reject {{
        left: 420px;
        top: 250px;
        background: #ffe6d5;
    }}

    .arrow-h {{
        position: absolute;
        height: 4px;
        background: #00a99d;
        animation: pulse 1s infinite;
    }}

    .arrow-v {{
        position: absolute;
        width: 4px;
        background: red;
        animation: pulse 1s infinite;
    }}

    @keyframes pulse {{

        0% {{opacity:0.3;}}

        50% {{opacity:1;}}

        100% {{opacity:0.3;}}
    }}

    .flow-text {{
        position:absolute;
        font-size:12px;
        font-weight:bold;
    }}
    </style>

    <div class="flow-container">

    <div class="box feed">
    💧 Feed<br>
    {feed_flow:.2f} m³/hr
    </div>

    <div class="box ro">
    ⚙️ RO Pass 1
    </div>

    <div class="box product">
    ✅ Product<br>
    {permeate_flow:.2f} m³/hr
    </div>

    <div class="box reject">
    ⚠️ Concentrate<br>
    {concentrate_flow:.2f} m³/hr
    </div>

    <div class="arrow-h"
    style="
    left:190px;
    top:145px;
    width:230px;
    ">
    </div>

    <div class="arrow-h"
    style="
    left:590px;
    top:145px;
    width:180px;
    ">
    </div>

    <div class="arrow-v"
    style="
    left:505px;
    top:170px;
    height:80px;
    ">
    </div>

    <div class="flow-text"
    style="
    left:280px;
    top:120px;
    ">
    Feed
    </div>

    <div class="flow-text"
    style="
    left:650px;
    top:120px;
    ">
    Permeate
    </div>

    <div class="flow-text"
    style="
    left:520px;
    top:210px;
    ">
    Reject
    </div>

    </div>

    """,
        height=380
    )
##############################################################################################################
# =====================================================
# FEED WATER ANALYSIS
# ====================================================
elif page == "💧 Feed Water Analysis":

    st.title("💧 Feed Water Analysis")

# Upload data from library>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



    uploaded_file = st.file_uploader(
        "Upload Water Analysis",
        type=["xlsx"]
    )

    if st.button("📂 Load Water Analysis"):

        if uploaded_file is None:

            st.warning("Please select Excel file")

        else:

            # Read IMS sheet
            df = pd.read_excel(
                uploaded_file,
                header=1,
                engine="openpyxl"
            )

            # Remove blank rows
            df = df.dropna(how="all")

            # Create dictionary
            water_dict = dict(
                zip(
                    df["Species"].astype(str).str.strip(),
                    df["Raw water"]
                )
            )

            # Auto populate session state

            st.session_state["ca"] = water_dict.get(
                "Calcium",
                0
            )

            st.session_state["mg"] = water_dict.get(
                "Magnesium",
                0
            )

            st.session_state["na"] = water_dict.get(
                "Sodium",
                0
            )

            st.session_state["k"] = water_dict.get(
                "Potassium",
                0
            )

            st.session_state["sr"] = water_dict.get(
                "Strontium",
                0
            )

            st.session_state["ba"] = water_dict.get(
                "Barium",
                0
            )

            st.session_state["fluoride"] = water_dict.get(
                "Fluoride",
                0
            )



            st.session_state["cl"] = water_dict.get(
                "Chloride",
                0
            )

            st.session_state["so4"] = water_dict.get(
                "Sulfate",
                0
            )

            st.session_state["no3"] = water_dict.get(
                "Nitrate",
                0
            )

            st.session_state["co3"] = water_dict.get(
                "Carbonate",
                0
            )

            st.session_state["hco3"] = water_dict.get(
                "Bicarbonate",
                0
            )


            st.session_state["boron"] = water_dict.get(
                "Boron",
                0
            )

            st.session_state["silica"] = water_dict.get(
                "Silica",
                0
            )

            st.session_state["feed_ph"] = water_dict.get(
                "pH",
                7
            )

            st.session_state["temperature"] = water_dict.get(
                "Temperature",
                25
            )

            # Optional
            st.session_state["calculated_tds"] = water_dict.get(
                "TDS",
                0
            )

            #######################################
            st.session_state["ca_widget"] = st.session_state["ca"]
            st.session_state["mg_widget"] = st.session_state["mg"]
            st.session_state["na_widget"] = st.session_state["na"]
            st.session_state["k_widget"] = st.session_state["k"]

            st.session_state["sr_widget"] = st.session_state["sr"]
            st.session_state["ba_widget"] = st.session_state["ba"]

            st.session_state["hco3_widget"] = st.session_state["hco3"]
            st.session_state["co3_widget"] = st.session_state["co3"]

            st.session_state["so4_widget"] = st.session_state["so4"]
            st.session_state["cl_widget"] = st.session_state["cl"]

            st.session_state["no3_widget"] = st.session_state["no3"]
            st.session_state["fluoride_widget"] = st.session_state["fluoride"]

            st.session_state["silica_widget"] = st.session_state["silica"]
            st.session_state["boron_widget"] = st.session_state["boron"]

            st.session_state["feed_ph_widget"] = st.session_state["feed_ph"]

            st.rerun()

            #######################################################

            st.success(
                "✅ Water Analysis Loaded Successfully"
            )

            st.write(df.head(30))
            st.write(df.columns.tolist())

            water_dict = dict(
                zip(
                    df["Species"].astype(str).str.strip(),
                    df["Raw water"]
                )
            )

            st.write(water_dict)


##########################################>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    st.markdown("### Feed Parameters")

    p1, p2, p3 = st.columns(3)
    with p1:

        water_types = [
            "RO/NF Permeate",
            "Softened Water",
            "Well Water",
            "Ground Water",
            "Municipal Water",
            "Surface Water",
            "Brackish Water",
            "Sea Water"
        ]

        water_type = st.selectbox(
            "Water Type",
            water_types,
            index=water_types.index(
                st.session_state["water_type"]
            ),
            key="water_type_widget"
        )

        st.session_state["water_type"] = water_type

        st.session_state["water_type"] = water_type



        sdi_requirements = {
            "RO/NF Permeate": ("SDI < 1", "green"),
            "Softened Water": ("SDI < 3", "green"),
            "Well Water": ("SDI < 3", "green"),
            "Ground Water": ("SDI < 3", "green"),
            "Municipal Water": ("SDI < 5", "orange"),
            "Surface Water": ("SDI < 5", "orange"),
            "Brackish Water": ("Membrane Pretreatment, SDI < 3", "red"),
            "Sea Water": ("Conventional Pretreatment + UF, SDI < 3", "red")
        }

        sdi_text, sdi_color = sdi_requirements[water_type]

        st.markdown(
            f"""
            <div style="
                padding:12px;
                border-radius:10px;
                background-color:{sdi_color};
                color:white;
                font-weight:bold;
                text-align:center;
            ">
            Recommended Feed Requirement: {sdi_text}
            </div>
            """,
            unsafe_allow_html=True
        )
    # =================================================
    # CATIONS
    # =================================================

    st.subheader("Feed Water Analysis")

    c1, c2, c3 = st.columns(
        [1, 1, 1],
        gap="small"
    )

    with c1:
        ca = st.number_input(
            "Calcium (Ca) mg/L",
            value=st.session_state["ca"],
            key="ca_widget"
        )
        st.session_state["ca"] = ca

        mg = st.number_input(
            "Magnesium (Mg) mg/L",
            value=st.session_state["mg"],
            key="mg_widget"
        )
        st.session_state["mg"] = mg

        na = st.number_input(
            "Sodium (Na) mg/L",
            value=st.session_state["na"],
            key="na_widget"
        )
        st.session_state["na"] = na

        k = st.number_input(
            "Potassium (K) mg/L",
            value=st.session_state["k"],
            key="k_widget"
        )
        st.session_state["k"] = k

        ba = st.number_input(
            "Barium (Ba) mg/L",
            value=st.session_state["ba"],
            key="ba_widget"
        )
        st.session_state["ba"] = ba

        sr = st.number_input(
            "Strontium (Sr) mg/L",
            value=st.session_state["sr"],
            key="sr_widget"
        )
        st.session_state["sr"] = sr

        # =================================================
        # ANIONS
        # =================================================

        with c2:

            hco3 = st.number_input(
                "Bicarbonate (HCO3) mg/L",
                value=st.session_state["hco3"],
                key="hco3_widget"
            )
            st.session_state["hco3"] = hco3

            co3 = st.number_input(
                "Carbonate (CO3) mg/L",
                value=st.session_state["co3"],
                key="co3_widget"
            )
            st.session_state["co3"] = co3

            so4 = st.number_input(
                "Sulphate (SO4) mg/L",
                value=st.session_state["so4"],
                key="so4_widget"
            )
            st.session_state["so4"] = so4

            cl = st.number_input(
                "Chloride (Cl) mg/L",
                value=st.session_state["cl"],
                key="cl_widget"
            )
            st.session_state["cl"] = cl

            no3 = st.number_input(
                "Nitrate (NO3) mg/L",
                value=st.session_state["no3"],
                key="no3_widget"
            )
            st.session_state["no3"] = no3


            fluoride = st.number_input(
                "Fluoride (F) mg/L",
                value=st.session_state["fluoride"],
                key="fluoride_widget"
            )
            st.session_state["fluoride"] = fluoride

        # =================================================
        # NEUTRALS
        # =================================================

        with c3:

            silica = st.number_input(
                "Silica (SiO2) mg/L",
                value=st.session_state["silica"],
                key="silica_widget"
            )
            st.session_state["silica"] = silica

            boron = st.number_input(
                "Boron (B) mg/L",
                value=st.session_state["boron"],
                key="boron_widget"
            )
            st.session_state["boron"] = boron

            iron = st.number_input(
                "Iron (Fe) mg/L",
                value=st.session_state["iron"],
                key="iron_widget"
            )
            st.session_state["iron"] = iron

            manganese = st.number_input(
                "Manganese (Mn) mg/L",
                value=st.session_state["manganese"],
                key="manganese_widget"
            )
            st.session_state["manganese"] = manganese


            temperature = st.number_input(
                "Temperature (°C)",
                value=st.session_state["temperature"],
                key="temperature_widget"
            )
            st.session_state["temperature"] = temperature

        ph = st.number_input(
            "pH",
            value=st.session_state["feed_ph"],
            key="feed_ph_widget"
        )
        st.session_state["feed_ph"] = ph

        # ==========================================
        # CO2 CALCULATION
        # ==========================================

        pka = (
                6.31
                - 0.002 *
                (temperature - 28.8)
        )

        co2 = (
                hco3 *
                (44 / 61) *
                10 ** (pka - ph)
        )

        st.session_state["co2"] = co2

        ##################################################################
        #####################################################################################
        # Save values permanently
        ######################################################################################
        total_cations = (
                ca + mg + na + k +
                ba + sr + iron +
                manganese
        )

        total_anions = (
                hco3 + co3 +
                so4 + cl +
                no3 + fluoride
        )

        total_neutral = (
                silica +
                boron +
                co2
        )

        tds = (
                total_cations +
                total_anions +
                silica +
                boron
        )

        hardness = (
                ca * 2.497 +
                mg * 4.118
        )

        conductivity = tds * 2

        ################################################################################

        osmotic_pressure = (
                                   tds / 10000
                           ) * 11.2

        alkalinity = (
                (hco3 * 50 / 61) +
                (co3 * 50 / 30)
        )

        ############################################################

        # ==========================================
        # CHARGE BALANCE
        # ==========================================

        # Cations (meq/L)

        ca_meq = ca / 20.04
        mg_meq = mg / 12.15
        na_meq = na / 23.00
        k_meq = k / 39.10

        ba_meq = ba / 68.67
        sr_meq = sr / 43.81

        # Anions (meq/L)

        hco3_meq = hco3 / 61.00
        co3_meq = co3 / 30.00
        so4_meq = so4 / 48.00
        cl_meq = cl / 35.45
        no3_meq = no3 / 62.00
        fluoride_meq = fluoride / 19.00

        total_cation_meq = (
                ca_meq +
                mg_meq +
                na_meq +
                k_meq +
                ba_meq +
                sr_meq
        )

        total_anion_meq = (
                hco3_meq +
                co3_meq +
                so4_meq +
                cl_meq +
                fluoride_meq
        )

        if (total_cation_meq + total_anion_meq) > 0:

            charge_balance_error = (
                                           (
                                                   total_cation_meq -
                                                   total_anion_meq
                                           )
                                           /
                                           (
                                                   total_cation_meq +
                                                   total_anion_meq
                                           )
                                   ) * 100

        else:

            charge_balance_error = 0



###############################################################################
    #KPI
###################################################################
    cb1, cb2, cb3 = st.columns(3)

    cb1.metric(
        "Cations (meq/L)",
        f"{total_cation_meq:.2f}"
    )

    cb2.metric(
        "Anions (meq/L)",
        f"{total_anion_meq:.2f}"
    )

    cb3.metric(
        "Charge Balance %",
        f"{charge_balance_error:.2f}"
    )

    st.info(
        f"Calculated CO₂ = {co2:.2f} mg/L"
    )

    #############################################################
#Status
    ######################################################

    if abs(charge_balance_error) <= 5:

        st.success(
            "✅ Charge Balance ACCEPTABLE"
        )

    elif abs(charge_balance_error) <= 10:

        st.warning(
            "⚠ Charge Balance Needs Review"
        )

    else:

        st.error(
            "❌ Charge Balance FAILED"
        )

####################################################################################

    # -----------------------------------
    # AUTO BALANCE
    # -----------------------------------

    st.subheader("Charge Balance Correction")

    if st.button(
            "Auto Balance Water Analysis"
    ):

        if total_cation_meq > total_anion_meq:

            correction = (
                                 total_cation_meq -
                                 total_anion_meq
                         ) * 61

            corrected_hco3 = (
                    hco3 +
                    correction
            )

        else:

            correction = (
                                 total_anion_meq -
                                 total_cation_meq
                         ) * 61

            corrected_hco3 = max(
                0,
                hco3 - correction
            )

        st.session_state["corrected_hco3"] = corrected_hco3

        st.success(
            f"""
    Original HCO3 = {hco3:.2f} mg/L

    Suggested HCO3 = {corrected_hco3:.2f} mg/L
    """
        )
  ###############################################################################################

    # =================================================
    # SAVE VALUES FOR OTHER MODULES
    # =================================================

    st.session_state["calculated_tds"] = tds
    st.session_state["hardness"] = hardness
    st.session_state["conductivity"] = conductivity
    st.session_state["feed_op"] = osmotic_pressure
    st.session_state["alkalinity"] = alkalinity
    #####
    st.subheader("Water Summary")

    st.markdown("""
    <style>

    .kpi-card {
        background-color:#102a43;
        padding:15px;
        border-radius:10px;
        text-align:center;
        border:1px solid #1f4e79;
    }

    .kpi-title {
        font-size:14px;
        color:#a0c4ff;
        margin-bottom:8px;
    }

    .kpi-value {
        font-size:28px;
        font-weight:bold;
        color:white;
    }

    </style>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">TDS (mg/L)</div>
            <div class="kpi-value">{tds:.1f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Hardness (mg/L)</div>
            <div class="kpi-value">{hardness:.1f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Conductivity (µS/cm)</div>
            <div class="kpi-value">{conductivity:.1f}</div>
        </div>
        """, unsafe_allow_html=True)

    c4, c5, c6, c7 = st.columns(4)

    with c4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Feed OP (bar)</div>
            <div class="kpi-value">{osmotic_pressure:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Cations (meq/L)</div>
            <div class="kpi-value">{total_cation_meq:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c6:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Anions (meq/L)</div>
            <div class="kpi-value">{total_anion_meq:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c7:
        st.metric(
        "CO₂",
        f"{co2:.2f} mg/L"
    )


    # =================================================
    # RESULTS
    # =================================================

    st.info(
        f"""
    Total Dissolved Solids : {tds:.1f} mg/L

    Hardness : {hardness:.1f} mg/L as CaCO3

    Conductivity : {conductivity:.1f} µS/cm

    Feed Osmotic Pressure : {osmotic_pressure:.2f} bar

    Alkalinity : {alkalinity:.1f} mg/L as CaCO3
    """
    )



###############################################################
#Conductivity
#######################################################################
elif page == "⚡ Conductivity":

    st.title("⚡ Conductivity Calculator")

    tds = st.session_state.get(
        "calculated_tds",
        0.0
    )

    temperature = st.session_state.get(
        "temperature",
        25.0
    )

    conductivity_input = st.number_input(
        "Measured Conductivity (µS/cm)",
        min_value=0.0,
        value=tds * 2
    )
    tds_factor = st.number_input(
        "TDS Conversion Factor",
        min_value=0.40,
        max_value=0.80,
        value=0.50,
        step=0.01
    )

    temp_coeff = 0.02
    calculated_conductivity = (
            tds / tds_factor
    )

    calculated_tds = (
            conductivity_input *
            tds_factor
    )

    conductivity_25 = (
            conductivity_input /
            (
                    1 +
                    temp_coeff *
                    (temperature - 25)
            )
    )

    if conductivity_input > 0:

        resistivity = (
                1000000 /
                conductivity_input
        )

    else:

        resistivity = 0

    feed_cond = conductivity_input

    rejection = st.number_input(
        "RO Rejection (%)",
        value=99.5
    )

    perm_cond = (
            feed_cond *
            (
                    1 -
                    rejection / 100
            )
    )

    if conductivity_input < 5:

        water_grade = "Ultra Pure Water"

    elif conductivity_input < 50:

        water_grade = "RO Permeate"

    elif conductivity_input < 500:

        water_grade = "Drinking Water"

    elif conductivity_input < 2000:

        water_grade = "Brackish Water"

    else:

        water_grade = "High Salinity Water"

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Measured Conductivity",
        f"{conductivity_input:.1f}"
    )

    c2.metric(
        "Conductivity @25°C",
        f"{conductivity_25:.1f}"
    )

    c3.metric(
        "Calculated TDS",
        f"{calculated_tds:.1f}"
    )

    c4.metric(
        "Resistivity",
        f"{resistivity:,.0f}"
    )

    st.subheader("RO Performance")

    r1, r2 = st.columns(2)

    r1.metric(
        "Feed Conductivity",
        f"{feed_cond:.1f} µS/cm"
    )

    r2.metric(
        "Predicted Permeate Conductivity",
        f"{perm_cond:.2f} µS/cm"
    )

    st.success(
        f"""
    Water Category : {water_grade}

    TDS : {calculated_tds:.1f} ppm

    Conductivity @25°C : {conductivity_25:.1f} µS/cm

    Predicted RO Permeate Conductivity : {perm_cond:.2f} µS/cm
    """
    )





# ====================================================
# RO DESIGN
# ====================================================


elif page == "📈 RO Design":

    st.title("📈 RO Design")




    ################################
    #Water Type and Flux
    ##################################

    flux_db = {
        "RO/NF Permeate": 16.0,
        "Softened Water": 15.0,
        "Ground Water": 12.0,
        "Well Water": 12.0,
        "Municipal Water": 13.0,
        "Surface Water": 10.0,
        "Brackish Water": 12.0,
        "Seawater": 8.0
    }

    pass2_flux_db = {

        "RO/NF Permeate": 18.0,
        "Softened Water": 16.0,
        "Ground Water": 15.0,
        "Well Water": 15.0,
        "Municipal Water": 16.0,
        "Surface Water": 12.0,
        "Brackish Water": 15.0,
        "Seawater": 10.0
    }

    water_type = st.session_state["water_type"]
    st.info(
        f"Selected Water Type = {water_type}"
    )

    st.write("RO Page:", st.session_state["water_type"])


    ###############################################
    #Membrane Database
    ###################################

    membrane_db = {


        # ==========================
        # DUPONT
        # ==========================

        "BW30-400": {
            "area": 400,
            "rejection": 99.5,
            "maker": "DuPont",
            "type": "BWRO"
        },

        "BW30HRLE-440i": {
            "area": 440,
            "rejection": 99.7,
            "maker": "DuPont",
            "type": "Low Energy BWRO"
        },

        "BW30XFR-400/34i": {
            "area": 400,
            "rejection": 99.7,
            "maker": "DuPont",
            "type": "Fouling Resistant BWRO"
        },

        "SW30HRLE-400": {
            "area": 400,
            "rejection": 99.8,
            "maker": "DuPont",
            "type": "SWRO"
        },

        # ==========================
        # HYDRANAUTICS
        # ==========================

        "ESPA2 MAX": {
            "area": 440,
            "rejection": 99.6,
            "maker": "Hydranautics",
            "type": "Low Energy BWRO"
        },

        "ESPA4 MAX": {
            "area": 440,
            "rejection": 99.5,
            "maker": "Hydranautics",
            "type": "BWRO"
        },

        "CPA5-LD": {
            "area": 440,
            "rejection": 99.8,
            "maker": "Hydranautics",
            "type": "High Rejection BWRO"
        },

        # ==========================
        # LG
        # ==========================

        "LG BW 400 R G2": {
            "area": 400,
            "rejection": 99.6,
            "maker": "LG",
            "type": "BWRO"
        },

        "LG BW 440 ES": {
            "area": 440,
            "rejection": 99.6,
            "maker": "LG",
            "type": "Low Energy BWRO"
        },

        # ==========================
        # TORAY
        # ==========================

        "TM820M-400": {
            "area": 400,
            "rejection": 99.5,
            "maker": "Toray",
            "type": "BWRO"
        },

        "TM820M-440": {
            "area": 440,
            "rejection": 99.7,
            "maker": "Toray",
            "type": "High Rejection BWRO"
        },

        # ==========================
        # LANXESS
        # ==========================

        "ACM5": {
            "area": 400,
            "rejection": 99.6,
            "maker": "Lanxess",
            "type": "BWRO"
        },

        "ACM6": {
            "area": 440,
            "rejection": 99.7,
            "maker": "Lanxess",
            "type": "High Rejection BWRO"
        }
    }

    membrane = st.selectbox(
        "Membrane Model",
        list(membrane_db.keys()),
        index=list(membrane_db.keys()).index(
            st.session_state.get(
                "membrane_model",
                "BW30-400"
            )
        )
    )

    membrane_area_ft2 = membrane_db[membrane]["area"]

    membrane_rejection = membrane_db[membrane]["rejection"]

    manufacturer = membrane_db[membrane]["maker"]

    # ====================================================
    # SAVE MEMBRANE DATA FOR PDF
    # ====================================================

    st.session_state["membrane_model"] = membrane

    st.session_state["manufacturer"] = manufacturer

    st.session_state["membrane_area"] = membrane_area_ft2

    st.session_state["membrane_rejection"] = membrane_rejection

    st.info(
        f"""
    Manufacturer : {manufacturer}

    Active Area : {membrane_area_ft2} ft²

    Nominal Salt Rejection : {membrane_rejection:.2f} %
    """
    )

    # ====================================================
    # TRAIN INFORMATION
    # ====================================================

    st.subheader("Train Information")

    c1, c2 = st.columns(2)

    with c1:

        pass1_feed_ph = st.number_input(
            "Pass 1 Feed pH",
            min_value=1.0,
            max_value=14.0,
            value=st.session_state.get(
                "pass1_feed_ph",
                st.session_state.get("feed_ph", 7.0)
            )
        )

        pass1_recovery = st.number_input(
            "Pass 1 Recovery (%)",
            min_value=1.0,
            max_value=99.0,
            value=st.session_state["pass1_recovery"]
        )

        pass1_permeate_flow = st.number_input(
            "Pass 1 Permeate Flow (m³/hr)",
            min_value=0.1,
            value=st.session_state["pass1_permeate_flow"]
        )

    with c2:

        passes = st.selectbox(
            "RO Passes",
            [1, 2],
            index=[1, 2].index(
                st.session_state["passes"]
            )
        )

    # ====================================================
    # PASS 1 CONFIGURATION
    # ====================================================

    st.subheader("Pass 1 Configuration")

    pass1_stages = st.selectbox(
        "Pass 1 Stages",
        [1, 2, 3],
        index=[1, 2, 3].index(
            st.session_state["pass1_stages"]
        )
    )

    s1, s2, s3 = st.columns(3)

    with s1:

        stage1_membrane = membrane

        stage1_elements = st.number_input(
            "Stage 1 Membranes/Vessel",
            min_value=1,
            value=st.session_state["stage1_elements"]
        )

        stage1_vessels = st.number_input(
            "Stage 1 No. Vessels",
            min_value=1,
            value=st.session_state["stage1_vessels"]
        )

    with s2:

        if pass1_stages >= 2:

            stage2_membrane = membrane

            stage2_elements = st.number_input(
                "Stage 2 Membranes/Vessel",
                min_value=1,
                value=st.session_state["stage2_elements"]
            )


            stage2_vessels = st.number_input(
                "Stage 2 No. Vessels",
                min_value=1,
                value=st.session_state["stage2_vessels"]
            )

        else:

            stage2_elements = 0
            stage2_vessels = 0

    with s3:

        if pass1_stages == 3:

            stage3_membrane = membrane

            stage3_elements = st.number_input(
                "Stage 3 Membranes/Vessel",
                min_value=1,
                value=st.session_state["stage3_elements"]
            )

            stage3_vessels = st.number_input(
                "Stage 3 No. Vessels",
                min_value=1,
                value=st.session_state["stage3_vessels"]
            )

        else:

            stage3_elements = 0
            stage3_vessels = 0

    # ====================================================
    # PASS 1 AREA
    # ====================================================

    pass1_area = (

            stage1_vessels *
            stage1_elements *
            membrane_area_ft2

    )

    if pass1_stages >= 2:
        pass1_area += (

                stage2_vessels *
                stage2_elements *
                membrane_area_ft2

        )

    if pass1_stages == 3:
        pass1_area += (

                stage3_vessels *
                stage3_elements *
                membrane_area_ft2

        )

    # ====================================================
    # PASS 1 FLOWS
    # ====================================================

    pass1_feed_flow = (

            pass1_permeate_flow /

            (pass1_recovery / 100)

    )

    pass1_concentrate_flow = (

            pass1_feed_flow -
            pass1_permeate_flow

    )


    # ====================================================
    # PASS 1 FLUX
    # ====================================================

    pass1_permeate_gpd = (

            pass1_permeate_flow *
            264.172 *
            24

    )

    pass1_flux = (

            pass1_permeate_gpd /

            pass1_area

    )

    st.session_state["pass1_flux"] = pass1_flux
###############################################################################################################

#####################################################################################################################
    # ====================================================
    # PASS 2
    # ====================================================

    if passes == 2:

        st.subheader("Pass 2 Configuration")

        pass2_feed_ph = st.number_input(
            "Pass 2 Feed pH",
            min_value=1.0,
            max_value=14.0,
            value=st.session_state["pass2_feed_ph"]
        )

        pass2_recovery = st.number_input(
            "Pass 2 Recovery (%)",
            min_value=1.0,
            max_value=99.0,
            value=st.session_state["pass2_recovery"]
        )

        pass2_stages = st.selectbox(
            "Pass 2 Stages",
            [1, 2, 3],
            index=[1, 2, 3].index(
                st.session_state["pass2_stages"]
            )
        )

        p21, p22, p23 = st.columns(3)

        with p21:

            pass2_stage1_elements = st.number_input(
                "Pass2 Stage1 Mem/Vessel",
                min_value=1,
                value=st.session_state["pass2_stage1_elements"]
            )

            pass2_stage1_vessels = st.number_input(
                "Pass2 Stage1 Vessels",
                min_value=1,
                value=st.session_state["pass2_stage1_vessels"]
            )

        with p22:

            if pass2_stages >= 2:

                pass2_stage2_elements = st.number_input(
                    "Pass2 Stage2 Mem/Vessel",
                    min_value=1,
                    value=st.session_state["pass2_stage2_elements"]
                )

                pass2_stage2_vessels = st.number_input(
                    "Pass2 Stage2 Vessels",
                    min_value=1,
                    value=st.session_state["pass2_stage2_vessels"]
                )


            else:

                pass2_stage2_elements = st.session_state["pass2_stage2_elements"]
                pass2_stage2_vessels = st.session_state["pass2_stage2_vessels"]

        with p23:

            if pass2_stages == 3:

                pass2_stage3_elements = st.number_input(
                    "Pass2 Stage3 Mem/Vessel",
                    min_value=1,
                    value=max(
                        1,
                        st.session_state["pass2_stage3_elements"]
                    )
                )

                pass2_stage3_vessels = st.number_input(
                    "Pass2 Stage3 Vessels",
                    min_value=1,
                    value=max(
                        1,
                        st.session_state["pass2_stage3_vessels"]
                    )
                )

            else:


                pass2_stage3_elements = st.session_state["pass2_stage3_elements"]
                pass2_stage3_vessels = st.session_state["pass2_stage3_vessels"]

        # ====================================================
        # PASS 2 FLOWS
        # ====================================================

        # Pass 2 Feed = Pass 1 Permeate

        pass2_feed_flow = pass1_permeate_flow

        pass2_permeate_flow = (

                pass2_feed_flow *
                pass2_recovery / 100

        )

        pass2_concentrate_flow = (

                pass2_feed_flow -
                pass2_permeate_flow

        )

        # ====================================================
        # PASS 2 AREA
        # ====================================================

        pass2_area = (

                pass2_stage1_elements *
                pass2_stage1_vessels *
                membrane_area_ft2

        )

        if pass2_stages >= 2:
            pass2_area += (

                    pass2_stage2_elements *
                    pass2_stage2_vessels *
                    membrane_area_ft2

            )

        if pass2_stages == 3:
            pass2_area += (

                    pass2_stage3_elements *
                    pass2_stage3_vessels *
                    membrane_area_ft2

            )

        # ====================================================
        # PASS 2 FLUX
        # ====================================================

        pass2_gpd = (

                pass2_permeate_flow *
                264.172 *
                24

        )

        pass2_flux = (

                pass2_gpd /

                pass2_area

        )

        st.session_state["pass2_flux"] = pass2_flux
    # ====================================================
    # KPI DISPLAY
    # ====================================================

    st.subheader("Train Summary")

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "Feed Flow",
        f"{pass1_feed_flow:.2f} m³/hr"
    )

    k2.metric(
        "Permeate Flow",
        f"{pass1_permeate_flow:.2f} m³/hr"
    )

    k3.metric(
        "Concentrate Flow",
        f"{pass1_concentrate_flow:.2f} m³/hr"
    )

    k4.metric(
        "Average Flux",
        f"{pass1_flux:.2f} GFD"
    )

    if passes == 2:
        st.divider()

        k5, k6, k7, k8 = st.columns(4)

        k5.metric(
            "Pass 2 Feed",
            f"{pass2_feed_flow:.2f} m³/hr"
        )

        k6.metric(
            "Pass 2 Product",
            f"{pass2_permeate_flow:.2f} m³/hr"
        )

        k7.metric(
            "Pass 2 Reject",
            f"{pass2_concentrate_flow:.2f} m³/hr"
        )

        k8.metric(
            "Pass 2 Flux",
            f"{pass2_flux:.2f} GFD"
        )
############################################################
    if st.button("💾 Save RO Design"):

        # --------------------------
        # Train Information
        # --------------------------
        st.session_state["pass1_feed_ph"] = pass1_feed_ph
        st.session_state["pass1_recovery"] = pass1_recovery
        st.session_state["pass1_permeate_flow"] = pass1_permeate_flow
        st.session_state["passes"] = passes

        # --------------------------
        # Pass 1
        # --------------------------
        st.session_state["pass1_stages"] = pass1_stages

        st.session_state["stage1_elements"] = stage1_elements
        st.session_state["stage1_vessels"] = stage1_vessels

        st.session_state["stage2_elements"] = stage2_elements
        st.session_state["stage2_vessels"] = stage2_vessels

        st.session_state["stage3_elements"] = stage3_elements
        st.session_state["stage3_vessels"] = stage3_vessels

        # --------------------------
        # Membrane
        # --------------------------
        st.session_state["membrane_model"] = membrane

        # --------------------------
        # Dashboard Values
        # --------------------------
        st.session_state["ro_feed"] = pass1_feed_flow
        st.session_state["ro_permeate"] = pass1_permeate_flow
        st.session_state["ro_concentrate"] = pass1_concentrate_flow

        # --------------------------
        # Pass 2
        # --------------------------
        if passes == 2:
            st.session_state["pass2_feed_ph"] = pass2_feed_ph
            st.session_state["pass2_recovery"] = pass2_recovery
            st.session_state["pass2_stages"] = pass2_stages

            st.session_state["pass2_stage1_elements"] = pass2_stage1_elements
            st.session_state["pass2_stage1_vessels"] = pass2_stage1_vessels

            st.session_state["pass2_stage2_elements"] = pass2_stage2_elements
            st.session_state["pass2_stage2_vessels"] = pass2_stage2_vessels

            st.session_state["pass2_stage3_elements"] = pass2_stage3_elements
            st.session_state["pass2_stage3_vessels"] = pass2_stage3_vessels

            # Membrane

            st.session_state["membrane_model"] = membrane

            st.session_state["membrane_rejection"] = membrane_rejection

            # Save for Dashboard

            st.session_state["ro_feed"] = pass1_feed_flow
            st.session_state["ro_pass1_recovery"] = pass1_recovery
            st.session_state["ro_permeate"] = pass1_permeate_flow
            st.session_state["ro_concentrate"] = pass1_concentrate_flow

        st.success("✅ RO Design Saved Successfully")
####################################################################################################################

        # ====================================================
        # CHEMICAL DOSING
        # ====================================================

elif page == "🧪 Chemical Dosing":

        st.title("🧪 Chemical Dosing Calculator")

        # ====================================================
        # DATA
        # ====================================================

        feed_flow = st.session_state.get(
            "ro_feed",
            50.0
        )

        feed_ph = st.session_state.get(
            "feed_ph",
            7.0
        )

        alkalinity = st.session_state.get(
            "alkalinity",
            100.0
        )

        recovery = st.session_state.get(
            "pass1_recovery",
            75.0
        )

        # ====================================================
        # CHEMICAL INPUTS
        # ====================================================

        chemicals = [
            "H2SO4",
            "HCl",
            "NaOH",
            "Antiscalant",
            "SMBS"
        ]

        saved_chemical = st.session_state.get(
            "selected_chemical",
            "H2SO4"
        )

        chemical = st.selectbox(
            "Select Chemical",
            chemicals,
            index=chemicals.index(saved_chemical)
        )

        chemical_strength = st.number_input(
            "Chemical Strength (%)",
            min_value=1.0,
            max_value=100.0,
            value=st.session_state.get(
                "chemical_strength",
                98.0
            )
        )

        target_ph = st.number_input(
            "Target pH",
            min_value=1.0,
            max_value=14.0,
            value=st.session_state.get(
                "target_ph",
                6.5
            )
        )

        # ====================================================
        # CALCULATION
        # ====================================================

        dosing_mg_l = 0.0

        if chemical == "H2SO4":

            dosing_mg_l = max(
                0,
                (
                        feed_ph -
                        target_ph
                )
                *
                alkalinity
                *
                0.20
            )

        elif chemical == "HCl":

            dosing_mg_l = max(
                0,
                (
                        feed_ph -
                        target_ph
                )
                *
                alkalinity
                *
                0.18
            )

        elif chemical == "NaOH":

            dosing_mg_l = max(
                0,
                (
                        target_ph -
                        feed_ph
                )
                *
                alkalinity
                *
                0.15
            )

        elif chemical == "Antiscalant":

            if recovery < 60:

                dosing_mg_l = 2

            elif recovery < 75:

                dosing_mg_l = 3

            elif recovery < 85:

                dosing_mg_l = 4

            else:

                dosing_mg_l = 5

        elif chemical == "SMBS":

            dosing_mg_l = 5

        # ====================================================
        # CONSUMPTION
        # ====================================================

        chemical_kg_hr = (
                                 dosing_mg_l *
                                 feed_flow
                         ) / 1000

        chemical_kg_day = (
                chemical_kg_hr * 24
        )

        solution_lph = (
                chemical_kg_hr /
                (chemical_strength / 100)
        )

        day_tank_volume = (
                solution_lph * 24
        )

        # ====================================================
        # KPI DISPLAY
        # ====================================================

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            f"{chemical} Dose",
            f"{dosing_mg_l:.2f} mg/L"
        )

        c2.metric(
            "kg/hr",
            f"{chemical_kg_hr:.2f}"
        )

        c3.metric(
            "kg/day",
            f"{chemical_kg_day:.2f}"
        )

        c4.metric(
            "L/hr",
            f"{solution_lph:.2f}"
        )

        st.divider()

        c5, c6 = st.columns(2)

        c5.metric(
            "Day Tank Volume",
            f"{day_tank_volume:.0f} L"
        )

        c6.metric(
            "Recovery",
            f"{recovery:.1f}%"
        )

        # ====================================================
        # WARNINGS
        # ====================================================

        warnings = []

        if recovery > 80:
            warnings.append(
                "⚠ High recovery. Antiscalant recommended."
            )

        if feed_ph > 8.5:
            warnings.append(
                "⚠ High pH. Scaling tendency may increase."
            )

        if alkalinity > 200:
            warnings.append(
                "⚠ High alkalinity. Acid addition may be required."
            )

        if len(warnings) == 0:

            st.success(
                "✅ No chemical dosing warnings."
            )

        else:

            for warning in warnings:
                st.warning(warning)

        # ====================================================
        # SUMMARY
        # ====================================================

        st.info(
            f"""
        Chemical : {chemical}

        Feed Flow : {feed_flow:.2f} m³/hr

        Feed pH : {feed_ph:.2f}

        Target pH : {target_ph:.2f}

        Chemical Dose : {dosing_mg_l:.2f} mg/L

        Chemical Consumption : {chemical_kg_day:.2f} kg/day

        Solution Requirement : {solution_lph:.2f} L/hr

        Day Tank Volume : {day_tank_volume:.0f} L
        """
        )

        # ====================================================
        # SAVE BUTTON
        # ====================================================

        if st.button("💾 Save Chemical Program"):
            st.session_state["selected_chemical"] = chemical

            st.session_state["chemical_strength"] = chemical_strength

            st.session_state["target_ph"] = target_ph

            st.session_state["chemical_dose"] = dosing_mg_l

            st.session_state["chemical_kg_hr"] = chemical_kg_hr

            st.session_state["chemical_kg_day"] = chemical_kg_day

            st.session_state["chemical_lph"] = solution_lph

            st.session_state["chemical_day_tank"] = day_tank_volume

            st.success(
                "✅ Chemical Program Saved"
            )

        # ====================================================
        # SAVED PROGRAM
        # ====================================================

        if st.session_state.get(
                "selected_chemical",
                ""
        ):
            st.subheader(
                "Saved Chemical Program"
            )

            st.info(
                f"""
        Chemical : {st.session_state.get('selected_chemical', '')}

        Strength : {st.session_state.get('chemical_strength', 0):.1f} %

        Target pH : {st.session_state.get('target_ph', 0):.2f}

        Dose : {st.session_state.get('chemical_dose', 0):.2f} mg/L

        Consumption : {st.session_state.get('chemical_kg_day', 0):.2f} kg/day

        Solution Flow : {st.session_state.get('chemical_lph', 0):.2f} L/hr

        Day Tank Volume : {st.session_state.get('chemical_day_tank', 0):.0f} L
        """
            )

########################################################################################################################


            # ====================================================
            # ADVANCED RO CHEMISTRY
            # ====================================================

            st.subheader("Advanced RO Chemistry")

            # ====================================================
            # INPUTS
            # ====================================================

            feed_flow = st.session_state.get("ro_feed", 50.0)

            recovery = st.session_state.get("pass1_recovery", 75.0)

            feed_ph = st.session_state.get("feed_ph", 7.0)

            temperature = st.session_state.get("temperature", 25.0)

            tds = st.session_state.get("calculated_tds", 0.0)

            ca = st.session_state.get("ca", 0.0)

            boron = st.session_state.get("boron", 0.0)

            mg = st.session_state.get("mg", 0.0)

            ba = st.session_state.get("ba", 0.0)

            sr = st.session_state.get("sr", 0.0)

            hco3 = st.session_state.get("hco3", 0.0)

            so4 = st.session_state.get("so4", 0.0)

            cl = st.session_state.get("cl", 0.0)

            silica = st.session_state.get("silica", 0.0)

            boron = st.session_state.get("boron", 0.0)

            alkalinity = st.session_state.get("alkalinity", 0.0)

            # ====================================================
            # CONCENTRATION FACTOR
            # ====================================================

            cf = 1 / (1 - recovery / 100)


############################################################################################################
        # ====================================================
        # BORON REMOVAL, pH ADJUSTMENT & NaOH DOSING
        # ====================================================

        st.subheader("Boron Removal, pH Adjustment & NaOH Dosing")

        feed_flow = st.session_state.get(
            "ro_feed",
            50.0
        )

        boron = st.session_state.get(
            "boron",
            0.0
        )

        passes = st.session_state.get(
            "passes",
            1
        )

        # ====================================================
        # INPUT
        # ====================================================

        pass2_feed_ph = st.number_input(
            "Pass 2 Feed pH",
            min_value=6.0,
            max_value=11.0,
            value=st.session_state.get(
                "pass2_feed_ph",
                8.2
            ),
            step=0.1,
            key="pass2_feed_ph_widget"
        )

        # ====================================================
        # NaOH DOSING CURVE
        # ====================================================

        ph_curve = np.array([
            6.0,
            7.0,
            7.5,
            8.2,
            8.5,
            9.0,
            9.5,
            10.0,
            11.0
        ])

        naoh_curve = np.array([
            20.0,
            48.2,
            54.3,
            57.3,
            58.3,
            60.9,
            65.5,
            83.0,
            138.0
        ])

        if passes == 2:

            naoh_dose = float(
                np.interp(
                    pass2_feed_ph,
                    ph_curve,
                    naoh_curve
                )
            )

        else:

            naoh_dose = 0.0

        # ====================================================
        # BORON REJECTION
        # ====================================================

        if pass2_feed_ph < 7.5:

            boron_rejection = 85

        elif pass2_feed_ph < 8.0:

            boron_rejection = 90

        elif pass2_feed_ph < 8.5:

            boron_rejection = 93

        elif pass2_feed_ph < 9.0:

            boron_rejection = 95

        elif pass2_feed_ph < 9.5:

            boron_rejection = 97

        else:

            boron_rejection = 98.5

        # ====================================================
        # PERMEATE BORON
        # ====================================================

        permeate_boron = (
                boron *
                (1 - boron_rejection / 100)
        )

        # ====================================================
        # CONSUMPTION
        # ====================================================

        naoh_kg_hr = (
                             naoh_dose *
                             feed_flow
                     ) / 1000

        naoh_kg_day = (
                naoh_kg_hr * 24
        )

        # ====================================================
        # DISPLAY
        # ====================================================

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Feed Boron",
            f"{boron:.2f} mg/L"
        )

        c2.metric(
            "Pass 2 Feed pH",
            f"{pass2_feed_ph:.2f}"
        )

        c3.metric(
            "NaOH Dose",
            f"{naoh_dose:.1f} mg/L"
        )

        c4.metric(
            "NaOH Consumption",
            f"{naoh_kg_day:.1f} kg/day"
        )

        st.divider()

        d1, d2 = st.columns(2)

        d1.metric(
            "Boron Rejection",
            f"{boron_rejection:.1f}%"
        )

        d2.metric(
            "Permeate Boron",
            f"{permeate_boron:.3f} mg/L"
        )

        # ====================================================
        # WARNINGS
        # ====================================================

        if passes != 2:
            st.warning(
                "⚠ Boron removal generally requires Pass‑2 RO."
            )

        if pass2_feed_ph >= 9.5:
            st.warning(
                "⚠ High caustic demand region above pH 9.5."
            )

        if boron > 1:
            st.warning(
                "⚠ High boron detected."
            )

        # ====================================================
        # SUMMARY
        # ====================================================

        st.info(
            f"""
        Pass 2 Feed pH : {pass2_feed_ph:.2f}

        NaOH Dose : {naoh_dose:.1f} mg/L

        NaOH Consumption : {naoh_kg_day:.1f} kg/day

        Boron Rejection : {boron_rejection:.1f} %

        Permeate Boron : {permeate_boron:.3f} mg/L
        """
        )

        # ====================================================
        # SAVE
        # ====================================================

        if st.button("💾 Save Boron Program"):
            st.session_state["pass2_feed_ph"] = pass2_feed_ph

            st.session_state["naoh_dose"] = naoh_dose

            st.session_state["naoh_kg_day"] = naoh_kg_day

            st.session_state["boron_rejection"] = boron_rejection

            st.session_state["permeate_boron"] = permeate_boron

            st.success(
                "✅ Boron Program Saved"
            )

        # ====================================================
        # DISPLAY SAVED VALUES
        # ====================================================

        if "naoh_dose" in st.session_state:
            st.subheader("Saved Boron Program")

            st.info(
                f"""
        Pass 2 Feed pH : {st.session_state.get('pass2_feed_ph', 0):.2f}

        NaOH Dose : {st.session_state.get('naoh_dose', 0):.1f} mg/L

        NaOH Consumption : {st.session_state.get('naoh_kg_day', 0):.1f} kg/day

        Boron Rejection : {st.session_state.get('boron_rejection', 0):.1f} %

        Permeate Boron : {st.session_state.get('permeate_boron', 0):.3f} mg/L
        """
            )
#########################################################################################################
        # ====================================================
        # ANTISCALANT PRODUCT DATABASE
        # ====================================================

        st.subheader("Antiscalant Product Selection")

        antiscalant_db = {

            "Genesys LF": {
                "vendor": "Genesys",
                "base_dose": 3.0,
                "application": "General BWRO"
            },

            "Genesys SI": {
                "vendor": "Genesys",
                "base_dose": 4.0,
                "application": "High Silica"
            },

            "Vitec 3000": {
                "vendor": "Avista",
                "base_dose": 4.0,
                "application": "General BWRO"
            },

            "Vitec 5100": {
                "vendor": "Avista",
                "base_dose": 5.0,
                "application": "High Recovery"
            },

            "RoClean L403": {
                "vendor": "Kurita",
                "base_dose": 4.0,
                "application": "General BWRO"
            },

            "Hypersperse MDC220": {
                "vendor": "Veolia",
                "base_dose": 4.0,
                "application": "High Sulfate"
            },

            "Hypersperse MDC150": {
                "vendor": "Veolia",
                "base_dose": 3.0,
                "application": "Municipal Water"
            }
        }

        products = list(antiscalant_db.keys())

        saved_product = st.session_state.get(
            "selected_antiscalant",
            "Vitec 3000"
        )

        selected_product = st.selectbox(
            "Antiscalant Product",
            products,
            index=products.index(saved_product)
        )

        vendor = antiscalant_db[selected_product]["vendor"]

        application = antiscalant_db[selected_product]["application"]

        base_dose = antiscalant_db[selected_product]["base_dose"]

        # ====================================================
        # PRODUCT ADJUSTED DOSE
        # ====================================================

        recommended_dose = base_dose

        if recovery > 75:
            recommended_dose += 1

        if recovery > 85:
            recommended_dose += 1

        if silica > 50:
            recommended_dose += 1

        if ba > 0.05:
            recommended_dose += 1

        if sr > 1:
            recommended_dose += 1

        if cf > 4:
            recommended_dose += 1

        # ====================================================
        # CONSUMPTION
        # ====================================================

        anti_kg_hr = (
                             recommended_dose *
                             feed_flow
                     ) / 1000

        anti_kg_day = anti_kg_hr * 24

        # ====================================================
        # DISPLAY
        # ====================================================

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Vendor",
            vendor
        )

        c2.metric(
            "Base Dose",
            f"{base_dose:.1f} mg/L"
        )

        c3.metric(
            "Recommended Dose",
            f"{recommended_dose:.1f} mg/L"
        )

        c4.metric(
            "CF",
            f"{cf:.2f}"
        )

        st.info(
            f"""
        Product : {selected_product}

        Vendor : {vendor}

        Application : {application}

        Recommended Dose : {recommended_dose:.1f} mg/L
        """
        )

        st.metric(
            "Antiscalant Consumption",
            f"{anti_kg_day:.2f} kg/day"
        )

        # ====================================================
        # SAVE
        # ====================================================

        if st.button("💾 Save Antiscalant Program"):
            st.session_state["selected_antiscalant"] = selected_product

            st.session_state["antiscalant_vendor"] = vendor

            st.session_state["antiscalant_application"] = application

            st.session_state["antiscalant_dose"] = recommended_dose

            st.session_state["antiscalant_kg_day"] = anti_kg_day

            st.success(
                "✅ Antiscalant Program Saved"
            )

        # ====================================================
        # SAVED RESULTS
        # ====================================================

        if st.session_state.get(
                "selected_antiscalant",
                ""
        ):
            st.subheader(
                "Saved Antiscalant Program"
            )

            st.info(
                f"""
        Product : {st.session_state.get('selected_antiscalant', '')}

        Vendor : {st.session_state.get('antiscalant_vendor', '')}

        Application : {st.session_state.get('antiscalant_application', '')}

        Dose : {st.session_state.get('antiscalant_dose', 0):.1f} mg/L

        Consumption : {st.session_state.get('antiscalant_kg_day', 0):.2f} kg/day
        """
            )

############################################################################################################
        # ====================================================
        # SMBS DOSING
        # ====================================================

        st.subheader("SMBS Dosing")

        feed_flow = st.session_state.get(
            "ro_feed",
            50.0
        )

        free_chlorine = st.number_input(
            "Free Chlorine (mg/L)",
            min_value=0.0,
            value=st.session_state.get(
                "smbs_free_chlorine",
                1.0
            ),
            step=0.1,
            key="smbs_free_chlorine_widget"
        )

        # ====================================================
        # DOSING CALCULATION
        # ====================================================

        # Industry Rule of Thumb:
        # 1 ppm Free Chlorine ≈ 3 ppm SMBS

        smbs_dose = (
                free_chlorine * 3
        )

        # ====================================================
        # CONSUMPTION
        # ====================================================

        smbs_kg_hr = (
                             smbs_dose *
                             feed_flow
                     ) / 1000

        smbs_kg_day = (
                smbs_kg_hr * 24
        )

        # ====================================================
        # DISPLAY
        # ====================================================

        s1, s2, s3 = st.columns(3)

        s1.metric(
            "Free Chlorine",
            f"{free_chlorine:.2f} mg/L"
        )

        s2.metric(
            "Recommended SMBS",
            f"{smbs_dose:.2f} mg/L"
        )

        s3.metric(
            "SMBS Consumption",
            f"{smbs_kg_day:.2f} kg/day"
        )

        # ====================================================
        # RECOMMENDATION
        # ====================================================

        if free_chlorine <= 0:

            st.success(
                "✅ No free chlorine detected. SMBS dosing may not be required."
            )

        elif free_chlorine <= 1:

            st.info(
                "ℹ Low chlorine level. Standard SMBS dosing is adequate."
            )

        elif free_chlorine <= 3:

            st.warning(
                "⚠ Moderate chlorine level. Verify SMBS residual."
            )

        else:

            st.error(
                "⚠ High chlorine level. Review dechlorination system."
            )

        # ====================================================
        # SUMMARY
        # ====================================================

        st.info(
            f"""
        Free Chlorine : {free_chlorine:.2f} mg/L

        SMBS Dose : {smbs_dose:.2f} mg/L

        Consumption : {smbs_kg_day:.2f} kg/day
        """
        )

        # ====================================================
        # SAVE BUTTON
        # ====================================================

        if st.button("💾 Save SMBS Program"):
            st.session_state["smbs_free_chlorine"] = free_chlorine

            st.session_state["smbs_dose"] = smbs_dose

            st.session_state["smbs_kg_day"] = smbs_kg_day

            st.success(
                "✅ SMBS Program Saved"
            )

        # ====================================================
        # SHOW SAVED DATA
        # ====================================================

        if st.session_state.get(
                "smbs_dose",
                0
        ) > 0:
            st.subheader(
                "Saved SMBS Program"
            )

            st.info(
                f"""
        Free Chlorine : {st.session_state.get('smbs_free_chlorine', 0):.2f} mg/L

        SMBS Dose : {st.session_state.get('smbs_dose', 0):.2f} mg/L

        Consumption : {st.session_state.get('smbs_kg_day', 0):.2f} kg/day
        """
            )
########################################################################
        #CONCDNTRATION
        #
        cf = 1 / (1 - recovery / 100)

        conc_tds = tds * cf

        conc_ca = ca * cf

        conc_alk = alkalinity * cf
###############################################################################################################
        # IMS concentrate pH is usually slightly higher

        conc_ph = feed_ph + 0.2


        # ====================================================
        # LSI CALCULATION
        # ====================================================

        # ====================================================
        # CONCENTRATE CONDITIONS
        # ====================================================

        recovery = st.session_state.get(
            "pass1_recovery",
            75.0
        )

        cf = 1 / (
                1 - recovery / 100
        )

        conc_tds = tds * cf

        conc_ca = ca * cf

        conc_alk = alkalinity * cf

        conc_ph = feed_ph + 0.2

        # ====================================================
        # LSI
        # ====================================================

        A = (
                    math.log10(
                        max(
                            conc_tds,
                            1
                        )
                    ) - 1
            ) / 10

        B = (
                -13.12 *
                math.log10(
                    temperature + 273
                )
                + 34.55
        )

        C = (
                math.log10(
                    max(
                        conc_ca * 2.497,
                        1
                    )
                )
                - 0.4
        )

        D = math.log10(
            max(
                conc_alk,
                1
            )
        )

        pHs = (
                9.3 +
                A +
                B -
                C -
                D
        )

        lsi = (
                conc_ph -
                pHs
        )

        # ====================================================
        # DISPLAY
        # ====================================================

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Concentrate pH",
            f"{conc_ph:.2f}"
        )

        c2.metric(
            "Concentrate TDS",
            f"{conc_tds:.1f}"
        )

        c3.metric(
            "Saturation pH",
            f"{pHs:.2f}"
        )

        c4.metric(
            "LSI",
            f"{lsi:.2f}"
        )

        # ====================================================
        # INTERPRETATION
        # ====================================================

        if lsi < -0.5:

            st.success(
                "✅ Low CaCO₃ scaling tendency"
            )

        elif lsi < 0:

            st.info(
                "ℹ Slightly undersaturated water"
            )

        elif lsi <= 0.5:

            st.warning(
                "⚠ Mild CaCO₃ scaling potential"
            )
        ###############################################################################################################
        # HYDRAULIC & ENERGY
        ###############################################################################################################

elif page == "🌊 Hydraulic & Energy":

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                membrane_age = st.number_input(
                    "Membrane Age (Years)",
                    value=3.0
                )

            with c2:
                flux_decline = st.number_input(
                    "Flux Decline / Year (%)",
                    value=7.0
                )

            with c3:
                fouling_factor = st.number_input(
                    "Fouling Factor",
                    value=0.80
                )

            with c4:
                sp_increase = st.number_input(
                    "SP Increase / Year (%)",
                    value=7.0
                )
#############################################################################################
            st.title("🌊 Hydraulic & Energy")

            permeate_pressure = st.number_input(
                "Permeate Pressure (psi)",
                value=5.0
            )

            # ====================================================
            # PASS 1 DATA
            # ====================================================

            feed_tds = st.session_state.get(
                "calculated_tds",
                0.0
            )

            pass1_recovery = st.session_state.get(
                "pass1_recovery",
                75.0
            )

            pass1_flux = st.session_state.get(
                "pass1_flux",
                13.5
            )

            cf1_total = 1 / (
                    1 - pass1_recovery / 100
            )

            cf1_stage1 = (
                    1 + (cf1_total - 1) * 0.33
            )

            cf1_stage2 = (
                    1 + (cf1_total - 1) * 0.67
            )

            cf1_stage3 = cf1_total

            # ----------------------------------------------------
            # STAGE TDS
            # ----------------------------------------------------

            p1_s1_tds = feed_tds * cf1_stage1
            p1_s2_tds = feed_tds * cf1_stage2
            p1_s3_tds = feed_tds * cf1_stage3

            # ----------------------------------------------------
            # OSMOTIC PRESSURE
            # ----------------------------------------------------

            p1_s1_op = p1_s1_tds * 11.2 / 10000
            p1_s2_op = p1_s2_tds * 11.2 / 10000
            p1_s3_op = p1_s3_tds * 11.2 / 10000

            # ----------------------------------------------------
            # IMS STYLE PRESSURE MODEL
            # ----------------------------------------------------

            # Base pressure primarily from flux
            # ====================================================
            # PASS 1 PRESSURE MODEL
            # ====================================================

            base_pressure_p1 = (
                    92 +
                    (feed_tds * 0.026)
            )

            base_ndp_p1 = (
                    72 +
                    (feed_tds * 0.010)
            )

            condition_correction = (
                    (flux_decline * 0.5) +
                    (sp_increase * 0.3) +
                    ((1.0 - fouling_factor) * 10)
            )

            pass1_feed_pressure = (
                    base_pressure_p1 +
                    condition_correction
            )

            pass1_ndp_avg = (
                    base_ndp_p1 +
                    (condition_correction * 0.8)
            )

            # ----------------------------------------------------
            # PASS 1 STAGE PRESSURES
            # ----------------------------------------------------

            p1_s1_pressure = (
                    pass1_feed_pressure * 0.77
            )

            p1_s2_pressure = (
                    pass1_feed_pressure * 0.60
            )

            p1_s3_pressure = (
                    pass1_feed_pressure * 0.24
            )

            # ----------------------------------------------------
            # PASS 1 NDP
            # ----------------------------------------------------

            p1_s1_ndp = (
                    p1_s1_pressure -
                    p1_s1_op -
                    permeate_pressure
            )

            p1_s2_ndp = (
                    p1_s2_pressure -
                    p1_s2_op -
                    permeate_pressure
            )

            p1_s3_ndp = (
                    p1_s3_pressure -
                    p1_s3_op -
                    permeate_pressure
            )

            # ====================================================
            # PASS 2 DATA
            # ====================================================

            pass2_tds = feed_tds * (
                    1 -
                    st.session_state.get(
                        "membrane_rejection",
                        99.5
                    ) / 100
            )

            pass2_recovery = st.session_state.get(
                "pass2_recovery",
                85.0
            )

            cf2_total = 1 / (
                    1 - pass2_recovery / 100
            )

            cf2_stage1 = (
                    1 + (cf2_total - 1) * 0.50
            )

            cf2_stage2 = cf2_total

            p2_s1_tds = (
                    pass2_tds * cf2_stage1
            )

            p2_s2_tds = (
                    pass2_tds * cf2_stage2
            )

            p2_s1_op = (
                    p2_s1_tds * 11.2 / 10000
            )

            p2_s2_op = (
                    p2_s2_tds * 11.2 / 10000
            )

            # ====================================================
            # PASS 2 PRESSURE MODEL
            # ====================================================

            pass2_feed_pressure = (
                    pass1_feed_pressure * 1.12
            )

            pass2_ndp_avg = (
                    pass1_ndp_avg * 1.08
            )

            # ----------------------------------------------------
            # PASS 2 STAGE PRESSURES
            # ----------------------------------------------------

            p2_s1_pressure = (
                    pass2_feed_pressure * 0.93
            )

            p2_s2_pressure = (
                    pass2_feed_pressure * 0.70
            )

            # ----------------------------------------------------
            # PASS 2 NDP
            # ----------------------------------------------------

            p2_s1_ndp = (
                    p2_s1_pressure -
                    p2_s1_op -
                    permeate_pressure
            )

            p2_s2_ndp = (
                    p2_s2_pressure -
                    p2_s2_op -
                    permeate_pressure
            )

            # ====================================================
            # PASS 1 TABLE
            # ====================================================

            st.subheader("Pass 1 Hydraulic Profile")

            pass1_df = pd.DataFrame({

                "Stage": [
                    "Stage 1",
                    "Stage 2",
                    "Stage 3"
                ],

                "TDS (ppm)": [
                    round(p1_s1_tds, 2),
                    round(p1_s2_tds, 2),
                    round(p1_s3_tds, 2)
                ],

                "OP (psi)": [
                    round(p1_s1_op, 2),
                    round(p1_s2_op, 2),
                    round(p1_s3_op, 2)
                ],

                "Pressure (psi)": [
                    round(p1_s1_pressure, 2),
                    round(p1_s2_pressure, 2),
                    round(p1_s3_pressure, 2)
                ],

                "NDP (psi)": [
                    round(p1_s1_ndp, 2),
                    round(p1_s2_ndp, 2),
                    round(p1_s3_ndp, 2)
                ]

            })

            st.dataframe(
                pass1_df,
                use_container_width=True
            )

            st.session_state["pass1_df"] = pass1_df


            # ====================================================
            # PASS 2 TABLE
            # ====================================================

            st.subheader("Pass 2 Hydraulic Profile")

            pass2_df = pd.DataFrame({

                "Stage": [
                    "Stage 1",
                    "Stage 2"
                ],

                "TDS (ppm)": [
                    round(p2_s1_tds, 2),
                    round(p2_s2_tds, 2)
                ],

                "OP (psi)": [
                    round(p2_s1_op, 2),
                    round(p2_s2_op, 2)
                ],

                "Pressure (psi)": [
                    round(p2_s1_pressure, 2),
                    round(p2_s2_pressure, 2)
                ],

                "NDP (psi)": [
                    round(p2_s1_ndp, 2),
                    round(p2_s2_ndp, 2)
                ]

            })

            st.dataframe(
                pass2_df,
                use_container_width=True
            )

            st.session_state["pass2_df"] = pass2_df

            # ====================================================
            # KPI
            # ====================================================

            st.subheader("Summary")

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "Pass 1 Feed Pressure",
                f"{pass1_feed_pressure:.1f} psi"
            )

            c2.metric(
                "Pass 2 Feed Pressure",
                f"{pass2_feed_pressure:.1f} psi"
            )

            c3.metric(
                "Pass 1 Flux",
                f"{pass1_flux:.1f} gfd"
            )

            c4.metric(
                "Pass 2 Feed TDS",
                f"{pass2_tds:.2f} ppm"
            )

            # ====================================================
            # AUTO SAVE TO SESSION STATE
            # ====================================================

            st.session_state["pass1_feed_pressure"] = pass1_feed_pressure
            st.session_state["pass2_feed_pressure"] = pass2_feed_pressure

            st.session_state["p1_s1_pressure"] = p1_s1_pressure
            st.session_state["p1_s2_pressure"] = p1_s2_pressure
            st.session_state["p1_s3_pressure"] = p1_s3_pressure

            st.session_state["p2_s1_pressure"] = p2_s1_pressure
            st.session_state["p2_s2_pressure"] = p2_s2_pressure

            st.session_state["p1_s1_ndp"] = p1_s1_ndp
            st.session_state["p1_s2_ndp"] = p1_s2_ndp
            st.session_state["p1_s3_ndp"] = p1_s3_ndp

            st.session_state["p2_s1_ndp"] = p2_s1_ndp
            st.session_state["p2_s2_ndp"] = p2_s2_ndp

            st.session_state["membrane_age"] = membrane_age
            st.session_state["flux_decline"] = flux_decline
            st.session_state["fouling_factor"] = fouling_factor
            st.session_state["sp_increase"] = sp_increase

            st.session_state["pass2_flux"] = 19.1
            # ====================================================
            # SAVE HYDRAULIC RESULTS
            # ====================================================

            if st.button("💾 Save Hydraulic Results"):
                st.session_state["pass1_feed_pressure"] = (
                    pass1_feed_pressure
                )

                st.session_state["pass2_feed_pressure"] = (
                    pass2_feed_pressure
                )

                st.session_state["p1_s1_pressure"] = (
                    p1_s1_pressure
                )

                st.session_state["p1_s2_pressure"] = (
                    p1_s2_pressure
                )

                st.session_state["p1_s3_pressure"] = (
                    p1_s3_pressure
                )

                st.session_state["p2_s1_pressure"] = (
                    p2_s1_pressure
                )

                st.session_state["p2_s2_pressure"] = (
                    p2_s2_pressure
                )

                st.session_state["p1_s1_ndp"] = (
                    p1_s1_ndp
                )

                st.session_state["p1_s2_ndp"] = (
                    p1_s2_ndp
                )

                st.session_state["p1_s3_ndp"] = (
                    p1_s3_ndp
                )

                st.session_state["p2_s1_ndp"] = (
                    p2_s1_ndp
                )

                st.session_state["p2_s2_ndp"] = (
                    p2_s2_ndp
                )

                st.success(
                    "✅ Hydraulic Results Saved Successfully"
                )

############################################################################################################
################################################################################################################

#TREATED WATER QUALITY

########################################################################################################################

elif page == "✅ Treated Water Quality":

        st.title("✅ Treated Water Quality Report")

        passes = st.session_state.get("passes", 1)

        pass1_recovery = st.session_state.get(
            "pass1_recovery",
            75.0
        )

        membrane_rejection = st.session_state.get(
            "membrane_rejection",
            99.5
        )

        rej = membrane_rejection / 100

        # ====================================================
        # RAW WATER DATA
        # ====================================================

        ions = {

            "Ca": st.session_state.get("ca", 0.0),
            "Mg": st.session_state.get("mg", 0.0),
            "Na": st.session_state.get("na", 0.0),
            "K": st.session_state.get("k", 0.0),

            "Ba": st.session_state.get("ba", 0.0),
            "Sr": st.session_state.get("sr", 0.0),

            "CO3": st.session_state.get("co3", 0.0),
            "HCO3": st.session_state.get("hco3", 0.0),

            "SO4": st.session_state.get("so4", 0.0),
            "Cl": st.session_state.get("cl", 0.0),
            "NO3": st.session_state.get("no3", 0.0),
            "F": st.session_state.get("fluoride", 0.0),

            "SiO2": st.session_state.get("silica", 0.0),

            "CO2": st.session_state.get("co2", 0.0),

            "B": st.session_state.get("boron", 0.0)

        }

        feed_tds = st.session_state.get(
            "calculated_tds",
            0.0
        )

        feed_ph = st.session_state.get(
            "feed_ph",
            7.0
        )

        cf1 = 1 / (
                1 - pass1_recovery / 100
        )

        # ====================================================
        # FEED WATER
        # ====================================================

        raw_ions = ions.copy()
        feed_ions = ions.copy()

        acid_dose = st.session_state.get(
            "chemical_dose",
            0.0
        )

        selected_chemical = st.session_state.get(
            "selected_chemical",
            ""
        )

        if selected_chemical == "H2SO4":

            feed_ions["SO4"] += (
                    acid_dose * 96 / 98
            )

        elif selected_chemical == "HCl":

            feed_ions["Cl"] += (
                    acid_dose * 35.5 / 36.5
            )

        # ====================================================
        # PASS 1 PERMEATE
        # ====================================================

        pass1_perm_ions = {}

        for ion, value in feed_ions.items():
            pass1_perm_ions[ion] = (
                    value * (1 - rej)
            )

        # IMS assumption:
        # CO2 passes freely

        if "CO2" in feed_ions:
            pass1_perm_ions["CO2"] = (
                feed_ions["CO2"]
            )

        # ====================================================
        # PASS 1 CONCENTRATES
        # ====================================================

        cf_total = 1 / (
                1 - pass1_recovery / 100
        )

        # Approximate IMS-style concentration progression
        cf1_stage1 = 1 + (cf_total - 1) * 0.33

        cf1_stage2 = 1 + (cf_total - 1) * 0.67

        cf1_stage3 = cf_total

        pass1_conc1 = {}
        pass1_conc2 = {}
        pass1_conc3 = {}

        for ion, value in feed_ions.items():
            pass1_conc1[ion] = (
                    value * cf1_stage1
            )

            pass1_conc2[ion] = (
                    value * cf1_stage2
            )

            pass1_conc3[ion] = (
                    value * cf1_stage3
            )


        # CO2 does not concentrate

        if "CO2" in feed_ions:
            pass1_conc1["CO2"] = (
                feed_ions["CO2"]
            )

            pass1_conc2["CO2"] = (
                feed_ions["CO2"]
            )

            pass1_conc3["CO2"] = (
                feed_ions["CO2"]
            )
        # ====================================================
        # PASS 2 FEED
        # ====================================================

        pass2_feed_ions = pass1_perm_ions.copy()

        naoh_dose = st.session_state.get(
            "naoh_dose",
            0.0
        )

        pass2_ph = st.session_state.get(
            "pass2_feed_ph",
            8.2
        )

        if passes == 2:
            pass2_feed_ions["Na"] += (
                    naoh_dose * 23 / 40
            )

            original_co2 = pass2_feed_ions.get(
                "CO2",
                0.0
            )

            conversion = 98.5

            converted_co2 = (
                    original_co2 *
                    conversion / 100
            )

            pass2_feed_ions["CO2"] = (
                    original_co2 -
                    converted_co2
            )

            pass2_feed_ions["HCO3"] += (
                    converted_co2 * 1.39
            )

            pass2_feed_ions["CO3"] += (
                    converted_co2 * 0.05
            )

        # ====================================================
        # PASS 2 PERMEATE
        # ====================================================

        pass2_perm_ions = {}

        for ion, value in pass2_feed_ions.items():
            pass2_perm_ions[ion] = (
                    value * (1 - rej)
            )

        # CO2 passes through RO

        if "CO2" in pass2_feed_ions:
            pass2_perm_ions["CO2"] = (
                pass2_feed_ions["CO2"]
            )

        # ====================================================
        # PASS 2 FEED CHEMISTRY (IMS APPROXIMATION)
        # ====================================================

        if passes == 2:

            if "HCO3" in pass2_feed_ions:
                hco3 = pass2_feed_ions["HCO3"]

                # Convert part of HCO3 to CO3 after NaOH addition
                co3_generated = hco3 * 0.20

                pass2_feed_ions["HCO3"] = (
                        hco3 - co3_generated
                )

                pass2_feed_ions["CO3"] = (
                        pass2_feed_ions.get("CO3", 0)
                        + co3_generated
                )

        # ====================================================
        # IMS PASS-2 CARBONATE ADJUSTMENT
        # ====================================================

        if passes == 2 and "HCO3" in pass2_feed_ions:

            target_ph = st.session_state.get(
                "pass2_target_ph",
                8.2
            )

            hco3 = pass2_feed_ions["HCO3"]

            if target_ph >= 8.2:
                # IMS behavior approximation
                pass2_feed_ions["HCO3"] = hco3 * 0.45

                pass2_feed_ions["CO3"] = (
                        pass2_feed_ions.get("CO3", 0)
                        + hco3 * 0.18
                )

                pass2_feed_ions["CO2"] = (
                        pass2_feed_ions.get("CO2", 0)
                        * 0.02
                )

        # ====================================================
        # PASS 2 CONCENTRATES
        # ====================================================

        pass2_recovery = st.session_state.get(
            "pass2_recovery",
            85.0
        )

        cf2_total = 1 / (
                1 - pass2_recovery / 100
        )

        cf2_stage1 = 1 + (
                cf2_total - 1
        ) * 0.50

        cf2_stage2 = cf2_total

        pass2_conc1 = {}
        pass2_conc2 = {}

        for ion, value in pass2_feed_ions.items():
            pass2_conc1[ion] = (
                    value * cf2_stage1
            )

            pass2_conc2[ion] = (
                    value * cf2_stage2
            )

        # ====================================================
        # IMS CO2 BEHAVIOUR
        # ====================================================

        if "CO2" in pass2_feed_ions:
            pass2_conc1["CO2"] = (
                pass2_feed_ions["CO2"]
            )

            pass2_conc2["CO2"] = (
                pass2_feed_ions["CO2"]
            )

        # ====================================================
        # TDS
        # ====================================================

        pass1_tds = sum(
            pass1_perm_ions.values()
        )

        if passes == 2:

            pass2_feed_tds = sum(
                pass2_feed_ions.values()
            )

            final_tds = sum(
                pass2_perm_ions.values()
            )

        else:

            pass2_feed_tds = pass1_tds

            final_tds = pass1_tds

        # ====================================================
        # COMPLETE IMS TABLE
        # ====================================================

        results = []

        for ion in feed_ions:
            results.append([

                ion,

                round(raw_ions.get(ion, 0), 3),

                round(feed_ions.get(ion, 0), 3),

                round(pass1_perm_ions.get(ion, 0), 3),

                round(pass1_conc1.get(ion, 0), 3),

                round(pass1_conc2.get(ion, 0), 3),

                round(pass1_conc3.get(ion, 0), 3),

                round(pass2_feed_ions.get(ion, 0), 3),

                round(pass2_perm_ions.get(ion, 0), 3),

                round(pass2_conc1.get(ion, 0), 3),

                round(pass2_conc2.get(ion, 0), 3)

            ])

        # ====================================================
        # BUILD DATAFRAME
        # ====================================================

        quality_df = pd.DataFrame(

            results,

            columns=[

                "Ion",

                "Raw Water",

                "RO Feed",

                "Pass1 Perm",

                "P1 Conc-1",

                "P1 Conc-2",

                "P1 Conc-3",

                "Pass2 Feed",

                "Pass2 Perm",

                "P2 Conc-1",

                "P2 Conc-2"

            ]

        )

        # ====================================================
        # TDS ROW
        # ====================================================

        quality_df.loc[len(quality_df)] = [

            "TDS",

            round(feed_tds, 2),

            round(sum(feed_ions.values()), 2),

            round(sum(pass1_perm_ions.values()), 2),

            round(sum(pass1_conc1.values()), 2),

            round(sum(pass1_conc2.values()), 2),

            round(sum(pass1_conc3.values()), 2),

            round(sum(pass2_feed_ions.values()), 2),

            round(sum(pass2_perm_ions.values()), 2),

            round(sum(pass2_conc1.values()), 2),

            round(sum(pass2_conc2.values()), 2)

        ]

        # ====================================================
        # pH ROW
        # ====================================================

        quality_df.loc[len(quality_df)] = [

            "pH",

            round(feed_ph, 2),

            round(feed_ph, 2),

            round(feed_ph - 1.2, 2),

            round(feed_ph + 0.3, 2),

            round(feed_ph + 0.6, 2),

            round(feed_ph + 0.8, 2),

            round(pass2_ph, 2),

            round(pass2_ph - 1.0, 2),

            round(pass2_ph + 0.3, 2),

            round(pass2_ph + 0.6, 2)

        ]

        # ====================================================
        # SAVE FOR PDF
        # ====================================================

        st.session_state["quality_df"] = quality_df

        # ====================================================
        # DISPLAY
        # ====================================================

        st.subheader(
            "IMS Style Water Quality Report"
        )

        st.dataframe(
            quality_df,
            use_container_width=True
        )

        # ====================================================
        # SAVE BUTTON
        # ====================================================

        if st.button(
                "💾 Save Water Quality Results"
        ):
            st.session_state["quality_df"] = quality_df

            st.success(
                "✅ Water Quality Results Saved"
            )
  #############################################################################################################
#PDF

elif page == "📄 PDF Report":

    st.title("📄 RO Design Pro PDF Report")

    if st.button("📄 Generate PDF Report"):

        from io import BytesIO
        from datetime import datetime

        pdf_buffer = BytesIO()

        doc = SimpleDocTemplate(
            pdf_buffer
        )

        styles = getSampleStyleSheet()

        elements = []

        # ====================================================
        # PAGE 1 - SYSTEM SUMMARY
        # ====================================================

        elements.append(
            Paragraph(
                "RO SYSTEM SUMMARY",
                styles["Heading1"]
            )
        )

        elements.append(
            Spacer(1, 12)
        )

        summary_data = [

            ["Parameter", "Pass 1", "Pass 2"],

            [
                "Feed Pressure (psi)",
                f"{st.session_state.get('pass1_feed_pressure',0):.1f}",
                f"{st.session_state.get('pass2_feed_pressure',0):.1f}"
            ],

            [
                "Average NDP (psi)",
                f"{st.session_state.get('p1_s1_ndp',0):.1f}",
                f"{st.session_state.get('p2_s1_ndp',0):.1f}"
            ],

            [
                "HP Pump Flow (gpm)",
                f"{st.session_state.get('ro_feed',0)*4.403:.1f}",
                f"{st.session_state.get('pass1_permeate_flow',0)*4.403:.1f}"
            ],

            [
                "Feed pH",
                f"{st.session_state.get('feed_ph',0):.2f}",
                f"{st.session_state.get('pass2_feed_ph',0):.2f}"
            ],

            [
                "NaOH Dose (mg/L)",
                "-",
                f"{st.session_state.get('naoh_dose',0):.1f}"
            ],

            [
                "Average Flux (gfd)",
                f"{st.session_state.get('pass1_flux',0):.1f}",
                f"{st.session_state.get('pass2_flux',19.1):.1f}"
            ],

            [
                "Permeate Flow (m3/hr)",
                f"{st.session_state.get('pass1_permeate_flow',0):.2f}",
                f"{st.session_state.get('ro_permeate',0):.2f}"
            ],

            [
                "Feed Flow (m3/hr)",
                f"{st.session_state.get('ro_feed',0):.2f}",
                f"{st.session_state.get('pass1_permeate_flow',0):.2f}"
            ],

            [
                "Recovery (%)",
                f"{st.session_state.get('pass1_recovery',0):.1f}",
                f"{st.session_state.get('pass2_recovery',0):.1f}"
            ],

            [
                "Flux Decline (%/yr)",
                f"{st.session_state.get('flux_decline',0):.1f}",
                f"{st.session_state.get('flux_decline',0):.1f}"
            ],

            [
                "Fouling Factor",
                f"{st.session_state.get('fouling_factor',0):.2f}",
                f"{st.session_state.get('fouling_factor',0):.2f}"
            ],

            [
                "SP Increase (%/yr)",
                f"{st.session_state.get('sp_increase',0):.1f}",
                f"{st.session_state.get('sp_increase',0):.1f}"
            ],

            [
                "Water Type",
                st.session_state.get("water_type",""),
                st.session_state.get("water_type","")
            ],

            [
                "Membrane Model",
                st.session_state.get("membrane_model", ""),
                st.session_state.get("membrane_model", "")
            ],

            [
                "Manufacturer",
                st.session_state.get("manufacturer", ""),
                st.session_state.get("manufacturer", "")
            ],

            [
                "Membrane Area (ft²)",
                f"{st.session_state.get('membrane_area', 0):.0f}",
                f"{st.session_state.get('membrane_area', 0):.0f}"
            ],

            [
                "No. of Passes",
                f"{st.session_state.get('passes', 1)}",
                f"{st.session_state.get('passes', 1)}"
            ],

            [
                "Pass 1 Stages",
                f"{st.session_state.get('pass1_stages', 0)}",
                "-"
            ],

            [
                "Pass 2 Stages",
                "-",
                f"{st.session_state.get('pass2_stages', 0)}"
            ],

            [
                "Pass 1 Permeate Flow (m³/hr)",
                f"{st.session_state.get('pass1_permeate_flow', 0):.2f}",
                "-"
            ],

            [
                "Pass 1 Concentrate Flow (m³/hr)",
                f"{st.session_state.get('ro_concentrate', 0):.2f}",
                "-"
            ],

            [
                "Pass 1 Flux (gfd)",
                f"{st.session_state.get('pass1_flux', 0):.2f}",
                "-"
            ],

            [
                "Pass 2 Feed Flow (m³/hr)",
                "-",
                f"{st.session_state.get('pass1_permeate_flow', 0):.2f}"
            ],

            [
                "Pass 2 Permeate Flow (m³/hr)",
                "-",
                f"{st.session_state.get('ro_permeate', 0):.2f}"
            ],

            [
                "Pass 2 Concentrate Flow (m³/hr)",
                "-",
                f"{(st.session_state.get('pass1_permeate_flow', 0) * (1 - st.session_state.get('pass2_recovery', 85) / 100)):.2f}"
            ],

            [
                "Pass 2 Flux (gfd)",
                "-",
                f"{st.session_state.get('pass2_flux', 19.1):.2f}"
            ]

        ]

        summary_table = Table(
            summary_data,
            colWidths=[180,120,120]
        )

        summary_table.setStyle(TableStyle([

            ("GRID",(0,0),(-1,-1),1,colors.black),

            ("BACKGROUND",
             (0,0),
             (-1,0),
             colors.HexColor("#4F81BD")),

            ("TEXTCOLOR",
             (0,0),
             (-1,0),
             colors.white),

            ("FONTNAME",
             (0,0),
             (-1,0),
             "Helvetica-Bold"),

            ("BACKGROUND",
             (0,1),
             (0,-1),
             colors.lightgrey),

            ("ALIGN",
             (1,1),
             (-1,-1),
             "CENTER")

        ]))

        elements.append(
            summary_table
        )

        elements.append(
            Spacer(1, 10)
        )

        elements.append(
            Paragraph(
                "HYDRAULIC SUMMARY",
                styles["Heading2"]
            )
        )

        hydraulic_summary = [

            ["Parameter", "Pass 1", "Pass 2"],

            [
                "Stage 1 NDP",
                f"{st.session_state.get('p1_s1_ndp', 0):.1f}",
                f"{st.session_state.get('p2_s1_ndp', 0):.1f}"
            ],

            [
                "Stage 2 NDP",
                f"{st.session_state.get('p1_s2_ndp', 0):.1f}",
                f"{st.session_state.get('p2_s2_ndp', 0):.1f}"
            ],

            [
                "Stage 3 NDP",
                f"{st.session_state.get('p1_s3_ndp', 0):.1f}",
                "-"
            ]

        ]

        tbl = Table(
            hydraulic_summary,
            colWidths=[150, 100, 100]
        )

        tbl.setStyle(TableStyle([

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("BACKGROUND",
             (0, 0),
             (-1, 0),
             colors.lightgrey)

        ]))

        elements.append(tbl)
#######################################################################################################





        ##################################################

        # ====================================================
        # WATER QUALITY PAGE
        # ====================================================

        quality_df = st.session_state.get(
            "quality_df",
            pd.DataFrame()
        )

        if not quality_df.empty:

            elements.append(
                PageBreak()
            )

            elements.append(
                Paragraph(
                    "TREATED WATER QUALITY REPORT",
                    styles["Heading1"]
                )
            )

            elements.append(
                Spacer(1, 10)
            )

            pdf_table = []

            pdf_table.append(
                quality_df.columns.tolist()
            )

            for _, row in quality_df.iterrows():
                pdf_table.append(
                    row.astype(str).tolist()
                )

            report_table = Table(
                pdf_table,
                repeatRows=1
            )

            report_table.setStyle(TableStyle([

                ("GRID",
                 (0, 0),
                 (-1, -1),
                 0.5,
                 colors.black),

                ("BACKGROUND",
                 (0, 0),
                 (-1, 0),
                 colors.HexColor("#A6C8E5")),

                ("FONTNAME",
                 (0, 0),
                 (-1, 0),
                 "Helvetica-Bold"),

                ("FONTSIZE",
                 (0, 0),
                 (-1, -1),
                 7),

                ("ALIGN",
                 (1, 1),
                 (-1, -1),
                 "RIGHT"),

                ("ALIGN",
                 (0, 0),
                 (0, -1),
                 "LEFT")

            ]))

            elements.append(
                report_table
            )

###########################################################################################
        # ====================================================
        # HYDRAULIC & ENERGY PAGE
        # ====================================================

        pass1_df = st.session_state.get(
            "pass1_df",
            pd.DataFrame()
        )

        pass2_df = st.session_state.get(
            "pass2_df",
            pd.DataFrame()
        )

        # ====================================================
        # PASS 1 HYDRAULIC PROFILE
        # ====================================================

        if not pass1_df.empty:

            elements.append(
                PageBreak()
            )

            elements.append(
                Paragraph(
                    "PASS 1 HYDRAULIC PROFILE",
                    styles["Heading1"]
                )
            )

            elements.append(
                Spacer(1, 10)
            )

            p1_data = []

            p1_data.append(
                pass1_df.columns.tolist()
            )

            for _, row in pass1_df.iterrows():
                p1_data.append(
                    row.astype(str).tolist()
                )

            p1_table = Table(
                p1_data,
                repeatRows=1,
                colWidths=[90, 90, 90, 90, 90]
            )

            p1_table.setStyle(TableStyle([

                ("GRID",
                 (0, 0),
                 (-1, -1),
                 0.5,
                 colors.black),

                ("BACKGROUND",
                 (0, 0),
                 (-1, 0),
                 colors.HexColor("#A6C8E5")),

                ("TEXTCOLOR",
                 (0, 0),
                 (-1, 0),
                 colors.black),

                ("FONTNAME",
                 (0, 0),
                 (-1, 0),
                 "Helvetica-Bold"),

                ("ALIGN",
                 (1, 1),
                 (-1, -1),
                 "CENTER"),

                ("FONTSIZE",
                 (0, 0),
                 (-1, -1),
                 8)

            ]))

            elements.append(
                p1_table
            )

        # ====================================================
        # PASS 2 HYDRAULIC PROFILE
        # ====================================================

        if not pass2_df.empty:

            elements.append(
                PageBreak()
            )

            elements.append(
                Paragraph(
                    "PASS 2 HYDRAULIC PROFILE",
                    styles["Heading1"]
                )
            )

            elements.append(
                Spacer(1, 10)
            )

            p2_data = []

            p2_data.append(
                pass2_df.columns.tolist()
            )

            for _, row in pass2_df.iterrows():
                p2_data.append(
                    row.astype(str).tolist()
                )

            p2_table = Table(
                p2_data,
                repeatRows=1,
                colWidths=[90, 90, 90, 90, 90]
            )

            p2_table.setStyle(TableStyle([

                ("GRID",
                 (0, 0),
                 (-1, -1),
                 0.5,
                 colors.black),

                ("BACKGROUND",
                 (0, 0),
                 (-1, 0),
                 colors.HexColor("#A6C8E5")),

                ("TEXTCOLOR",
                 (0, 0),
                 (-1, 0),
                 colors.black),

                ("FONTNAME",
                 (0, 0),
                 (-1, 0),
                 "Helvetica-Bold"),

                ("ALIGN",
                 (1, 1),
                 (-1, -1),
                 "CENTER"),

                ("FONTSIZE",
                 (0, 0),
                 (-1, -1),
                 8)

            ]))

            elements.append(
                p2_table
            )

        # ====================================================
        # CHEMICAL DOSING PAGE
        # ====================================================

        elements.append(
            PageBreak()
        )

        elements.append(
            Paragraph(
                "CHEMICAL DOSING SUMMARY",
                styles["Heading1"]
            )
        )

        elements.append(
            Spacer(1, 10)
        )

        chemical_data = [

            ["Parameter", "Value"],

            [
                "Selected Chemical",
                str(
                    st.session_state.get(
                        "selected_chemical",
                        ""
                    )
                )
            ],

            [
                "Chemical Strength (%)",
                f"{st.session_state.get('chemical_strength', 0):.1f}"
            ],

            [
                "Target pH",
                f"{st.session_state.get('target_ph', 0):.2f}"
            ],

            [
                "Chemical Dose (mg/L)",
                f"{st.session_state.get('chemical_dose', 0):.2f}"
            ],

            [
                "Chemical Consumption (kg/day)",
                f"{st.session_state.get('chemical_kg_day', 0):.2f}"
            ],

            [
                "Chemical Solution Flow (L/hr)",
                f"{st.session_state.get('chemical_lph', 0):.2f}"
            ],

            [
                "Day Tank Volume (L)",
                f"{st.session_state.get('chemical_day_tank', 0):.0f}"
            ],

            [
                "Pass 2 Feed pH",
                f"{st.session_state.get('pass2_feed_ph', 0):.2f}"
            ],

            [
                "NaOH Dose (mg/L)",
                f"{st.session_state.get('naoh_dose', 0):.1f}"
            ],

            [
                "NaOH Consumption (kg/day)",
                f"{st.session_state.get('naoh_kg_day', 0):.1f}"
            ],

            [
                "Boron Rejection (%)",
                f"{st.session_state.get('boron_rejection', 0):.1f}"
            ],

            [
                "Permeate Boron (mg/L)",
                f"{st.session_state.get('permeate_boron', 0):.3f}"
            ],

            [
                "Antiscalant Product",
                str(
                    st.session_state.get(
                        "selected_antiscalant",
                        ""
                    )
                )
            ],

            [
                "Antiscalant Vendor",
                str(
                    st.session_state.get(
                        "antiscalant_vendor",
                        ""
                    )
                )
            ],

            [
                "Antiscalant Application",
                str(
                    st.session_state.get(
                        "antiscalant_application",
                        ""
                    )
                )
            ],

            [
                "Antiscalant Dose (mg/L)",
                f"{st.session_state.get('antiscalant_dose', 0):.2f}"
            ],

            [
                "Antiscalant Consumption (kg/day)",
                f"{st.session_state.get('antiscalant_kg_day', 0):.2f}"
            ],

            [
                "Free Chlorine (mg/L)",
                f"{st.session_state.get('smbs_free_chlorine', 0):.2f}"
            ],

            [
                "SMBS Dose (mg/L)",
                f"{st.session_state.get('smbs_dose', 0):.2f}"
            ],

            [
                "SMBS Consumption (kg/day)",
                f"{st.session_state.get('smbs_kg_day', 0):.2f}"
            ]

        ]

        chem_table = Table(
            chemical_data,
            colWidths=[250, 150]
        )

        chem_table.setStyle(TableStyle([

            ("GRID",
             (0, 0),
             (-1, -1),
             0.75,
             colors.black),

            ("BACKGROUND",
             (0, 0),
             (-1, 0),
             colors.HexColor("#A6C8E5")),

            ("FONTNAME",
             (0, 0),
             (-1, 0),
             "Helvetica-Bold"),

            ("FONTSIZE",
             (0, 0),
             (-1, -1),
             9),

            ("ALIGN",
             (1, 1),
             (-1, -1),
             "CENTER")

        ]))

        elements.append(
            chem_table
        )



        # ====================================================
        # BUILD PDF
        # ====================================================

        doc.build(elements)

        pdf_buffer.seek(0)

        st.download_button(
            "⬇ Download PDF",
            data=pdf_buffer,
            file_name=f"RO_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf"
        )




###############################################################################################################################

                                                        #NOTES

    #Flux is based on type of water we used in RO

                            # Single pass RO

    #Feed:  TDS = 2000   ppm
   # Permeate:   10 - 50   ppm

    #Often    acceptable    for:

   # Industrial    water
   # Cooling    water
   # General    process    water

                           #Two Pass RO

# Needed when required permeate is:

           # < 10 ppm TDS
           # < 2 µS/cm conductivity
           # EDI Feed
           # Boiler Makeup
           # Semiconductor Water

          #      Then:
    #Pass    1 → 20    ppm
    #Pass    2 → 1    ppm

    #BASED ON TDS REQUIREMENT AT OUTLET , NO.OF PASSES ARE DECIDED. IF FLOW IS INCREASING WE CAN
    # INCREASE STAGES, NO OF MODULES, BUT TO GET VERY TDS WE NEED TO ADD PASS. SINCE STAGES ARE IN PARALLEL AND PASS
    # IN SERIES

    #Ph increase then co2 decrease and vice versa
    #Temp increase co2 dissolved decrease

            #Why is pKa important for CO₂ calculations?
            #The Henderson-Hasselbalch equation is:
            #pH = pKa + log10(HCO3⁻ / CO2)

    #pKa = Negative Logarithm of the Acid Dissociation Constant (Ka)
    #pKa indicates how easily an acid releases a hydrogen ion (H⁺).
    #Lower pKa  → Stronger acid
    #Higher pKa → Weaker acid

            #pKa1 ≈ 6.3
            #CO2 ⇌ HCO3⁻

            #pKa2 ≈ 10.3
            #HCO3⁻ ⇌ CO3²⁻

        #Why EDI Engineers Hate CO₂
        #CO2 + H2O → H+ + HCO3⁻           This consumes EDI capacity and increases power consumption.
        #That's why high-CO₂ waters often need:
                        #RO
                        #↓
                        #Degasser
                        #↓
                        #EDI
           #OR NaOH before RO

           #CO2 is difficult for RO to remove.
           #HCO3⁻ is easy for RO to remove.

        #LSI = Langelier Saturation Index
        #It is one of the most important indicators in
        # RO design because it helps predict whether calcium carbonate (CaCO₃) scale will form.
        #LSI = pH - pHs
            #pH  = Actual water pH
            #pHs = Saturation pH
        #LSI < 0          Water is undersaturated/Low CaCO₃ scaling tendency
        #LSI > 0       Water is supersaturated /Calcium carbonate scale may form/Antiscalant may be required

        #in App we feed flow, pass1_recovery and select stage and pass , since we know flow and filter area we can check what flux is coming
        # if flux is within range of selected type of water . also pass to be added if criteria is <10 ppm TDS

        #RO Feed Conditioning pass 1
        #Acid	Reduce scaling
        #Antiscalant	Prevent crystal formation
        #SMBS	Remove chlorine

        #This is pretreatment chemistry.

        #RO Pass 2
        #NaOH	Increase boron rejection or Ph raise
        #NaOH	EDI feed quality improvement


        #RO Chemical Dosing - Short Summary

        #SMBS Dosing: Removes free chlorine before RO membranes to prevent membrane oxidation and damage.
        #Acid Dosing (H₂SO₄/HCl): Lowers feed pH, converts bicarbonate to CO₂, reduces LSI, and prevents calcium carbonate scaling.
        #Antiscalant Dosing: Prevents formation of CaCO₃, CaSO₄, BaSO₄, SrSO₄, and silica scale, allowing higher RO recovery.
        #NaOH Dosing: Typically used before second-pass RO to raise pH and improve boron rejection.

        #LSI (Langelier Saturation Index): Predicts calcium carbonate scaling tendency.

        #LSI < 0 → Safe
        #LSI > 0 → Scaling risk

        #CCPP: Indicates calcium carbonate precipitation potential.

        #Negative → Safe
        #Positive → Scaling likely

                        #UF vs RO

        #UF:

        #Acid → Removes inorganic fouling (Fe, Mn, CaCO₃).
        #NaOH → Removes organic fouling and biofilm.
        #Focus: Fouling control.



        #RO:

        #SMBS → Removes chlorine.
        #Acid → Reduces scaling.
        #Antiscalant → Prevents crystal growth.
        #NaOH → Improves boron rejection.
        #Focus: Scaling control.

        # UF pores are bigger hence dissolved ions pass as it is hence no change in TDS, hence no reaction of Ca with hco3-
        # and concentration factor is very less, means there is no concentrate after UF filtration

        # RO pores are very small hence dissolved ions react like ca+ with hco3-, hence form caco3. therefore acid is used to lower ph
        # so that hc03- converts to co2

        # UF does not significantly concentrate dissolved salts, therefore dissolved ion scaling is usually low and chemicals
#        are mainly used for fouling control and membrane cleaning.
#
#       RO concentrates dissolved salts in the reject stream. As concentration increases, scale-forming salts may exceed
#       their solubility limits. Therefore acid is used to reduce carbonate scaling and antiscalant is used to control
#       sulfate, barium, strontium, and silica scaling.
#
#
                    #       #PRESSURE DROP##

        #FEED PRESSURE= Osmotic pressure+Net driving pressure+ permeate pressure+line pressure drop

        #Higher flux requires higher NDP.
        #Osmotic pressure is a pressure by which fresh water can go to salt water side with membrane in between.
# In RO , salt water is flowing to fresh water side with membrane in between. hence external pressure required. which is
# calculated as  :

            # External pressure (Feed pressure)= osmotic press  +NDP + DP

            # Osmotic pressur (π) = i M R T

               # π = Osmotic  pressure
               # i = van't Hoff factor
               # M = molar concentration
                #R = gas constant
               # T = temperature

                           # Feed Water
                           #    ↓
                           # Stage - 1 Concentration
                           #    ↓
                           # Stage - 1  Osmotic Pressure
                           #    ↓
                            # Stage - 1  NDP

                           #Stage - 2  Concentration
                           #    ↓
                            #Stage - 2 Osmotic  Pressure
                            # ↓
                            #Stage - 2 NDP

                            #Stage - 3  Concentration
                            #   ↓
                            #Stage - 3   Osmotic Pressure
                            #     ↓
                            #Stage - 3   NDP
