from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.PhantomJS()
driver.get('http://www.baidu.com')
data=driver.find_element_by_id("wrapper").text
print(data)
print(driver.title)


# 可变型变量做参数的异常情况
# class Bus:
#
#     def __init__(self, passengers=[]):
#         self.passengers = passengers
#
#     def pick(self, name):
#         self.passengers.append(name)
#
#     def drop(self, name):
#         self.passengers.remove(name)
#
#
# bus1 = Bus(['Alice', 'Bill'])
# print(bus1.passengers)
# bus1.pick('charlie')
# bus1.drop('Alice')
# print(bus1.passengers)
#
# bus2 = Bus()
# bus2.pick('Carrie')
# print(bus2.passengers)
#
# bus3 = Bus()
# print(bus3.passengers)
# bus3.pick('Dave')
# print(bus2.passengers)
# print(bus1.passengers)

