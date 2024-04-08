# EC2 Setup 
https://sgtbombadil.com/diy-arma-3-server-hosting-on-amazon-ec2/

# Install Arma 3 Server for Ubuntu

# Update Ubuntu
sudo apt-get update

# Install dependencies for Arma 3 and steamcmd
sudo apt-get install lib32stdc++6 lib32gcc-s1 screen -y

# Install Arma 3 User
sudo adduser arma3

# Give new user access to screen
chmod o+rw /dev/pts/0

# Switch to Arma 3 User
sudo -i -u arma3

# Create and navigate to steamcmd directory
mkdir ~/steamcmd && cd ~/steamcmd

# Download steamcmd tarball
wget http://media.steampowered.com/installer/steamcmd_linux.tar.gz

# Extract steamcmd tarball
tar -xvzf steamcmd_linux.tar.gz

# Run SteamCMD
./steamcmd.sh

# Specify Arma 3 Install Location
force_install_dir ./arma3/

# Login to Steam account on SteamCMD
login BigDaddyDong69

# Install Arma 3 dedicated server files
app_update 233780 validate

# Exit SteamCMD
exit

# Create Arma Profiles
mkdir -p ~/".local/share/Arma 3" && mkdir -p ~/".local/share/Arma 3 - Other Profiles"

# Launch Arma Server
script /dev/null
screen -S armaserver
cd arma3
./arma3server_x64 -name=server -config=server.cfg
./arma3server_x64 -name=server -mod=@mod1 -mod=@mod2 -mod=@mod3 -config=server.cfg # with mods


# Add Server Configuration
cd ~/steamcmd/arma3
nano server.cfg

# MODS
# Use WinSCP to connect to ec2 instance and move mods to "home/ubuntu/mods"

# Move mods from root user to arma 3 instance
sudo cp -r /home/ubuntu/mods /home/arma3/steamcmd/arma3/mods

# Copy Keys
sudo cp -r /home/ubuntu/mods/@<>/keys/<>.bikey /home/arma3/steamcmd/arma3/keys/<>.bikey

# rename all to lowercase
find . -depth -exec rename 's/(.*)\/([^\/]*)/$1\/\L$2/' {} \;

# transfer ownership of mods to arma3 user
chown -R arma3 /home/arma3/steamcmd/arma3/<mod-directory>

# install pip
sudo apt install python3-pip

# Give all access to arma3 user
sudo chmod 777 /home/arma3

# Connect SSH
ssh -i C:/Users/Adam/.ssh/windows-arma-server-key-openssh.ppk ubuntu@ec2-54-208-91-12.compute-1.amazonaws.com

# launch arma3 antistasi server
./arma3server_x64 -name=server -mod="mods/@antistasiultimatemod;" -mod="mods/@cbaa3;" -mod="mods/@duisquadradar;" -mod="mods/@enhancedmovement;" -mod="mods/@enhancedmovementrework;" -mod="mods/@jsrssoundmod;" -mod="mods/@jsrssoundmodrhsafrfmodpacksoundsupport;" -mod="mods/@jsrssoundmodrhsgrefmodpacksoundsupport;" -mod="mods/@jsrssoundmodrhssafmodpacksupport;" -mod="mods/@jsrssoundmodrhsusafmodpacksoundsupport" -mod=";mods/@removestamina;" -mod="mods/@rhsafrf;" -mod="mods/@rhsgref;" -mod="mods/@rhssaf;" -mod="mods/@rhsusaf;" -config=server.cfg