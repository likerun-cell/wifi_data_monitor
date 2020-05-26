statsd_host = "15.160.17.189"
statsd_port = 8125

config = {"monitor_path": "/wifi_data"}
kafka_host = "15.160.17.195"

import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("/app/logs/wifi_data.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addHandler(console)
