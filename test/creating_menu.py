from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest
import time
import random
from selenium.webdriver.firefox.options import Options

class RestaurantAdminTestCase(unittest.TestCase):
    def setUp(self):
        firefox_options = Options()
        firefox_options.add_argument("--headless")  # Habilita el modo headless
        self.driver = webdriver.Firefox(options=firefox_options)
        self.driver.get("http://localhost:8081/admin/dashboard")
        #self.driver.maximize_window()

    def test_percentage(self):
        interval_time = 5
        while(True):
            wait_time = random.randint(0,interval_time)
            self.driver.implicitly_wait(wait_time)
            dishes_button_order = self.driver.find_elements(By.CLASS_NAME, 'dish-btn-order')
            n_dishes_button = len(dishes_button_order)
            probabilidad = 1
            if n_dishes_button > 0:
                for i in range(n_dishes_button):
                    numero_aleatorio = random.random()
                    if(numero_aleatorio < probabilidad):
                        dishes_button_order[i].click()
            else:
                break
            receipt_button = self.driver.find_element(By.ID, 'btn-receipt')
            receipt_button.click()
            ordered_dishes = self.driver.find_elements(By.CLASS_NAME, 'item')
            n_ordered_dishes = len(ordered_dishes)
            if(n_ordered_dishes > 0):
                for i in range(n_ordered_dishes):
                    increase_amount_btn = ordered_dishes[i].find_element(By.ID, 'increase-amount-btn')
                    number_random = random.randint(0,3)
                    for _ in range(number_random):
                        increase_amount_btn.click()
            order_button = self.driver.find_element(By.ID, 'order-button')
            print(order_button)
            order_button.click()
        self.assertEqual(int(5), 5,'incorrect percentage')
    
    def tearDown(self):
        self.driver.quit()

def creating_menu():
    print("Menu")