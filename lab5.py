import io
import re  # regular expressions
from collections import Counter
import statistics
import os
import gzip


# чтение логов
def read_log(log):
    if os.path.splitext(log)[1] == '.gz':
        with gzip.open(log) as zip_log:
            with io.TextIOWrapper(zip_log, encoding='utf-8') as unzip_log:
                log = unzip_log.read()

    else:
        with open(log, 'r') as file:
            log = file.read()
    return log


def parser():
    folder = {"LOG_DIR": "./logs"}

    # паттерны для филтрации логов
    patterns = {'search_url': r'\"[A-Z]+ ([^\s]+)', 'search_request_time': r'.* (\d+\.\d+)'}

    log_names = sorted(os.listdir(folder.get("LOG_DIR")))
    if not log_names:
        return print('Logs has not found!')
    log_name = log_names[-1]

    log_path = f'{folder.get("LOG_DIR")}/{log_name}'

    total = 0

    # отфильтрованные логи
    clear_urls = re.findall(patterns['search_url'], read_log(log_path))
    clear_request_time = re.findall(patterns['search_request_time'], read_log(log_path))

    # подсчет того, сколько раз попадается url
    number_of_urls = Counter(clear_urls)

    report = []

    if not clear_request_time:
        print("[WARNING] $request_time has not found!")

        for key, value in number_of_urls.items():
            total += value

        for key, value in number_of_urls.items():
            report.append(f"URL - {key} - {value} - {round((value / total) * 100)}% - !not found!")

        for i in range(len(report)):
            print(report[i])

        print("[WARNING] Can't calculate median without $request_time!")

    else:
        for key, value in number_of_urls.items():
            total += value

        j = 0

        for key, value in number_of_urls.items():
            if not clear_request_time[j]:
                report.append(f"URL - {key} - {value} - {round((value / total) * 100)}% - not found")
                j += 1
            else:
                report.append(f"URL - {key} - {value} - {round((value / total) * 100)}% - {clear_request_time[j]}")
                j += 1

        for i in range(len(report)):
            print(report[i])

        # медиана времени запроса
        print('Медиана - ' + str(statistics.median(map(float, clear_request_time))))


if __name__ == '__main__':
    parser()