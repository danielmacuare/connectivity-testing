import argparse
import csv
import logging
import os
import subprocess
import sys

# RESULTS_DIRECTORY = "../../connectivity_test_results"
RESULTS_DIRECTORY = (
    "/Users/dmac/repos/connectivity-tests-automation/connectivity_test_results"
)


def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Created directory: {directory}")


def setup_logging():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def extract_ip_addresses(file_path, column_name):
    try:
        with open(file_path, mode="r", encoding="UTF-8") as file:
            csv_reader = csv.DictReader(file)
            if column_name not in csv_reader.fieldnames:
                raise ValueError(f"Column '{column_name}' not found in CSV file")
            return [row[column_name] for row in csv_reader]
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        sys.exit(1)
    except csv.Error as e:
        logging.error(f"Error reading CSV file: {e}")
        sys.exit(1)


def run_connectivity_check(ip, port, protocol):
    command = f"nc -l -u {ip} {port}"
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        return f"IP: {ip}, {protocol.upper()} Success: {result.stdout.strip()}"
    except subprocess.CalledProcessError as e:
        return f"IP: {ip}, {protocol.upper()} Error: {e.stderr.strip()}"


def check_connectivity(ip_addresses, port, protocol):
    results = []
    for ip in ip_addresses:
        output = run_connectivity_check(ip, port, protocol)
        logging.info(output)
        results.append(output)

    result_file_path = os.path.join(RESULTS_DIRECTORY, f"{protocol}.txt")
    with open(result_file_path, "w") as f:
        for result in results:
            f.write(f"{result}\n")
    logging.info(f"Results written to {result_file_path}")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Network Connectivity Tester")
    parser.add_argument(
        "file_path", help="Path to the CSV file containing IP addresses"
    )
    parser.add_argument(
        "column_name", help="Name of the column containing IP addresses"
    )
    parser.add_argument(
        "--protocols",
        nargs="+",
        choices=["snmp", "ssh"],
        default=["snmp", "ssh"],
        help="Protocols to test (default: both snmp and ssh)",
    )
    return parser.parse_args()


def main():
    setup_logging()
    ensure_directory_exists(RESULTS_DIRECTORY)

    args = parse_arguments()
    logging.info(
        f"Starting connectivity tests with file: {args.file_path}, column: {args.column_name}"
    )

    ip_addresses = extract_ip_addresses(args.file_path, args.column_name)
    logging.info(f"Extracted {len(ip_addresses)} IP addresses")

    protocol_ports = {"snmp": 161, "ssh": 22}

    for protocol in args.protocols:
        check_connectivity(ip_addresses, protocol_ports[protocol], protocol)


if __name__ == "__main__":
    main()
