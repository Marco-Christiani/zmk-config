{
  description = "Glove80 ZMK firmware build";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
    zmk.url = "github:moergo-sc/zmk";
    zmk.flake = false;
  };

  outputs = {
    self,
    nixpkgs,
    zmk,
  }: let
    system = "x86_64-linux";
    pkgs = import nixpkgs {inherit system;};

    firmware = import zmk {inherit pkgs;};

    config = ./config;

    glove80_left = firmware.zmk.override {
      board = "glove80_lh";
      keymap = "${config}/glove80.keymap";
      kconfig = "${config}/glove80.conf";
    };

    glove80_right = firmware.zmk.override {
      board = "glove80_rh";
      keymap = "${config}/glove80.keymap";
      kconfig = "${config}/glove80.conf";
    };
  in {
    packages.${system}.default =
      firmware.combine_uf2 glove80_left glove80_right;
  };
}
