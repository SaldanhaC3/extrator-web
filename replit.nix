{ pkgs }: {
  deps = [
    pkgs.python310Full
    pkgs.chromedriver
    pkgs.chromium
  ];

  preBuild = ''
    pip install -r requirements.txt
  '';
}
