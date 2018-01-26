import io
import os
import json
import zipfile
import requests
import argparse


def extract_zip_file(file_for_extract):
    if zipfile.is_zipfile(io.BytesIO(file_for_extract)):
        extracted_file = zipfile.ZipFile(io.BytesIO(file_for_extract))
        return extracted_file.read(extracted_file.namelist()[0])
    else:
        return file_for_extract


def pretty_print_json(data_dictionary):
    print(json.dumps(
        data_dictionary,
        indent=4,
        sort_keys=True,
        ensure_ascii=False,
    ))


def decode_file(file_for_decoding, codec):
    return file_for_decoding.decode(codec)


def load_json(json_file):
    return json.loads(json_file, encoding='utf-8')


def get_args():

    def fetch_web_url(url):
        response = requests.get(url)
        if response.ok:
            return response.content

    def read_local_file(path):
        if os.path.isfile(path):
            with open(path, 'rb') as file_to_read:
                return file_to_read.read()

    codecs = [
        'utf_8',
        'cp1251',
        'koi8_r',
        'cp866',
        'mac_cyrillic',
    ]
    parser = argparse.ArgumentParser(
        description='Print JSON files in correct and readable form'
    )
    parser.add_argument(
        'path',
        metavar='path',
        type=str,
        help='File path: local or URL',
    )
    parser.add_argument(
        '-l',
        '--local',
        dest='load_data',
        action='store_const',
        const=read_local_file,
        default=fetch_web_url,
        help='Use if you print a local JSON file',
    )
    parser.add_argument(
        '-c',
        '--codec',
        action='store',
        nargs='?',
        default='utf_8',
        choices=codecs,
        help='Use for decode a original file',
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    load_data, path, codec = args.load_data, args.path, args.codec
    try:
        json_file = load_data(path)
        if json_file is None:
            print('{} {} {}'.format(
                'Filepath',
                path,
                'does not correct, check it',
            ))
        else:
            data = load_json(
                decode_file(
                    extract_zip_file(json_file),
                    codec,
                ),
            )
            pretty_print_json(data)

    except (requests.exceptions.RequestException, IOError) as error:
        print('{}\n{} {}\n{}\n{}'.format(
            error,
            'Cannot open the file:',
            path,
            'Check your internet connection or file path is correct',
            'For opening a local file use "-l" command string option',
        ))
    except ValueError as error:
        print('{}\n{} {} {} {}'.format(
            error,
            'Cannot decode file with',
            codec,
            'codec or cannot read it. Check this JSON file',
            'with a validator or try to use other codec!',
        ))
