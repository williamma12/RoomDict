import logging
import logging.config
import os

import yaml


def _setup_logging(
    default_path="logging.yml",
    default_level=logging.INFO,
):
    """Setup logging configuration"""
    if os.path.exists(default_path):
        with open(default_path, "rt") as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
