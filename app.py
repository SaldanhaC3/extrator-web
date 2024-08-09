import streamlit as st
import pandas as pd
from requests_html import HTMLSession
from urllib.parse import urlparse
import io

# Função para validar URLs
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# Função para extrair dados das URLs com JavaScript renderizado
def extract_data(urls):
    session = HTMLSession()
    titles = []
    meta_descriptions = []

    for url in urls:
        try:
            response = session.get(url)
            response.html.render(timeout=20)  # Renderiza o JavaScript

            # Extrai o título da página
            title = response.html.find('title', first=True).text if response.html.find('title', first=True) else 'Título não encontrado'

            # Extrai a meta descrição
            meta = response.html.find('meta[name="description"]', first=True)
            meta_description = meta.attrs['content'] if meta else 'Meta description não encontrada'

        except Exception as e:
            title = f'ERROR: {str(e)}'
            meta_description = 'N/A'

        titles.append(title)
        meta_descriptions.append(meta_description)

    df = pd.DataFrame({
        'URL': urls,
        'Title': titles,
        'Meta Description': meta_descriptions
    })

    return df

# Interface do Streamlit
st.title("Extrator de Títulos e Meta Descriptions")
st.write("""
    Esta ferramenta permite a extração de títulos e meta descriptions de múltiplas páginas web. 
    Insira as URLs abaixo para gerar um relatório.
""")

# Entrada de URLs pelo usuário
urls = st.text_area("Cole as URLs aqui (uma por linha):")

if st.button("Extrair Informações"):
    urls_list = [url.strip() for url in urls.splitlines() if is_valid_url(url.strip())]

    if len(urls_list) == 0:
        st.error("Nenhuma URL válida foi fornecida.")
    elif len(urls_list) > 100:
        st.error(f"O limite é de 100 URLs por extração. Você forneceu {len(urls_list)} URLs.")
    else:
        df = extract_data(urls_list)
        st.dataframe(df)

        # Prepara o arquivo Excel para download
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Resultados')
        buffer.seek(0)

        st.download_button(
            label="📥 Baixar Resultados",
            data=buffer,
            file_name="resultados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
