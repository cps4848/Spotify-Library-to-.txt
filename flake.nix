{
  description = "flake for spotify dumper";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-22.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem(system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
        python-pkgs = p: with p; [
          poetry-core
        ];
      in
      with pkgs;
      {
        devShells.default = pkgs.mkShell rec {
          nativeBuildInputs = [
          ];
          
          buildInputs = [
            python38
            poetry
          ];
        };
      }
    );
}
