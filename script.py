from random import randint
import requests
import time
import datetime
import os
import os.path
def parse():
    global link
    global diversion
    global start
    global x
    with open("REST.txt") as file:
        rest = file.read()
    rest = rest.split('&')
    x = 0
    i = 0
    while i < len(rest):
        arr = rest[i].split('=')
        if arr[0] == "status" and arr[1] == "Success":
            x = x+2
        if arr[0] == "link":
            link = arr[1]
            x = x+1
        if arr[0] == "diversion":
            diversion = arr[1]
            x = x+1
        if arr[0] == "start":
            start = arr[1]
            x = x+1 
        i = i+1

def file_create():
    global file_name
    link_edit = link.replace('%2F' ,'/')
    link_edit = link_edit.replace('%3A' ,':') 
    rand = randint(0, 10000000)
    file_name =  f"records/{rand}.mp3"
    file_get = requests.get(link_edit)
    if file_get.status_code != 200:
        time.sleep(70)
        file_get = requests.get(link_edit)
    if file_get.status_code != 200:
        exit()
    with open(file_name, 'wb') as f:
         f.write(file_get.content)

def datetime_create():
    global call_time
    date_time_obj = datetime.datetime.strptime(start, '%Y%m%dT%H%M%SZ')
    delta = datetime.timedelta(hours=3, minutes=0)
    call_time = date_time_obj + delta

def scandir_and_delete_file_string():
    global array
    j = 0
    dir = 'records/'
    files = os.listdir(dir)
    while j < len(files):
        file_name_delete = f"records/{files[j]}"
        time_create = os.path.getmtime(file_name_delete)
        realtime = time.time()
        delta = realtime - time_create
        if delta > 10:
            k = 0
            with open("index.html") as file:
                array = [row.strip() for row in file]
            while k < len(array): 
                if file_name_delete in array[k]:
                    array.pop(k)
                    os.remove(file_name_delete)
                    edit()
                k = k+1
        j =  j +1

def edit():
    global array
    а = 0
    with open('index.html', 'w') as file:
        for a in array:
            file.write(a + '\n')


def create_string():
    global array 
    if x == 5:
        line = f"<p><h3>Тип вызова: Входящий (на номер  {diversion}) | Дата/время вызова: {call_time} | <a href='{file_name}'>Ссылка на запись</a></h3></p><hr />"
    elif x == 4:
        line = f"<p><h3>Тип вызова: Исходящий | Дата/время вызова: {call_time} | <a href='{file_name}'>Ссылка на запись</a></h3></p><hr />"
    else:
        exit()
    with open("index.html") as file:
        array = [row.strip() for row in file]
    array.append(line)
    edit() 
file_name = ''
file_name_delete = ''
link = ''
diversion = ''
start = ''
array = ''
x = 0
parse()
file_create()
datetime_create()
scandir_and_delete_file_string()
create_string()
