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


def pretty_print_json(json_file):
    print(json.dumps(json_file, indent=4, sort_keys=True, ensure_ascii=False))


def read_url_file(path):
    if path[:4] != 'http':
        path = 'http://' + path
    try:
        rq = requests.get(path)
    except requests.exceptions.ConnectionError:
        json_file = None
        response_code = -1
        return json_file, response_code
    if rq.ok:
        json_file = rq.content
        response_code = 0
        return json_file, response_code
    else:
        json_file = None
        response_code = -2
        return json_file, response_code


def read_local_file(path):
    if os.path.isfile(path):
        try:
            with open(path, 'rb') as file_to_read:
                json_file = file_to_read.read()
                response_code = 0
        except IOError:
            json_file = None
            response_code = -5
    else:
        json_file = None
        response_code = -6
    return json_file, response_code


if __name__ == '__main__':

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
        nargs=1,
        help='File path: local or URL'
    )
    parser.add_argument(
        '-l',
        '--local',
        dest='load_data',
        action='store_const',
        const=read_local_file,
        default=read_url_file,
        help='Use if you print a local JSON file'
    )
    parser.add_argument(
        '-c',
        '--codec',
        action='store',
        nargs='?',
        default='utf_8',
        choices=codecs,
        help='Use for decode a original file'
    )
    args = parser.parse_args()
    response_code = 1
    response_texts = {
        1: 'Work with the file is not implemented',
        0: 'OK',
        -1: '{}{}\n{}\n{}'.format(
            'Cannot connect to ',
            args.path[0],
            'Check your internet connection or file path is correct',
            'For opening a local file use "-l" command string option'
        ),
        -2: 'Incorrect or unavailable URL',
        -3: '{}{} codec. Try to use other codec'.format(
            'Cannot decode file with ',
            args.codec,
            'codec.\n Try to use other codec!',
        ),
        -4: '{}{}'.format(
            'Cannot read JSON file, check this JSON file ',
            'on the validator or try to use codec.',
        ),
        -5: 'Cannot open the file: {}'.format(args.path[0]),
        -6: 'File {} does not exist, check it location'.format(args.path[0]),
    }

    json_file, response_code = args.load_data(args.path[0])
    if not response_code:
        json_file = extract_zip_file(json_file)
        try:
            json_file = json_file.decode(args.codec)
        except ValueError:
            json_file, response_code = None, -3
        if not response_code:
            try:
                json_file = json.loads(json_file, encoding='utf-8')
            except json.decoder.JSONDecodeError:
                json_file, response_code = None, -4
            if not response_code:
                pretty_print_json(json_file)
    print(response_code and response_texts[response_code] or '')
