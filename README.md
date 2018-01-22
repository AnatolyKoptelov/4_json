# Prettify JSON

Application for gett pretty view of JSON files - local or downloaded from web. 
Use **-l** option for local file, for web file option using by default.
Sometimes, these files can be zipped for traffic volume economy.
For example: https://op.mos.ru/EHDWSREST/catalog/export/get?id=232872
Application  can read a JSON file by path in web or local and and even open zipped files.
By default, it works with encoded utf_8 files, but sometimes downloaded files can have a different encoding.
You can use optional parameter **-c** for decode original file. 
This application supports these codecs:
 - utf_8
 - cp1251
 - koi8_r
 - cp866
 - mac_cyrillic  

# Quickstart

Example of script launch on Linux, Python 3.*:

```
$ python pprint_json.py https://op.mos.ru/EHDWSREST/catalog/export/get?id=232872 -c cp1251 

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
```

Use **-h** option for read application info:
```
pprint_json.py -h 
usage: pprint_json.py [-h] [-l]
                      [-c [{utf_8,cp1251,koi8_r,cp866,mac_cyrillic}]]
                      path

Print JSON files in correct and readable form

positional arguments:
  path                  File path: local or URL

optional arguments:
  -h, --help            show this help message and exit
  -l, --local           Use if you print a local JSON file
  -c [{utf_8,cp1251,koi8_r,cp866,mac_cyrillic}], --codec [{utf_8,cp1251,koi8_r,cp866,mac_cyrillic}]
                        Use for decode a original file
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
