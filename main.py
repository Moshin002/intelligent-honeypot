#!/usr/bin/env python3
"""
Intelligent Honeypot Main Controller
"""

import logging
import sys
from pathlib import Path
import json
from modules.ssh_honeypot import SSHHoneypot


# Configure logging first to catch startup errors
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('honeypot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_config():
    """Load configuration from JSON file"""
    config_path = Path(__file__).parent / 'config' / 'devices.json'
    try:
        with open(config_path) as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("Config file not found at %s", config_path)
        sys.exit(1)
    except json.JSONDecodeError:
        logger.error("Invalid JSON in config file")
        sys.exit(1)


class IntelligentHoneypot:
    """Main honeypot controller class"""

    def __init__(self, config):
        """Initialize honeypot with configuration"""
        self.config = config
        try:
            # Get the first device's config (e.g., home_router)
            device_name = next(iter(self.config))
            device_config = self.config[device_name]

            self.ssh_honeypot = SSHHoneypot(config=device_config['ssh'])
            logger.info(f"SSH honeypot initialized for {device_name}")
        except KeyError:
            logger.error("Missing SSH configuration in device settings")
            sys.exit(1)
        except StopIteration:
            logger.error("No devices configured")
            sys.exit(1)
