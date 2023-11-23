import csv
import sys
import pycountry
import time


def find_country_code(country):
    """
    Function that finds the country code for the region.
    If the country code is not found it returns 'XXX'.
    """
    try:
        region = pycountry.subdivisions.lookup(country).country_code
        region_two = pycountry.countries.lookup(region).alpha_3
        return region_two
    except LookupError:
        return 'XXX'


def format_date(other_date):
    """
    Function that changes the date format from 'mm/dd/yyyy' to 'yyyy-mm-dd'.
    """
    old_format = time.strptime(other_date, '%m/%d/%Y')
    formatted_date = time.strftime('%Y-%m-%d', old_format)
    return formatted_date


def calculate_clicks(impression, ctr):
    """
    Function that calculates the number of clicks from the number of impressions and CTR rate.
    """
    ctr_percent = float(ctr[:-1])
    number_clicks = round(float(impression) * ctr_percent / 100)
    return number_clicks


def process_data(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8', newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=",")
            next(reader)  # Skip header row
            
            results = []
            for row in reader:
                formatted_date = format_date(row[0])
                country_code = find_country_code(row[1])
                clicks = calculate_clicks(row[2], row[3])
                results.append([formatted_date, country_code, row[2], clicks])

        headers = ['date', 'country code', 'number of impressions', 'number of clicks']
        with open(output_file, 'w', newline='', encoding='utf-8') as out_file:
            writer = csv.writer(out_file, delimiter=",")
            writer.writerow(headers)
            writer.writerows(results)
    except csv.Error as e:
        sys.exit('File {}, line {}: {}'.format(input_file, reader.line_num, e))
        
         
if __name__ == '__main__':
    input_file = 'report.csv'
    output_file = 'output.csv'
    process_data(input_file, output_file)
 