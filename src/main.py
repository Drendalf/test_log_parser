import argparse
import os
from tabulate import tabulate
import datetime


class ReportMakerException(Exception):
    """Exception for reports."""


class ReportMaker:
    serial_number=0

    def __init__(self, files:list):
        self.files=files

    def _file_path(self, file_path:str)->str:
        return os.path.abspath(file_path)

    def _prepare_data_for_average_report(self, line:dict, data:dict):
        if line['url'] in data:
            data[line['url']][2] += line['response_time']
            data[line['url']][3] += 1
        else:
            data[line['url']] = [self.serial_number, line['url'], line['response_time'], 1]
            self.serial_number+=1
        return data

    def _make_average_report(self, files:list, report_date:str)->dict:
        data={}
        if report_date:
            try:
                report_date = datetime.datetime.strptime(report_date, '%Y-%m-%d').date()
            except ValueError as exc:
                raise ReportMakerException(f'{report_date}  not valid date format. {repr(exc)}')

        for file in files:
            try:
                with open (self._file_path(file), 'r') as file_data:
                    for line in file_data:
                        line = eval(line)
                        if not report_date:
                            self._prepare_data_for_average_report(line, data)
                        else:
                            date =line['@timestamp'].split('T')[0]

                            if report_date == datetime.datetime.strptime(date, '%Y-%m-%d').date():
                                self._prepare_data_for_average_report(line, data)
                            else:
                                continue

            except FileNotFoundError as exc:
                print(f'{self._file_path(file)} is not correct path. {repr(exc)}')

        return data

    def make_report(self, report_type:str, date:str=None)->str:
        types_of_reports = {'average': {'data':self._make_average_report(self.files, date), 'headers':['', 'handler', 'total', 'avg_response_time']}}

        if report_type in types_of_reports:
            data = types_of_reports[report_type]['data'].values()
            for el in data:
                avg_response_time = el[2]/el[3]
                el.pop(3)
                el.insert(3, avg_response_time)

            return tabulate(data, headers=types_of_reports[report_type]['headers'])
        else:
            raise ReportMakerException(f'{report_type}  is not correct report type.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parser for logs.')
    parser.add_argument('--file', help='file path', nargs='+')
    parser.add_argument('--report', help='report type')
    parser.add_argument('--date', help='date logs')
    args = parser.parse_args()

    print(ReportMaker(files=args.file).make_report(args.report, args.date))



