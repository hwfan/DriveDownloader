# DriveDownloader

A useful tool for downloading files on online drives. Now supports **OneDrive** and **GoogleDrive**.

## Requirements

  - Python 3
    - argparse
    - requests
    - tqdm
    - fake-useragent
  - Use `pip install -r requirements.txt` to install the packages.
  - Proxy server if necessary. **We don't provide proxy service for DriveDownloader.**
 
## Usage


### Source Version

```
  python main.py URL --filename FILENAME --proxy PROXY
```

### Packed Version
```
  pip install DriveDownloader -i https://pypi.org/simple
  ddl URL --filename FILENAME --proxy PROXY
```

See release for details.

### Options

 - `URL`: target url to download from. **Apostrophes are needed when '!' can be parsed by shell.**
    - OneDrive Example: '<https://1drv.ms/t/s!ArUVoRxpBphY5U-axxe-xf3fidKh?e=kPexEF>'
    - GoogleDrive Example: 
      - '<https://drive.google.com/file/d/1XQRdK8ewbpOlQn7CvB99aT1FLi6cUKt_/view?usp=sharing>'
      - '<https://drive.google.com/open?id=1XQRdK8ewbpOlQn7CvB99aT1FLi6cUKt_>'
 - `--filename FILENAME`: (optional) output filename. Example: 'hello.txt'
 - `--proxy PROXY`: (optional) the proxy address through which to download the file. Example: `--proxy http://example.com:80`

## FAQ

**Why does "Size:Invalid" occur?**

We extract the size of file by using the "Content-Length" of HTTP response. If this parameter is empty, the file size will fall back to "Invalid". (The response of GoogleDrive often hides this header.)

**I couldn't connect to the target server through a socks5 proxy.**

Try "socks5h" as the protocol prefix instead. It will transmit the url to proxy server for parsing.
