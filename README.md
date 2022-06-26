# DriveDownloader

English | [中文文档](README_CN.md)

**DriveDownloader** is a Python-based **CLI** tool for downloading files on online drives. With DriveDownloader, one can download the resources from netdrive with **only one command line**. 

DriveDownloader now supports:
  - OneDrive
  - OneDrive for Business
  - GoogleDrive
  - Dropbox
  - Direct Link

## Usage

  ```
    ddl URL/FILELIST [--filename FILENAME] [--thread-number NUMBER] [--version] [--help]
  ```

  - `URL/FILELIST`: target url/filelist to download from. **The example of filelist is shown in `tests/test.list`.**
  - `--filename/-o FILENAME`: (optional) output filename. Example: 'hello.txt'
  - `--thread-number/-n NUMBER`: (optional) the thread number when using multithread.
  - `--force-back-google/-F`: (optional) use the backup downloader for Google drive (it needs authentication, but is more stable).
  - Using proxy:
      - Set the environment variables `http_proxy` and `https_proxy` to your proxy addresses, and DriveDownloader will automatically read them.
  - Resume:
      - If your download was interrupted accidentally, simply restart the command will resume, regardless the number of threads.
      
## Installation
  1. Install from pip
  ```
    pip install DriveDownloader
  ```

  2. Install from source
  ```
    git clone https://github.com/hwfan/DriveDownloader.git && cd DriveDownloader
    python setup.py install
  ```

## Quick Start
  
  Coming Soon.

## Requirements

  - Python 3.7+
  - Use `pip install -r requirements.txt` to install the packages.
  - Proxy server if necessary. **We don't provide proxy service for DriveDownloader.**
 
## Examples

  You can also see these examples in `tests/run.sh`.

  ```
  echo "Unit Tests of DriveDownloader"
  mkdir -p test_outputs

  echo "Testing Direct Link..."
  # direct link
  ddl https://www.google.com.hk/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png -o test_outputs/directlink.png

  echo "Testing OneDrive..."
  # OneDrive
  ddl https://1drv.ms/t/s!ArUVoRxpBphY5U-a3JznLkLG1uEY?e=czbq1R -o test_outputs/hello_od.txt

  echo "Testing GoogleDrive..."
  # GoogleDrive
  ddl https://drive.google.com/file/d/1XQRdK8ewbpOlQn7CvB99aT1FLi6cUKt_/view?usp=sharing -o test_outputs/hello_gd.txt

  echo "Testing SharePoint..."
  # SharePoint
  ddl https://bupteducn-my.sharepoint.com/:t:/g/personal/hwfan_bupt_edu_cn/EQzn4SeFkJZHq8OikhX7X3QB97PSiNvJpPVtllBQln8EQw?e=NmgRSc -o test_outputs/hello_sp.txt

  echo "Testing Dropbox..."
  # Dropbox
  ddl https://www.dropbox.com/s/bd0bak3h9dlfw3z/hello.txt?dl=0 -o test_outputs/hello_db.txt

  echo "Testing File List..."
  # file list
  ddl test.list -l

  echo "Testing Multi Thread..."
  # Multi Thread
  ddl https://www.dropbox.com/s/r4bme0kew42oo7e/Get%20Started%20with%20Dropbox.pdf?dl=0 -o test_outputs/Dropbox.pdf -n 8
  ```

## FAQ

- Why does "Size:Invalid" occur?

  - We extract the size of file from the "Content-Length" of HTTP response. If this parameter is empty, the file size will fall back to "Invalid". (The response of GoogleDrive often hides this header.)

- I couldn't connect to the target server through a socks5 proxy.

  - Try "socks5h" as the protocol prefix instead. It will transmit the url to proxy server for parsing.

- There exists some old bugs in my DriveDownloader.

  - Try `pip install DriveDownloader --force-reinstall --upgrade` to update. We keep the latest version of DDL free from those bugs.

- !{some string}: event not found

  - Since bash can parse "!" from the url, single quotes(') should be added before and after the url when using bash.
  
    ```
    ddl 'https://1drv.ms/t/s!ArUVoRxpBphY5U-a3JznLkLG1uEY?e=czbq1R' -o test_outputs/hello_od.txt
    ```

## Acknowledgement

Some code of DriveDownloader is borrowed from [PyDrive2](https://github.com/iterative/PyDrive2) and [rich](https://github.com/Textualize/rich). Thanks for their wonderful jobs!

## TODOs

 - [x] General downloader API - one class for downloading, and several inheritance classes to load the configurations.
 - [x] Support more netdrives - OneDrive for Business, Dropbox, ...
 - [x] Downloading files from a list.
 - [x] Multi-thread downloading.
 - [x] Resume downloading.
 - [ ] Window-based UI.
 - [ ] Quick Start.

## Update Log

### v1.6.0

- Added automatic resume downloading.
- Changed the progress bar manager to [rich](https://github.com/Textualize/rich).

### v1.5.0

- Solved the problem of "not accessible" when downloading a large file on Google Drive.
- The input type (URL/FILELIST) is now automatically detected by the downloader, and `-l/--list` is deprecated.
- The proxy server is now parsed from environmental variables, and `-p/--proxy` is deprecated.
- Added the version option `-v/--version`.

### v1.4.0

- Supported Multi-thread and downloading from a list and a direct link.
- Removed interactive mode.

### v1.3.0

- Supported Sharepoint and Dropbox.
- Removed the deprecated fake-useragent.