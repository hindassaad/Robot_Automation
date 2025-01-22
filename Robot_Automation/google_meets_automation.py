from selenium import webdriver  #selenium is the package, webdriver is the module
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import xarm

"""
A script to control the HiWonder Robotic Arm over Google Meets using chat prompts: up, down, left, and right.
"""

#initializations
arm = xarm.Controller('USB')
arm.setPosition([[1,500],[2,500 ],[3,500],[4,500],[5,500],[6,500]], duration = 1200)
serv_one=500
serv_two = 500 
serv_three=500
serv_four =500 
serv_five=500
serv_six = 500
PATH = "/Users/hinda/chromedriver-win64/chromedriver.exe"
curr_message = ""
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True) #detaches browser from python's execution
driver = webdriver.Chrome(PATH, options=options)

def login():
    try:
        your_name = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "input-for-name")))
        print(your_name.text)
        your_name.click()
        your_name.send_keys("Arm 2D2")
        your_name.send_keys(Keys.RETURN)

    except:
        print("login successful")

def open_chat():
    opened_chat = input("Did you open the chat?")
    if opened_chat:
        read_chat()
    else:
        print("Chat not opened.")

def read_chat():
    stop = False
    iteration = 0
    stop_commands = ["stop", "quit", "end", "end program", "terminate"]
    seen_messages = []
    big_container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ReactVirtualized__Grid__innerScrollContainer")))
    chat_item_containers = big_container.find_elements(By.CLASS_NAME, "chat-item-container")
    iteration+=1
    for chat_item in chat_item_containers:
        if chat_item in stop_commands:
            driver.quit()
        chat_message = chat_item.find_element(By.CSS_SELECTOR, ".new-chat-message__text-box").text.lower()
        print(chat_message)    
        seen_messages.insert(0, chat_message)    
        if chat_message in stop_commands:
            stop = True
    print(iteration)
    current_motion(seen_messages)

def current_motion(seen_messages):
    global curr_message
    movement_list = ["up", "down", "left", "right", "close", "open", "shake hand", "shakehand", "hand shake", "handshake"]
    print(movement_list)
    if seen_messages[0] in movement_list:
        if seen_messages[0] != curr_message:
            curr_message = seen_messages[0]
            direction = curr_message
            if direction == "shake hand":
                shake_hand()
            else:
                print("curr direction", direction)
                motion(direction)
        else:
            read_chat()
    else:
        read_chat()
    
def motion(direction):
    global serv_one, serv_two, serv_three, serv_four, serv_five, serv_six
    if direction == "shake hand":
        shake_hand()
    if direction == "left" and serv_six >= 100 and serv_six < 1000:
        serv_six += 400
    elif direction == "right" and serv_six > 100 and serv_six <= 1000:
        serv_six -= 400
    elif direction == "up" and serv_three >= 100 and serv_three < 1000:
        serv_four += 400
    elif direction == "down" and serv_three > 100 and serv_three <= 1000:
        serv_four -= 400
    elif direction == "close" and serv_one >= 100 and serv_one < 1000:
        serv_one += 400
    elif direction == "open" and serv_one > 100 and serv_one <= 1000:
        serv_one -= 400

    if 0<serv_one<1000 and 0<serv_two<1000 and 0<serv_three<1000 and 0<serv_four<1000 and 0<serv_five<1000 and 0<serv_six<1000:
        arm.setPosition([[1,serv_one],[2, serv_two],[3,serv_three],[4,serv_four],[5,serv_five],[6,serv_six]], duration = 1200)
    else:
        if direction == "left":
            serv_six -= 400
        elif direction == "right":
            serv_six += 400
        elif direction == "up":
            serv_four -= 400
        elif direction == "down":
            serv_four += 400
        elif direction == "close":
            serv_one -= 400
        elif direction == "open":
            serv_one += 400
    read_chat()

def shake_hand():
    global options, driver
    arm.setPosition([[1,500],[2, 500],[3,500],[4,500],[5,500],[6,500]], duration = 1000)
    time.sleep(1)
    arm.setPosition([[1,38],[2, 934],[3,500],[4,501],[5,500],[6,500]], duration = 1000)
    time.sleep(1)
    arm.setPosition([[1,38],[2, 880],[3,307],[4,713],[5,500],[6,500]], duration = 800)
    time.sleep(1)
    arm.setPosition([[1,477],[2, 880],[3,307],[4,714],[5,500],[6,500]], duration = 800)
    time.sleep(1)
    arm.setPosition([[1,476],[2, 880],[3,230],[4,714],[5,500],[6,500]], duration = 800)
    time.sleep(1)
    arm.setPosition([[1,476],[2, 880],[3,369],[4,714],[5,500],[6,500]], duration = 800)
    time.sleep(1)
    arm.setPosition([[1,476],[2, 880],[3,215],[4,714],[5,500],[6,500]], duration = 800)
    time.sleep(1)
    arm.setPosition([[1,22],[2, 880],[3,215],[4,714],[5,500],[6,500]], duration = 800)
    time.sleep(1)
    arm.setPosition([[1,498],[2, 500],[3,499],[4,500],[5,500],[6,500]], duration = 800)
    time.sleep(1)
    read_chat()
    

def main():
    meeting_id = "99811900708"
    driver.get(f"https://us04web.zoom.us/wc/join/{meeting_id}?")
    login()
    time.sleep(10)
    open_chat()
    driver.quit()

main()