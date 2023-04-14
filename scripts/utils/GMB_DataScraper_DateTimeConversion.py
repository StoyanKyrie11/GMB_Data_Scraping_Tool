import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
from tkinter import messagebox


def dict_prev_months(counter, date_format="%b %Y"):
    """Method for estimating the previous month in short month yyyy format. Data to be inserted in web navigation."""
    prev_month_one = datetime.today() + relativedelta(months=-counter)
    month_ago = prev_month_one.strftime(date_format)
    counter += 1
    prev_month_two = datetime.today() + relativedelta(months=-counter)
    two_months_ago = prev_month_two.strftime(date_format)
    counter += 1
    prev_month_three = datetime.today() + relativedelta(months=-counter)
    three_months_ago = prev_month_three.strftime(date_format)
    counter += 1
    prev_month_four = datetime.today() + relativedelta(months=-counter)
    four_months_ago = prev_month_four.strftime(date_format)
    counter += 1
    prev_month_five = datetime.today() + relativedelta(months=-counter)
    five_months_ago = prev_month_five.strftime(date_format)
    counter += 1
    prev_month_six = datetime.today() + relativedelta(months=-counter)
    six_months_ago = prev_month_six.strftime(date_format)
    counter += 1

    return month_ago, two_months_ago, three_months_ago, four_months_ago, five_months_ago, six_months_ago


def date_time_for_table(counter, date_format="%Y-%m-%d"):
    """Converting local datetime format to yyyy-MM-dd format for gbq query insertion."""
    previous_month = datetime.today() + relativedelta(months=-counter)
    date_for_gbq = previous_month.strftime(date_format)

    return date_for_gbq


def month_estimation(dict_date_time):
    """Method for locating latin month convention and replacing it with cyrillic equivalent. ex. Jan 2021 with яну 2021"""
    counter = 0
    date_time_month_list = []
    while counter < 10:
        if "Jan" in dict_date_time:
            new_value = dict_date_time.replace(dict_date_time[:3], "яну")
            date_time_month_list.append(new_value)
            break
        if "Feb" in dict_date_time:
            new_value = dict_date_time.replace(dict_date_time[:3], "фев")
            date_time_month_list.append(new_value)
            break
        if "Mar" in dict_date_time:
            new_value = dict_date_time.replace(dict_date_time[:3], "мар")
            date_time_month_list.append(new_value)
            break
        if "Apr" in dict_date_time:
            new_value = dict_date_time.replace(dict_date_time[:3], "апр")
            date_time_month_list.append(new_value)
            break
        if "May" in dict_date_time:
            new_value = dict_date_time.replace(dict_date_time[:3], "май")
            date_time_month_list.append(new_value)
            break
        if "Jun" in dict_date_time:
            new_value = dict_date_time.replace(dict_date_time[:3], "юни")
            date_time_month_list.append(new_value)
            break
        if "Jul" in dict_date_time:
            new_value = dict_date_time.replace(dict_date_time[:3], "юли")
            date_time_month_list.append(new_value)
            break
        if "Aug" in dict_date_time:
            new_value = dict_date_time.replace(dict_date_time[:3], "авг")
            date_time_month_list.append(new_value)
            break
        if "Sep" in dict_date_time:
            new_value = dict_date_time.replace(dict_date_time[:3], "сеп")
            date_time_month_list.append(new_value)
            break
        if "Oct" in dict_date_time:
            new_value = dict_date_time.replace(dict_date_time[:3], "окт")
            date_time_month_list.append(new_value)
            break
        if "Nov" in dict_date_time:
            new_value = dict_date_time.replace(dict_date_time[:3], "нов")
            date_time_month_list.append(new_value)
            break
        if "Dec" in dict_date_time:
            new_value = dict_date_time.replace(dict_date_time[:3], "дек")
            date_time_month_list.append(new_value)
            break
        counter += 1

    return date_time_month_list