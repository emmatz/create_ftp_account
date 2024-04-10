#!/usr/bin/env python3
# With this script we can add new users to Filezilla Server configuration file (FileZilla Server 0.9.60 Beta).
# Default configuration file --> 'FileZilla Server.xml'
#
# developed by: emmatz
#
# version: 1.4 4/Apr/2023 - Allow to FTP account to delete files

import hashlib
import string
import secrets
import os
import shutil
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
import subprocess

main_dir = r'c:\your_path'
backup_directory = r'C:\Program Files (x86)\FileZilla Server\conf_backup'
f_xml_file = r'C:\Program Files (x86)\FileZilla Server\FileZilla Server.xml'


def makeBackup(file):
    """
    This function needs the file to be backup as parameter and creates a copy it

    :param file: FileZilla server configuration file
    :return: None
    """

    day_of_backup = datetime.now().strftime("_%m_%d_%y_%H%M%S")

    if not os.path.exists(backup_directory):
        os.mkdir(backup_directory)
        logspa(f'New directory created: {backup_directory}')

    if os.path.isfile(file):
        shutil.copy2(file, os.path.join(backup_directory, os.path.basename(file).split(".")[0] + day_of_backup + ".xml"))
        logspa(f'Backup created "FileZilla Server{day_of_backup}.xml"')
    else:
        print(f'Configuration file not found.')
        logspa(f'Configuration file not found.')
        sys.exit(3)


def homeDirectory(user):
    """
    Build a directory tree (if not exist) for the user

    :param user: FTP username
    :return: User home
    """

    dir = os.path.join(main_dir, user.upper())
    if not os.path.exists(dir):
        os.mkdir(dir)
        logspa(f'New directory "{user.upper()}" created in {main_dir}')
    else:
        logspa(f'Home directory of "{user.upper()}" exists in {main_dir}. Checking subfolders.')

    for subd in ["subdir_1", "subdir_2", "subdir_3"]:
        dir2 = os.path.join(main_dir, user.upper(), subd)
        if not os.path.exists(dir2):
            os.mkdir(dir2)
            logspa(f'New directory "{subd}" created in {dir}')
        else:
            logspa(f'Directory "{subd}" exists in {dir}')
    return dir


def accountData(account):
    """
    Generates the information needed for the FTP user account
    :param account: FTP username
    :return: USER, PASSWORD, SALT and HASH
    """
    user = account
    alphabet = string.printable[0:-6]
    salt = "".join(secrets.SystemRandom().choice(alphabet) for _ in range(80))
    password = ''.join(secrets.choice(alphabet) for i in range(20))
    tmp_info = password + salt
    hash = hashlib.sha512(tmp_info.encode("utf-8")).hexdigest().upper()

    return user, password, salt, hash


def addUserInfo(file, username, user_salt, user_hash, user_home):
    """
    Appends the information needed in FileZilla server configuration file
    :param file: FileZilla XML configuration file.
    :param username: FTP username account.
    :param user_salt: SALT.
    :param user_hash: password encrypted
    :param user_home: User home directory
    :return:
    """

    tree = ET.parse(file)
    root = tree.getroot()
    node = ET.Element('Users')

    new_user = ET.SubElement(node, 'User', Name=username.upper())
    new_user_option = ET.SubElement(new_user, 'Option', Name='Pass')
    new_user_option.text = user_hash
    new_user_option = ET.SubElement(new_user, 'Option', Name='Salt')
    new_user_option.text = user_salt
    new_user_option = ET.SubElement(new_user, 'Option', Name='Group')
    new_user_option.text = ''
    new_user_option = ET.SubElement(new_user, 'Option', Name='Bypass server userlimit')
    new_user_option.text = '0'
    new_user_option = ET.SubElement(new_user, 'Option', Name='User Limit')
    new_user_option.text = '0'
    new_user_option = ET.SubElement(new_user, 'Option', Name='IP Limit')
    new_user_option.text = '0'
    new_user_option = ET.SubElement(new_user, 'Option', Name='Enabled')
    new_user_option.text = '1'
    new_user_option = ET.SubElement(new_user, 'Option', Name='Comments')
    new_user_option.text = ''
    new_user_option = ET.SubElement(new_user, 'Option', Name='ForceSsl')
    new_user_option.text = '0'

    ip_f = ET.SubElement(new_user, 'IpFilter')
    ip_f_o = ET.SubElement(ip_f, 'Disallowed')
    ip_f_o = ET.SubElement(ip_f, 'Allowed')

    user_permissions = ET.SubElement(new_user, 'Permissions')
    user_permission = ET.SubElement(user_permissions, 'Permission', Dir=user_home)
    user_permission_o = ET.SubElement(user_permission, 'Option', Name='FileRead')
    user_permission_o.text = '1'
    user_permission_o = ET.SubElement(user_permission, 'Option', Name='FileWrite')
    user_permission_o.text = '1'
    user_permission_o = ET.SubElement(user_permission, 'Option', Name='FileDelete')
    user_permission_o.text = '1'
    user_permission_o = ET.SubElement(user_permission, 'Option', Name='FileAppend')
    user_permission_o.text = '1'
    user_permission_o = ET.SubElement(user_permission, 'Option', Name='DirCreate')
    user_permission_o.text = '0'
    user_permission_o = ET.SubElement(user_permission, 'Option', Name='DirDelete')
    user_permission_o.text = '0'
    user_permission_o = ET.SubElement(user_permission, 'Option', Name='DirList')
    user_permission_o.text = '1'
    user_permission_o = ET.SubElement(user_permission, 'Option', Name='DirSubdirs')
    user_permission_o.text = '1'
    user_permission_o = ET.SubElement(user_permission, 'Option', Name='IsHome')
    user_permission_o.text = '1'
    user_permission_o = ET.SubElement(user_permission, 'Option', Name='AutoCreate')
    user_permission_o.text = '0'

    user_speed_limits = ET.SubElement(new_user, 'SpeedLimits', DlType='0', DlLimit="10",
                                      ServerDlLimitBypass="0", UlType="0", UlLimit="10",
                                      ServerUlLimitBypass="0")
    user_speed_limits_o = ET.SubElement(user_speed_limits, 'Download')
    user_speed_limits_o = ET.SubElement(user_speed_limits, 'Upload')

    root[2].append(new_user)
    ET.indent(root)
    tree.write(file)
    logspa(f'Parameters for user {username} added.')


def checkIfAccountExist(ftp_account, xmlfile):
    """
    Checks if the ftp account is already defined in XML configuration file

    :param xmlfile: xml configuration file
    :param ftp_account: FTP account for looking for
    :return: Boolean
    """

    tree = ET.parse(xmlfile)
    root = tree.getroot()

    for users in root.findall("./Users/"):
        if ftp_account.upper() in users.attrib.get("Name"):
            return True
    return False


def reloadConfiguration():
    """
    Reloads the new configuration in order for the new user to be active in FTP server
    :return: Description of the execution
    """
    command_result = subprocess.run([os.path.dirname(f_xml_file) + "\\FileZilla Server.exe", "/reload-config"],
                                    capture_output=True, text=True)
    logspa(f'[Reload configuration] Status: {command_result.returncode}')
    logspa(f'[Reload configuration] Error: "{command_result.stderr}" ')
    logspa(f'[Reload configuration] Output: "{command_result.stdout}"')
    return command_result


def logspa(details, is_end=False):
    """
    Creates a log file with the stages executed

    :param details: Details you need to add
    :param is_end: if True, then it prints out a bar
    :return:
    """

    if is_end:
        with open(backup_directory + "\\new_ftp_accounts.log", 'a') as logs:
            logs.write(f'{details * 80}\n')
    else:
        with open(backup_directory + "\\new_ftp_accounts.log", 'a') as logs:
            logs.write(f'{datetime.now().strftime("%m-%d-%y_%H:%M:%S")} {details}\n')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'New user account must be specified.\nUSAGE: {sys.argv[0]} <user>')
        logspa(f'Error missing username.')
        logspa("=", is_end=True)
        sys.exit(1)
    elif checkIfAccountExist(sys.argv[1], f_xml_file):
        print(f'FTP account "{sys.argv[1].upper()}" already exist.')
        logspa(f'FTP account "{sys.argv[1].upper()}" already exist.')
        logspa("=", is_end=True)
        sys.exit(2)
    else:
        makeBackup(f_xml_file)
        home = homeDirectory(sys.argv[1])
        user, password, salt, hash = accountData(sys.argv[1])
        addUserInfo(f_xml_file, sys.argv[1], salt, hash, home)
        reloadConfiguration()
        print(f'user:     {user.upper()}\npassword: {password}\n')
        logspa("=", is_end=True)
