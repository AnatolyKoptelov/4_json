# Prettify JSON

Application for gett pretty view of JSON files downloaded from web. 
Sometimes, theire files can be zipped for traffic volume economy.
For example: https://op.mos.ru/EHDWSREST/catalog/export/get?id=232872
Application  can read a JSON file by path in web and and even open the zipped files.
By default, it works with encoded utf_8 files, but sometimes downloaded files can have a different encoding.
You can use optional parameter "codec" for decode original file. 
iA value of this parameter  should be taken from the list on the oficial Python site:
https://docs.python.org/3.5/library/codecs.html#standard-encodings 
There are 2 ways for using this application:

1.	With command line.
    Run command python pprint_json.py <path_to_file> [codec]
2.	With import function
    Function returns a dictionary with 3 objects:
	- rc: request code = 1 for success, negative value for unsuccess 
	- rt: text explanation of request code
	- json: pretty view of original json file if success or None if unsuccess

Simpe example:
``````````````````````````````````````````````````````````````````````
from  pprint_json import pretty_json

url='https://op.mos.ru/EHDWSREST/catalog/export/get?id=232872'
result = pretty_json(url, codec='cp1251')
if result['rc']>0:
    print(result['json'])
else:
    print(result['rt'])
``````````````````````````````````````````````````````````````````````

# Quickstart


Example of script launch on Linux, Python 3.5:

```#!bash
$ python pprint_json.py https://op.mos.ru/EHDWSREST/catalog/export/get?id=232872 cp1251 
# output:

[
    {
        "Address": "улица Декабристов, дом 47Б",
        "AdmArea": "Северо-Восточный административный округ",
        "District": "район Отрадное",
        "FullName": "Автомобильный заправочный комплекс № 1 «РН-Москва»",
        "ID": 14,
        "Owner": "ОАО «РН-Москва»",
        "ShortName": "АЗК № 1 «РН-Москва»",
        "TestDate": "04.04.2013",
        "geoData": {
            "coordinates": [
                37.623636836021696,
                55.85834864447605
            ],
            "type": "Point"
        },
        "global_id": 4539435
    },
    {
        "Address": "Дубнинская улица, дом 52",
        "AdmArea": "Северный административный округ",
        "District": "Бескудниковский район",
        "FullName": "Автомобильный заправочный комплекс № 11 «РН-Москва»",
        "ID": 15,
        "Owner": "ОАО «РН-Москва»",
        "ShortName": "АЗК № 11 «РН-Москва»",
        "TestDate": "04.04.2013",
        "geoData": {
            "coordinates": [
                37.552540305200964,
                55.89733548475162
            ],
            "type": "Point"
        },
        "global_id": 4539436
    },...
`

```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
