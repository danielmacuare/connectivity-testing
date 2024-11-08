import argparse
import csv
import logging
import os
import subprocess
import sys

FILE_PATH = "/Users/dmac/repos/connectivity-tests-automation/Conn_data.csv"
COLUMN_NAME = "ansible_host"
RESULTS_DIRECTORY = (
    "/Users/dmac/repos/connectivity-tests-automation/connectivity_test_results"
)


def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Created directory: {directory}")


def extract_ip_addresses(FILE_PATH, COLUMN_NAME):
    try:
        with open(FILE_PATH, mode="r", encoding="UTF-8") as file:
            csv_reader = csv.DictReader(file)
            if COLUMN_NAME not in csv_reader.fieldnames:
                raise ValueError(f"Column '{COLUMN_NAME}' not found in CSV file")
            return [row[COLUMN_NAME] for row in csv_reader]
    except FileNotFoundError:
        logging.error(f"File not found: {FILE_PATH}")
        sys.exit(1)
    except csv.Error as e:
        logging.error(f"Error reading CSV file: {e}")
        sys.exit(1)


def setup_logging():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def main():
    setup_logging()
    ensure_directory_exists(RESULTS_DIRECTORY)

    logging.info(
        f"Starting connectivity tests with file: {FILE_PATH}, column: {COLUMN_NAME}"
    )

    ip_addresses = extract_ip_addresses(FILE_PATH, COLUMN_NAME)
    print(ip_addresses)


if __name__ == "__main__":
    main()
