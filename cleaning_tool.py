import pandas as pd
import sys
from string_cleaning import clean_string

def main(column_name, input_file, output_file):
    """
        This function produce a csv file
        where a column, supposing it contains a string, is cleaned
        :param column_name: column where to apply the cleaning
        :param input_file: input csv file
        :param output_file: output csv file
        """

    print("\nSetup completed.")
    print("Reading input file: " + input_file)
    # Load the CSV file
    df = pd.read_csv(input_file)

    # Apply the clean_text function to the 'title' column
    df[column_name] = df[column_name].apply(clean_string)

    # Save the updated dataframe to a new CSV file
    df.to_csv(output_file, index=False)

    print("Done! Produced output file: " + output_file)

if __name__ == "__main__":
    # Get input and output file paths from the command line arguments
    if len(sys.argv) != 4:
        print("Usage: python script.py column_name <input_file> <output_file>")
        sys.exit(1)

    column_name = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    # Run the main function
    main(column_name,input_file, output_file)
