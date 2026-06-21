{
  description = "yt-dlp-cli";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, flake-utils, nixpkgs }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            python313
            uv
            self.packages.${system}.default
          ];
          shellHook = ''
            uv sync
          '';
        };

        packages = rec {
          default = yt-dlp-cli;
          yt-dlp-cli = pkgs.python313Packages.buildPythonApplication {
            pname = "yt-dlp-cli";
            version = "0.1.0";
            src = ./.;
            pyproject = true;
            build-system = with pkgs.python313Packages; [
              setuptools
            ];
            propagatedBuildInputs = [
              click
              pkgs.python313Packages.yt-dlp
            ];
          };
          click = pkgs.python313Packages.buildPythonPackage rec {
            pname = "click";
            version = "8.4.1";
            pyproject = true;
            build-system = with pkgs.python313Packages; [
              flit-core
            ];
            src = pkgs.fetchPypi {
              inherit pname version;
              hash = "sha256-kYtWM+3fa0HDLU9FS/DegQBlx04/fb+O5UUvi+iNPpY=";
            };
          };
        };
      }
    );
}
