import os
import re
import sys
import csv
import time
import traceback
from lxml import html
import keyring
import pyautogui as P
import pyperclip
from datetime import datetime
import yagmail

from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Importing GMB process related modules.
from scripts.gbq.GMB_DataScraper_GBQ import GBQ
from scripts.utils.GMB_DataScraper_InitValues import InitValues
from GMB_DataScraper_NoHistoricalData import NoHistoricalData
from GMB_DataScraper_LanguageChange import SetLanguage
import GMB_DataScraper_UserPass_Encryption
from tkinter import messagebox


# Invoke powershell script, set language as per default.
# powershell_language = SetLanguage.powershell_language_script()

class GMB_DataScraper_Main(InitValues):

    def __init__(self):
        """Inheriting __init__ class from InitValues base class into GMB_DataScraper_Main derived class."""
        super().__init__()
        # Instantiate account_id, location_id, url_address and historical_data parameters in init constructor of derived class.
        self.account_id = ""
        self.location_id = ""
        self.url_address = ""
        self.historical_data = ""

    def main(self):
        """Main method - read .csv file, extract process-relevant data."""
        # Declaring link to url address as a global variable.
        global link_url_address
        print(f"Iter-counter value: {self.iter_counter}")
        csv_file = open(self.GMB_Business_Accounts)
        self.csv_reader = csv.reader(csv_file)
        # Skipping header row with next iterator protocol.
        next(self.csv_reader)
        # Iterate over each data row in project_list_db.csv.
        for self.row in self.csv_reader:
            # Extracting process relevant data from project_list_db.csv file.
            self.account_id = self.row[1]
            self.location_id = self.row[3]
            self.url_address = self.row[6]
            self.historical_data = self.row[7]
            # If condition - check for True/False bool in historical .csv column.
            if self.historical_data:
                # Extract data only for the previous month if False in historical data column.
                historical_data_flag = True
                # global link_url_address
                link_url_address = self.url_address
                return historical_data_flag, self.account_id, self.location_id, link_url_address
            else:
                # Extract data for 5 months back if True in historical data column.
                historical_data_flag = False
                # global link_url_address
                link_url_address = self.url_address
                return historical_data_flag, self.account_id, self.location_id, link_url_address

    def log_in_GMB(self):
        """Accessing Google My Business account with username and password credentials."""
        # Declaring global variables.
        global month_counter, path, driver
        # Chromedriver .exe absolute path location.
        path = os.path.dirname(os.path.abspath(__file__)) + '/chromedriver.exe'
        # Instantiate Google Chromedriver.
        driver = webdriver.Chrome(executable_path=path)
        # Load extracted web link.
        driver.get(link_url_address)
        self.logger.info(f"Accessing link: {link_url_address}")
        time.sleep(2)
        # Maximize active web window.
        driver.maximize_window()
        time.sleep(2)

        if self.iter_counter == 1:
            # Select the username input field.
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input')))
            user_element = driver.find_element(By.CSS_SELECTOR, 'input')
            # Insert username credential.
            credential_username = GMB_DataScraper_UserPass_Encryption.Credentials.cred_invoker()[0]
            user_element.send_keys(credential_username)
            self.logger.info("Entering username credential.")
            # Click on Next button.
            button_element = driver.find_element(By.ID, 'identifierNext')
            button_element.click()
            # Select the password input field.
            WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.NAME, 'password')))
            time.sleep(3)
            password_element = driver.find_element(By.NAME, 'password')
            time.sleep(3)
            self.logger.info("Entering password credential.")
            try:
                # Enter password credentials.
                credential_password = GMB_DataScraper_UserPass_Encryption.Credentials.cred_invoker()[1]
                password_element.send_keys(credential_password)
                time.sleep(1)
                # Click on Next button.
                button_element = driver.find_element(By.ID, 'passwordNext')
                time.sleep(1)
                button_element.click()
                time.sleep(1)
                self.logger.info("Navigating into GMB Data Scraper business account")
            except Exception as ex:
                ex_type, ex_value, ex_traceback = sys.exc_info()
                date = time.strftime('%d-%m-%Y %H:%M:%S')
                trace_back = traceback.extract_tb(ex_traceback)
                stack_trace = []
                for trace in trace_back:
                    stack_trace.append(
                        "File : %s , Line: %s , Func.Name: %s, Message: %s" % (
                            trace[0], trace[1], trace[2], trace[3]))
                    driver.save_screenshot("{0}_Error_{1}.png".format(date, ex_type.__name__))
                    self.logger.info(
                        f"Error! Invalid credentials entered. Error message: {ex}\n Error type: {ex_type.__name__}")
                    try:
                        # Sending email due to error encountered to recipient list.
                        yag = yagmail.SMTP(self.email_sender,
                                           password=keyring.get_password(self.cred_email_username,
                                                                         self.cred_email_username))
                        yag.send(to=self.email_receiver, subject=self.email_subject_error,
                                 contents=self.email_body_fail,
                                 attachments=self.execution_log)
                    except Exception as e:
                        print(f"Error encountered during email dispatch: {e}\n {ex_type.__name__}")
            # Increment counter by 1.
            self.iter_counter += 1
        if self.iter_counter != 1:
            # Click on the 'Покажи още резултати' button
            actions = ActionChains(driver)
            WebDriverWait(driver, 8).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div[2]/div[1]/div/div/div[1]/div[2]/div[2]/div/div/div')))
            # Navigate to search query and volume module window.
            button_keywords = driver.find_element(By.XPATH,
                                                       '//*[@id="yDmH0d"]/c-wiz/div[2]/div[1]/div/div/div[1]/div[2]/div[2]/div/div/div')
            WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.CLASS_NAME, 'VfPpkd-vQzf8d')))
            button_keywords.click()
            time.sleep(3)

            # Navigate into web browser of shop, dynamically extract html content. (TO BE PARAMETERIZED)
            # Navigation logic.
            list_of_period_of_time_element = ""
            """Logic breaks here -- figure out what is wrong with button navigation."""
            try:
                button_class_value = "RmDiQe"
                P.press('F12', presses=1)
                time.sleep(3)
                P.click(button='left', x=1617, y=707, clicks=1)
                time.sleep(4)
                P.hotkey('ctrl', 'f')
                time.sleep(4)
                pyperclip.copy(button_class_value)
                time.sleep(3)
                P.hotkey('ctrl', 'v')
                time.sleep(3)
                P.press('enter', presses=1)
                time.sleep(2)
                P.click(button='left', x=1623, y=653, clicks=1)
                time.sleep(2)
                P.hotkey('ctrl', 'c')
                extracted_web_data = str(pyperclip.paste())
                split_data = extracted_web_data.split('"')
                time.sleep(2)
                P.press('F12', presses=1)
                time.sleep(2)
            except Exception as exc:
                # Extracting entire div class data from web page.
                button_class_value = "RmDiQe"
                P.hotkey('ctrl', 'f5')
                time.sleep(3)
                actions = ActionChains(driver)
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div[2]/div[1]/div/div/div[1]/div[2]/div[2]/div/div/div')))
                # Navigate to search query and volume module window.
                button_keywords = driver.find_element(By.XPATH,
                                                           '//*[@id="yDmH0d"]/c-wiz/div[2]/div[1]/div/div/div[1]/div[2]/div[2]/div/div/div')
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'VfPpkd-vQzf8d')))
                button_keywords.click()
                time.sleep(3)
                P.click(button='left', x=1617, y=707, clicks=1)
                time.sleep(4)
                P.hotkey('ctrl', 'f')
                time.sleep(4)
                pyperclip.copy(button_class_value)
                time.sleep(3)
                P.hotkey('ctrl', 'v')
                time.sleep(3)
                P.press('enter', presses=1)
                time.sleep(2)
                P.click(button='left', x=1623, y=653, clicks=1)
                time.sleep(2)
                P.hotkey('ctrl', 'c')
                extracted_web_data = str(pyperclip.paste())
                split_data = extracted_web_data.split('"')
                time.sleep(2)
                P.press('F12', presses=1)
                time.sleep(2)

            # Extracting calendar string text range from web interface.
            convertedHtmlText = html.fromstring(extracted_web_data)
            list_web_months = convertedHtmlText.xpath('//div[@class="EAXFTd"]/text()')
            # Reversing logic for month looping.
            list_web_months.reverse()
            # Extract active months for iteration.
            active_period = convertedHtmlText.xpath('//span[@class="vrR7q"]/text()')
            start_month = active_period[0].split(' – ')
            month_counter = list_web_months.index(start_month[0])
            return month_counter

    def execute_historical_data(self):
        """Execute method for extracting search queries for previous month of current one."""
        # Declaring global variables.
        global scroll_down, date_prev_month, index_exceeded_flag
        index_exceeded_flag = False
        scroll_down = - 20000
        # Iterate with a loop within the range of the month counter value.
        # for i in range(0, month_counter):
        # Reinitialize while counter.
        self.while_counter = 0
        print(f"Month counter == total API counter: {month_counter}")
        print(f"While counter: {self.while_counter}")
        # print(f"Inner counter: {self.inner_counter}")
        # Navigate back one month from current month.
        time.sleep(2)
        P.click(button='left', x=1080, y=280, clicks=1)
        time.sleep(2)
        date_prev_month = (datetime.today() + relativedelta(months=-(6 - month_counter))).strftime("%Y-%m-%d")
        P.press('tab', presses=month_counter, _pause=True)
        time.sleep(2)
        P.press('space', presses=1)
        time.sleep(2)
        P.press('space', presses=1)
        time.sleep(2)
        P.click(button='left', x=1058, y=546, clicks=1)
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
        # Condition when data for month is not present - look for Разбивка на търсенията.
        if search_query_value_indicator not in list_extracted_web_elements:
            return
            # continue

        # Check for 'Ефективност' web element.
        if self.while_counter == 0:
            # print(f"While counter == {while_counter}")
            WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.TAG_NAME, 'header')))
            time.sleep(3)
            # Make modular window active.
            P.click(button='left', x=950, y=688, clicks=1)
            time.sleep(2)
            # Click on show more results button after scroll down.
            P.click(button='left', x=1228, y=880, clicks=1)
            time.sleep(2)
            # Scroll down.
            P.scroll(scroll_down)
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

            self.split_on_pipe_list = [l.split('|') for l in '|'.join(list_trim_carriage_return).split('|')]
            # Remove 'Разширения на търсенията'.
            self.split_on_pipe_list.pop(0)
            self.split_on_pipe_list.pop(0)
            # Extract index only dynamically at each iteration.
            index = self.split_on_pipe_list[0::3]
            # Instantiate list for storing index values.
            list_ext_web_index = []
            list_ext_web_index.clear()
            # Append each index to the empty list.
            list_ext_web_index.append(index[-2])
            # TEST WITH LIST WEB INDEX OUT OF THE LIST -- SEE WHERE IT CLICKS
            list_ext_web_index[-1] = 120
            print(f"List of extension web index value for test: {list_ext_web_index}")
            if list_ext_web_index[-1] not in self.list_arr_page_indexes:
                # GBQ.gbq_api_call(split_on_pipe_list=self.split_on_pipe_list, account_id=GMB_DataScraper_Main().main()[2],
                #                              location_id=GMB_DataScraper_Main().main()[3], date_prev_month=self.date_prev_month)
                list_ext_flag = True
                # self.inner_counter += 1
                print(f"List ext flag: {list_ext_flag}")
                # print(f"Inner counter: {self.inner_counter}")
                return list_ext_flag
                # continue

            self.while_counter = 1
            # Click on Show more result queries button.
            messagebox.showinfo("Indicate Show more results button!")
            print(P.position())
            messagebox.showinfo("Indicate Show more results button!")
            P.click(button='left', x=635, y=891, clicks=1)
            time.sleep(3)
            # print(f"While counter value: {while_counter}")
        if self.while_counter != 0:
            # Instantiate inner while loop counter.
            counter = 0
            # Execute at least 15 iterations of click, extract and copy to clipboard search query data.
            while counter <= 7:
                # Click on Show more results button from web interface.
                P.scroll(scroll_down)
                time.sleep(2)
                # P.click(button='left', x=635, y=891, clicks=1)
                if counter == 1:
                    # Show more results button click.
                    messagebox.showinfo("Indicate Show more results button!")
                    print(P.position())
                    messagebox.showinfo("Indicate Show more results button!")
                    P.click(button='left', x=780, y=261, clicks=1)
                    time.sleep(2)
                # Scroll down the web page.
                P.scroll(scroll_down)
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

                self.split_on_pipe_list = [l.split('|') for l in '|'.join(list_trim_carriage_return).split('|')]
                # Remove 'Разширения на търсенията'.
                self.split_on_pipe_list.pop(0)
                self.split_on_pipe_list.pop(0)
                # Extract index only dynamically at each iteration.
                index = self.split_on_pipe_list[0::3]
                time.sleep(1)
                # Instantiate list for storing index values.
                list_ext_web_index = []
                list_ext_web_index.clear()
                # Append each index to the empty list.
                list_ext_web_index.append(index[-2])
                # Check if web index exists in np array of indices, break if statement NOT true.
                if list_ext_web_index[-1] in self.list_arr_page_indexes:
                    # Scroll down.
                    P.scroll(scroll_down)
                    time.sleep(2)
                    # Click on Show more results button.
                    P.click(button='left', x=780, y=261, clicks=1)
                    time.sleep(2)
                    # Scroll down.
                    P.scroll(scroll_down)
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

                    self.split_on_pipe_list = [l.split('|') for l in
                                               '|'.join(list_trim_carriage_return).split('|')]
                    # Remove 'Разширения на търсенията'.
                    self.split_on_pipe_list.pop(0)
                    self.split_on_pipe_list.pop(0)
                    # Extract index only dynamically at each iteration.
                    index = self.split_on_pipe_list[0::3]
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
                            # GBQ.gbq_api_call()
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
        # self.inner_counter += 1

        # Uploading e data on Google Big Query.
        GBQ.gbq_api_call(split_on_pipe_list=self.split_on_pipe_list, account_id=GMB_DataScraper_Main().main()[2],
                         location_id=GMB_DataScraper_Main().main()[3], date_prev_month=self.date_prev_month)
        time.sleep(2)
        # Sending results email to business user/dev team _ TO BE CONFIGURED.
        # SendEmailToBU.sending_email_to_BU()
        # Select the return to calendar page button.
        # time.sleep(2)
        messagebox.showinfo("Capture correct position!")
        print(P.position())
        messagebox.showinfo("Capture correct position!")
        P.click(button='left', x=320, y=205, clicks=1)
        time.sleep(3)
        messagebox.showinfo("Capture correct position 2!")
        print(P.position())
        messagebox.showinfo("Capture correct position 2!")
        P.click(button='left', x=757, y=286, clicks=1)

        # Closing web browser after successful search query extraction.
        driver.quit()
        # Instantiate self.inner_counter value for Calendar estimation logic.
        # self.inner_counter = 1
        # index_exceeded_flag = False

    def execute_non_historical_data(self):
        """Execute logic to extract search queries 5 months back."""
        for i in range(0, month_counter):
            # Reinitialize while counter.
            while_counter = 0
            print(f"Month counter == total API counter: {month_counter}")
            print(f"While counter: {while_counter}")
            print(f"Inner counter: {self.inner_counter}")
            messagebox.showinfo("Execute NON-historical data logic!")
            # Navigation logic in Calendar.
            if self.inner_counter == 1:
                time.sleep(2)
                P.click(button='left', x=757, y=286, clicks=1)
                time.sleep(2)
                self.date_prev_month = (datetime.today() + relativedelta(months=-(6 - self.inner_counter))).strftime(
                    "%Y-%m-%d")
                P.press('tab', presses=self.inner_counter, _pause=True)
                # P.press('tab', presses=num_dict_values - 1, _pause=True)
                P.press('space', presses=1)
                time.sleep(3)
                P.press('space', presses=1)
                P.click(button='left', x=733, y=481, clicks=1)
            elif self.inner_counter == 2:
                self.date_prev_month = (datetime.today() + relativedelta(months=-(6 - self.inner_counter))).strftime(
                    "%Y-%m-%d")
                P.press('tab', presses=self.inner_counter, _pause=True)
                # P.press('tab', presses=num_dict_values - 2, _pause=True)
                P.press('space', presses=1)
                time.sleep(3)
                P.press('space', presses=1)
                P.click(button='left', x=733, y=481, clicks=1)
            elif self.inner_counter == 3:
                self.date_prev_month = (datetime.today() + relativedelta(months=-(6 - self.inner_counter))).strftime(
                    "%Y-%m-%d")
                P.press('tab', presses=self.inner_counter, _pause=True)
                # P.press('tab', presses=num_dict_values - 3, _pause=True)
                P.press('space', presses=1)
                time.sleep(3)
                P.press('space', presses=1)
                P.click(button='left', x=733, y=481, clicks=1)
            elif self.inner_counter == 4:
                self.date_prev_month = (datetime.today() + relativedelta(months=-(6 - self.inner_counter))).strftime(
                    "%Y-%m-%d")
                P.press('tab', presses=self.inner_counter, _pause=True)
                # P.press('tab', presses=num_dict_values - 4, _pause=True)
                P.press('space', presses=1)
                time.sleep(3)
                P.press('space', presses=1)
                P.click(button='left', x=733, y=481, clicks=1)
            elif self.inner_counter == 5:
                self.date_prev_month = (datetime.today() + relativedelta(months=-(6 - self.inner_counter))).strftime(
                    "%Y-%m-%d")
                P.press('tab', presses=self.inner_counter, _pause=True)
                # P.press('tab', presses=num_dict_values - 5, _pause=True)
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
                self.inner_counter -= 1
                continue

            # Check for 'Ефективност' web element.
            if while_counter == 0:
                # print(f"While counter == {while_counter}")
                WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.TAG_NAME, 'header')))
                time.sleep(3)
                # Make modular window active.
                P.click(button='left', x=356, y=818, clicks=1)
                time.sleep(2)
                # Scroll down.
                P.scroll(scroll_down)
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

                self.split_on_pipe_list = [l.split('|') for l in '|'.join(list_trim_carriage_return).split('|')]
                # Remove 'Разширения на търсенията'.
                self.split_on_pipe_list.pop(0)
                self.split_on_pipe_list.pop(0)
                # Extract index only dynamically at each iteration.
                index = self.split_on_pipe_list[0::3]
                # Instantiate list for storing index values.
                list_ext_web_index = []
                list_ext_web_index.clear()
                # Append each index to the empty list.
                list_ext_web_index.append(index[-2])
                if list_ext_web_index[-1] not in self.list_arr_page_indexes:
                    self.inner_counter += 1
                    GBQ.gbq_api_call(split_on_pipe_list=self.split_on_pipe_list,
                                     account_id=GMB_DataScraper_Main().main()[2],
                                     location_id=GMB_DataScraper_Main().main()[3], date_prev_month=self.date_prev_month)
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
                    P.scroll(scroll_down)
                    time.sleep(2)
                    # P.click(button='left', x=635, y=891, clicks=1)
                    if counter == 1:
                        P.click(button='left', x=780, y=261, clicks=1)
                        time.sleep(2)
                    # Scroll down the web page.
                    P.scroll(scroll_down)
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

                    self.split_on_pipe_list = [l.split('|') for l in '|'.join(list_trim_carriage_return).split('|')]
                    # Remove 'Разширения на търсенията'.
                    self.split_on_pipe_list.pop(0)
                    self.split_on_pipe_list.pop(0)
                    # Extract index only dynamically at each iteration.
                    index = self.split_on_pipe_list[0::3]
                    time.sleep(1)
                    # Instantiate list for storing index values.
                    list_ext_web_index = []
                    list_ext_web_index.clear()
                    # Append each index to the empty list.
                    list_ext_web_index.append(index[-2])
                    # Check if web index exists in np array of indices, break if statement NOT true.
                    if list_ext_web_index[-1] in self.list_arr_page_indexes:
                        # Scroll down.
                        P.scroll(scroll_down)
                        time.sleep(2)
                        # Click on Show more results button.
                        P.click(button='left', x=780, y=261, clicks=1)
                        time.sleep(2)
                        # Scroll down.
                        P.scroll(scroll_down)
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

                        self.split_on_pipe_list = [l.split('|') for l in '|'.join(list_trim_carriage_return).split('|')]
                        # Remove 'Разширения на търсенията'.
                        self.split_on_pipe_list.pop(0)
                        self.split_on_pipe_list.pop(0)
                        # Extract index only dynamically at each iteration.
                        index = self.split_on_pipe_list[0::3]
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
                                GBQ.gbq_api_call(split_on_pipe_list=self.split_on_pipe_list,
                                                 account_id=GMB_DataScraper_Main().main()[2],
                                                 location_id=GMB_DataScraper_Main().main()[3],
                                                 date_prev_month=self.date_prev_month)
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
            self.inner_counter += 1

            # Uploading e data on Google Big Query.
            GBQ.gbq_api_call(split_on_pipe_list=self.split_on_pipe_list, account_id=GMB_DataScraper_Main().main()[2],
                             location_id=GMB_DataScraper_Main().main()[3], date_prev_month=self.date_prev_month)
            time.sleep(2)
            # Sending results email to business user/dev team _ TO BE CONFIGURED.
            # SendEmailToBU.sending_email_to_BU()
            # Select the return to calendar page button.
            # time.sleep(2)
            P.click(button='left', x=320, y=205, clicks=1)
            time.sleep(3)
            P.click(button='left', x=757, y=286, clicks=1)


if __name__ == "__main__":
    # Instantiate variables for main logic.
    iter_counter = 1
    GMB_Business_Accounts = "project_list_db.csv"
    # Initiate process execution start time.
    start_time = InitValues().start_time
    # Add logger class to indicate start execution time.
    print(f"Start execution: {start_time}")
    obj = GMB_DataScraper_Main().main()[0]
    print(f"Iter-counter value: {iter_counter}")
    csv_file = open(GMB_Business_Accounts)
    csv_reader = csv.reader(csv_file)
    # Skipping header row with next iterator protocol.
    next(csv_reader)
    counter_test = 0
    while_counter = 0
    # Loop over each store inside project_list_db.csv file.
    for item in csv_reader:
        # Extracting the account_id, location_id, url_address and historical_data indicators from .csv file.
        account_id = item[1]
        location_id = item[3]
        url_address = item[6]
        historical_data = item[7]
        print(f"Historical data value: {historical_data}")
        # If condition -- execute for historical data.
        if historical_data:
            messagebox.showinfo("Historical data Iteration!")
            # Log in into Google My business.
            GMB_DataScraper_Main().log_in_GMB()
            # Execute logic with historical data.
            GMB_DataScraper_Main().execute_historical_data()
            ### See how I can fix the while counter value to be relayed properly.
            if GMB_DataScraper_Main().execute_historical_data():
                time.sleep(2)
                P.click(button='left', x=1086, y=532, clicks=1)
                time.sleep(2)
                P.click(button='left', x=636, y=208, clicks=1)
                time.sleep(2)
                P.click(button='left', x=1080, y=280, clicks=1)
                time.sleep(2)
                # continue
            while_counter += 1
        # Else -- execute for no historical data.
        else:
            messagebox.showinfo("No historical data Iteration!")
            # Log in into Google My business.
            GMB_DataScraper_Main().log_in_GMB()
            # Execute logic with no historical data.
            GMB_DataScraper_Main().execute_non_historical_data()
            while_counter += 1

        # Increment counter_test value.
        counter_test += 1
        print(f"Counter test value: {counter_test}")
        messagebox.showinfo("Counter test value!")
    # account = GMB_DataScraper_Main().project_list_db_csv_read()[0]
    # location = GMB_DataScraper_Main().project_list_db_csv_read()[1]
    # print(account)
    # print(location)
    # End process execution time estimation.
    end_time = datetime.now()
    elapsed_time = datetime.now() - relativedelta(end_time)
    # Estimate process execution time.
    process_exec_time = elapsed_time.strftime("%H:%M:%S.%f")
    print(f"Execution time: {process_exec_time}")
