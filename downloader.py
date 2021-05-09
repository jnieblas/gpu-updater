import requests
import urllib.request
import os

from definitions import ROOT_DIR

rtx_20_series_id = 107
rtx_2070_super_id = 903
windows_10_64_id = 57


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

    # Remove old directory & file, recreate if
    try:
        os.rmdir(path)
    except FileNotFoundError:
        print('Driver directory not found - skipping deletion...')

    print('Creating driver directory at path: ' + path)
    os.mkdir(path)

    file_path = '{path}/{file_name}'.format(path=path, file_name=file_name)
    print('Downloading file at path: ' + file_path)
    urllib.request.urlretrieve(url, file_path)
    print('Download Complete!')


if __name__ == "__main__":
    download_url = get_download_url(rtx_20_series_id, rtx_2070_super_id, windows_10_64_id)

    download_driver(download_url)



