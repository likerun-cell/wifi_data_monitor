import os
import zipfile

from statsd import StatsClient

from utils.common_config import statsd_host, statsd_port, config
from utils.monitor import Monitor

from watchdog.observers import Observer


def main():

    statsd_client = StatsClient(statsd_host, statsd_port, prefix="wifi.parse.data")
    statsd_client.gauge("WA_SOURCE_FJ_1001.success", 0)
    statsd_client.gauge("WA_SOURCE_FJ_1001.failed", 0)
    statsd_client.gauge("WA_BASIC_FJ_1003.success", 0)
    statsd_client.gauge("WA_BASIC_FJ_1003.failed", 0)
    statsd_client.gauge("file.failed", 0)
    list = os.listdir(config["monitor_path"])  # 列出文件夹下所有的目录与文件
    for i in list:
        com_path = os.path.join(config["monitor_path"], i)
        Monitor(stastd=statsd_client, zipinfo="True").operate_change(com_path)
    event_handler = Monitor(stastd=statsd_client)
    observer = Observer()
    observer.schedule(event_handler, path=config["monitor_path"], recursive=True)  # recursive递归的
    observer.start()
    observer.join()

