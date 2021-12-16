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