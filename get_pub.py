
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import logging
# import statistics
import re


# url = 'https://www.tripadvisor.ie/Restaurant_Review-g186338-d6635485-Reviews-The_Clink_Restaurant-London_England.html'

url = 'https://www.tripadvisor.ie/Restaurants-g186338-London_England.html'
driver = webdriver.Chrome()
driver.get(url)

name = []
address = []
email = []
phone = []
website = []


def get_website(url):

    driver = url
    html_source = driver.page_source
    try:
        website = re.findall(r'website":"(.*?)","email', html_source)
        website = website
    except:
        website = 'ERROR'

    print(website)

    return website


def get_phone(url):

    driver = url

    try:
        phone = driver.find_element_by_xpath(
            '//span[@class="detail  is-hidden-mobile"]')
        phone = phone.text
    except:
        phone = 'ERROR'

    print(phone)
    return phone


def get_address(url):

    driver = url
    try:
        street = driver.find_element_by_xpath(
            '//span[@class="street-address"]')
        street = street.text
        locality = driver.find_element_by_xpath('//span[@class="locality"]')
        locality = locality.text

    except:
        street = 'ERROR'
        locality = 'ERROR'

    print(street)
    print(locality)

    address = street + ', ' + locality

    return address


def get_email(url):

    driver = url
    html_source = driver.page_source
    # email = re.findall(r'\w+@\w+', html_source)
    try:
        email = re.findall(r'mailto:([^"]*@.[^"]*)', html_source)
        email = email
    except:
        email = 'ERROR'

    print(email)

    return email


def save(name, address, email, phone, website):

    print(name, address, email, phone)

    # df = pd.DataFrame(
    #     {'Name': name,
    #      'Address': address,
    #      'Email': email,
    #      'Phone': phone,
    #      'Website': website


    #      })
    # writer = pd.ExcelWriter('restaurants_london.xlsx', engine='xlsxwriter')

    # # Convert the dataframe to an XlsxWriter Excel object.
    # df.to_excel(writer, sheet_name='Sheet1')

    # # Close the Pandas Excel writer and output the Excel file.
    # writer.save()


def get_info(driver):
    print('get_info')
    time.sleep(4)
    restaurants = ui.WebDriverWait(driver, 15).until(
        lambda driver: driver.find_elements_by_xpath('//a[@class="property_title"]'))

    print(restaurants)

    for res in restaurants:
        try:
            name.append(res.text)
            print(res.text)
            res.click()
            driver.switch_to.window(driver.window_handles[1])
            print('\n')
            try:
                address.append(get_address(driver))
                email.append(get_email(driver))
                phone.append(get_phone(driver))
                website.append(get_website(driver))
                driver.close()
            except:
                print('ERROR')

            driver.switch_to.window(driver.window_handles[0])
        except:
            save(name, address, email, phone, website)

    # Next = driver.find_element_by_xpath('//a[@class="nav next rndBtn ui_button primary taLnk"]')
    # Next.click()
    previous = driver.find_element_by_xpath(
        '//a[@class="nav previous rndBtn ui_button primary taLnk"]')
    previous.click()
    print('\n\n****NEXT**** ')
    save(name, address, email, phone, website)


def next(url, contador, decrementador):
    driver = url
    try:
        Next = ui.WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_xpath(
            '//a[@class="nav next rndBtn ui_button primary taLnk"]'))
        time.sleep(1)
        Next.click()
        decrementador = decrementador + 1
    except:
        print('ta na except, meu decrementador e:' + str(decrementador))
        time.sleep(4)
    return decrementador


cont = 0


p640 = driver.find_elements_by_xpath('//a[@class="pageNum taLnk"]')
for x in p640:
    cont += 1
    # print('p640')
    if(cont == 6):
        print(x.text)
        x.click()


contador = 245
decrementador = 0
'''
while decrementador <= contador:
	decrementador = next(driver,contador,decrementador)
	print('contador:' + str(contador) + ', decrementador' + str(decrementador))
'''
while True:
    try:
        print('while')
        get_info(driver)
    except Exception as e:
        logging.exception("message")

        save(name, address, email, phone, website)

'''

    # qty_followup = fields.Text(string = 'Follow up', compute = '_delivery_followup')

    @api.depends('product_uom_qty', 'qty_delivered')
    def _delivery_followup(self):

        qty_followup = self.product_uom_qty - self.qty_delivered

        return qty_followup
'''
