import PyPDF2
import streamlit as st

# Cambiar la fuente personalizada
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Añadir el logo
st.image("https://upload.wikimedia.org/wikipedia/commons/a/ab/Logo_TV_2015.png", width=150)

# Encabezado personalizado
st.markdown(
    """
    <h1 style="text-align: center; color: #4CAF50;">Extractor de Diplomas</h1>
    <p style="text-align: center;">Sube un archivo PDF y extrae los diplomas de los participantes ingresando sus DNIs separados por espacios.</p>
    """,
    unsafe_allow_html=True
)

# Inicializar variables de estado para reiniciar los campos
if "reset" not in st.session_state:
    st.session_state.reset = False

# Reiniciar los campos si se hace clic en "Nueva Extracción"
if st.session_state.reset:
    pdf_file = None
    dni_input = ""
    st.session_state.reset = False
else:
    pdf_file = st.file_uploader("Cargar el archivo PDF", type=["pdf"])
    dni_input = st.text_area("Introduce los DNIs separados por espacios:")

# Botón para realizar la extracción
if st.button("Extraer Diplomas"):
    if pdf_file and dni_input:
        lista_dnis = dni_input.split()  # Divide los DNIs por espacios
        escritor = PyPDF2.PdfWriter()
        lector = PyPDF2.PdfReader(pdf_file)
        paginas_por_dni = []

        for i, pagina in enumerate(lector.pages):
            texto = pagina.extract_text()
            for dni in lista_dnis:
                if dni.strip() in texto:
                    paginas_por_dni.append(i)
                    if i + 1 < len(lector.pages):
                        paginas_por_dni.append(i + 1)
                    break

        paginas_por_dni = sorted(set(paginas_por_dni))
        for pagina in paginas_por_dni:
            escritor.add_page(lector.pages[pagina])

        with open("resultado.pdf", "wb") as salida:
            escritor.write(salida)
        
        st.success("¡Diplomas extraídos!")
        st.download_button("Descargar el PDF", data=open("resultado.pdf", "rb"), file_name="diplomas_filtrados.pdf")
    else:
        st.error("Por favor, carga un PDF e introduce los DNIs.")

# Botón para reiniciar el formulario
if st.button("Nueva Extracción"):
    st.session_state.reset = True
    st.experimental_rerun()
