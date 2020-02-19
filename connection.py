import csv


def open_file(filename: str) -> list:
    """
    simpler variation of open_file function
    """
    with open(filename, newline='') as csvfile:
        return [(dict(row)) for row in csv.DictReader(csvfile)]


def save_file(data_to_write: list, filename: str):
    fieldnames = list(data_to_write[0].keys())
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for line in data_to_write:
            writer.writerow(line)