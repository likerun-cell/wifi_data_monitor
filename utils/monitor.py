import os

from watchdog.events import FileSystemEventHandler

from utils.common_config import logger
from utils.database import KafkaData
from utils.parser import CSVParser
from utils.wifi import WiFiData


class Monitor(FileSystemEventHandler):
    def __init__(self, stastd=None, zipinfo=None):
        FileSystemEventHandler.__init__(self)
        self.statsd = stastd
        self.zipinfo = zipinfo

    def on_created(self, event):
        self.operate_change(event)

    def on_moved(self, event):
        self.operate_change(event)

    def on_modified(self, event):
        self.operate_change(event)

    def operate_change(self, event):
        timer = self.statsd.timer("time").start()
        try:
            if self.zipinfo:
                csv_obj = CSVParser.from_zip(event)
            else:
                event = event.src_path
                csv_obj = CSVParser.from_zip(event)
            if not csv_obj:
                return
            csv_list, meta = csv_obj.reader
        except Exception as e:
            logger.error(e)
            logger.error(event)
            self.statsd.gauge("file.failed", 1, delta=True)
            return
        wifis = []
        try:
            for row in csv_list:
                wifi = WiFiData(row, meta).to_tuple()
                wifis.append(wifi)
            if "WA_SOURCE_FJ_1001" in meta.source_info:
                table_name = "wa_source"
                KafkaData().send_data(table_name, wifis)
                self.statsd.gauge("WA_SOURCE_FJ_1001.success", 1, delta=True)
            elif "WA_BASIC_FJ_1003" in meta.source_info:
                table_name = "wa_basic"
                KafkaData().send_data(table_name, wifis)
                self.statsd.gauge("WA_BASIC_FJ_1003.success", 1, delta=True)
            timer.stop()
            os.remove(event)
            print("done")
        except Exception as e:
            self.statsd.gauge(meta.source_info[2] + ".failed", 1, delta=True)
            logger.info(e)
            return
