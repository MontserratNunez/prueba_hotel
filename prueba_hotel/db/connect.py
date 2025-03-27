import csv

def write(name, columns):
    """Write the header of a file with the values of the arguments"""
    with open(f".\\db\\db_csv\\{name}.csv", "w", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()

def append(name, values):
    """Appends the values to a file with the name argument"""
    with open(f".\\db\\db_csv\\{name}.csv", "a", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(values)

def read(name):
    """Read the file with the name argument"""
    info = []
    with open(f".\\db\\db_csv\\{name}.csv", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            info.append(row)
        return info
