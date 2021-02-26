from setuptools import setup, find_packages
setup(
    name = "DriveDownloader",
    version = "1.2.0",
    keywords = ("drivedownloader", "drive", "netdrive", "download"),
    description = "A Python netdrive downloader.",
    long_description = "A Python netdrive downloader.",
    license = "MIT Licence",

    url = "https://hwfan.io",
    author = "hwfan",
    author_email = "hwnorm@outlook.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['argparse', 'requests', 'tqdm', 'fake-useragent'],
    
    scripts = [],
    entry_points = {
        'console_scripts': [
            'ddl = downloader:simple_cli'
        ]
    }
)