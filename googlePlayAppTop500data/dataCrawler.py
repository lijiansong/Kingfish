import requests
import pyquery as pq
import re
import csv
import json


def write_csv(data, filename):
    with open(filename, 'w') as outf:
        dw = csv.DictWriter(outf, data[0].keys())
        dw.writeheader()
        for row in data:
            dw.writerow(row)


header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'cookie': "OGPC=19009956-2:19010294-2:; ANID=AHWqTUkw7HjOb27LoyIkESoupoUkuV0bvjd7NggaXfswEOrP2S01A73GzOrWMyEr; CONSENT=YES+CN.zh-CN+20180121-08-0; _ga=GA1.3.926786579.1548054766; _gid=GA1.3.1459889700.1548054766; OTZ=4762513_24_24__24_; SID=_AZXyP5BZm7pDmo8vhCTHhOOL65ZznYiqOaym7cmjX21WBcAiZKJgReYcCiRbAlkOB0_5w.; HSID=ATreg8SORsrDXBZL6; SSID=AM9fldCzyCad8-5XF; APISID=1BRqrBoutgG2FtYW/Ac-8gHhnBB2PTWVUD; SAPISID=J5kIEMpfavcPOhVB/Ana2zr3100lUTtv5l; PLAY_ACTIVE_ACCOUNT=ICrt_XL61NBE_S0rhk8RpG0k65e0XwQVdDlvB6kxiQ8=andrewcao95@gmail.com; PLAY_PREFS=CtcLCNeQ66zrCBLNCxqZCxESExQVFhjUAdUBpwLEBOMF5QXoBdcG2AbeBt8GkJWBBpGVgQaSlYEGlZWBBpeVgQaklYEGuJWBBsCVgQbBlYEGxJWBBsWVgQbIlYEGzpWBBs-VgQbQlYEG1JWBBtmVgQbylYEGhpaBBomWgQaMloEGj5aBBpKWgQadloEGnpaBBp-WgQagloEGppaBBqeWgQaoloEGqZaBBu6XgQbvl4EGhZiBBomYgQarm4EGrZuBBsqbgQbLm4EG1ZuBBrydgQbdnYEG552BBpCegQbiooEG86KBBoujgQaapIEGv6WBBuqlgQbGpoEGzqiBBrysgQbWr4EGh7KBBomygQbWsoEGybOBBrG0gQbWuYEGjsCBBqLAgQbAwIEGwcCBBvLAgQbWwoEGjMWBBsrGgQbLxoEG-MeBBqrKgQbYzIEG3MyBBt3NgQaGzoEGoc-BBsTSgQaV1YEG2tiBBvLbgQbY5IEGl-WBBrjogQbP64EGsOyBBtf1gQa6-4EGu_-BBsn_gQbVg4IGyISCBrmGggamh4IGp4eCBuyHggbth4IG642CBvuNggaJjoIGlZiCBo-aggaZmoIGwZqCBveaggadnoIG9qKCBpKlggaeqIIGtKiCBtG1ggattoIG_LmCBv65ggb_uYIGwruCBo-_gga8wYIGkMuCBpHLggbRy4IG3MyCBtjQggaL0oIG2tOCBoHYggaG2oIGj9qCBpvaggaj2oIGxduCBrHcggb43YIG79-CBqThggaW6YIGo-2CBoXuggaz7oIGsfCCBuv2ggat-IIGs_iCBvb6ggbj-4IG2_yCBoCAgwbygYMG6oSDBpCFgwbXhYMGm4iDBrmIgwbwiIMGhY-DBpCPgwbZkYMG_pGDBvySgwaslYMGuJWDBsCWgwbmloMG3JeDBpmbgwbQnIMG8Z6DBvSegwaYoIMGm6CDBv2ggwbsr4MGiLCDBpW0gwantIMGqLSDBri2gwaAuIMG4LyDBvS8gwb2vIMGsL6DBs2-gwaew4MG5MaDBq3IgwaeyYMGm8qDBsrNgwb-zYMGotCDBvnTgwbr1IMGz9aDBuPXgwbp14MG0dmDBoDegwaw34MGiOCDBpfhgwbv44MGpuWDBpPmgwam7IMG6uyDBpXugwbA74MG4--DBp7ygwad9IMG1fSDBvn3gwaN-IMGrfuDBqT-gwaH_4MG3YGEBt-BhAbygoQG-oOEBo-EhAbXhIQGyYiEBsqIhAa-iYQGp4uEBpqMhAb1jIQGgI6EBqyOhAatjoQGhpCEBtuThAaKmIQG9JiEBpWZhAb9moQG-ZyEBoqdhAbhn4QGlaCEBs2jhAbPo4QG0KOEBqGkhAaopYQG0aaEBv-nhAaSqYQGk6mEBq2vhAbBr4QG2rOEBsq0hAagtoQGobaEBq24hAbhuIQGoLmEBsC5hAbIu4QG_buEBoe_hAasv4QGt7-EBqPBhAbWwoQG8sKEBozDhAaaw4QG5sWEBqbIhAa3yIQGhcqEBpPLhAbLy4QGsMyEBunOhAb7zoQG_tCEBp_RhAap0YQGgdOEBoTThAaG1IQGr9iEBsfYhAbr3oQGpeGEBtjhhAaK4oQGx-aEBuvmhAb_5oQGiOeEBsLnhAac6IQG8umEBq7qhAbi64QGyu2EBsnxhAaP9IQGyfSEBtz2hAaL-IQGyfiEBpv5hAby-oQGifuEBq77hAa2_IQGwvyEBoT-hAaF_oQGp_6EBvH-hAb6_oQGv4GFBsqBhQbLgYUGiIKFBraEhQbThIUGo4WFBqWFhQazhoUGtoaFBuKGhQayh4UGyYeFBtmHhQaBiIUGgoiFBu6JhQanjIUGmY2FBqaNhQbJjYUG9I2FBv6NhQaHjoUGto6FBoKUhQaDlIUG2pSFBoGVhQbNlYUG9JWFBsWWhQb0l4UGKJ322cmHLTokZDE1N2NlMGItMjhiNy00NzQ4LTkxZjMtMjI5NzE4MWVjNDE5QAFIAA:S:ANO1ljJGMkG5hZZ7kA; 1P_JAR=2019-1-23-5; NID=156=TmJ1KP6SMc5SrfV_g_wZ9g1BDVRftB_pU4F2TbsCql5p-PvjbMrB9IxTtWwGsvhq4OA2N-HeSRYVwMZYgcL9FHkvw47238-xnKIAob6AMoWemq9cdvuPTOao6IZllxSADebfGP26BsiK5hgMs4ng9E91sUBMd0tQn1Jic0nunU2zSsKyXPAvOVQdVwZaQ6ix7YAKZBtdnPw4nuJBJWltIBDypVs4t6wmZIpUGVr8haxdmj2_5FgNe9BFyW_-B8oIesjsWMuxPN7ly8ESfu5M5i5l6T0Xi6zu-hjrQy9joWQrHOMAgkoGTvrCcFeBddJSjw; S=billing-ui-v3=mTZk3IglMtywXDPVUANbYPJ-VFe5IlUb:billing-ui-v3-efe=mTZk3IglMtywXDPVUANbYPJ-VFe5IlUb; _gat=1; SIDCC=ABtHo-Eh3lGtrKVe2LAydjyhCIOPbdpevNhDRxNWj6HBSrnKtsmv1FbrLOf-YlGOzLX032EgJA"
}

url = 'https://play.google.com/store/apps/collection/topselling_free?authuser=0'


# url = 'https://play.google.com/store/apps/collection/topgrossing?authuser=0'


def getOnePage(start, num):
    data = {
        'start': start,
        'num': num,
        'numChildren': 0,
        'cctcss': 'square-cover',
        'cllayout': 'NORMAL',
        'ipf': 1,
        'xhr': 1,
        'token': 'pzoDCGeZDOdn02YGNGMMMb-gRfU:1548222057735'
    }

    response = requests.post(url, data=data, headers=header)

    if response.status_code == 200:
        html = response.text

        pattern = '<div.*?data-original-classes.*?card-click-targe.*?<a.*?title.*?tabindex="-1">(.*?)<span.*?data-docid="(.*?)".*?<div.*?reason-set.*?current-rating.*?"width:(.*?);".*?</div>'

        results = re.findall(pattern, html, re.S)

        with open("topFreeApp.txt", "a") as file:
            for result in results:
                APPInfo = {
                    'rank': result[0].strip().split(".")[0].strip(),
                    'name': result[0].strip().split(".")[1].strip(),
                    'package': result[1].strip(),
                    'rating': round(float(result[2].strip()[:-1]) / 20, 1)
                }

                print(APPInfo)


def main():
    for i in range(9):
        getOnePage(i * 60, 60)


if __name__ == "__main__":
    main()
