import xarm
import time
import random
import speech_recognition
import pyttsx3
import replicate
from openai import OpenAI
from playsound import playsound
import os


os.environ["REPLICATE_API_TOKEN"] = ""

class Robot_arm:
    def __init__(self):    
        self.arm = xarm.Controller('USB') 
        self.recognizer = speech_recognition.Recognizer()
        self.client = OpenAI()


    def home_position(self):  
        print("Setting up Home position ..... ")
        self.arm.setPosition([[2,500],[3,130],[4,700],[5,700],[6,500]])


    def give_item(self):    
        self.arm.setPosition([[2,500],[3,263],[4,415],[5,160],[6,500]])


    def gripper_open(self): 
        print("Opening Gripper ..... ")
        self.arm.setPosition(xarm.Servo(1,170))


    def gripper_close(self): 
        print("Closing Gripper ..... ")
        self.arm.setPosition(xarm.Servo(1,540))


    def get_coffee(self): 
        print("Getting coffee")
        self.gripper_open()
        time.sleep(1)
        self.arm.setPosition([[2,500],[3,263],[4,415],[5,160],[6,620]])
        time.sleep(1)
        self.gripper_close()
        time.sleep(1)
        self.home_position()
        time.sleep(1)
        self.give_item()


    def get_keys(self):   
        print("Getting keys")
        self.gripper_open()
        time.sleep(1)
        self.arm.setPosition([[2,500],[3,263],[4,415],[5,160],[6,320]])
        time.sleep(1)
        self.gripper_close()
        time.sleep(1)
        self.home_position()
        time.sleep(1)
        self.give_item()


    def get_chips(self):   
        print("Getting chips")
        self.gripper_open()   
        time.sleep(1)
        self.arm.setPosition([[2,500],[3,263],[4,415],[5,160],[6,980]])
        time.sleep(1)
        self.gripper_close()
        time.sleep(1)
        self.home_position()
        time.sleep(1)
        self.give_item()


def send_request(text): 
    
    out = []   

    for event in replicate.stream("meta/meta-llama-3-8b-instruct",
    input={
        "top_k": 0,
        "top_p": 0.95,
        "prompt": text,
        "max_tokens": 512,
        "temperature": 0.7,
        "system_prompt": "You are a helpful assistant. Assume you are connected to a Robot and the key is to the right, coffee on the left and chips in the back . And prompt to help pick it up the item I ask and give it to me, Don't provide any non lexical fillers or actions. Answer them as either \"Certainly, let me pick up your \" and coffee\", \"key\" or \"chips\"",
        "length_penalty": 1,
        "max_new_tokens": 512,
        "stop_sequences": "<|end_of_text|>,<|eot_id|>",
        "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
        "presence_penalty": 0,
        "log_performance_metrics": False
    },
    ): 
        out.append(str(event))
        final_out = final_out.join(out)

        response = client.audio.speech.create(model="tts-1",voice="alloy", input=final_out)  
        response.stream_to_file("output.mp3") 
    return final_out


def main():   
    my_arm = Robot_arm()       

    while True:

        try:
            with speech_recognition.Microphone(0) as mic:  
                
                my_arm.recognizer.adjust_for_ambient_noise(mic) 
                audio = my_arm.recognizer.listen(mic)
                
                text = my_arm.recognizer.recognize_google(audio) 
                text = text.lower()
                print(f"Recognized: {text}")
                
                output_pred = send_request(text)    
                process_data = output_pred.split(" ")
                
                stripped_var = process_data[-1].strip(".") 
                
                playsound('output.mp3') 
                
                if stripped_var == "coffee":
                    my_arm.get_coffee()
                elif stripped_var == "keys":
                    my_arm.get_keys()
                elif stripped_var == "chips":
                    my_arm.get_chips()
                else:
                    print("Invalid !!! ")
                    main()

        except speech_recognition.UnknownValueError:  
            my_arm.recognizer = speech_recognition.Recognizer()
            continue

        except Exception as e:   
            print(f"An error occurred: {e}")
            break


if __name__ == "__main__":  
    main()   