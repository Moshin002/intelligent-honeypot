import logging


def setup_logger():
    logging.basicConfig(
        filename='threats.log',
        format='%(asctime)s - %(message)s',
        level=logging.INFO
    )


def log_threat(ip: str, payload: str, threat_type: str):
    logging.info(f"THREAT |IP:{ip}|Type:{threat_type}|Payload: {payload[:50]}")
