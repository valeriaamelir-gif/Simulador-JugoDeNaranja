import streamlit as st
import os
import matplotlib.pyplot as plt

# Título de tu sección en la web del equipo
st.subheader("Módulo 3 y 4: Tamizado y Enfriamiento")
st.markdown("---")

# ==========================================
# 1. CONTROLES DESLIZANTES (Sliders de Entrada)
# ==========================================
st.sidebar.header("Parámetros: Tamizado y Enfriamiento")

# Entradas para Tamizado
m_jugo_crudo = st.sidebar.slider("Flujo de Entrada ($\dot{m}_{in}$) [kg/h]", 100.0, 1500.0, 580.0, 10.0)
x_pulpa_in = st.sidebar.slider("Fracción de Pulpa Inicial ($x_{pulpa}$)", 0.05, 0.20, 0.12, 0.01)
eficiencia_tamiz = st.sidebar.slider("Eficiencia de Retención del Tamiz", 0.50, 0.98, 0.85, 0.01)

# Entradas para Enfriamiento
T_in = st.sidebar.slider("Temperatura de Entrada [°C]", 20.0, 40.0, 28.0, 0.5)
T_out = st.sidebar.slider("Temperatura de Salida Deseada [°C]", 2.0, 15.0, 5.0, 0.5)

# ==========================================
# 2. MODELO DE CÁLCULO (Balances)
# ==========================================
# Balance Tamizado
m_pulpa_residuo = m_jugo_crudo * x_pulpa_in * eficiencia_tamiz
m_jugo_refinado = m_jugo_crudo - m_pulpa_residuo
x_pulpa_final = ((x_pulpa_in * m_jugo_crudo) - m_pulpa_residuo) / m_jugo_refinado if m_jugo_refinado > 0 else 0.0

# Balance Enfriamiento
Cp_jugo = 3.93  # kJ/(kg·°C)
Q_kJ_h = m_jugo_refinado * Cp_jugo * (T_in - T_out)
Q_kW = Q_kJ_h / 3600.0

# ==========================================
# 3. INTERFAZ VISUAL E IMÁGENES DE LOS EQUIPOS
# ==========================================
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 3. Unidad de Tamizado")
    
    # Carga de la imagen local del tamiz
    ruta_tamiz = "img/tamiz.png"
    if os.path.exists(ruta_tamiz):
        st.image(ruta_tamiz, caption="Tamiz vibratorio industrial", use_column_width=True)
    else:
        st.info("💡 Coloca tu imagen del tamiz en la ruta: `img/tamiz.png`")
        
    st.metric(label="Flujo Refinado Obtenido", value=f"{m_jugo_refinado:.2f} kg/h")
    st.metric(label="Residuo Separado", value=f"{m_pulpa_residuo:.2f} kg/h")
    st.write(f"**Fracción de pulpa final:** {x_pulpa_final*100:.2f}%")

with col2:
    st.markdown("### 4. Unidad de Enfriamiento")
    
    # Carga de la imagen local del enfriador
    ruta_enfriador = "img/enfriador.png"
    if os.path.exists(ruta_enfriador):
        st.image(ruta_enfriador, caption="Intercambiador de calor de placas", use_column_width=True)
    else:
        st.info("💡 Coloca tu imagen del enfriador en la ruta: `img/enfriador.png`")
        
    st.metric(label="Carga Térmica del Sistema", value=f"{Q_kW:.2f} kW")
    st.metric(label="Temperatura de Salida", value=f"{T_out} °C")

st.markdown("---")

# ==========================================
# 4. GRÁFICAS EN VIVO
# ==========================================
st.markdown("### 📊 Gráficas de Resultados en Tiempo Real")
g_col1, g_col2 = st.columns(2)

with g_col1:
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.bar(['Entrada Crudo', 'Flujo Refinado', 'Residuo'], [m_jugo_crudo, m_jugo_refinado, m_pulpa_residuo], color=['#ff9933', '#66b3ff', '#99ff99'])
    ax.set_ylabel("kg/h")
    ax.set_title("Balance en Tamizado")
    st.pyplot(fig)

with g_col2:
    fig2, ax2 = plt.subplots(figsize=(4, 3))
    ax2.bar(['Entrada', 'Salida'], [T_in, T_out], color=['#ff6666', '#3399ff'])
    ax2.set_ylabel("°C")
    ax2.set_title("Perfil Térmico (Enfriamiento)")
    st.pyplot(fig2)
# ==========================================
# 5. ARTÍCULO TÉCNICO
# ==========================================
st.markdown("---")
st.markdown("### 📄 Artículo Técnico del Proceso")

# Opción para poner el botón de descarga del PDF de Canva
import os
ruta_pdf = "img/articulo.pdf"

if os.path.exists(ruta_pdf):
    with open(ruta_pdf, "rb") as f:
        pdf_bytes = f.read()
    st.download_button(
        label="📥 Descargar Artículo Técnico (PDF)",
        data=pdf_bytes,
        file_name="Articulo_Tamizado_y_Enfriamiento.pdf",
        mime="application/pdf"
    )
else:
    st.info("💡 Sube tu archivo PDF a la carpeta `img/` con el nombre: `articulo.pdf` para habilitar el botón de descarga.")
