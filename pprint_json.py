# coding: utf8
import requests 
import zipfile
import io, sys
import json

# list of codex for python 3.5
CODECS = ['ascii',
 'big5', 'big5hkscs', 'cp037', 'cp273', 'cp424', 'cp437', 'cp500',
 'cp720', 'cp737', 'cp775', 'cp850', 'cp852', 'cp855', 'cp856',
 'cp857', 'cp858', 'cp860', 'cp861', 'cp862', 'cp863', 'cp864',
 'cp865', 'cp866', 'cp869', 'cp874', 'cp875', 'cp932', 'cp949',
 'cp950', 'cp1006', 'cp1026', 'cp1125', 'cp1140', 'cp1250', 'cp1251',
 'cp1252', 'cp1253', 'cp1254', 'cp1255', 'cp1256', 'cp1257', 'cp1258',
 'cp65001', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213', 'euc_kr', 'gb2312',
 'gbk', 'gb18030', 'hz', 'iso2022_jp', 'iso2022_jp_1', 'iso2022_jp_2',
 'iso2022_jp_2004', 'iso2022_jp_3', 'iso2022_jp_ext', 'iso2022_kr',
 'latin_1', 'iso8859_2', 'iso8859_3', 'iso8859_4', 'iso8859_5',
 'iso8859_6', 'iso8859_7', 'iso8859_8', 'iso8859_9', 'iso8859_10',
 'iso8859_11', 'iso8859_13', 'iso8859_14', 'iso8859_15', 'iso8859_16',
 'johab', 'koi8_r', 'koi8_t', 'koi8_u', 'kz1048', 'mac_cyrillic',
 'mac_greek', 'mac_iceland', 'mac_latin2', 'mac_roman', 'mac_turkish',
 'ptcp154', 'shift_jis', 'shift_jis_2004', 'shift_jisx0213', 'utf_32',
 'utf_32_be', 'utf_32_le', 'utf_16', 'utf_16_be', 'utf_16_le', 'utf_7',
 'utf_8', 'utf_8_sig']

# URL to codeclist
cl = 'https://docs.python.org/3.5/library/codecs.html#standard-encodings'

def pretty_json(path, codec=''):
    
    # Check http or https before URL
    if path[:4] != 'http':
        path = 'https://' + url 
    # Check URL connection
    rq = requests.get(path)
    if rq.status_code == 200:
        # Is this file is zipfile?
        if zipfile.is_zipfile(io.BytesIO(rq.content)):
            input_file =  zipfile.ZipFile(io.BytesIO(rq.content))
            input_file = input_file.read(input_file.namelist()[0])
        # Not zip
        else:
            input_file = rq.content
    # HTTP response code !=200, return errorcode
    else:
        return({'rc':-1, 
                'rt':'Incorrect or unavalible URL', 
                'json': None
               })
    # Use custom codec
    if codec:
        if codec in CODECS:
            # Decode file, if possible
            try:
                input_file =  input_file.decode(codec)
            except:
                # Return errorcode
                return({'rc':-2, 
                        'rt':'Can not decode data with codec: %s'%codec,
                        'json':None
                       })

        else:
            # Wrong codec, return errorcode
            return({'rc':-4, 
                    'rt':'Incorrect codec, use one of codeclist: %s'%cl,
                    'json':None
                    })
    # Read JSON file, if possible
    try:
        output = json.loads(input_file, encoding='utf-8')
    except:
        # Return errorcode
        return({'rc':-3, 
                'rt':'Can not read JSON file, try to use codec',
                'json':None
               })
    # Everything is OK, great job
    return({'rc':1,
            'rt':'OK',
            'json':json.dumps(output, indent=4, sort_keys=True, ensure_ascii=False)
           })


# main app
if __name__ == '__main__':
    # Check commandline values
    if len(sys.argv) not in (2,3):
        print("""\n
               Usage:\n
               python pretty_json.py URL [codec]\n
               where codec is one of codeclist:\n
               %s\n
               """%cl)
        sys.exit(-1)
    url = sys.argv[1]
    codec = len(sys.argv)>2 and sys.argv[2] or ''
    # Return pretty JSON
    pj = pretty_json(url, codec = codec)
    print(pj['json'], pj['rc'], pj['rt'])
