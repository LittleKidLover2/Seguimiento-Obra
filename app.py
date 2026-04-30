import streamlit as st
import pandas as pd
from datetime import date
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Configuración de la página
st.set_page_config(page_title="Seguimiento de Obra", layout="centered")

# --- 1. LOGO DE LA EMPRESA ---
# Asegúrate de tener un archivo 'logo.png' en tu repositorio de GitHub
try:
    st.image("logo.png", width=200)
except:
    st.warning("⚠️ No se encontró el archivo 'logo.png'. Por favor, súbelo a GitHub.")

st.title("🏗️ Control de Seguimiento de Obra")

# --- 2. FORMULARIO DE DATOS ---
with st.form("form_registro", clear_on_submit=True):
    # Nombre del trabajador y Fecha
    col1, col2 = st.columns(2)
    with col1:
        trabajador = st.text_input("Nombre del Trabajador")
    with col2:
        fecha = st.date_input("Fecha de envío", value=date.today())

    # Desplegable de Tareas
    tareas = [
        "Trazado y marcado de cajas, tubos y cuadros", "Ejecución rozas en paredes y techos",
        "Montaje de soportes", "Colocación tubos y conductos", "Tendido de cables",
        "Identificación y etiquetado", "Conexionado de cables en bornes o regletas",
        "Instalación y conexionado de mecanismos", "Fijación de carril DIN y mecanismos en cuadro eléctrico",
        "Cableado interno del cuadro eléctrico", "Configuración de equipos domóticos y/o automáticos",
        "Conexionado de sensores/actuadores de equipos domóticos/automáticos", "Pruebas de continuidad",
        "Pruebas de aislamiento", "Verificación de tierras", "Programación del automatismo",
        "Pruebas de funcionamiento"
    ]
    tarea_seleccionada = st.selectbox("Seleccionar Tarea:", tareas)

    # Desplegable de Estado
    estados = [
        "Avance de la tarea en torno al 25% aprox.", "Avance de la tarea en torno al 50% aprox.",
        "Avance de la tarea en torno al 75% aprox.", "OK, finalizado sin errores",
        "Finalizado, pero con errores pendientes de corregir", "Finalizado y corregidos los errores"
    ]
    estado_seleccionado = st.selectbox("Estado de la tarea:", estados)

    submit = st.form_submit_button("Registrar Datos")

# --- 3. GESTIÓN DE DATOS (EXCEL) ---
# Inicializamos el historial en la sesión del navegador
if 'historial' not in st.session_state:
    st.session_state['historial'] = pd.DataFrame(columns=["Fecha", "Trabajador", "Tarea", "Estado"])

if submit:
    nuevo_registro = {
        "Fecha": str(fecha),
        "Trabajador": trabajador,
        "Tarea": tarea_seleccionada,
        "Estado": estado_seleccionado
    }
    st.session_state['historial'] = pd.concat([st.session_state['historial'], pd.DataFrame([nuevo_registro])], ignore_index=True)
    st.success("✅ Registro añadido correctamente.")

# Mostrar tabla actual
st.subheader("Registros Actuales")
st.dataframe(st.session_state['historial'])

# --- 4. DESCARGA Y ENVÍO POR EMAIL ---
if not st.session_state['historial'].empty:
    
    # Crear Excel en memoria
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        st.session_state['historial'].to_excel(writer, index=False, sheet_name='Seguimiento')
    excel_data = output.getvalue()

    # Botón Descargar
    st.download_button(
        label="📥 Descargar Excel",
        data=excel_data,
        file_name=f"seguimiento_obra_{date.today()}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Sección de Envío por Email
    st.divider()
    st.subheader("📧 Enviar reporte por Correo")
    email_destino = "fmo@fundacionmasaveu.com" # Definida por la empresa
    
    if st.button("Enviar Excel a la Empresa"):
        # NOTA: Para que esto funcione en producción, debes configurar Secrets en Streamlit Cloud
        # con las credenciales de un servidor SMTP (Gmail, Outlook, etc.)
        st.info(f"Simulando envío a: {email_destino}")
        # Aquí iría la lógica smtplib utilizando st.secrets["email_user"] y st.secrets["password"]
        st.success("Correo enviado con éxito (Simulación)")
