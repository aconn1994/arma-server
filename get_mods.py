#!/usr/bin/python3

import os
import argparse
from bs4 import BeautifulSoup
import pandas
import re
from pysteamcmdwrapper import SteamCMD, SteamCMDException
import subprocess

def parse_args():
    argp = argparse.ArgumentParser()
    argp.add_argument(
        '-mf', '--mod-file',
        help='Specify the name of Arma 3 mod file to use; Comes from Arma 3 Client Launcher'
    )

    return argp.parse_args()

# Parses/Formats an HTML Mod file exported from the Arma 3 Client Launcher
def get_mod_list(file_name):
    mod_file = open(file_name, 'r')
    mod_file_parsed = BeautifulSoup(mod_file, 'html.parser')
    container_table = mod_file_parsed.body.div.table
    container_items = container_table.find_all('tr')
    dataDi = {
        'mod_name': [],
        'id': [],
        'link': [],
        'for_mod_name': []
    }

    for item in container_items:
        mod_link = item.find('a')['href']
        mod_link_split = mod_link.split('=')
        mod_name = str(item.td.string)
        dataDi['mod_name'].append(mod_name)
        dataDi['id'].append(mod_link_split[1])
        dataDi['link'].append(mod_link)
        dataDi['for_mod_name'].append(mod_name.lower())
    
    return pandas.DataFrame(dataDi)

# Format mod name for Linux processing
def format_mod_name(name):
    return re.sub('[^A-Za-z0-9]+', '', name)


# Download mods from Steam Workshop from Mod List and configure for server use
def mod_handler(steamcmd, mod):

    mod_name = mod['mod_name']
    mod_id = mod['id']

    # Download Mod
    print(f'Downloading {mod_name} From List...')
    steamcmd.workshop_update(107410, mod_id, os.path.join(os.getcwd(), 'steamcmd', 'arma3'), validate=True)

# Link Mods and Keys to Server directories
def link_mods(mod, LOCAL_MOD_DIR, STEAM_DOWNLOAD_DIR, LOCAL_KEYS_DIR):

    mod_name = mod['mod_name']
    mod_id = mod['id']
    for_mod_name = mod['for_mod_name']

    print(f'Linking Mod and Key for {mod_name}...')

    # Format mod name
    formatted_mod_name = format_mod_name(for_mod_name)

    # Link Mod Directory to Game Mod Folder
    try:
        os.symlink(os.path.join(STEAM_DOWNLOAD_DIR, mod_id), os.path.join(LOCAL_MOD_DIR, f'@{formatted_mod_name}'))
    except FileExistsError:
        print('Mod already Linked')

    # Link Mod Keys to Game Keys Folder
    MOD_KEYS_DIR = os.path.join(LOCAL_MOD_DIR, f'@{formatted_mod_name}', 'keys')
    if not os.path.isdir(MOD_KEYS_DIR):
        MOD_KEYS_DIR = os.path.join(LOCAL_MOD_DIR, f'@{formatted_mod_name}', 'key')
    
    for key in os.listdir(MOD_KEYS_DIR):
        print('Linking ', key)
        try:
            os.symlink(os.path.join(MOD_KEYS_DIR, key), os.path.join(LOCAL_KEYS_DIR, key))
        except FileExistsError:
            print('Key Already Linked')


def build_launch_file(mod_list_df):
    print('Building launch file...')
    search_text = 'mods='
    replace_text = 'mods='

    i = 0
    mod_list_length = mod_list_df.shape[0]
    while (i < mod_list_length):
        formatted_mod_name = format_mod_name(mod_list_df.iloc[i]['for_mod_name'])
        # print(formatted_mod_name)
        replace_text = f'{replace_text}mods/@{formatted_mod_name};'
        i = i + 1

    print('Replace Text: ', replace_text)

    with open(os.path.join(os.getcwd(), 'steamcmd', 'arma3', 'launch.sh'), 'r') as launch_file:
        launch_file_lines = launch_file.readlines()
        # print(launch_file_lines)
        for line in launch_file_lines:
            if (search_text in line):
                line_num = launch_file_lines.index(line)
                new_launch_file_lines = launch_file_lines
                new_launch_file_lines[line_num] = replace_text + '\n'
        # print(new_launch_file_lines)
    
    with open(os.path.join(os.getcwd(), 'steamcmd', 'arma3', 'launch.sh'), 'w') as new_launch_file:
        new_launch_file.writelines(new_launch_file_lines)


    

def main():
    # Set paths
    LOCAL_MOD_DIR = os.path.join(os.getcwd(), 'steamcmd', 'arma3', 'mods')
    LOCAL_KEYS_DIR = os.path.join(os.getcwd(), 'steamcmd', 'arma3', 'keys')
    STEAM_DOWNLOAD_DIR = os.path.join(os.getcwd(), 'steamcmd', 'arma3', 'steamapps', 'workshop', 'content', '107410')
    print(LOCAL_MOD_DIR)
    print(LOCAL_KEYS_DIR)
    print(STEAM_DOWNLOAD_DIR)

    # Configure Mod List
    args = parse_args()
    mod_file = f'{args.mod_file}.html'
    mod_list_df = get_mod_list(mod_file)
    
    # Config SteamCMD
    s = SteamCMD("steamcmd")
    try:
        s.install()
    except SteamCMDException:
        print("SteamCMD already installed")

    s.login()

    # # Download Mods
    i = 0
    mod_list_length = mod_list_df.shape[0]
    while (i < mod_list_length): # change to mod_list_length
        mod_handler(s, mod_list_df.iloc[i])
        i = i + 1
    
    # Rename all files to lowercase
    subprocess.call(['sh', './handle_mods.sh'])

    # Link Mods and Keys for Server Use
    i = 0
    while (i < mod_list_length): # change to mod_list_length
        link_mods(mod_list_df.iloc[i], LOCAL_MOD_DIR, STEAM_DOWNLOAD_DIR, LOCAL_KEYS_DIR)
        i = i + 1
    
    # Build server launch file
    build_launch_file(mod_list_df)

if __name__ == '__main__':
    main()