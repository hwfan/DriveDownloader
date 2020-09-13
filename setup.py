from setuptools import setup, find_packages
setup(
    name = "DriveDownloader",
    version = "1.1.2-b0",
    keywords = ("pip", "ddl", "drivedownloader", "hwfan"),
    description = "Net Drive Downloader with python",
    long_description = "A useful tool for downloading files on net drives.",
    license = "MIT Licence",

    url = "http://hwfan.io",
    author = "hwfan",
    author_email = "hwnorm@outlook.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['argparse', 'requests', 'tqdm', 'fake-useragent'],
    
    scripts = [],
    entry_points = {
        'console_scripts': [
            'ddl = src.main:main'
        ]
    }
)
