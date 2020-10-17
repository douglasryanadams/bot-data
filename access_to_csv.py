"""
This script takes our access logs and transforms them into tabularized CSV files
"""
import os
import sys
import csv
from datetime import datetime
import argparse
import logging
from typing import List, Union

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
LOGGER = logging.getLogger()
OUTPUT_DIRECTORY = './csv'
DATE_FORMAT = '[%d/%b/%Y:%H:%M:%S %z]'
VALID_HTTP_METHODS = {'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'}


class Processor:
    """
    This processor will read through access.log files and transform them into CSVs
    """

    def __init__(self, access_log_path: str):
        LOGGER.debug('Initializing Process for: %s', access_log_path)

        self.__access_log_path = access_log_path
        access_filename = self.__access_log_path.split('/')[-1]
        LOGGER.debug('  access_filename: %s', access_filename)
        csv_filename = f'{access_filename[0: -4]}.csv'
        LOGGER.debug('  csv_filename=%s', csv_filename)
        self.__csv_file_path = os.path.join(OUTPUT_DIRECTORY, csv_filename)

        self.__access_file_reader = None
        self.__csv_file_writer = None

        self.previous_line_data = []

    def __enter__(self):
        if not os.path.exists(OUTPUT_DIRECTORY):
            os.mkdir(OUTPUT_DIRECTORY)
        self.__access_file_reader = open(self.__access_log_path, 'r')
        open(self.__csv_file_path, 'w').close()  # Start with an empty file
        self.__csv_file_writer = open(self.__csv_file_path, 'a')
        self.__csv_util = csv.writer(
            self.__csv_file_writer,
            delimiter=',',
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__access_file_reader.close()
        self.__csv_file_writer.close()

    def process(self) -> None:
        """
        This takes the output of the parsed data and writes it into a CSV file

        Currently, this appears to process roughly 20,000 to 40,000 lines every second
        This, and the parse logic could be re-implemented in either Rust, C, or C++ and may execute much faster
        """
        for line in self.__access_file_reader:
            try:
                data = parse_line(line)
                self.__write_csv_line(data)
            except ValueError as e:
                LOGGER.warning('Failed to parse line (%s): %s', e, line)

    def __write_csv_line(self, data: List[Union[int, str]]) -> None:
        self.__csv_util.writerow(data)


def parse_line(line: str) -> List:
    """
    This method is written to optimize for speed over readability

    It's general strategy is to iterate over the characters in the log line and
    store them in a temporary list as we go. Once we find a logic place to save
    the stored characters, we add them as a string to the result list.

    See 'test_parse_line.py' for test cases to make sure we handle weird edges
    found in the wild appropriately.

    Resulting List Positions:
         0: IP Address
         1: 'Identity' via identd
         2: UserID
         3: Date and Time
         4: HTTP Method
         5: URI
         6: HTTP Version
         7: HTTP Response Code
         8: Size of Response
         9: Referrer
        10: User Agent
    """
    result = []
    position = 0
    current_str = []
    active_string = False
    skip_to_end_of_string = False
    previous_char_space = False
    previous_char_quote = False
    for c in line:
        if active_string and skip_to_end_of_string and c != '"':
            # Allows us to skip malformed HTTP Request Lines
            continue

        if c == '"':
            if previous_char_quote:
                # Found an empty string
                result.append(None),
                previous_char_quote = False
                active_string = False
                position += 1
                continue

            previous_char_quote = True
            if active_string:
                active_string = False
                if skip_to_end_of_string:
                    skip_to_end_of_string = False
                if position > 10:
                    # We don't care what comes after the user agent string (if anything)
                    # so we break out of the loop
                    break
            else:
                active_string = True
            # There's no reason to capture quotes so we can skip these characters
            continue
        else:
            previous_char_quote = False

        if c == ' ':
            if previous_char_space:
                # This allows multiple consecutive spaces to be treated as one
                continue

            # Position 3 is the first part of the timestamp, position 4 is the timezone
            # Position 10 is the beginning of the user agent string
            if position == 3 or (position > 10 and active_string):
                current_str.append(' ')
                position += 1
                continue

            restringed = ''.join(current_str)
            if restringed == '-':
                result.append(None)
            elif position == 4:
                # Ignoring timezones for now
                result.append(datetime.strptime(restringed, DATE_FORMAT).replace(tzinfo=None))
            elif position == 5:
                if restringed in VALID_HTTP_METHODS:
                    result.append(restringed)
                else:
                    # We've discovered a malformed HTTP Request Line
                    result.append('malformed')
                    result.append('malformed')
                    result.append('malformed')
                    position += 2
                    skip_to_end_of_string = True

            elif position in (8, 9):
                result.append(int(restringed))
            else:
                result.append(restringed)
            current_str = []
            position += 1
            previous_char_space = True
        else:
            previous_char_space = False
            current_str.append(c)

    if current_str == ['-']:
        result.append(None)
    else:
        result.append(''.join(current_str))

    return result


def main() -> None:
    parser = argparse.ArgumentParser('This script turns access.log files into CSV files')
    parser.add_argument('-f', '--filename', type=str, help='Name of file to read', required=True)
    args = parser.parse_args()

    with Processor(args.filename) as processor:
        processor.process()


if __name__ == '__main__':
    main()
