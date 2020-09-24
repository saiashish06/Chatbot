import io
import random
import string
import warnings
import mysql.connector
import time
from time import sleep
from datetime import datetime, date, time, timedelta
connection = mysql.connector.connect(host="localhost", user="root", passwd="", database="yoyopizza")
cursor = connection.cursor()
warnings.filterwarnings('ignore')
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
Order_INPUTS = ("order", "pizza", "menu", "1", "i want pizza","i would like to order pizza",)
track_INPUTS = ("track","status","my","2",)
GREETING_RESPONSES = ["hi", "hey", "hi there", "hello", "I am glad! You are talking to me"]
Check_Input =["yes","okay","fine","go","S"]
check_corn=["corn",'Corn','Cornveg']
check_Cheese=["cheese","chese","cheeseveg"]
check_chicken=["chicken","Chicken"]
check_super=["supreme","nonvegsupreme","nonveg"]
check_small=["small","s","smal","Small","S"]
check_lar=["large","L","l","Large"]
check_mid=["medium","Medium","M","m","med"]
def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def order(sentence):
    for word in sentence.split():
        if word.lower() in Order_INPUTS:
            return "menu"
def track(sentence):
    for word in sentence.split():
        if word.lower() in track_INPUTS:
            return "track"
def Check_detials(sentence):
    for word in sentence.split():
        if word.lower() in Check_Input:
            return "okay"
def select_pizza(sentence):
    for word in sentence.split():
        if word.lower() in check_corn:
            return "Corn Veg"
    for word in sentence.split():
        if word.lower() in check_Cheese:
            return "Cheese Veg"
    for word in sentence.split():
        if word.lower() in check_chicken:
            return "Chicken"
    for word in sentence.split():
        if word.lower() in check_super:
            return "NonVegSupreme"
def select_size(sentence):
    for word in sentence.split():
        if word.lower() in check_small:
            return "Corn Veg"
    for word in sentence.split():
        if word.lower() in check_mid:
            return "Cheese Veg"
    for word in sentence.split():
        if word.lower() in check_lar:
            return "Chicken"

flag=True
sql="SELECT MAX(`order_id`) FROM `orders`"
cursor.execute(sql)
res=cursor.fetchall()
if(res[0][0]!=None):
    genorder=res[0][0]
else:
    genorder=101
while(True):
    print("YOYOBOT: Welcome to YOYO Pizza!!\nText hey to get start")
    user_response = input("You: ")
    user_response=user_response.lower()
    if(greeting(user_response)!=None):
        print("YOYOBOT: "+greeting(user_response)+"\n\nHow can I help you? \n1- Order pizza\n2-Track your order status\n3-Nothing :( \n")
        while(True):
            user_response = input("You: ")
            if(track(user_response)!=None):
                cus_orid=input("Please enter your OrderID:")
                inpu=(cus_orid,)
                sql="SELECT * FROM `orders` WHERE `order_id`=%s"
                cursor.execute(sql,inpu)
                res=cursor.fetchall()
                print("your order for\nPizza:",res[0][2])
                print("Size",res[0][3])
                print("\n Will be ready by time ",res[0][5])
                break

            elif(order(user_response)!=None):
                cus_num=input("Enter your number\nYou: ")
                sql="SELECT `cus_num` FROM `customer` WHERE `cus_num`=%s"
                inpu=(cus_num,)
                cursor.execute(sql,inpu)
                res=cursor.fetchall()
                if(res):
                    print("Hey your data is already with us")
                    sql="SELECT * FROM `customer` WHERE `cus_num`=%s"
                    cursor.execute(sql,inpu)
                    res=cursor.fetchall()
                    print("Number: ",res[0][0])
                    print("Name: ",res[0][1])
                    print("Address: ",res[0][2])
                    print("\nIs everything correct?")
                    check_res = input("You: ")
                    if(Check_detials(check_res)!=None):
                        print("\nThank you")
                    else:
                        sql="DELETE FROM `customer` WHERE `cus_num`=%s"
                        cursor.execute(sql,inpu)
                        connection.commit()
                        cus_nam=input("Enter your Name\nYou:")
                        cus_add=input("Enter your Address\nYou:")
                        inpu=(cus_num,cus_nam,cus_add)
                        sql="INSERT INTO `customer`(`cus_num`, `cus_nam`, `cus_add`) VALUES (%s,%s,%s)"
                        cursor.execute(sql,inpu)
                        connection.commit()
                else:
                    cus_nam=input("Enter your Name\nYou:")
                    cus_add=input("Enter your Address\nYou:")
                    inpu=(cus_num,cus_nam,cus_add)
                    sql="INSERT INTO `customer`(`cus_num`, `cus_nam`, `cus_add`) VALUES (%s,%s,%s)"
                    cursor.execute(sql,inpu)
                    connection.commit()
                while(True):
                    pizza=input("\nSelect Pizza\nCornveg\ncheeseveg\nchicken\nNonVegSupreme\nMake Your Choice:\nYou: ")
                    if(select_pizza(pizza)!=None):
                        pizza=select_pizza(pizza)
                        break
                    print("Sorry please specify clearly\n")

                while(True):
                    size=input("Please select your pizza size:\nSmall,medium or Large \nYou:")
                    if(select_size(size)!=None):
                        pizza=select_size(size)
                        break
                    print("Sorry please specify clearly\n")
                print("please Finish payment\n\n")
                sleep(10)
                now = (datetime.now() + timedelta(minutes = 15))
                current_time = now.strftime("%H:%M:%S")
                genorder+=1
                inpu=(genorder,cus_num,pizza,size,"done",current_time)
                sql="INSERT INTO `orders`(`order_id`, `cus_num`, `pizza_name`, `pizza_size`, `payment`, `time`) VALUES (%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql,inpu)
                connection.commit()
                print("Thank you \n\nYour order is taken for")
                print(pizza,"of size",size,"your orderID:",genorder)
                print("\nYou get your pizza in 15min\n\n")
                break;
            else:
                break
