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

* ### updateSortTitle.py (requires ````.env````)
    This script will update the sort title of all your series by removing the leading articles (*a, an, the*)
    and appending it to the end of the title.
    ```bash
        python updateSortTitle.py
    ```
  
* ### emailNotification.py (requires ````.env````)
    With this script you can send an email notification to all your users, using their E-Mail address.
    You need to configure a SMTP server in the script before you can use it.
    It will notify abut all new books in the notification interval.
    Use a cronjob to run this script regularly.
    ```bash
        python emailNotification.py
    ```  

## Environment Variables
The following environment variables are required for some scripts to work.
Set them in your ```.env``` file. See ```.env.example``` for an example.
+ ### KOMGA_URL
    The URL of your Komga server.
    ```bash
        KOMGA_URL=http://192.168.123.45:8080
    ```
+ ### KOMGA_USER
    The username of an Admin user.
    ```bash
        KOMGA_USER=admin@komga.com
    ```
+ ### KOMGA_PASSWORD
    The password of the Admin user.
    ```bash
        KOMGA_PASSWORD=supersecretpassword
    ```
