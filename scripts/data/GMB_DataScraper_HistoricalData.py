import csv
import datetime
import logging
import os
import re
import sys
import time
import traceback
from collections import OrderedDict
from ctypes import windll
from datetime import datetime
from tkinter import messagebox
import subprocess
import keyring
import numpy as np
import pandas as pd
import pyautogui as P
import pyperclip
import yagmail
from dateutil.relativedelta import relativedelta
from google.cloud import bigquery
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from lxml import html

# Importing GMB process related modules.
import GMB_DataScraper_UserPass_Encryption
from scripts.utils.GMB_DataScraper_InitValues import InitValues
from scripts.main.GMB_DataScraper_Main import GMB_DataScraper_Main


class HistoricalData(GMB_DataScraper_Main):
    def __init__(self):
        """Inheriting __init__ class from InitValues base class into GMB_DataScraper_HistoricalData derived class."""
        # Inherit __init__ from Init values Base class.
        super().__init__()

    def historical_data(self):
        self.driver.get(self.url_address)
        time.sleep(3)
        # Maximize active web window.
        self.driver.maximize_window()
        time.sleep(2)
        messagebox.showinfo("URL address!")

        if self.iter_counter == 1:
            # Select the username input field.
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input')))
            user_element = self.driver.find_element(By.CSS_SELECTOR, 'input')
            # Insert username credential.
            credential_username = GMB_DataScraper_UserPass_Encryption.Credentials.cred_invoker()[0]
            user_element.send_keys(credential_username)
            self.logger.info("Entering username credential.")
            # Click on Next button.
            button_element = self.driver.find_element(By.ID, 'identifierNext')
            button_element.click()
            # Select the password input field.
            WebDriverWait(self.driver, 4).until(EC.presence_of_element_located((By.NAME, 'password')))
            time.sleep(3)
            password_element = self.driver.find_element(By.NAME, 'password')
            time.sleep(3)
            self.logger.info("Entering password credential.")
            try:
                # Enter password credentials.
                credential_password = GMB_DataScraper_UserPass_Encryption.Credentials.cred_invoker()[1]
                password_element.send_keys(credential_password)
                time.sleep(1)
                # Click on Next button.
                button_element = self.driver.find_element(By.ID, 'passwordNext')
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
                    self.driver.save_screenshot("{0}_Error_{1}.png".format(date, ex_type.__name__))
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
            actions = ActionChains(self.driver)
            WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div[2]/div[1]/div/div/div[1]/div[2]/div[2]/div/div/div')))
            # Navigate to search query and volume module window.
            button_keywords = self.driver.find_element(By.XPATH,
                                                       '//*[@id="yDmH0d"]/c-wiz/div[2]/div[1]/div/div/div[1]/div[2]/div[2]/div/div/div')
            WebDriverWait(self.driver, 7).until(EC.presence_of_element_located((By.CLASS_NAME, 'VfPpkd-vQzf8d')))
            button_keywords.click()
            time.sleep(3)

            # Navigate into web browser of shop, dynamically extract html content. (TO BE PARAMETERIZED)
            # Navigation logic.
            list_of_period_of_time_element = ""
            try:
                button_class_value = "RmDiQe"
                P.press('F12', presses=1)
                time.sleep(3)
                P.click(button='left', x=1021, y=648, clicks=1)
                time.sleep(4)
                P.hotkey('ctrl', 'f')
                time.sleep(4)
                pyperclip.copy(button_class_value)
                time.sleep(3)
                P.hotkey('ctrl', 'v')
                time.sleep(3)
                P.press('enter', presses=1)
                time.sleep(2)
                P.click(button='left', x=987, y=591, clicks=1)
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
                actions = ActionChains(self.driver)
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div[2]/div[1]/div/div/div[1]/div[2]/div[2]/div/div/div')))
                # Navigate to search query and volume module window.
                button_keywords = self.driver.find_element(By.XPATH,
                                                           '//*[@id="yDmH0d"]/c-wiz/div[2]/div[1]/div/div/div[1]/div[2]/div[2]/div/div/div')
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'VfPpkd-vQzf8d')))
                button_keywords.click()
                time.sleep(3)
                P.click(button='left', x=1021, y=648, clicks=1)
                time.sleep(4)
                P.hotkey('ctrl', 'f')
                time.sleep(4)
                pyperclip.copy(button_class_value)
                time.sleep(3)
                P.hotkey('ctrl', 'v')
                time.sleep(3)
                P.press('enter', presses=1)
                time.sleep(2)
                P.click(button='left', x=987, y=591, clicks=1)
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

            # Instantiate inner_counter value for Calendar estimation logic.
            inner_counter = 1
            index_exceeded_flag = False
            for i in range(0, month_counter):
                # Reinitialize while counter.
                while_counter = 0
                print(f"Month counter == total API counter: {month_counter}")
                # print(f"While counter: {while_counter}")
                # print(f"Inner counter: {inner_counter}")
                # Navigation logic in Calendar.
                # if inner_counter == 1:
                time.sleep(2)
                P.click(button='left', x=757, y=286, clicks=1)
                time.sleep(2)
                date_prev_month = (datetime.today() + relativedelta(months=-(6 - inner_counter))).strftime(
                    "%Y-%m-%d")
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
                extension = copy_clipboard()
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
                    WebDriverWait(self.driver, 7).until(EC.presence_of_element_located((By.TAG_NAME, 'header')))
                    time.sleep(3)
                    # Make modular window active.
                    P.click(button='left', x=356, y=818, clicks=1)
                    time.sleep(2)
                    # Scroll down.
                    P.scroll(-20000)
                    time.sleep(2)
                    # Dynamic list to append web element data from Search query and Volume.
                    messagebox.showinfo("Pause before copy clipboard!")
                    var = copy_clipboard()
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
                    # Instantiate list for storing index values.
                    list_ext_web_index = []
                    list_ext_web_index.clear()
                    # Append each index to the empty list.
                    list_ext_web_index.append(index[-2])
                    if list_ext_web_index[-1] not in self.list_arr_page_indexes:
                        inner_counter += 1
                        # GBQ.gbq_api_call()
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
                        var = copy_clipboard()
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
                            var = copy_clipboard()
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

                # Closing web browser after successful search query extraction.
            self.driver.quit()