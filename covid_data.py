import argparse
import csv
from datetime import datetime

# command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--date', help="Formate date like 2020-04-16")
parser.add_argument('-conf',action='store_true')
parser.add_argument('-rec', action='store_true')
parser.add_argument('-c', '--country',help="Enclose country name inside ' ' ")
parser.add_argument('-co', '--continent',help="Enclose continet name inside ' ' ")
parser.add_argument('-s', '--state',help="Enclose state name inside ' ' ")
args = parser.parse_args()


class getData():
    def __init__(self,args):
        date_req = args.date
        # initial check for date argument and its correct format
        if date_req is None:
            print("Date is a required argument. -d <date>")
        datetime.strptime(date_req, "%Y-%m-%d")

    def fetch_data(self,args):
        date_req = args.date
        confirmed = args.conf
        recovered = args.rec
        country = args.country
        continent = args.continent
        state = args.state
        params = {'date': date_req, 'country': country,'state':state}
        # if no country or continent provided then search for global cases
        if (country is None) and (continent is None):
            # condition that checks for only confirmed cases
            if (confirmed is True) and (recovered is False):
                confirmedCases = self.confirmed_cases(params)
                print("confirmed cases=", confirmedCases)
            # condition that checks for only recovered cases
            if (recovered is True) and (confirmed is False): 
                recoveredCases = self.recovered_cases(params)
                print("recovered cases=",recoveredCases)
            # if no filter is defined then fetch both confirmed and recovered cases
            if (confirmed is False) and (recovered is False):  
                confirmedCases = self.confirmed_cases(params)
                recoveredCases = self.recovered_cases(params)
                recoveryratio = round(recoveredCases/confirmedCases,2)
                print("recovered cases=",recoveredCases, ", confirmed cases=", confirmedCases,", recovery_ratio=",recoveryratio)
        else:
            # condition that checks for the presence of continent
            if country is None:
                # condition that checks for only confirmed cases for the entire continent
                if (confirmed is True) and (recovered is False):
                    total_confirmed = 0
                    all_countries = self.countries_by_continent(continent)
                    for i in range(len(all_countries)):
                        params = {'date': date_req, 'country': all_countries[i],'state':state}
                        total_confirmed += self.confirmed_cases(params)
                    print("confirmed cases=", total_confirmed)
                # condition that checks for only recovered cases for the entire continent
                elif (recovered is True) and (confirmed is False): 
                    total_recovered = 0
                    all_countries = self.countries_by_continent(continent)
                    for i in range(len(all_countries)):
                        params = {'date': date_req, 'country': all_countries[i],'state':state}
                        total_recovered += self.recovered_cases(params)
                    print("recovered cases=", total_recovered)
                # if no filter is defined then fetch both confirmed and recovered cases for entire continent
                else:  
                    total_confirmed = 0
                    total_recovered = 0
                    all_countries = self.countries_by_continent(continent)
                    for i in range(len(all_countries)):
                        params = {'date': date_req, 'country': all_countries[i],'state':state}
                        total_confirmed += self.confirmed_cases(params)
                        total_recovered += self.recovered_cases(params)
                    recoveryratio = round(total_recovered/total_confirmed,2)     
                    print("recovered cases=",total_recovered, ", confirmed cases=", total_confirmed,", recovery_ratio=",recoveryratio)

            else:
                # brings only confirmed cases w.r.t the country and state provided
                if (confirmed is True) and (recovered is False):
                    confirmedCases = self.confirmed_cases(params)
                    print("confirmed cases=", confirmedCases)
                # brings only recovered cases w.r.t the country and state provided
                elif (recovered is True) and (confirmed is False): 
                    recoveredCases = self.recovered_cases(params)
                    print("recovered cases=",recoveredCases)
                # if no filter is defined then fetch both confirmed and recovered cases for that country and its state
                else: 
                    confirmedCases = self.confirmed_cases(params)
                    recoveredCases = self.recovered_cases(params)
                    recoveryratio = round(recoveredCases/confirmedCases,2)
                    print("recovered cases=",recoveredCases, ", confirmed cases=", confirmedCases,", recovery_ratio=",recoveryratio)
                    
    def recovered_cases(self,params):
        dt = params['date']
        res = 0
        new_dt = format_date(dt)
        # reading covid_recovered.csv file
        with open('covid_recovered.csv','r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            # check if the country was provided then fetch global data
            if params['country'] is None:
                for line in csv_reader:
                    res += int(line[new_dt])
            # if the country was present, check for the state first
            else:
                # if the state was present then fetch data for that country w.r.t state
                if params['state']:
                    for line in csv_reader:
                        if (params['state'] == line['Province/State']) and (params['country'] == line['Country/Region']):
                            res = (int(line[new_dt]))
                # if a specific state is not defined then fetch data of state/states for that country
                else:   
                    for line in csv_reader:
                        if params['country'] == line['Country/Region']:
                             # check whether the country has an avilable state or not
                            if line['Province/State'] != '':
                               res += int(line[new_dt])
                            else:
                                res = (int(line[new_dt]))  
        return res

    def confirmed_cases(self,params):
        dt = params['date']
        res = 0
        new_dt = format_date(dt)
        with open('covid_confirmed.csv','r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            # check if the country was provided then fetch global data
            if params['country'] is None:
                for line in csv_reader:
                    res += int(line[new_dt])
             # if the country was present, check for the state first
            else:
                # if the state was present then fetch data for that country w.r.t state
                if params['state']:
                    for line in csv_reader:
                        if (params['state'] == line['Province/State']) and (params['country'] == line['Country/Region']):
                            res = (int(line[new_dt]))
                # if a specific state is not defined then fetch data of state/states for that country
                else:   
                    for line in csv_reader:
                        if params['country'] == line['Country/Region']:
                             # check whether the country has an avilable state or not
                            if line['Province/State'] != '':
                               res += int(line[new_dt])
                            else:
                                res = (int(line[new_dt]))  
        return res

# function thet accepts the continent name and fetch all countries in that continent
    def countries_by_continent(self,continent):
        self.continent = continent
        countries = []
        with open('countries_to_continent.csv','r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for line in csv_reader:
                if line['Continent'] == continent:
                    countries.append(line['Country'])
        return countries            

# function for formatting date in the format required to parse csv data
def format_date(dt):
    dt = datetime.strptime(dt, '%Y-%m-%d').strftime('%m %d %Y')
    dt_array = dt.split()
    if int(dt_array[0]) < 10:
            dt_array[0] = dt_array[0][1:]
    new_date = dt_array[0]+"/"+dt_array[1]+"/"+dt_array[2][2:]
    return new_date

if __name__ == '__main__':
    d = getData(args)
    d.fetch_data(args)