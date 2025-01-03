# To learn more about how to use Nix to configure your environment
# see: https://developers.google.com/idx/guides/customize-idx-env
{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-23.11"; # or "unstable"
  services.docker.enable=true;
  # Use https://search.nixos.org/packages to find packages
  packages = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.docker
  ];

  # Sets environment variables in the workspace
  env = {};
  idx = {
    # Search for the extensions you want on https://open-vsx.org/ and use "publisher.id"
    extensions = [
      "ms-python.python"
      "ms-azuretools.vscode-docker"
      "ms-python.debugpy"
    ];

    # Workspace lifecycle hooks
    workspace = {
      onCreate = {
        create-env-file = "cp .env.sample .env";
      };
      onStart = {
        docker-build = "docker compose build";
      };
    };
  };
}
