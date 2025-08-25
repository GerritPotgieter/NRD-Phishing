# NRD-Phishing
This repo will serve as a testing ground to see how we can automatically download updated NRD lists and flag suspicious domains names


## List downloader usage

To download the latest lists from the Whois databse we will be using the script from the https://github.com/PeterDaveHello/nrd-list-downloader repo.

Steps to execute the script:
1. Open a Unix terminal (WSL in my preffered case)

2. ```DAY_RANGE=7 ./nrd-list-downloader.sh ```

This should download the latest lists and store them under a created directory called daily/free

If the script does not want to execute my fix was to use the dos2unix command as follows



```dos2unix nrd-list-downloader.sh ```

Then the script can execute and download as needed. For fruther troubleshooting of the script please consult the Repo from PeterDave.

## Running the Python files
Access the repo and run the scripts from root using the following:

``` python3 scripts/parser.py ```

## Using the GO Scanner
First make sure that GO is installed in your enviroment. My current version is 1.24.5.

The GO script in this repo is directly taken from https://github.com/g0ldencybersec/gungnir

Go into the root GO Scanner folder and run 

``` go run . -r roots.txt ```

Make sure the domains you want to scan are in the roots.txt folder
