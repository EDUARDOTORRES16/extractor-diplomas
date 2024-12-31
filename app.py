import PyPDF2
import streamlit as st

def extraer_diplomas(pdf_file, lista_dnis):
    lector = PyPDF2.PdfReader(pdf_file)
    escritor = PyPDF2.PdfWriter()
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
    
    return escritor

# Interfaz con Streamlit
st.title("Extractor de Diplomas")
pdf_file = st.file_uploader("Cargar el archivo PDF", type=["pdf"])
dni_input = st.text_area("Introduce los DNIs separados por espacios:")
if st.button("Extraer Diplomas"):
    if pdf_file and dni_input:
        lista_dnis = dni_input.split()  # Divide los DNIs por espacios
        escritor = extraer_diplomas(pdf_file, lista_dnis)
        with open("resultado.pdf", "wb") as salida:
            escritor.write(salida)
        st.success("¡Diplomas extraídos!")
        st.download_button("Descargar el PDF", data=open("resultado.pdf", "rb"), file_name="diplomas_filtrados.pdf")
    else:
        st.error("Por favor, carga un PDF e introduce los DNIs.")
