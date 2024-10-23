import pandas as pd
import sys

def read_csv_file(filename):
    try:
        # Read the CSV file into a pandas DataFrame
        data = pd.read_csv(filename)
        return data
    except FileNotFoundError:
        print("The specified file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Get csv file name from the command line arguments
    if len(sys.argv) != 2:
        print("Usage: python script.py <csv_file>")
        sys.exit(1)

    filename = sys.argv[1]

    # Run function that reads csv file
    data = read_csv_file(filename)

    # Get the number of issues for each assignee
    total_issues = data['assignee'].value_counts()
    print(total_issues)