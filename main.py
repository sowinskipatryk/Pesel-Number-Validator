import pandas as pd
from faker import Faker
from time import time
from datetime import datetime
from datetime import timedelta
from faker.providers.ssn.pl_PL import calculate_month

fake = Faker('pl-PL')


# creating a function that returns the number of PESEL numbers in the form of a Series object given as an input argument
def generate_ssns(amount):
    ssns = [fake.ssn() for _ in range(amount)]
    return pd.Series(data=ssns, index=(list(range(amount))))

# printing the result object of the function for argument value equal to 10
# print(generate_ssns(10))


# implementing a helper function to generate a list of valid PESEL numbers fragments based on a date range
# given as arguments
def generate_pesel_list(from_date, to_date):

    pesel_dates = []

    from_date_str = from_date
    to_date_str = to_date

    from_date_obj = datetime.strptime(from_date_str, '%Y-%m-%d')
    to_date_obj = datetime.strptime(to_date_str, '%Y-%m-%d')

    iter_date_obj = from_date_obj
    while iter_date_obj < to_date_obj + timedelta(days=1):
        pesel_year = int(iter_date_obj.strftime("%y"))
        pesel_month = calculate_month(iter_date_obj)
        pesel_day = int(iter_date_obj.strftime("%d"))

        pesel_digits = [
            int(pesel_year / 10),
            pesel_year % 10,
            int(pesel_month / 10),
            pesel_month % 10,
            int(pesel_day / 10),
            pesel_day % 10,
        ]

        pesel_date = "".join(str(digit) for digit in pesel_digits)

        pesel_dates.append(pesel_date)

        iter_date_obj += timedelta(days=1)

    return pesel_dates


# implementation of the function that returns the number of PESEL numbers meeting the given conditions - gender
# and date of birth determined by the input parameter
def generate_unique_ssns(amount, sex, from_date, to_date):
    pesel_dates = generate_pesel_list(from_date, to_date)
    ssns = []
    while len(ssns) < amount:
        result = fake.unique.ssn()
        if ((sex == "M" and int(result[9]) % 2 != 0) or (sex == "F" and int(result[9]) % 2 == 0)) \
                and (result[0:6] in pesel_dates):
            ssns.append(result)
    return pd.Series(data=ssns, index=(list(range(amount))))


# calling the function and displaying the result on the screen for the argument equal to 10 and the conditions to be
# fulfilled - gender equals male and date range from 17-07-1994 to 11-12-1995
# print(generate_unique_ssns(10, "M", '1994-07-17', '1995-12-11'))


# implementation of a helper function to call the function given as an argument in a loop and measure the iteration time
def func_iterate(i, func, *args):
    start = time()
    for _ in range(i):
        func(*args)
    end = time() - start
    print(f'It took {(round(end,2))} seconds to execute {i} iterations of the {func.__name__} function.')

# calling the helper function for both ssns generating functions for 10, 100 and 1000 iterations of 1000 records
# func_iterate(10, generate_ssns, 1000)
# func_iterate(100, generate_ssns, 1000)
# func_iterate(1000, generate_ssns, 1000)
# func_iterate(10, generate_unique_ssns, 1000, "M", '1994-06-19', '1995-12-18')
# func_iterate(100, generate_unique_ssns, 1000, "M", '1994-06-19', '1995-12-18')
# func_iterate(1000, generate_unique_ssns, 1000, "M", '1994-06-19', '1995-12-18')


# implementation of the function which returns information about correct or incorrect validation of the PESEL number
# based on the given data - PESEL number to be checked, gender and date of birth
def validate_ssn(pesel, sex, birth_date_str):
    if (int(pesel[9]) % 2 == 0 and sex == 'F') or (int(pesel[9]) % 2 != 0 and sex == 'M') or sex == '':

        birth_date_obj = datetime.strptime(birth_date_str, '%Y-%m-%d')

        pesel_year = int(birth_date_obj.strftime("%y"))
        pesel_month = calculate_month(birth_date_obj)
        pesel_day = int(birth_date_obj.strftime("%d"))

        pesel_digits = [
            int(pesel_year / 10),
            pesel_year % 10,
            int(pesel_month / 10),
            pesel_month % 10,
            int(pesel_day / 10),
            pesel_day % 10,
        ]

        pesel_date = "".join(str(digit) for digit in pesel_digits)

        if pesel_date == pesel[0:6]:
            print('Valid')
            return
    print('Invalid')
    return


# some examples of using the validation function
validate_ssn('92120704192', 'M', '1992-12-07')
validate_ssn('92120704182', 'M', '1992-12-07')  # validation error - wrong sex (PESEL number indicates female)
validate_ssn('92120704192', 'F', '1992-12-07')  # validation error - wrong sex (PESEL number indicates male)
validate_ssn('92120704182', 'F', '1992-12-07')
validate_ssn('92120704192', 'M', '1992-12-08')  # validation error - birth date (day) doesn't match with PESEL number
validate_ssn('02320704192', 'M', '2002-12-07')
validate_ssn('02120704192', 'M', '2002-12-07')  # validation error - birth date (month) doesn't match with PESEL number
validate_ssn('97040204102', 'F', '1997-04-02')
validate_ssn('04231104132', 'M', '2004-03-11')
