import csv
import sys
import pycountry
import time


def find_country_code(country):
    """Function that finds country code for the region"""
    try:
        region = pycountry.subdivisions.lookup(country).country_code
        region_two = pycountry.countries.lookup(region).alpha_3
        return region_two
    except LookupError:
        return 'XXX'


def format_date(other_date):
    """Function that changes the date format."""
    old_format = time.strptime(other_date, '%m/%d/%Y')
    formatted_date = time.strftime('%Y-%m-%d', old_format)
    return formatted_date


def calculate_clicks(impression, ctr):
    """Calculation the number of clicks from number of impressions and CTR rate"""
    ctr_percent = float(ctr[:-1])
    number_clicks = round(float(impression) * ctr_percent / 100)
    return number_clicks


def process_data(input_file, output_file):
    try:
        with open('report.csv', 'r', encoding='utf-8', newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=",")
            rows = [row for i, row in enumerate(reader) if i > 0]
    except csv.Error as e:
        sys.exit('file {}, line {}: {}'.format('report.csv', reader.line_num, e))

    results = []
    for row in rows:
        row[0] = format_date(row[0])
        row[1] = country_code(row[1])
        row[3] = calculate_clicks((row[2], row[3])
        results.append(row)

    headers = ['date', 'country code', 'number of impressions', 'number of clicks']
    with open('output.csv','w', newline='', encoding='utf-8') as out_file:
        writer = csv.writer(out_file, delimiter=",")
        writer.writerow(headers)
        for result in results:
            writer.writerow(result)
         

if __name__ == '__main__':
    process_data()
    