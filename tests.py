import unittest
import platform
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from random import randint

base_url_client = 'http://localhost:3000'
base_url_server = 'http://localhost:5000'

example_username = 'YAHYA'
example_userpass = '1234'

example_not_username = 'NOTAUSER'
example_not_userpass = 'NOTAPASSWORD'

admin_username = 'superAdmin'
admin_password = 'superAdmin'


class Test(unittest.TestCase):
    if platform.system() == 'Darwin':
        browser = webdriver.Chrome('./chromedrivers/chromedriver_darwin')
    elif platform.system() == 'Windows':
        browser = webdriver.Chrome('./chromedrivers/chromedriver_windows.exe')
    elif platform.system() == 'Linux':
        browser = webdriver.Chrome('./chromedrivers/chromedriver_linux')
    else:
        raise ValueError('Different platform.')

    def check_text(self, elem_xpath, text, err_msg):
        sleep(2)
        try:
            elem = self.browser.find_element_by_xpath(elem_xpath)
        except NoSuchElementException as e:
            elem = None
        if elem:
            self.assertEqual(elem.text, text, err_msg)
        else:
            assert False, err_msg

    def log_out(self):
        try:
            logout_menu_btn = self.browser.find_element_by_xpath('//*[@id="root"]/nav/ul/li/div/button')
        except NoSuchElementException as e:
            logout_menu_btn = None

        if logout_menu_btn:
            logout_menu_btn.click()
            sleep(0.2)
            logout_btn = self.browser.find_element_by_xpath('//*[@id="root"]/nav/ul/li/div/div/button')
            logout_btn.click()
            
    def test_is_server_running(self):
        self.log_out()
        sleep(0.3)
        self.browser.get(base_url_client)
        title = '/html/body/div/div/form/div[1]/h1'
        sleep(0.3)
        self.check_text(title, 'Branch Tracker', 'Website is not responding')

    def test_user_can_login(self, username=None, password=None):
        self.log_out()
        sleep(0.3)
        self.browser.get(base_url_client)
        submit_btn_xpath = '//*[@id="root"]/div/form/button'
        username_form_xpath = '//*[@id="root"]/div/form/div[2]/input'
        password_form_xpath = '//*[@id="root"]/div/form/div[3]/input'
        username = username if username else example_username
        password = password if password else example_userpass
        username_form = self.browser.find_element_by_xpath(username_form_xpath).send_keys(username)
        password_form = self.browser.find_element_by_xpath(password_form_xpath).send_keys(password)
        submit_btn = self.browser.find_element_by_xpath(submit_btn_xpath).click()
        sleep(0.2)
        assert self.browser.current_url ==  f'{base_url_client}/userPanel', 'User Couldnt Logged In'

    def test_not_user_cant_login(self):
        self.log_out()
        self.browser.get(base_url_client)
        submit_btn_xpath = '//*[@id="root"]/div/form/button'
        username_form_xpath = '//*[@id="root"]/div/form/div[2]/input'
        password_form_xpath = '//*[@id="root"]/div/form/div[3]/input'

        username_form = self.browser.find_element_by_xpath(username_form_xpath).send_keys(example_not_username)
        password_form = self.browser.find_element_by_xpath(password_form_xpath).send_keys(example_not_userpass)
        submit_btn = self.browser.find_element_by_xpath(submit_btn_xpath).click()

        sleep(0.5)
        invalid_user_msg_xpath = '//*[@id="root"]/div/form/div[1]/div'

        assert self.browser.current_url == f'{base_url_client}/', 'Unvalid User Can Logged In'
        
    def log_out(self):
        try:
            logout_menu_btn = self.browser.find_element_by_xpath('//*[@id="root"]/nav/ul/li/div/button')
        except NoSuchElementException as e:
            logout_menu_btn = None

        if logout_menu_btn:
            logout_menu_btn.click()
            sleep(0.2)
            logout_btn = self.browser.find_element_by_xpath('//*[@id="root"]/nav/ul/li/div/div/button')
            logout_btn.click()


    def test_admin_can_see_daily_reports(self):
        self.log_out()
        sleep(2)
        self.browser.get(base_url_client)
        submit_btn_xpath = '//*[@id="root"]/div/form/button'
        username_form_xpath = '//*[@id="root"]/div/form/div[2]/input'
        password_form_xpath = '//*[@id="root"]/div/form/div[3]/input'
        sleep(0.4)
        username_form = self.browser.find_element_by_xpath(username_form_xpath).send_keys(admin_username)
        sleep(0.1)
        password_form = self.browser.find_element_by_xpath(password_form_xpath).send_keys(admin_password)
        sleep(0.1)
        submit_btn = self.browser.find_element_by_xpath(submit_btn_xpath).click()
        sleep(0.3)
        page_head_xpath = '/html/body/div/div/div/main/div/h1'
        self.check_text(page_head_xpath, 'Günlük Rapor', 'Admin Couldn\'t Logged in Panel')


    def test_check_invalid_credential_message(self):
        self.log_out()
        sleep(0.3)
        self.browser.get(base_url_client)
        submit_btn_xpath = '//*[@id="root"]/div/form/button'
        username_form_xpath = '//*[@id="root"]/div/form/div[2]/input'
        password_form_xpath = '//*[@id="root"]/div/form/div[3]/input'

        username_form = self.browser.find_element_by_xpath(username_form_xpath).send_keys(example_not_username)
        sleep(0.1)
        password_form = self.browser.find_element_by_xpath(password_form_xpath).send_keys(example_not_userpass)
        sleep(0.1)
        submit_btn = self.browser.find_element_by_xpath(submit_btn_xpath).click()

        sleep(0.5)
        invalid_user_msg_xpath = '//*[@id="root"]/div/form/div[1]/div'
        self.check_text(invalid_user_msg_xpath, 'username or password incorrect', 'Invalid Message Dont Showed Up')

    def test_admin_can_create_user(self):
        self.test_admin_can_see_daily_reports()
        sleep(0.3)
        url = f'{base_url_client}/controlPanel/users'
        self.browser.get(url)
        sleep(0.2)
        name_surname = '/html/body/div/div/div/main/form/div[1]/input'
        region_name = '/html/body/div/div/div/main/form/div[2]/input'
        username = '/html/body/div/div/div/main/form/div[3]/input'
        password = '/html/body/div/div/div/main/form/div[4]/input'
        submit = '//*[@id="root"]/div/div/main/form/button'
        username = f'johndoe{randint(0, 1000)}' 
        self.browser.find_element_by_xpath(name_surname).send_keys('John Doe')
        self.browser.find_element_by_xpath(region_name).send_keys('Sample Region')
        self.browser.find_element_by_xpath(username).send_keys(username)
        self.browser.find_element_by_xpath(password).send_keys('superPassword')
        sleep(0.2)
        self.browser.find_element_by_xpath(submit).click()
        sleep(0.2)
        table = '/html/body/div/div/div/main/table/tbody'
        user_info = 'John Doe Sample Region johndoe3 superPassword'
        assert user_info in self.browser.find_element_by_xpath(table).text, 'User Not Created'

    def test_admin_can_add_new_branch(self):
        self.test_admin_can_see_daily_reports()
        sleep(0.3)
        url = f'{base_url_client}/controlPanel/users'
        self.browser.get(url)
        sleep(0.2)
        branch_code_xpath = '/html/body/div/div/div/main/table/tbody/tr[1]/td[5]/table/tbody/tr[1]/td/form/div/input[1]'
        branch_name_xpath = '/html/body/div/div/div/main/table/tbody/tr[1]/td[5]/table/tbody/tr[1]/td/form/div/input[2]'
        branch_submit = '/html/body/div/div/div/main/table/tbody/tr[1]/td[5]/table/tbody/tr[1]/td/form/div/div/button'
        
        branch_code = randint(0, 10000)
        branch_name = 'Sample Branch'
        self.browser.find_element_by_xpath(branch_code_xpath).send_keys(branch_code)
        self.browser.find_element_by_xpath(branch_name_xpath).send_keys(branch_name)
        self.browser.find_element_by_xpath(branch_submit).click()
        sleep(0.2)
        table = '/html/body/div/div/div/main/table/tbody'
        branch_info = f'{branch_code} {branch_name}'
        assert branch_info in self.browser.find_element_by_xpath(table).text, 'Branch Not Created'

    def test_user_can_see_their_branches(self):
        self.log_out()
        sleep(0.3)
        username = 'NAİM'
        password = '1234'
        self.test_user_can_login(username, password)
        self.browser.get(f'{base_url_client}/userPanel')
        sleep(1)
        table = '//*[@id="root"]/div/div/main/form/table/tbody'
        table_data = self.browser.find_element_by_xpath(table).text
        braches = table_data.split('\n')[:-1]

        users_braches = ['DENİZLİ', 'UŞAK', 'İZMİR SEVGİYOLU']
        assert set(users_braches) == set(braches), "User can see other branches or cant see theirs"
        
    def test_user_can_enter_earning(self):
        self.log_out()
        sleep(0.3)
        username = 'NAİM'
        password = '1234'
        self.test_user_can_login(username, password)
        self.browser.get(f'{base_url_client}/userPanel')
        sleep(1)
        success_msg = '/html/body/div/div/div/main/div[2]'

        table = '//*[@id="root"]/div/div/main/form/table/tbody'
        table_data = self.browser.find_element_by_xpath(table).text
        braches = table_data.split('\n')[:-1]
        num_of_braches = len(braches)
        for num in range(1, num_of_braches+1):
            branch_earning = f'/html/body/div/div/div/main/form/table/tbody/tr[{num}]/td[2]/input'
            self.browser.find_element_by_xpath(branch_earning).send_keys('10')
        sleep(0.2)
        submit = '/html/body/div/div/div/main/form/table/tbody/tr[4]/td/button'
        self.browser.find_element_by_xpath(submit).click()
        sleep(0.1)
        try:
            elem = self.browser.find_element_by_xpath(success_msg)
            elem_exist = True
        except NoSuchElementException as e:
            elem_exist = False
        sleep(0.2)
        if elem_exist:
            assert elem.text == 'Başarı ile kayıt edildi', 'User Can Enter Earning'

    def test_user_cant_enter_negative_earning(self):
        self.log_out()
        sleep(0.3)
        username = 'NAİM'
        password = '1234'
        self.test_user_can_login(username, password)
        self.browser.get(f'{base_url_client}/userPanel')
        sleep(1)
        success_msg = '/html/body/div/div/div/main/div[2]'
        branch_earning = '/html/body/div/div/div/main/form/table/tbody/tr[1]/td[2]/input'
        submit = '/html/body/div/div/div/main/form/table/tbody/tr[9]/td/button'
        self.browser.find_element_by_xpath(branch_earning).send_keys('-1')
        self.browser.find_element_by_xpath(submit).click()
        sleep(0.1)
        try:
            elem = self.browser.find_element_by_xpath(success_msg)
            elem_exist = True
        except NoSuchElementException as e:
            elem_exist = False
        sleep(0.2)
        if elem_exist:
            assert elem.text != 'Başarı ile kayıt edildi', 'User Can Enter Negative Value'


if __name__ == "__main__":
	unittest.main()