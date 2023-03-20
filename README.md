# Komga-Scripts
Collection of scripts for use with [Komga](https://komga.org/).
Provided by the Komga-Discord community. 

For more information, please visit the [Komga-Discord](https://discord.gg/TdRpkDu) server.
[![Discord](https://img.shields.io/discord/678794935368941569?label=Discord&color=blue)](https://discord.gg/TdRpkDu)

## Scripts

* ### resetKomgaPassword.py
    If you want to reset the Admin password, you need to do it through the database.
    This script will do that for you.
    ```bash
        python resetKomgaPassword.py <path to database.sqlite>
    ```
    You will be prompted to choose a user and a new password, 
    which will be hashed and stored in the database.
    The ```<path to database.sqlite>``` is the path to the database file, found in your Komga config folder.


