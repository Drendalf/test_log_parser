import argparse
import datetime
import json
import os

from tabulate import tabulate


class ReportMakerException(Exception):
    """Exception for reports."""


class Average_report:
    serial_number = 0
    data = {}

    def _prepare_data_for_average_report(self, line: dict):
        if line["url"] in self.data:
            self.data[line["url"]][2] += line["response_time"]
            self.data[line["url"]][3] += 1
        else:
            self.data[line["url"]] = [
                self.serial_number,
                line["url"],
                line["response_time"],
                1,
            ]
            self.serial_number += 1

    def _count_average(self, data: list) -> list:
        for el in data:
            avg_response_time = el[2] / el[3]
            el.pop(3)
            el.insert(3, avg_response_time)
        return data

    def make_report(self, files: list, report_date: str) -> list:
        for file in files:
            try:
                with open(file) as file_data:
                    for line in file_data:
                        line = json.loads(line)
                        if not report_date:
                            self._prepare_data_for_average_report(line)
                        else:
                            date = line["@timestamp"].split("T")[0]

                            if (
                                report_date
                                == datetime.datetime.strptime(date, "%Y-%m-%d").date()
                            ):
                                self._prepare_data_for_average_report(line)
                            else:
                                continue

            except FileNotFoundError as exc:
                print(f"{self._file_path(file)} is not correct path. {repr(exc)}")

        report = self._count_average(list(self.data.values()))

        return report


class ReportMaker:
    def __init__(self, files: list, date: str = None):
        self.files = self._file_path(files)
        if date:
            self.report_date = self._check_date(date)
        else:
            self.report_date = date

    def _file_path(self, files_path: list) -> list:
        path_list = []
        for file_path in files_path:
            path_list.append(os.path.abspath(file_path))
        return path_list

    def _check_date(self, report_date: str):
        try:
            report_date = datetime.datetime.strptime(report_date, "%Y-%m-%d").date()
        except ValueError as exc:
            raise ReportMakerException(
                f"{report_date}  not valid date format. {repr(exc)}"
            )
        return report_date

    def get_report(self, report_type: str) -> str:
        types_of_reports = {
            "average": {
                "report": Average_report(),
                "headers": ["", "handler", "total", "avg_response_time"],
            }
        }

        if report_type in types_of_reports:
            report = types_of_reports[report_type]["report"].make_report(
                self.files, self.report_date
            )
            return tabulate(report, headers=types_of_reports[report_type]["headers"])
        else:
            raise ReportMakerException(f"{report_type}  is not correct report type.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parser for logs.")
    parser.add_argument("--file", help="file path", nargs="+")
    parser.add_argument("--report", help="report type")
    parser.add_argument("--date", help="date logs")
    args = parser.parse_args()

    print(ReportMaker(files=args.file, date=args.date).get_report(args.report))
