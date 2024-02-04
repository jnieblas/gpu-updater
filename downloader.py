import requests
import urllib.request
import os
import shutil
import subprocess

from definitions import ROOT_DIR

rtx_20_series_id = 107
rtx_2070_super_id = 903
windows_10_64_id = 57
windows_11_64_id = 135


def get_download_url(ps_id, pf_id, os_id, language_code=1033):
    url = 'https://gfwsl.geforce.com/services_toolkit/services/com/nvidia/services/AjaxDriverService.php'
    params = {
        'func': 'DriverManualLookup',
        'psid': ps_id,
        'pfid': pf_id,
        'osID': os_id,
        'languageCode': language_code,
        'beta': None,
        'isWHQL': 0,
        'dltype': -1,
        'dch': 1,
        'upCRD': None,
        'qnf': 0,
        'sort1': 0,
        'numberOfResults': 1
    }

    r = requests.get(url, params=params)
    download_info = r.json()['IDS'][0]['downloadInfo']

    print('Download URl:' + url)
    return download_info['DownloadURL']


def download_driver(url):
    path = ROOT_DIR + '/tmp'
    file_name = url[[index for index, char in enumerate(url) if char == '/'][4] + 1:]

    # Remove old directory & file
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        print('Driver directory not found - skipping deletion...')

    print('Creating driver directory at path: ' + path)
    os.mkdir(path)

    # Build file path, retrieve URL & download to file path
    file_path = '{path}/{file_name}'.format(path=path, file_name=file_name)
    print('Downloading file at path: ' + file_path)
    urllib.request.urlretrieve(url, file_path)
    print('Download Complete!')

def execute_driver():
    os.chdir(ROOT_DIR + '/tmp')
    files = os.listdir()
    driver = next((file for file in files if file.lower().endswith('.exe')), None)

    if driver:
        driver_path = os.path.abspath(driver)
        subprocess.run(driver_path)
    else:
        print("Unable to run executable file.")


if __name__ == "__main__":
    download_url = get_download_url(rtx_20_series_id, rtx_2070_super_id, windows_11_64_id)
    download_driver(download_url)
    execute_driver()


