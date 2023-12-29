FROM nixos/nix:latest
RUN mkdir /app
WORKDIR /app
RUN git clone https://github.com/moergo-sc/zmk src
# ENTRYPOINT [ "nix-build", "config", "-o", "config/combined" ]
ENTRYPOINT ["sh", "-c", "nix-build config -o config/combined && cp -Lr config/combined/glove80.uf2 config/"]
