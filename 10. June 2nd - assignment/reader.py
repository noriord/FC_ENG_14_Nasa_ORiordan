
import sys
import os
import csv
import json
import pickle

# In Terminal, enter cd ..\Lesson9
# python reader.py source.csv destination.json "0,0,piano" "1,1,mug"


# Base class
class FileHandler:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = []

    def read(self):
        pass

    def write(self):
        pass

    def display(self):
        for row in self.data:
            print(row)


# CSV handler
class CSVHandler(FileHandler):
    def read(self):
        file = open(self.filepath, "r", newline="")
        reader = csv.reader(file)
        self.data = []
        for row in reader:
            self.data.append(row)
        file.close()

    def write(self):
        file = open(self.filepath, "w", newline="")
        writer = csv.writer(file)
        for row in self.data:
            writer.writerow(row)
        file.close()


# JSON handler
class JSONHandler(FileHandler):
    def read(self):
        file = open(self.filepath, "r")
        self.data = json.load(file)
        file.close()

    def write(self):
        file = open(self.filepath, "w")
        json.dump(self.data, file, indent=2)
        file.close()


# Pickle handler
class PickleHandler(FileHandler):
    def read(self):
        file = open(self.filepath, "rb")
        self.data = pickle.load(file)
        file.close()

    def write(self):
        file = open(self.filepath, "wb")
        pickle.dump(self.data, file)
        file.close()


# Function to get the right handler based on file extension
def get_handler(filepath):
    extension = os.path.splitext(filepath)[1]
    if extension == ".csv":
        return CSVHandler(filepath)
    elif extension == ".json":
        return JSONHandler(filepath)
    elif extension == ".pickle":
        return PickleHandler(filepath)
    else:
        print("Error: Unsupported file type: " + extension)
        return None


# Main program
if len(sys.argv) < 3:
    print("Usage: python reader.py source destination [changes...]")
    print('Example: python reader.py source.csv destination.json "0,0,piano" "1,1,mug"')
    sys.exit(1)

src = sys.argv[1]
dst = sys.argv[2]
changes = sys.argv[3:]

# Check if source file exists
if not os.path.exists(src) or not os.path.isfile(src):
    print("Error: File not found: " + src)
    directory = os.path.dirname(src)
    if directory == "":
        directory = "."
    print("Files in directory:")
    for item in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, item)):
            print("  " + item)
    sys.exit(1)

# Read source file
source_handler = get_handler(src)
if source_handler is None:
    sys.exit(1)

source_handler.read()

# Apply changes
for change in changes:
    parts = change.split(",", 2)  # Split into at most 3 parts
    x = int(parts[0].strip())     # column
    y = int(parts[1].strip())     # row
    value = parts[2].strip()
    source_handler.data[y][x] = value

# Display modified data
print("Modified data:")
print("-" * 30)
source_handler.display()
print("-" * 30)

# Save to destination
dest_handler = get_handler(dst)
if dest_handler is None:
    sys.exit(1)

dest_handler.data = source_handler.data
dest_handler.write()
print("Saved to: " + dst)
