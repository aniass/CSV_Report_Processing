import csv
import sys
import time
from pathlib import Path
import pycountry

def find_country_code(country: str) -> str:
    """
    Find the country code for a given country/region name.
    If not found, returns 'XXX'.
    """
    try:
        region = pycountry.subdivisions.lookup(country).country_code
        region_two = pycountry.countries.lookup(region).alpha_3
        return region_two
    except LookupError:
        return 'XXX'


def format_date(other_date: str) -> str:
    """
    Convert date format from 'mm/dd/YYYY' to 'YYYY-mm-dd'.
    """
    old_format = time.strptime(other_date, '%m/%d/%Y')
    formatted_date = time.strftime('%Y-%m-%d', old_format)
    return formatted_date


def calculate_clicks(impression: str, ctr: str) -> int:
    """
    Calculate number of clicks from the number of impressions and CTR rate.
    """
    ctr_percent = float(ctr.rstrip('%'))
    number_clicks = round(float(impression) * ctr_percent / 100.0)
    return int(number_clicks)


def process_data(input_path:Path, output_path:Path)-> None:
    """
    Read input CSV, transform data, and write to output CSV.
    Expected input columns: date (mm/dd/YYYY), country, impressions, ctr.
    Output columns: date, country code, number of impressions, number of clicks.
    """
    try:
        with input_path.open('r', encoding='utf-8', newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=",")
            next(reader)  # Skip header row
            
            results = []
            for row in reader:
                if len(row) < 4:
                    continue # Skip malformed rows

                formatted_date = format_date(row[0])
                country_code = find_country_code(row[1])
                clicks = calculate_clicks(row[2], row[3])
                results.append([formatted_date, country_code, row[2], clicks])

        headers = ['date', 'country code', 'number of impressions', 'number of clicks']
        with output_path.open('w', newline='', encoding='utf-8') as out_file:
            writer = csv.writer(out_file, delimiter=",")
            writer.writerow(headers)
            writer.writerows(results)

    except FileNotFoundError as e:
        sys.exit(f'Input file not found: {e}')
    except csv.Error as e:
        sys.exit(f'CSV error: {e}')
    except Exception as e:
        sys.exit(f'Unexpected error: {e}')
        

def main():
    """
    Entry point. Supports optional CLI arguments for input/output paths.
    Usage: python script.py [input.csv] [output.csv].
    """
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('report.csv')
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('output.csv')
    process_data(input_path, output_path) 
        
         
if __name__ == '__main__':
    main()

 