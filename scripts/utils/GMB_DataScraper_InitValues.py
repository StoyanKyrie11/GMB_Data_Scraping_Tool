import logging
import os
import sys
import time
import traceback
import keyring
import pyautogui as P
import pyperclip
import yagmail
import yagmail as yag
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from lxml import html
from ctypes import windll

# Importing GMB process related modules.
from GMB_DataScraper_UserPass_Encryption import Credentials


class InitValues:
    """InitValues class."""

    def __init__(self):
        """Initialize method - instantiate project-specific system attributes."""
        # Assign username and password variable values from Credentials class.
        self.cred_username = Credentials.cred_invoker()[0]
        self.cred_password = Credentials.cred_invoker()[1]
        # Initialize start time - format -(hours:minutes:seconds.microseconds)
        self.start_time = datetime.now().strftime("%H:%M:%S.%f")
        # Instantiate date time value indicating previous month.
        self.date_prev_month = ""
        # Input .csv file name.
        self.GMB_Business_Accounts = "project_list_db.csv"
        # Init GMB_BusinessAccount argument value - empty.
        self.csv_reader = ""
        # Instantiate pyperclip method.
        self.pyperclip = pyperclip
        # Instantiate iter counter value - default 1.
        self.iter_counter = 1
        # Instantiate inner counter for historical and non-historical data logic.
        self.inner_counter = 1
        # Instantiate JS XPATH web element.
        self.button_class_value = "RmDiQe"
        # Instantiate Execution log file name.
        self.execution_log = "Execution.log"
        # Instantiate custom logger object instance.
        self.logger = logging.getLogger(__name__)
        # Instantiate Windows Credential manager username and password parameter values.
        self.cred_email_username = "GMB_EmailUsername"
        self.cred_email_password = "GMB_EmailPassword"
        # Instantiate email sender.
        self.email_sender = "serpactgmb@gmail.com"
        # Instantiate email receiver.
        self.email_receiver = ["ivanovzlatan@gmail.com", "stoyan.ch.stoyanov11@gmail.com"]
        # Instantiate email subject error/success, email body error/success.
        self.email_subject_success = f"GMB_DataScraping - successful execution. {time.strftime('%d-%m-%Y %H:%M:%S')}"
        self.email_subject_error = f"GMB_DataScraping - unsuccessful execution. {time.strftime('%d-%m-%Y %H:%M:%S')}"
        self.email_body_success = "Dear business owner, \n\n the Search queries and Volume data have been successfully extracted " \
                                  "from your store. \n\n Kind regards, \n\n GMB_DataScraping Team"
        self.email_body_fail = "Dear business owner, \n\n the process for extracting Search query and Volume data has encountered \
                            an error. Process was terminated. \n\n Kind regards, \n\n GMB_DataScraping Team"
        # Defining the keyword and number of occurrences of web elements value lists.
        # TO BE DEVELOPED TOMORROW - THINK OUT A WAY TO PASS THE VARIABLES OF THE LISTS INTO HISTORICAL AND NO_HISTORICAL DATA SCRIPTS.
        # self.gl_keywords_list = gl_keywords_list
        # self.gl_times_list = gl_times_list
        # Instantiate emtpy lists to hold extracted web element data.
        # self.list_elements = list_elements
        # self.new_list_elements = new_list_elements
        # Search query, Volume init raw data list.
        # self.dynamic_web_list = dynamic_web_list
        # Instantiate split on pipe data empty list.
        self.split_on_pipe_list = []
        # Numpy array holding page index comparison values.
        self.list_arr_page_indexes = [["100"], ["200"], ["300"], ["400"], ["500"], ["600"], ["700"], ["800"], ["900"],
                                      ["1000"], ["1100"]]

    @staticmethod
    def copy_clipboard():
        """Copy data from web browser into clipboard."""
        # Empty the clipboard.
        windll.user32.EmptyClipboard()
        P.hotkey('ctrl', 'a')
        time.sleep(0.5)
        P.hotkey('ctrl', 'c')
        time.sleep(0.5)
        return pyperclip.paste()

    def execution_log_format_logger(self):
        """Instantiate execution log file name and logger object instance."""
        # Instantiate logger variable value implementing the logging method from the getLogger object instance.
        self.logger = logging.getLogger(__name__)
        # Setting logging level to leg messages from INFO above - INFO, DEBUG, ERROR, FATAL.
        self.logger.setLevel(logging.INFO)
        # Instantiate file handler object instance.
        file_handler = logging.FileHandler(self.execution_log)
        # Instantiate custom file format logger object instance.
        format_logger = logging.Formatter('%(name)s - %(levelname)s - %(message)s : %(asctime)s', datefmt='%d-%m-%Y %H:%M:%S')
        file_handler.setFormatter(format_logger)
        # Assigning custom logging handler using the addHandler() function of the logger external base class.
        self.logger.addHandler(file_handler)
        # return self.execution_log, self.logger

    def chrome_driver_specs(self):
        """Instantiate chromedriver engine for Selenium Webdriver web navigation."""
        # Chromedriver .exe absolute path location.
        path = os.path.dirname(os.path.abspath(__file__)) + '/chromedriver.exe'
        # Chromedriver.exe path. NB: Browser navigation made to headless with options set to True.
        driver = webdriver.Chrome(executable_path=path)
        browser_version = driver.capabilities['browserVersion']
        driver_version = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
        return browser_version, driver_version


    def send_email(self, email_receiver):  # Define a keyword argument - email sender/receiver.
        """Instantiate email variable values - email_receiver(input arg), email_subject_success, email_subject_fail,
        email_body_success, email_body_error"""
        email_subject_success = f"GMB_DataScraping - successful execution. {time.strftime('%d-%m-%Y %H:%M:%S')}"
        email_subject_error = f"GMB_DataScraping - unsuccessful execution. {time.strftime('%d-%m-%Y %H:%M:%S')}"
        email_body_success = "Dear business owner, \n\n the Search queries and Volume data have been successfully extracted " \
                             "from your store. \n\n Kind regards, \n\n GMB_Serpact_Robot"
        email_body_error = "Dear developer, \n\n the process for extracting Search query and Volume data has encountered \
                    an error due to which process has been terminated. \n\n Kind regards, \n\n GMB_Serpact_Robot"
        # execution_log_init = InitValues.execution_log_format_logger(self.path)[0]
        # execution_log = execution_log_init
        # logger_init = InitValues.execution_log_format_logger(self.path)[1]
        # Instantiate the logger object from the execution format logger info method.
        # logger = logger_init
        try:
            # Sending email to developer team.
            mail = yag.SMTP(email_receiver, password=Credentials.cred_invoker()[1])
            mail.send(to=email_receiver, subject=email_subject_success, contents=email_body_success,
                      attachments=self.execution_log)
            self.logger.info(f"Sending email to user:{email_receiver} with log name: {self.execution_log}")
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
                    f"Error encountered during email dispatch. Error value: {ex}\n Error type: {ex_type.__name__}")
                break
            # Sending error email message with the respective error mail subject and body.
            mail = yag.SMTP(email_receiver,
                            password=Credentials.cred_invoker()[1])
            mail.send(to=email_receiver, subject=email_subject_error, contents=email_body_error,
                      attachments=self.execution_log)

