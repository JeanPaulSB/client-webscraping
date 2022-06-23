#Initializing our web driver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from datetime import datetime
import pandas as pd
import time
with open("settings.txt") as file:
    data=file.readlines()
shares=data[0].split(";")
timing=set(data[1].split(","))



def login(driver,actions):
    user="" ##change this with our user 
    password="" ##change this with your password

    user_input=WebDriverWait(driver,10).until(lambda driver:driver.find_element(By.XPATH,"/html/body/form/div/div[1]/div[2]/div/div/div[3]/div[1]/div/div[3]/div[1]/input"))
    actions.send_keys_to_element(user_input,user).perform()
    password_input=driver.find_element(By.XPATH,"/html/body/form/div/div[1]/div[2]/div/div/div[3]/div[1]/div/div[3]/div[2]/input")
    actions.send_keys_to_element(password_input,password).perform()
    login_button=driver.find_element(By.XPATH,"/html/body/form/div/div[1]/div[2]/div/div/div[3]/div[1]/div/div[3]/div[4]/button")
    actions.click(login_button).perform()


    


options=Options()
#options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.page_load_strategy = 'eager'
driver=webdriver.Chrome(options=options)
driver.get("https://www.cmcmarketsstockbroking.com.au/clients/homepage.aspx")
actions=webdriver.ActionChains(driver)
start=time.time()
#login(driver,actions)
time.sleep(6)

print(f"Login execution time:{time.time()-start}")
first_window=driver.current_window_handle
#after logged in we need to query for 



for share  in shares:
    url=f'https://www.cmcmarketsstockbroking.com.au/Market/Summary.aspx?asxcode={share}'
    driver.switch_to.new_window('tab')
    driver.get(url)



#child windows

chwd=driver.window_handles

driver.switch_to.window(first_window)
chwd.remove(first_window)
driver.close()
values=[0]*len(shares)
changes=[0]*len(shares)
while True:
    i=0
    start=time.time()
    now=str(datetime.now().strftime("%H:%M"))
    
    for window in chwd:
        driver.switch_to.window(window)
        driver.refresh()
        #share_name=driver.find_element(By.XPATH,"/html/body/form/div[4]/div[2]/div/div[1]/div[3]/div[1]/div/div[1]/div[1]/h1").text
        share_name=WebDriverWait(driver,10).until(lambda driver: driver.find_element(By.CSS_SELECTOR,"#page-header > h1")).text
        #ind_open=driver.find_element(By.XPATH,"/html/body/form/div[4]/div[2]/div/div[1]/div[3]/div[2]/div/table[2]/tbody/tr[1]/td[1]").text
        ind_open=WebDriverWait(driver,10).until(lambda driver: driver.find_element(By.ID,"_ctl0__ctl0_uiMainSection_InstrumentQuotePrices_IndicativePrice")).text
        

        if ind_open!="":
            ind_open=float(ind_open)
            if ind_open>values[i]:
                changes[i]==1
                values[i]=ind_open
            else:
                changes[i]==0
        else:
            values[i]=0
        i+=1
    df=pd.DataFrame({
        'Share':shares,
        'Ind Open':values,
        'Has changed':changes
    })
    if now in timing:
        print(datetime.now())
        print(df.sort_values(by=["Has changed"]))
    
    print(f"Execution time: {time.time()-start}")


#_ctl0__ctl0_uiMainSection_InstrumentQuotePrices_IndicativePrice
