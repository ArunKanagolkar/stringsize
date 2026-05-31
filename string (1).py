#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import math

st.set_page_config(page_title="Solar String Designer", layout="wide")

st.title("☀️ Solar String Designer")

col1, col2 = st.columns(2)

with col1:
    st.subheader("PV Module Data")

    Vmp = st.number_input("Vmp (V)", value=41.1)
    Imp = st.number_input("Imp (A)", value=13.14)
    Voc = st.number_input("Voc (V)", value=49.5)
    Isc = st.number_input("Isc (A)", value=13.89)

    Alpha_Voc = st.number_input("Voc Temp Coefficient (%/°C)", value=-0.28)
    Gamma_Vmp = st.number_input("Vmp Temp Coefficient (%/°C)", value=-0.36)
    Beta_Isc = st.number_input("Isc Temp Coefficient (%/°C)", value=0.05)

with col2:
    st.subheader("Inverter Data")

    Vmppt_min = st.number_input("MPPT Min Voltage (V)", value=200.0)
    Vmppt_max = st.number_input("MPPT Max Voltage (V)", value=1000.0)
    Vdc_max = st.number_input("Max DC Voltage (V)", value=1100.0)
    Idc_max = st.number_input("Max MPPT Current (A)", value=26.0)

    Tmin = st.number_input("Minimum Ambient Temperature (°C)", value=5.0)
    Tmax = st.number_input("Maximum Cell Temperature (°C)", value=75.0)

if st.button("Calculate String Design"):

    Voc_Tmin = Voc * (1 + (Alpha_Voc/100)*(Tmin-25))
    Vmp_Tmax = Vmp * (1 + (Gamma_Vmp/100)*(Tmax-25))
    Isc_Tmax = Isc * (1 + (Beta_Isc/100)*(Tmax-25))
    Imp_Tmax = Imp * (1 + (Beta_Isc/100)*(Tmax-25))

    Nmin = math.ceil(Vmppt_min / Vmp_Tmax)
    Nmax = math.floor(Vdc_max / Voc_Tmin)

    Nparallel = math.floor(Idc_max / Imp_Tmax)

    st.header("Results")

    c1, c2, c3 = st.columns(3)

    c1.metric("Voc @ Tmin", f"{Voc_Tmin:.2f} V")
    c2.metric("Vmp @ Tmax", f"{Vmp_Tmax:.2f} V")
    c3.metric("Max Parallel Strings", Nparallel)

    st.success(f"Minimum Modules in Series : {Nmin}")
    st.success(f"Maximum Modules in Series : {Nmax}")

    recommended = round((Nmin + Nmax)/2)

    st.info(
        f"Recommended String Configuration: "
        f"{recommended} Modules in Series × "
        f"{Nparallel} Parallel Strings / MPPT"
    )

    string_voc = recommended * Voc_Tmin
    string_vmp = recommended * Vmp_Tmax

    st.subheader("Design Verification")

    st.write(f"String Voc = {string_voc:.2f} V")
    st.write(f"String Vmp = {string_vmp:.2f} V")

    if string_voc < Vdc_max:
        st.success("✓ Voc within inverter limit")
    else:
        st.error("✗ Voc exceeds inverter limit")

    if Vmppt_min < string_vmp < Vmppt_max:
        st.success("✓ Vmp within MPPT range")
    else:
        st.error("✗ Vmp outside MPPT range")


# In[ ]:




