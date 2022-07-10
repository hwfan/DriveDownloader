from setuptools import setup, find_packages
setup(
    name = "DriveDownloader",
    version = "1.6.0.post1",
    keywords = ("drivedownloader", "drive", "netdrive", "download"),
    description = "A Python netdrive downloader.",
    long_description = "A Python netdrive downloader.",
    license = "MIT Licence",

    url = "https://github.com/hwfan",
    author = "hwfan",
    author_email = "hwnorm@outlook.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['argparse', 'requests', 'tqdm', 'rich', 'pysocks', 'requests_random_user_agent',
                        "google-api-python-client >= 1.12.5", "six >= 1.13.0", "oauth2client >= 4.0.0",
                        "PyYAML >= 3.0", "pyOpenSSL >= 19.1.0"],
    scripts = [],
    entry_points = {
        'console_scripts': [
            'ddl = DriveDownloader.downloader:simple_cli'
        ]
    }
)
