import pandas as pd
import sys
import argparse
from pathlib import Path
from string_cleaning import clean_string, remove_emoji, remove_special_char


def main(column_names: list[str], input_file: Path, output_file: Path):
    """
        This function produce a csv file
        where a column, supposing it contains a string, is cleaned
        :param column_names: list of columns to clean
        :param input_file: input csv file
        :param output_file: output csv file
        """

    print("\nSetup completed.")
    print("Reading input file: " + input_file.as_posix())
    # Load the CSV file    number,title,assignee,body
    df = (pd.read_csv(input_file,
                      dtype={"number": "int64", "title": "string", "assignee": "string", "body": "string"})
          .fillna({"number": "-1", "title": "", "assignee": "", "body": ""}))

    for current_column in column_names:
        df[current_column] = df[current_column].apply(clean_string)
        df[current_column] = df[current_column].apply(remove_emoji)
        df[current_column] = df[current_column].apply(remove_special_char)

    # Save the updated dataframe to a new CSV file
    df.to_csv(output_file, index=False)

    print("Done! Produced output file: " + output_file.as_posix())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='cleaning',
        description='clean the text')
    parser.add_argument("--col", nargs="+", default=["body", "title"],
                        help="list of columns that will be cleaned: -c <col 1> <col 2>")
    parser.add_argument("--input", help="input file path", type=Path, default="output.csv")
    parser.add_argument("--output", help="output file path", type=Path, default="cleaned_output.csv")

    args = parser.parse_args()

    columns_names: list[str] = args.col
    print(columns_names)
    in_file: Path = Path(args.input)
    out_file: Path = Path(args.output)

    # Get input and output file paths from the command line arguments

    # Run the main function
    main(columns_names, in_file, out_file)
