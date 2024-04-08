#!/bin/bash
# Wrapper file to start the A3 server

# Server Name
server=server

# Server mods
mods=mods/@antistasiultimatemod;mods/@cbaa3;mods/@duisquadradar;mods/@enhancedmovement;mods/@enhancedmovementrework;mods/@jsrssoundmod;mods/@jsrssoundmodrhsafrfmodpacksoundsupport;mods/@jsrssoundmodrhsgrefmodpacksoundsupport;mods/@jsrssoundmodrhssafmodpacksupport;mods/@jsrssoundmodrhsusafmodpacksoundsupport;mods/@removestamina;mods/@rhsafrf;mods/@rhsgref;mods/@rhssaf;mods/@rhsusaf;

# Config File Name
config=server.cfg

# Start Server
./arma3server_x64 -name=$server -mod=$mods -config=$config
