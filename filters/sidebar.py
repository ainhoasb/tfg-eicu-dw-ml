import streamlit as st
import os

def render_sidebar(df_general):
    with st.sidebar:
        # Logo al inicio
        logo_path = "images/logo_uci.png"
        if os.path.exists(logo_path):
            st.image(logo_path, width="stretch")
        else:
            st.title("🏥 DW Clínico")

        # Encabezado destacado
        st.markdown("""
            <div style="
                background-color: #D7DDE0; 
                border: 1px solid #D7DDE0; 
                border-radius: 10px; 
                padding: 12px 10px; 
                text-align: center; 
                margin-top: 10px;
                margin-bottom: 15px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.04);
            ">
                <span style="
                    font-size: 1.1rem; 
                    font-weight: 700; 
                    color: #295778;
                    letter-spacing: 0.5px;
                ">🔍 FILTROS GLOBALES</span>
            </div>
        """, unsafe_allow_html=True)

        #st.header("🔍 Filtros Globales")
        #st.divider()

        # Calculamos las opciones disponibles ANTES del botón,
        # porque el botón necesita conocerlas para poder restablecer.
        available_years = sorted(df_general['AdmitYear'].dropna().unique())
        raw_genders = df_general['Gender'].dropna().astype(str).str.strip()
        available_genders = sorted([g for g in raw_genders.unique() if g != ""])
        raw_ethnicities = df_general['Ethnicity'].dropna().astype(str).str.strip()
        available_ethnicities = sorted([e for e in raw_ethnicities.unique() if e != ""])
        min_age = int(df_general['Age'].min()) if not df_general['Age'].empty else 0
        max_age = int(df_general['Age'].max()) if not df_general['Age'].empty else 100
        regions = sorted(df_general['Region'].dropna().unique())
        unit_types = sorted(df_general['UnitType'].dropna().unique())
        services = sorted(df_general['Service'].dropna().unique())

        # Botón de Restablecer filtros
        if st.button("🔄 Restablecer filtros", use_container_width=True):
            for year in available_years:
                st.session_state[f"year_{year}"] = True
            for _, valor in opciones_estado:
                st.session_state[f"died_{valor}"] = True
            for gender in available_genders:
                st.session_state[f"gender_{gender}"] = True
            st.session_state["ethnicities_filter"] = available_ethnicities
            st.session_state["regions_filter"] = regions
            st.session_state["units_filter"] = unit_types
            st.session_state["services_filter"] = services
            st.session_state["age_range_filter"] = (min_age, max_age)
            st.rerun()

        st.divider()

        # Filtro de Año mediante Checkboxes
        st.subheader("⌛ Año de Ingreso")
        available_years = sorted(df_general['AdmitYear'].dropna().unique())
        selected_years = []
        for year in available_years:
            if st.checkbox(str(int(year)), value=True, key=f"year_{year}"):
                selected_years.append(year)

        st.divider()

        st.subheader("❤️ Estado al Alta")
        opciones_estado = [("Egreso vivo", 0), ("Fallecido", 1)]
        selected_died = []
        for etiqueta, valor in opciones_estado:
            if st.checkbox(etiqueta, value=True, key=f"died_{valor}"):
                selected_died.append(valor)

        st.divider()

        # 2. Filtro de Género mediante Checkboxes
        st.subheader("👤 Género")
        raw_genders = df_general['Gender'].dropna().astype(str).str.strip()
        available_genders = sorted([g for g in raw_genders.unique() if g != ""])
        
        selected_genders = []
        for gender in available_genders:
            if st.checkbox(gender, value=True, key=f"gender_{gender}"):
                selected_genders.append(gender)

        st.divider()

        # Filtro de Etnicidad
        st.subheader("🧬 Etnicidad")
        selected_ethnicities = st.multiselect(
            "Seleccionar etnicidad:",
            options=available_ethnicities,
            default=available_ethnicities,
            key="ethnicities_filter",
        )

        st.divider()

        # Filtro por Rango de Edad
        st.subheader("📅 Rango de Edad")
        selected_age_range = st.slider(
            "Seleccionar edades:",
            min_value=min_age,
            max_value=max_age,
            value=(min_age, max_age),
            key="age_range_filter",
        )

        st.divider()

        # Filtro por Región y Tipo de Unidad
        st.subheader("🌍 Ubicación y Servicio")
        selected_regions = st.multiselect("Región", regions, default=regions, key="regions_filter")
        selected_units = st.multiselect("Tipo de Unidad", unit_types, default=unit_types, key="units_filter")
        selected_services = st.multiselect("Área Clínica (Service)", services, default=services, key="services_filter")


    return {
        "years": selected_years,
        "genders": selected_genders,
        "age_range": selected_age_range,
        "ethnicities": selected_ethnicities,
        "regions": selected_regions,
        "units": selected_units,
        "services": selected_services,
        "died_in_hospital": selected_died,
    }