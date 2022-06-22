# DriveDownloader

[English](README.md) | 中文文档

**DriveDownloader**是一个基于Python的命令行工具，用来下载OneDrive, 谷歌网盘等在线存储上的文件。使用DriveDownloader，只需要一行简洁的命令，就可以从各类网盘上下载文件。

DriveDownloader当前支持：
  - OneDrive
  - OneDrive for Business
  - GoogleDrive
  - Dropbox
  - 直链

## 命令用法

  ```
    ddl URL/FILELIST [--filename FILENAME] [--thread-number NUMBER] [--version] [--help]
  ```

  - `URL/FILELIST`: 目标的URL或者文件列表。**文件列表的格式请参考：`tests/test.list`.**
  - `--filename/-o FILENAME`: (可选) 输出的文件名，如'hello.txt'
  - `--thread-number/-n NUMBER`: (可选) 多线程的线程数量。
  - 使用代理服务器：
      - 请将环境变量 `http_proxy` 与 `https_proxy` 设置成你的代理服务器地址，DriveDownloader会自动读取它们。

## 安装方式

  1. 从pip安装
  ```
    pip install DriveDownloader
  ```

  2. 从源代码安装
  ```
    git clone https://github.com/hwfan/DriveDownloader.git && cd DriveDownloader
    python setup.py install
  ```

## 快速开始
  
  制作中，与新版本共同发布。

## 依赖

  - Python 3
  - 请使用`pip install -r requirements.txt`安装依赖。
 
## 用例

  这些用例也可以在`tests/run.sh`中找到。

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

## 常见问题

- 为什么提示"Size:Invalid"?

  - 我们根据HTTP报文中的"Content-Length"提取文件大小。如果该参数置空，文件大小就会回落至默认的"Invalid". (谷歌网盘会隐藏这个参数)

- 通过socks5代理无法连接目标服务器。

  - 请使用"socks5h"作为协议前缀。该前缀会将URL发送给代理服务器进行解析。

- 我的DriveDownloader中有一些没有修复的bug。

  - 请使用`pip install DriveDownloader --force-reinstall --upgrade`更新DriveDownloader。

- !{some string}: event not found

  - 在bash中，URL中的"!"是一个关键字, 请在URL前后增加引号(')以解决该问题，例如
  
    ```
    ddl 'https://1drv.ms/t/s!ArUVoRxpBphY5U-a3JznLkLG1uEY?e=czbq1R' -o test_outputs/hello_od.txt
    ```

## 鸣谢

本项目的部分代码来源于[PyDrive2](https://github.com/iterative/PyDrive2)与[rich](https://github.com/Textualize/rich)。感谢他们优秀的工作！

## 开发计划

 - [x] 通用的下载API - 一个下载类，多个网盘下载的继承类。
 - [x] 支持更多网盘 - OneDrive for Business, Dropbox, 直链等。
 - [x] 从列表下载
 - [x] 多线程下载
 - [ ] 断点续传
 - [ ] 基于窗口的UI
 - [ ] 快速开始
 
## 更新日志

### v1.6.0

- (WIP) 增加断点续传功能。
- 采用新的进度条管理器[rich](https://github.com/Textualize/rich)。

### v1.5.0

- 解决了在部分情况下无法访问谷歌网盘文件的问题。
- 输入是URL还是文件将由下载器自行判断，`-l/--list`选项将不再维护。
- 统一读取环境变量中的代理，`-p/--proxy`选项将不再维护。
- 增加了版本号显示选项`-v/--version`。

### v1.4.0

- 支持多线程，从文件下载，从直链下载。
- 移除了交互模式。

### v1.3.0

- 支持Sharepoint与Dropbox。
- 移除了fake-useragent的依赖。