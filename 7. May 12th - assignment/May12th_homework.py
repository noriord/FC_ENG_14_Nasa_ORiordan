#Enter Terminal : "cd .\Lesson6\" & after that "python May12th_homework.py in.csv out.csv 0,0,piano 3,1,mug 1,2,17 3,3,0"
#Enter Terminal (test error)  :"python May12th_homework.py fake.csv out.csv 0,0,piano" error message comes up

import sys
import os
import csv

# Get arguments from command line
args = sys.argv

# Check we have at least src and dst
if len(args) < 3:
    print("Usage: python reader.py <src> <dst> <change1> <change2> ...")
    sys.exit(1)

src = args[1]       # source file
dst = args[2]       # destination file
changes = args[3:]  # list of changes

# Check if source file exists
if not os.path.exists(src) or not os.path.isfile(src):
    print(f"Error: '{src}' does not exist or is not a file.")
    print("Files in this directory:")
    for item in os.listdir("."):
        print(f"  {item}")
    sys.exit(1)

# Read the CSV file
data = []
with open(src, "r") as file:
    reader = csv.reader(file)
    for row in reader:
        data.append(row)

# Apply changes
for change in changes:
    parts = change.split(",", 2)
    col = int(parts[0])
    row = int(parts[1])
    value = parts[2]
    data[row][col] = value

# Display the result
print("Modified CSV content:")
for row in data:
    print(",".join(row))

# Save to destination
with open(dst, "w", newline="") as file:
    writer = csv.writer(file)
    for row in data:
        writer.writerow(row)