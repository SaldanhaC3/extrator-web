{ pkgs }: {
  deps = [
    pkgs.geckodriver
    pkgs.glibcLocales
    pkgs.python310Full
    pkgs.poetry
    pkgs.chromedriver
    pkgs.chromium
  ];
}
