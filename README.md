# DriveDownloader

DriveDownloader is a Python tool for downloading files on online drives. With DriveDownloader, one can download the resources from netdrive with only one command line. 

DriveDownloader now supports **OneDrive** and **GoogleDrive**.

## Requirements

  - Python 3
    - argparse
    - requests
    - tqdm
    - fake-useragent
  - Use `pip install -r requirements.txt` to install the packages.
  - Proxy server if necessary. **We don't provide proxy service for DriveDownloader.**
 
## Installation
  ```
    pip install DriveDownloader
  ```

## Usage

### Interactive Mode

  1. Simply input "ddl" in the shell and press enter.
  ```
      ddl
  ```
  2. The shell will return an interface for inputting the user info.
  ```
      ============ Drive Downloader V1.2 ============
      URL: (input your url here)
      Filename: (input your filename here)
      Proxy: (input your proxy here)
  ```
  3. The downloading procedure will start after these inputs.
  ```
      Name: noname.out, Size: ** MB
      100%|█████| **M/**M [00:01<00:00, **MB/s]
      Download finished.
  ```

### Non-interactive Mode

  For non-interactive mode, please input the user info as the arguments after "ddl".
  - Since Linux shell can parse "!" from the url, 
  - **double quotes(") should be added before and after the url**
  - when using non-interactive mode.

  ```
    ddl "URL" --filename FILENAME --proxy PROXY
  ```

### Options

 - `URL`: target url to download from. 
    - OneDrive Example: <https://1drv.ms/t/s!ArUVoRxpBphY5U-axxe-xf3fidKh?e=kPexEF>
    - GoogleDrive Example: 
      - <https://drive.google.com/file/d/1XQRdK8ewbpOlQn7CvB99aT1FLi6cUKt_/view?usp=sharing>
      - <https://drive.google.com/open?id=1XQRdK8ewbpOlQn7CvB99aT1FLi6cUKt_>
 - `--filename FILENAME`: (optional) output filename. Example: 'hello.txt'
 - `--proxy PROXY`: (optional) the proxy address through which to download the file. Example: `--proxy http://example.com:80`

## FAQ

**Why does "Size:Invalid" occur?**

We extract the size of file by using the "Content-Length" of HTTP response. If this parameter is empty, the file size will fall back to "Invalid". (The response of GoogleDrive often hides this header.)

**I couldn't connect to the target server through a socks5 proxy.**

Try "socks5h" as the protocol prefix instead. It will transmit the url to proxy server for parsing.

## TODOS

 - [x] General downloader API - one class for downloading, and several inheritance classes to load the configurations.
 - [x] Command-line UI - apostrophes will not be needed in the newest version.
 - [ ] Window based UI - PyQt, X Window, ...
 - [ ] Support more netdrives - Dropbox, MEGA, ...
 - [ ] Multi-process downloading.
 - [ ] Downloading files from a list.