{ pkgs }: {
  deps = [
    pkgs.python310Full
    pkgs.streamlit
  ];

  # Isso faz com que o Replit rode o Streamlit na porta 8501 automaticamente
  postBuild = ''
    streamlit run app.py --server.port 8501
  '';
}
