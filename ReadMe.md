# Extrator de Títulos e Meta Descriptions

Este projeto é uma aplicação web para extrair títulos e meta descriptions de URLs fornecidas. A aplicação é construída em Flask e usa Selenium para processar as páginas web.

## Funcionalidades

- Extração de títulos e meta descriptions de uma lista de URLs.
- Visualização dos resultados em uma tabela interativa.
- Download dos resultados em formato Excel (.xlsx).

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/extrator-web.git
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd extrator-web
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute a aplicação:
   ```bash
   python app.py
   ```

## Uso

1. Acesse `http://127.0.0.1:8080` no seu navegador.
2. Cole as URLs que você deseja processar no campo de texto.
3. Clique em "Extrair Informações" e visualize os resultados.
4. Faça o download do arquivo Excel se estiver satisfeito com os resultados.

## Contribuição

Se você deseja contribuir para este projeto, siga os passos abaixo:
- Fork o repositório.
- Crie um branch para a sua feature (`git checkout -b feature/nova-feature`).
- Faça o commit das suas mudanças (`git commit -m 'Adiciona nova feature'`).
- Envie o branch para o GitHub (`git push origin feature/nova-feature`).
- Abra um Pull Request.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
