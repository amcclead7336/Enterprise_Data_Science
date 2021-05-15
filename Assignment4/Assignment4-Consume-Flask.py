import requests
import random
import time

url = "http://localhost:5000/sign_img"

for _ in range(5):
    test_sign = random.randint(0, 42)
    filename = "TrafficData/Meta/"+str(test_sign)+".png"

    file = {"input_file": open(filename, "rb")}
    r = requests.post(url,files=file)
    print("Test sign was: " + str(test_sign) +"\nPred "+r.text.lower())
    print()
    time.sleep(3)

