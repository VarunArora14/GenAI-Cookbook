'''
Consider scenarios when API call does retries. We do not want retries to increase the traffic constantly affecting other services. For this, we use exponential 
backoff when doing retries. Below is implementation for same - 
'''
import random, time
from datetime import datetime

def tprint(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(timestamp, msg)

i=0

def fn():
    global i
    i+=1
    tprint(f"i={i}") # number of times this function is being called
    num = random.randint(0,2)
    print("num:",num)
    if num==0:
        tprint("Bad response")
        raise Exception("Bad response")
    elif num==1:
        tprint("Good response") 
    else:
        tprint("429 rate limit error!")
        raise Exception("429 rate limit error!")

# below function will go through max 5 retries and if retries exist, it can all the fn() again. The fn() has 3 states based on which it can give errors/messages
def retryWithBackoff(max_retries=5, backoff_factor=1):
    retries=0
    print("retries:", retries)
    while retries<=max_retries:
        try:
            fn()
        except Exception as e:
            if "429" in str(e):
                sleep_time = (retries+1)*backoff_factor
                sleep_time+=(2**retries)*backoff_factor
                time.sleep(sleep_time)
                retries+=1 # retries only increase when rate limit comes, otherwise it was infinite loop
            else:
                print("Bad response! Cannot be proceeded")
                


retryWithBackoff()