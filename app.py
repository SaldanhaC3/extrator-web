import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from urllib.parse import urlparse
import io

# Função para validar URLs
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# Função para extrair dados das URLs
def extract_data(urls):
    chromedriver_autoinstaller.install()  # Instala o Chromedriver automaticamente
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)

    titles = []
    meta_descriptions = []

    for url in urls:
        try:
            driver.get(url)
            driver.implicitly_wait(10)
            title = driver.title
            try:
                meta_description = driver.find_element(By.CSS_SELECTOR, "meta[name='description']").get_attribute("content")
            except:
                meta_description = 'Meta description não encontrada'

        except Exception as e:
            title = f'ERROR: {str(e)}'
            meta_description = 'N/A'

        titles.append(title)
        meta_descriptions.append(meta_description)

    driver.quit()

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
