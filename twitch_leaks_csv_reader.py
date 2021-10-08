import tablib
import time

# Change streamer id here.
# See https://www.streamweasels.com/support/convert-twitch-username-to-user-id/ to find ID from username.
STREAMER_ID = 212955371

# Change year here.
YEAR = 21

# Change months range here.
# Each month is the month of pay, corresponding to the previous month of stream.
# For the year 2019, range is 8 to 12.
# For the year 2020, range is 1 to 12 (complete year).
# For the year 2021, range is 1 to 10.
FIRST_MONTH = 1
LAST_MONTH = 10

CALENDAR = {
    "01": "January",
    "02": "February",
    "03": "March",
    "04": "April",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "August",
    "09": "September",
    "10": "October",
    "11": "November",
    "12": "December"
}


def elapsed_time_formatted(begin_time):
    """
    Calculates difference between begin_time and actual time,
    and formats it in HH:MM:SS:ms.
    :param begin_time: time we want to compare with, in seconds.
    """
    return time.strftime(
        "%H:%M:%S", (time.gmtime(time.perf_counter() - begin_time))
    )


def extract_csv(data_file):
    return tablib.Dataset().load(data_file.read(), format='csv', headers=True)


start = time.perf_counter()
results = []
for i in range(FIRST_MONTH, LAST_MONTH + 1):
    month_results = []

    pay_month = str(i)
    if len(pay_month) == 1:
        pay_month = "0" + pay_month

    if i == 1:
        stream_month = "12"
    else:
        stream_month = str(i - 1)
    if len(stream_month) == 1:
        stream_month = "0" + stream_month

    if i == FIRST_MONTH:
        first_month = pay_month

    pay_complete_year = "20" + str(YEAR)

    if stream_month == "01":
        stream_complete_year = "20" + (str(YEAR + 1))
    elif stream_month == "12":
        stream_complete_year = "20" + (str(YEAR - 1))
    else:
        stream_complete_year = "20" + str(YEAR)

    print(f"Processing with {CALENDAR[pay_month]} {pay_complete_year}, please wait...")
    with open(f"all_revenues_{YEAR}_{pay_month}.csv") as file:
        imported_data = extract_csv(file)
        for row in imported_data:
            if int(row[0]) == STREAMER_ID:
                for column in row:
                    month_results.append(column)

        sum_salary = 0
        # Selects and sums payment columns from original CSV file streamer line excluding indexes 0,1 and 11.
        # Index 0 is user_id, index 1 is payout_entity_id, index 11 is report_date.
        for j in range(2, len(month_results)):
            if j != 11:
                sum_salary += int(float(month_results[j])*100)
        print(f"Time elapsed: {elapsed_time_formatted(start)}")
        print(f"Length of datafile: {len(imported_data)} rows")
        imported_data = []
    results.append(sum_salary)

    print(f"Payment of {CALENDAR[pay_month]} {pay_complete_year} "
          f"(stream month: {CALENDAR[stream_month]} {stream_complete_year}): {round(sum_salary / 100, 2)}$")
    print(f"Details: ad_share_gross: {month_results[2]}$, sub_share_gross: {month_results[3]}$, bits_share_gross: {month_results[4]}$, prime_sub_share_gross: {month_results[7]}$, bb_rev_gross: {month_results[10]}$, bits_developer_share_gross: {month_results[5]}$, bits_extension_share_gross: {month_results[6]}$, bit_share_ad_gross: {month_results[8]}$, fuel_rev_gross: {month_results[9]}$")
    print()

total = round(sum(results)/100, 2)
nb_of_months = LAST_MONTH - FIRST_MONTH + 1
average = round(total/nb_of_months, 2)
print(f"Total pay of {CALENDAR[first_month]} to {CALENDAR[pay_month]} {pay_complete_year} ({nb_of_months} months): {total}$")
print(f"Average month pay: {average}$")
print(f"Duration of Analysis: {elapsed_time_formatted(start)}")