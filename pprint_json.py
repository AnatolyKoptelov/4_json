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


def read_web_file(path):
    response = requests.get(path)
    readed_file = response.ok and response.content or None
    return readed_file


def read_local_file(path):
    if os.path.isfile(path):
        with open(path, 'rb') as file_to_read:
            readed_file = file_to_read.read()
    else:
        readed_file = None
    return readed_file


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
        help='File path: local or URL',
    )
    parser.add_argument(
        '-l',
        '--local',
        dest='load_data',
        action='store_const',
        const=read_local_file,
        default=read_web_file,
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
    args = parser.parse_args()
    try:
        json_file = args.load_data(args.path[0])
        json_file = extract_zip_file(json_file)
        json_file = json_file.decode(args.codec)
        data_dictionary = json.loads(json_file, encoding='utf-8')
        pretty_print_json(data_dictionary)

    except AttributeError:
        print('{} {} {}'.format(
                'Filepath',
                args.path[0],
                'does not correct, check it',
            ))
    except requests.exceptions.ConnectionError:
        print('{} {}\n{}\n{}'.format(
            'Cannot connect to',
            args.path[0],
            'Check your internet connection or file path is correct',
            'For opening a local file use "-l" command string option',
        ))
    except requests.exceptions.MissingSchema as error:
        print('{}\n{}'.format(
            error,
            'For opening a local file use "-l" command string option',
        ))
    except json.decoder.JSONDecodeError:
        print('{} {}'.format(
            'Cannot read JSON file, check this JSON file',
            'on the validator or try to use codec.',
        ))
    except IOError as error:
        print('{}\n{}{}'.format(
            error,
            'Cannot open the file: ',
            args.path[0],
        ))
    except ValueError as error:
        print('{}\n{}{} {}'.format(
            error,
            'Cannot decode file with ',
            args.codec,
            'Try to use other codec!',
        ))
