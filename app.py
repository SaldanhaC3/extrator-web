from flask import Flask, request, render_template, send_file, jsonify
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
import io
from urllib.parse import urlparse

app = Flask(__name__)

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def extract_data(urls):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

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

        except TimeoutException:
            title = 'ERROR: Timeout ao tentar carregar a página'
            meta_description = 'N/A'
        except WebDriverException as e:
            title = f'ERROR: Problema ao acessar a URL - {str(e)}'
            meta_description = 'N/A'
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        urls = request.form['urls'].splitlines()
        urls = [url.strip() for url in urls if is_valid_url(url.strip())]

        # Verifique se há URLs válidas
        if not urls:
            return render_template('index.html', message="Nenhuma URL válida foi fornecida.", message_class="error")

        # Limite o número de URLs a 100
        if len(urls) > 100:
            return render_template('index.html', message="O limite é de 100 URLs por extração. Você forneceu {} URLs.".format(len(urls)), message_class="error")

        # Extraia os dados das URLs válidas
        df = extract_data(urls)
        table_html = df.to_html(classes='table table-striped table-bordered', index=False)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Resultados')
        output.seek(0)

        return render_template('index.html', table_html=table_html, download_ready=True, data=output.getvalue())

    except Exception as e:
        print(f"Error: {e}")
        return render_template('index.html', message="Ocorreu um erro ao processar as URLs. Tente novamente.", message_class="error")

@app.route('/download')
def download():
    try:
        data = request.args.get('data')
        if data:
            output = io.BytesIO(data.encode())
            return send_file(output, download_name='resultados.xlsx', as_attachment=True)
        else:
            return "Nenhum dado disponível para download.", 400
    except Exception as e:
        print(f"Error: {e}")
        return "Ocorreu um erro ao tentar fazer o download.", 500

@app.route('/check_status', methods=['GET'])
def check_status():
    return jsonify(status="extraindo")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
