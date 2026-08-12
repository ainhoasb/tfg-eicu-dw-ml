import streamlit as st

def get_kpi_color(value, low_threshold, high_threshold, reverse=False):
    """
    Función auxiliar para determinar el color (Verde, Amarillo, Rojo)
    según umbrales dinámicos.
    """
    if reverse: # Por si en algún KPI un valor alto fuera 'bueno'
        if value >= high_threshold:
            return "#10b981", "#ecfdf5", "Bajo" # Verde
        elif value >= low_threshold:
            return "#f59e0b", "#fffbeb", "Medio" # Amarillo
        else:
            return "#ef4444", "#fef2f2", "Alto" # Rojo
    else:
        if value < low_threshold:
            return "#10b981", "#ecfdf5", "Bajo" # Verde
        elif value <= high_threshold:
            return "#f59e0b", "#fffbeb", "Medio" # Amarillo
        else:
            return "#ef4444", "#fef2f2", "Alto" # Rojo

def render_kpis(df):
    total_ingresos = len(df)
    mortalidad = (df['DiedInHospital'].sum() / total_ingresos * 100) if total_ingresos > 0 else 0
    apache_avg = df['ApacheScore'].mean() if total_ingresos > 0 else 0
    vent_pct = (df['Vent'].sum() / total_ingresos * 100) if total_ingresos > 0 else 0

    # Asignación de colores dinámicos
    color_mort, bg_mort, tag_mort = get_kpi_color(mortalidad, 8.0, 15.0)
    color_apache, bg_apache, tag_apache = get_kpi_color(apache_avg, 15.0, 25.0)
    color_vent, bg_vent, tag_vent = get_kpi_color(vent_pct, 20.0, 40.0)

    st.markdown("### Indicadores Clave del Resumen Clínico")

    col1, col2, col3, col4 = st.columns(4)

    card_base = (
        "border-radius: 12px; "
        "padding: 18px; "
        "text-align: center; "
        "box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.08); "
        "margin-bottom: 10px;"
    )

    with col1:
        st.markdown(f"""
            <div style="{card_base} background-color: #ffffff; border: 1px solid #e5e7eb; border-left: 6px solid #3b82f6;">
                <div style="color: #6b7280; font-size: 0.9rem; font-weight: 600; text-transform: uppercase;">Total Ingresos</div>
                <div style="color: #111827; font-size: 2.3rem; font-weight: 800; margin: 6px 0;">{total_ingresos:,}</div>
                <div style="color: #6b7280; font-size: 0.8rem; font-weight: 500;">Muestra total UCI</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div style="{card_base} background-color: {bg_mort}; border: 1px solid #e5e7eb; border-left: 6px solid {color_mort};">
                <div style="color: #6b7280; font-size: 0.9rem; font-weight: 600; text-transform: uppercase;">Mortalidad</div>
                <div style="color: {color_mort}; font-size: 2.3rem; font-weight: 800; margin: 6px 0;">{mortalidad:.1f}%</div>
                <div style="color: {color_mort}; font-size: 0.8rem; font-weight: 600;">Nivel {tag_mort}</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div style="{card_base} background-color: {bg_apache}; border: 1px solid #e5e7eb; border-left: 6px solid {color_apache};">
                <div style="color: #6b7280; font-size: 0.9rem; font-weight: 600; text-transform: uppercase;">APACHE Score</div>
                <div style="color: {color_apache}; font-size: 2.3rem; font-weight: 800; margin: 6px 0;">{apache_avg:.1f}</div>
                <div style="color: {color_apache}; font-size: 0.8rem; font-weight: 600;">Riesgo {tag_apache}</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div style="{card_base} background-color: {bg_vent}; border: 1px solid #e5e7eb; border-left: 6px solid {color_vent};">
                <div style="color: #6b7280; font-size: 0.9rem; font-weight: 600; text-transform: uppercase;">Ventilación Mecánica</div>
                <div style="color: {color_vent}; font-size: 2.3rem; font-weight: 800; margin: 6px 0;">{vent_pct:.1f}%</div>
                <div style="color: {color_vent}; font-size: 0.8rem; font-weight: 600;">Soporte {tag_vent}</div>
            </div>
        """, unsafe_allow_html=True)