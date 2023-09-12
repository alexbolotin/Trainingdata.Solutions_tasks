import requests
from bs4 import BeautifulSoup


# url = "https://auto.ru/-/ajax/desktop/listing/"
# url = "https://auto.ru/-/ajax/desktop/events_log/"
url = "https://auto.ru"
print('URL:', url)
param = {
    "events":"[{\"timestamp\":\"2023-09-10T08:30:54.307Z\",\"web_tab_id\":\"e4b23a2e653f4b50d820b9963618b7cc\",\"page_view\":{},\"web_referer\":\"https://auto.ru/\",\"original_request_id\":\"efd1d83f5bb5c27071c3d73e2883702f\",\"context_rereferer\":\"https://auto.ru/\"}]",
    "geo_id":[],
    "_csrf_token":"1ec53943dd78b99b450c10b1d9e3bf7f0ff5ef5c14e8c76d"
    }

# param = {
#     "catalog_filter":[{"mark":"VAZ"}],
#     "section":"all",
#     "category":"cars",
#     "output_type":"list",
#     "geo_id":[],
#     }

headers = """
Host: auto.ru
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0
Accept: */*
Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
Referer: https://auto.ru/
Content-Type: application/json; charset=utf-8
Content-Length: 346
Origin: https://auto.ru
Connection: keep-alive
Cookie: suid=bbc43c91a03264b00492d698fe4c8697.c139711cbffc0188caba3aea44ec868f; autoru_sid=a%3Ag64fb32d72q1qmqpksmn3ao11vkuho0b.cfc09a4b69582e46882cfbdc67511c0b%7C1694184151506.604800.4AJcgkYW8UfkU5ECZaJPvg.oswoshErDyMsVCA003bEn8RimhAK_p7gL_Td7DX4GKo; autoruuid=g64fb32d72q1qmqpksmn3ao11vkuho0b.cfc09a4b69582e46882cfbdc67511c0b; _yasc=AH0lAcHSBMUPROX7krTCBWQ80i/5cOJYtucOWHD1a/vvtp9QXuVbWYD4HThvy9s5pEMZGMYZ; yandex_login=; i=3Rs7bz5K/f84rA9KgRGTCwYBRCQ/ermN0pSlbmOyYdY1NH+sZ6ixNEb8jFCScMV4PDpK95PHjo2+pZtUfWGmkr4fHso=; yandexuid=3069368771694334634; mda2_beacon=1694334634865; layout-config={"screen_height":1548,"screen_width":2752,"win_width":2752,"win_height":546.0999755859375}; popups-dr-shown-count=1; fp=6f4ff62b2e23dc96e25255cddc2084d1%7C1694184158528; crookie=0bxH1EJC3Zac54+5GvKxk9E3rmjaD5775E3AT2mNSzR8vUDxPXTxNdpJ+h0NDhU1q/3bBUSIIjPFQYsVWzn8yciZ91I=; cmtchd=MTY5NDE4NDE1ODk1MQ==; los=1; bltsr=1; coockoos=1; spravka=dD0xNjk0MTg0ODczO2k9NDYuNTMuMjQ0LjMwO0Q9Njk5NkEzMjM5ODc1NTEyODMxODcyOUQwNkM0NkNDMDBBQUYzMjg2N0EyRjI3RkE2MzBGODQ3MjkyMkI2MzRBNjk4RjFCQUU5RTQzQkU4NDBBRUEzRkEzNzE2ODE1ODE5QTk0NUVGMjJEODI3NkI4MUJGRTVCMDJDNzQ1NjlENDY3OTU0NzE4RDA4RDNGOTA4O3U9MTY5NDE4NDg3MzU2NDM1MTAwMDtoPWJhMzU2ZTlmM2ZhZTAwNWI4MTY4MjQwYmYxMzRmMzNi; _csrf_token=1ec53943dd78b99b450c10b1d9e3bf7f0ff5ef5c14e8c76d; from_lifetime=1694334649909; from=direct; ys=c_chck.2743144257; count-visits=3; sso_status=sso.passport.yandex.ru:synchronized; autoru_sso_blocked=1; Session_id=noauth:1694334634; sessar=1.1181.CiBNzYnl0BRGx9IaC1z9hfk6UWPZBrL_wgAmiKxPqbwatQ.skWlC9XLNxbvG8cZhAVg4EhadBzNarQ5aspkngPqPMA; autoru_gdpr=1; yaPassportTryAutologin=1
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
TE: trailers
""".strip().split("\n")

dict_headers = {}
for header in headers:
    key,value = header.split(": ", 1)
    dict_headers[key] = value

response = requests.post(url, json=param, headers=dict_headers)
print(response)
print(response.text)
# print(dir(response))
# print(response.text)
# Проверка успешности запроса
# if response.status_code == 200:
#     html = response.text
#     print(html)
# else:
#     print(f"Ошибка при запросе: {response.status_code}")