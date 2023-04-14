import re
import time
from tkinter import messagebox
import pyautogui as P

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Importing GMB process related modules.
from scripts.utils.GMB_DataScraper_InitValues import InitValues
from GMB_DataScraper_UserPass_Encryption import Credentials
from scripts.gbq.GMB_DataScraper_GBQ import GBQ
from GMB_DataScraper_DateTimeConversion import dict_prev_months


class NoHistoricalData(InitValues):
    # Create a .csv reader and csv_dict variables, read the GMB Account links from .csv file.
    def __init__(self, *args):
        """Inheriting __init__ class from Init values base class into GMB_DataScraper_NoHistoricalData derived class.
        Logic to go 5 months back and extract the data."""
        # Inherit __init__ from Init values Base class.
        super().__init__(*args)


    def no_historical_data(self):
        # Instantiate inner_counter value for Calendar estimation logic.
        inner_counter = 1
        date_time = ""
        index_exceeded_flag = False
        for i in range(0, InitValues.log_in_GMB_account()):
            # Reinitialize while counter.
            while_counter = 0
            print(f"Month counter == total API counter: {InitValues.log_in_GMB_account()}")
            print(f"While counter: {while_counter}")
            print(f"Inner counter: {inner_counter}")
            # Navigation logic in Calendar.
            if self.inner_counter == 1:
                time.sleep(2)
                P.click(button='left', x=757, y=286, clicks=1)
                time.sleep(2)
                # date_prev_month = (datetime.today() + relativedelta(months=-(6 - inner_counter))).strftime("%Y-%m-%d")
                date_time = (dict_prev_months(inner_counter)[0])
                # TESTING VALUES FROM InitValues __init__ built-in constructor method.
                print(f"Date time: {date_time}")
                print(f"List_arr_page_indices: {self.list_arr_page_indexes}")
                messagebox.showinfo("Testing values!")
                messagebox.showinfo("Date previous month inserted!")
                P.press('tab', presses=inner_counter, _pause=True)
                # P.press('tab', presses=num_dict_values - 1, _pause=True)
                P.press('space', presses=1)
                time.sleep(3)
                P.press('space', presses=1)
                P.click(button='left', x=733, y=481, clicks=1)

            time.sleep(2)
            # Scrolling down the page.
            P.scroll(-2000)
            time.sleep(2)
            # Variable for empty search query.
            search_query_value_indicator = ["Разбивка на търсенията"]
            # Call clipboard select all and copy method.
            extension = InitValues.copy_clipboard()
            # Instantiate empty web list for web extension elements.
            extension_web_list = []
            extension_web_list.clear()
            extension_web_list.append(extension)
            # List to hold trimmed from carriage returns and newline web elements.
            list_trim_whitespaces = []
            for m in extension_web_list:
                list_trim_whitespaces = [re.sub(r'\r\n', '|', m) for m in extension_web_list]

            list_extracted_web_elements = [l.split('|') for l in '|'.join(list_trim_whitespaces).split('|')]
            # print(f"List of extracted web elements: {list_extracted_web_elements}")

            # Condition when data for month is not present - look for Разбивка на търсенията.
            if search_query_value_indicator not in list_extracted_web_elements:
                time.sleep(2)
                P.scroll(+2000)
                # Select the return to calendar page button.
                P.click(button='left', x=639, y=200, clicks=1)
                time.sleep(2)
                inner_counter -= 1
                continue

            # Check for 'Ефективност' web element.
            if while_counter == 0:
                # print(f"While counter == {while_counter}")
                WebDriverWait(InitValues.chrome_driver, 7).until(EC.presence_of_element_located((By.TAG_NAME, 'header')))
                time.sleep(3)
                # Make modular window active.
                P.click(button='left', x=356, y=818, clicks=1)
                time.sleep(2)
                # Scroll down.
                P.scroll(-20000)
                time.sleep(2)
                # Dynamic list to append web element data from Search query and Volume.
                var = InitValues.copy_clipboard()
                dynamic_web_list = []
                dynamic_web_list.clear()
                dynamic_web_list.append(var)
                # List to hold trimmed from carriage returns and newline web elements.
                list_trim_carriage_return = []
                for el in dynamic_web_list:
                    list_trim_carriage_return = [re.sub(r'\r\n', '|', el) for el in dynamic_web_list]

                split_on_pipe_list = [l.split('|') for l in '|'.join(list_trim_carriage_return).split('|')]
                # Remove 'Разширения на търсенията'.
                split_on_pipe_list.pop(0)
                split_on_pipe_list.pop(0)
                # Extract index only dynamically at each iteration.
                index = split_on_pipe_list[0::3]
                print(index)
                messagebox.showinfo("Pause!")
                # Instantiate list for storing index values.
                list_ext_web_index = []
                list_ext_web_index.clear()
                # Append each index to the empty list.
                list_ext_web_index.append(index[-2])
                if list_ext_web_index[-1] not in self.list_arr_page_indexes:
                    inner_counter += 1
                    # IMPORTANT -- Fill in all the parameters.
                    GBQ.gbq_api_call(split_on_pipe_list=split_on_pipe_list, account_id=self.account_id,
                                     location_id=self.location_id, date_prev_month=date_time)
                    time.sleep(2)
                    P.click(button='left', x=350, y=215, clicks=1)
                    time.sleep(1)
                    P.click(button='left', x=320, y=207, clicks=1)
                    time.sleep(2)
                    P.click(button='left', x=757, y=286, clicks=1)
                    time.sleep(2)
                    continue

                while_counter = 1
                # Click on Show more result queries button.
                P.click(button='left', x=635, y=891, clicks=1)
                time.sleep(3)
                # print(f"While counter value: {while_counter}")
            if while_counter != 0:
                # Instantiate inner while loop counter.
                counter = 0
                # Execute at least 15 iterations of click, extract and copy to clipboard search query data.
                while counter <= 7:
                    # Click on Show more results button from web interface.
                    P.scroll(-20000)
                    time.sleep(2)
                    # P.click(button='left', x=635, y=891, clicks=1)
                    if counter == 1:
                        P.click(button='left', x=780, y=261, clicks=1)
                        time.sleep(2)
                    # Scroll down the web page.
                    P.scroll(-20000)
                    time.sleep(2)
                    # Dynamic list to append web element data from Search query and Volume.
                    var = InitValues.copy_clipboard()
                    dynamic_web_list = []
                    dynamic_web_list.clear()
                    dynamic_web_list.append(var)
                    # List to hold trimmed from carriage returns and newline web elements.
                    list_trim_carriage_return = []
                    for el in dynamic_web_list:
                        list_trim_carriage_return = [re.sub(r'\r\n', '|', el) for el in dynamic_web_list]

                    split_on_pipe_list = [l.split('|') for l in '|'.join(list_trim_carriage_return).split('|')]
                    # Remove 'Разширения на търсенията'.
                    split_on_pipe_list.pop(0)
                    split_on_pipe_list.pop(0)
                    # Extract index only dynamically at each iteration.
                    index = split_on_pipe_list[0::3]
                    time.sleep(1)
                    # Instantiate list for storing index values.
                    list_ext_web_index = []
                    list_ext_web_index.clear()
                    # Append each index to the empty list.
                    list_ext_web_index.append(index[-2])
                    # Check if web index exists in np array of indices, break if statement NOT true.
                    if list_ext_web_index[-1] in self.list_arr_page_indexes:
                        # Scroll down.
                        P.scroll(-20000)
                        time.sleep(2)
                        # Click on Show more results button.
                        P.click(button='left', x=780, y=261, clicks=1)
                        time.sleep(2)
                        # Scroll down.
                        P.scroll(-20000)
                        time.sleep(2)
                        # Dynamic list to append web element data from Search query and Volume.
                        var = InitValues.copy_clipboard()
                        dynamic_web_list = []
                        dynamic_web_list.clear()
                        dynamic_web_list.append(var)
                        # List to hold trimmed from carriage returns and newline web elements.
                        list_trim_carriage_return = []
                        for el in dynamic_web_list:
                            list_trim_carriage_return = [re.sub(r'\r\n', '|', el) for el in dynamic_web_list]

                        split_on_pipe_list = [l.split('|') for l in
                                              '|'.join(list_trim_carriage_return).split('|')]
                        # Remove 'Разширения на търсенията'.
                        split_on_pipe_list.pop(0)
                        split_on_pipe_list.pop(0)
                        # Extract index only dynamically at each iteration.
                        index = split_on_pipe_list[0::3]
                        time.sleep(1)
                        list_ext_web_index = []
                        list_ext_web_index.clear()
                        # Append each index to the empty list.
                        list_ext_web_index.append(index[-2])
                        if list_ext_web_index[-1] in self.list_arr_page_indexes:
                            P.click(button='left', x=635, y=891, clicks=1)
                            time.sleep(2)
                            # print(f"Current iteration: {counter}")
                            counter += 1
                            if counter == 7:
                                index_exceeded_flag = True
                                GBQ.gbq_api_call(split_on_pipe_list=split_on_pipe_list, account_id=self.account_id,
                                                 location_id=self.location_id, date_prev_month=date_time)
                                time.sleep(2)
                                # Sending results email to business user/dev team _ TO BE CONFIGURED.
                                # SendEmailToBU.sending_email_to_BU()
                                # Select the return to calendar page button.
                                # time.sleep(2)
                                P.click(button='left', x=320, y=205, clicks=1)
                                time.sleep(3)
                                P.click(button='left', x=757, y=286, clicks=1)
                                break

                    # Increment inner while counter value.
                    counter += 1
            # Incrementing inner loop counter.
            inner_counter += 1

            # Uploading e data on Google Big Query.
            # GBQ.gbq_api_call()
            time.sleep(2)
            # Sending results email to business user/dev team _ TO BE CONFIGURED.
            # SendEmailToBU.sending_email_to_BU()
            # Select the return to calendar page button.
            # time.sleep(2)
            P.click(button='left', x=320, y=205, clicks=1)
            time.sleep(3)
            P.click(button='left', x=757, y=286, clicks=1)