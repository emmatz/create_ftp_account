<h1 align="center"> Adding new FTP account </h1>

## Description

This python script helps to add new ftp account to **FileZilla Server**, it was tested with _FileZilla Server 0.9.60 Beta._

Usually the FileZilla configuration file is located at ${\color{lightblue}C:/Program Files (x86)/FileZilla Server/FileZilla Server.xml}$ and this script uses that file, if yours is in different location, then update it in the script. Prior to modification, the configuration file 
undergoes a backup procedure, with the backup being preserved at **C:/Program Files (x86)/FileZilla Server/conf_backup**

If an FTP account already exists, the system will not generate a duplicate account.

In the event that the FTP account does not exist, the system will proceed to generate the following components:
- An FTP account
- A home directory for the account
- Necessary subfolders within the home directory

Upon creation, the new FTP account is automatically endowed with default permissions, which encompass the following capabilities:
- Read a file
- Write a file
- Delete a file
- Append new files
- List directories
- List sub-directories

A log file, documenting all executed actions, is generated and stored in the same location as the backup of the configuration file.

# Usage

The usage is very simple, you can executed it

```shell
python3 filezilla_add_user.py <new_account>
```

or set the execution permissions, and then

```shell
./filezilla_add_user.py <new_account>
```

Use the flag -h in order to get some extra information

```shell
python3 filezilla_add_user.py -h
```

> :memo: **Note:** Due to the FileZilla process needs to be reloaded, it is necessary to run the script with admin privileges

