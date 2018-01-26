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


def fetch_web_url(url):
    response = requests.get(url)
    if response.ok:
        return response.content


def read_local_file(path):
    if os.path.isfile(path):
        with open(path, 'rb') as file_to_read:
            return file_to_read.read()


def get_args(
    read_local_file_function,
    fetch_web_url_function,
    list_of_allowable_codecs,
):
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
        const=read_local_file_function,
        default=fetch_web_url_function,
        help='Use if you print a local JSON file',
    )
    parser.add_argument(
        '-c',
        '--codec',
        action='store',
        nargs='?',
        default='utf_8',
        choices=list_of_allowable_codecs,
        help='Use for decode a original file',
    )
    return parser.parse_args()


if __name__ == '__main__':
    codecs = [
        'utf_8',
        'cp1251',
        'koi8_r',
        'cp866',
        'mac_cyrillic',
    ]
    args = get_args(
        read_local_file_function=read_local_file,
        fetch_web_url_function=fetch_web_url,
        list_of_allowable_codecs=codecs,
    )
    try:
        json_file = args.load_data(args.path)
        if json_file is None:
            print('{} {} {}'.format(
                'Filepath',
                args.path,
                'does not correct, check it',
            ))
        else:
            received_data = load_json(
                decode_file(
                    extract_zip_file(json_file),
                    args.codec,
                ),
            )
            pretty_print_json(received_data)

    except (requests.exceptions.RequestException, IOError) as error:
        print('{}\n{} {}\n{}\n{}'.format(
            error,
            'Cannot open the file:',
            args.path,
            'Check your internet connection or file path is correct',
            'For opening a local file use "-l" command string option',
        ))
    except ValueError as error:
        print('{}\n{} {} {} {}'.format(
            error,
            'Cannot decode file with',
            args.codec,
            'codec or cannot read it. Check this JSON file',
            'with a validator or try to use other codec!',
        ))
