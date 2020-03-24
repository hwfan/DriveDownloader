# DriveDownloader

A useful tool for downloading files on online drives. Now supports **OneDrive** and **GoogleDrive**.

## Requirements

 - Python 3
    - argparse
    - requests
 - Proxy server if necessary. **We don't provide proxy service for DriveDownloader.**
 
## Usage


### Default Version

```
  python main.py URL FILENAME --proxy PROXY
```

### Packed Version

```
  unzip ddl.zip
  sudo mv ./ddl /usr/bin/ddl
  ddl URL FILENAME --proxy PROXY
```

See release for details.

### Options

 - `URL`: target url to download from. **Apostrophes are needed when '!' can be parsed by shell.**
    - OneDrive Example: '<https://1drv.ms/t/s!ArUVoRxpBphY5U-axxe-xf3fidKh?e=kPexEF>'
    - GoogleDrive Example: '<https://drive.google.com/open?id=1XQRdK8ewbpOlQn7CvB99aT1FLi6cUKt_>'
 - `FILENAME`: output filename. Example: 'hello.txt'
 - `--proxy PROXY`: (optional) the proxy address through which to download the file. Example: `--proxy http://example.com:80`

## FAQ

**Why does "Size:Invalid" occur?**

We recognize the size of file by using the "Content-Length" of HTTP response. If this param is empty, the file size will return "Invalid".

**I couldn't connect to the target server through a socks5 proxy.**

Try "socks5h" as the protocol prefix instead. It will forward the url to proxy server for parsing.