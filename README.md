# DriveDownloader

DriveDownloader is a Python tool for downloading files on online drives. With DriveDownloader, one can download the resources from netdrive with only one command line. 

DriveDownloader now supports:
  - OneDrive
  - OneDrive for Business
  - GoogleDrive
  - Dropbox
  - Direct Link

**[News] Update version 1.4.0: Supported Multi-thread and downloading from a list and a direct link. Removed interactive mode.**

**[News] Update version 1.3.0: Supported Sharepoint and Dropbox. Removed the deprecated fake-useragent.**

## Requirements

  - Python 3
    - argparse
    - requests
    - tqdm
    - pysocks
  - Use `pip install -r requirements.txt` to install the packages.
  - Proxy server if necessary. **We don't provide proxy service for DriveDownloader.**
 
## Installation
  1. Install from pip
  ```
    pip install DriveDownloader
  ```

  2. Install from source
  ```
    git clone https://github.com/hwfan/DriveDownloader.git
    python setup.py install
  ```

## Usage

<!-- ### Non-interactive Mode -->

  ```
    ddl URL/FILELIST [--filename FILENAME] [--proxy PROXY] 
                     [--list] [--thread-number NUMBER]
  ```

  - `URL/FILELIST`: target url/filelist to download from. **The example of filelist is shown in `tests/test.list`.**
  - `--filename/-o FILENAME`: (optional) output filename. Example: 'hello.txt'
  - `--proxy/-p PROXY`: (optional) the proxy address through which to download the file. Example: `--proxy http://example.com:80`
  - `--list/-l`: (optional, boolean) choose whether the input is a filelist.
  - `--thread-number/-n NUMBER`: (optional) the thread number when using multithread.

  Simple examples:

  ```
  ddl https://www.dropbox.com/s/r4bme0kew42oo7e/Get%20Started%20with%20Dropbox.pdf?dl=0 -o test/test.pdf -n 4
  ddl test.list -l
  ```
  
  **See `tests/run.sh` for more examples.**

### Warning for OneDrive user

  Since Linux shell can parse "!" from the url, single quotes(') should be added before and after the url when using non-interactive mode.
  
<!-- ### Interactive Mode

  1. Simply input "ddl" in the shell and press enter.
  ```
      ddl
  ```
  2. The shell will return an interface for inputting the user info.
  ```
      ============ Drive Downloader ============
      URL: (input your url here)
      Filename: (input your filename here)
      Proxy: (input your proxy here)
  ```
  3. The downloading procedure will start after these inputs.
  ```
      Name: noname.out, Size: ** MB
      100%|█████| **M/**M [00:01<00:00, **MB/s]
      Download finished.
  ``` -->

## FAQ

**Why does "Size:Invalid" occur?**

We extract the size of file from the "Content-Length" of HTTP response. If this parameter is empty, the file size will fall back to "Invalid". (The response of GoogleDrive often hides this header.)

**I couldn't connect to the target server through a socks5 proxy.**

Try "socks5h" as the protocol prefix instead. It will transmit the url to proxy server for parsing.

<!-- **fake_useragent.errors.FakeUserAgentError: Maximum amount of retries reached**

This message may occur when DriveDownloader is first used. Try again and if this also occurs, please report in the issue. -->

## TODO

 - [x] General downloader API - one class for downloading, and several inheritance classes to load the configurations.
 - [x] Command-line UI - apostrophes will not be needed in the newest version.
 - [x] Support more netdrives - OneDrive for Business, Dropbox, ...
 - [x] Downloading files from a list.
 - [x] Multi-thread downloading.
 - [ ] Window based UI - PyQt, X Window, ...
