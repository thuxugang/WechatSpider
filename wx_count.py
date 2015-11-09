# -*- coding: utf-8 -*-
"""
Created on Fri Oct 09 17:16:56 2015

@author: XuGang
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os


global browser


SLEEP_TIME = 1

def toTongXunLu():
    
    group = browser.find_element_by_xpath("//div[@class='tab_item no_extra']/a[@class='chat']")
    ActionChains(browser).double_click(group).perform()
    
def getIndivGroup(webElement):
    
    ActionChains(browser).double_click(webElement).perform()
    
    try:
        indiv = browser.find_element_by_xpath("//div[@class='title poi']")  
    except:
        time.sleep(SLEEP_TIME)
        indiv = browser.find_element_by_xpath("//div[@class='title poi']") 
        
    return indiv

def getIndivGroup_button():
    
    try:
        button = browser.find_element_by_xpath("//a[@class='button']")
    except:
        time.sleep(SLEEP_TIME)
        button = browser.find_element_by_xpath("//a[@class='button']")
        
    ActionChains(browser).double_click(button).perform() 
    
    try:
        indiv = browser.find_element_by_xpath("//div[@class='title poi']")  
    except:
        time.sleep(SLEEP_TIME)
        indiv = browser.find_element_by_xpath("//div[@class='title poi']")  
        
    return indiv
    
def getFirstGroupNames():
    
    print u"开始.." 
    time.sleep(3)
    
    groupNames = []
    
    toTongXunLu()
    
    try:
        webElement = browser.find_elements(By.XPATH, "//h4[@class='nickname ng-binding']")
    except:
        time.sleep(SLEEP_TIME)       
        webElement = browser.find_elements(By.XPATH, "//h4[@class='nickname ng-binding']")

    for i in webElement:        
        groupNames.append(i.text)

    return groupNames[0]

def getNumbers(fistGroupName):
    
    result = []
    
    toTongXunLu()
        
    string = "//h4[text() = " + "\'" + fistGroupName + "\'" + "]"
    webElement = browser.find_element(By.XPATH, string)

    indiv = getIndivGroup(webElement)
        
    temp = (indiv.text).split()[-1]
    judge = re.search('^\([0-9]+\)$',temp)
    
    while (not judge):
        
        indiv = getIndivGroup(webElement)
      
        temp = (indiv.text).split()[-1]
        judge = re.search('^\([0-9]+\)$',temp)  

    print indiv.text
    result.append(indiv.text)
        
    while(True):   
        
        group = browser.find_element_by_xpath("//div[@class='tab_item no_extra']/a[@class='chat']")
        ActionChains(browser).double_click(group).perform()       
        group.send_keys(Keys.DOWN)
        
        indiv = getIndivGroup_button()
        
        temp = (indiv.text).split()[-1]
        judge = re.search('^\([0-9]+\)$',temp)

        count = 0  
        while (not judge):
            
            count = count + 1
            
            toTongXunLu()  
        
            indiv = getIndivGroup_button()  
            
            temp = (indiv.text).split()[-1]
            judge = re.search('^\([0-9]+\)$',temp)
            
            if(count == 3):
                return result
                break
        try:
            print indiv.text
        except:        
	 continue
        result.append(indiv.text)

def analysis(result):
    total = 0
    for i in result:        
        temp = i.split()[-1]
        indiv = int(re.findall('[0-9]+',temp)[0])
        total = total + indiv
    return total

def output(result, total):
    file = open("log.txt","w")    
    names = []
    numbers = []
    for i in result:  
        name = ""
        temp_name = i.split()[:-1]
        for j in temp_name:
            name = name + " " + j
        temp_number = i.split()[-1]
        number = int(re.findall('[0-9]+',temp_number)[0])
        
        names.append(name)
        numbers.append(str(number))
        
    for i in names:
        file.writelines(i)
  	file.writelines("\n")
    file.writelines("\n") 

    for j in numbers:
        file.writelines(j)
	file.writelines("\n")
    file.writelines("\n") 
        
    sum_group = u"总群数：" + str(len(result))
    sum_peple = u"总人数：" + str(total)
    file.writelines(sum_group)
    file.writelines("\n")
    file.writelines(sum_peple)
    file.writelines("\n")
    
    file.close()  
    
    return sum_group,sum_peple

        
if __name__ == '__main__':
    
    url = "https://wx.qq.com"
    chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

    os.environ["webdriver.chrome.driver"] = chromedriver
    
    print u"正在打开网页，请稍后.."

    print u"请给网速打分，good:1-5:bad"
    
    SLEEP_TIME = raw_input('')
    SLEEP_TIME = float(SLEEP_TIME)
    
    browser = webdriver.Chrome(chromedriver)
    browser.get(url)
    
    print u"请登录,然后按任意键继续.."
    
    PRICE = raw_input('')
    
    fistGroupName = getFirstGroupNames()    
    result = getNumbers(fistGroupName)
    total = analysis(result)    
    sum_group,sum_peple = output(result, total)
    
    print u"总群数：" + sum_group
    print u"总人数：" + sum_peple
    print u"已完成，详见log.txt.."


browser.quit()


