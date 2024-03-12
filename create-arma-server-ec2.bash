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
./arma3server -name=server -config=server.cfg

# Add Server Configuration
cd ~/steamcmd/arma3
nano server.cfg
