import PyPDF2
import streamlit as st

# Cambiar la fuente personalizada y estilos
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif;
    }
    h1 {
        color: #FE7235;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Añadir el logo
st.image("https://info.criteria.es/hubfs/Criteria_Logo_RGB.png", width=200)

# Encabezado personalizado
st.markdown(
    """
    <h1>Extractor de Diplomas</h1>
    <p style="text-align: center;">Sube un archivo PDF y extrae los diplomas de los participantes ingresando sus DNIs separados por espacios.</p>
    """,
    unsafe_allow_html=True
)

# Inicializar variables de estado para PDF y DNIs
if "pdf_file" not in st.session_state:
    st.session_state.pdf_file = None
if "dni_input" not in st.session_state:
    st.session_state.dni_input = ""

# Botón para reiniciar los campos
if st.button("Nueva Extracción"):
    st.session_state.pdf_file = None
    st.session_state.dni_input = ""

# Subida de PDF
pdf_file = st.file_uploader("Cargar el archivo PDF", type=["pdf"], key="pdf_file")
st.session_state.pdf_file = pdf_file  # Guardar el archivo en el estado

# Entrada de DNIs
dni_input = st.text_area("Introduce los DNIs separados por espacios:", value=st.session_state.dni_input, key="dni_input")

# Botón para realizar la extracción
if st.button("Extraer Diplomas"):
    if st.session_state.pdf_file and dni_input:
        lista_dnis = dni_input.split()  # Divide los DNIs por espacios
        escritor = PyPDF2.PdfWriter()
        lector = PyPDF2.PdfReader(st.session_state.pdf_file)
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
        
        # Limpiar el cuadro de texto después de extraer
        st.session_state.dni_input = ""
    else:
        st.error("Por favor, carga un PDF e introduce los DNIs.")
