from sklearn.externals import joblib
import cv2
from matplotlib.image import imsave as save
import os
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import sys

def chek(x,y,w,h, norm_arr):
    for x_n, y_n, w_n, h_n  in norm_arr:
        if((x >= x_n) and (x + w <= x_n + w_n) and (y >= y_n) and (y + h  <= y_n + h_n)):
            return False
    return True

def chek2(x,y,w,h,norm_arr):
    if not chek(x,y,w,h,norm_arr):
        #print ("1")
        return norm_arr
    delete_index = np.array([])
    first = True
    for ind, ar in enumerate(norm_arr):
        t_x,t_y,t_w,t_h = ar
       
        if not chek(t_x,t_y,t_w,t_h, [[x,y,w,h]]):
            delete_index = np.hstack((delete_index, ind))
        #t_norm_arr = np.vstack(((np.delete(norm_arr, ind ,0)), [x,y,w,h]))
        #if  not chek(t_x,t_y,t_w,t_h, t_norm_arr):
        #print (2)
            #return np.vstack(((np.delete(norm_arr, ind ,0)), [x,y,w,h]))
    #print ("3")
    norm_arr = np.delete(norm_arr, delete_index, 0)
    return np.vstack((norm_arr, [x,y,w,h]))

def norm(x):
    if(x > 128):
        return np.uint8(255)
    return np.uint8(0)

import pylab as pl
from mpl_toolkits.mplot3d import axes3d

def evaluation_of_func (formula, file_path):
    global x, y
    x = np.arange(-5.0, 5.0, 0.5)
    y = np.arange(-5.0, 5.0, 0.5)
    #   reshape (1, count_of_all_y_variables) 
    y = y.reshape(1, 20)
    #   reshape (count_of_all_x_variables, 1) 
    x = x.reshape(20, 1)
    #   function evaluation
    z = eval(func(formula))
    write_elements(z, file_path)

def write_elements (elements, file_path):
    print(len(elements))
    print(elements)

    output_file = open('file', 'wb')
    elements.tofile(file_path)
    output_file.close()


    #plt.show()

#   не меняй, всё норм работает)
#   сохранение png картинки по имени
def save2(name='', fmt='png'):
    pwd = os.getcwd()
    #   директория для сохранения картинки 
    iPath = 'C:\\Program Files\\Epic Games\\UE_4.18\\Engine\\Binaries\\Win64'
    if not os.path.exists(iPath):
        os.mkdir(iPath)
    name="RenderTargetFinal"
    os.chdir(iPath)
    plt.savefig('{}.{}'.format(name, fmt), fmt='png')
    os.chdir(pwd)

def func(string):
    i = 0
    start = 0
    #   массив непреобразованный с помощью numpy
    fun_str = []
    #   конечная строка
    fun = ""
    j = 0
    flag = True
    
    #   проверка на '-' в начале строки, то есть умножение на -1 
    if string[0] == '-': 
        fun_str.append('-1') 
        fun_str.append('*') 
        start = 1 
        j = 1 
    #   вставляем скобки вокруг тригонометрического "наполнителя"
    p = string.find('sin') 
    if not p == -1:
        string = string[0:p+3] + '(' + string[p+3] + ')' + string[p+4:len(string)] 
    p = string.find('cos') 
    if not p == -1: 
        string = string[0:p+3] + '(' + string[p+3] + ')' + string[p+4:len(string)]
    
    for i in range(start, len(string)):
        #   костыль, который позволяет выражение под тригонометрической функцией считать, как единое целое
        if string[i] == '(':
            flag = False;
        if string[i] == ')':
            flag = True
        if flag:
            #   отделяет знаки, от всего иного
            if string[i] == '+' or string[i] == '*' or string[i] == '/' or string[i] == '-' or string[i] == '^':
                if i != j:
                    fun_str.append(string[j:i])
                fun_str.append(string[i])
                j = i+1
            elif string[i] == 'x' and i != 0 and string[i-1] != '+' and string[i] != '*' and string[i] != '/' and string[i] != '-' and string[i] != '^':
                fun_str.append(string[j:i])
                fun_str.append('*')
                fun_str.append(string[i])
                j = i + 1
            #   окончание разбиения
            if i == len(string)-1:
                fun_str.append(string[j:i+1])
            i+=1
    
    for i in range(0,len(fun_str)):
        #   проверка на степень с последующей заменой на ** - степень в питоне
        if fun_str[i].find('^') != -1:
            fun_str[i] = fun_str[i].replace("^","**")
        #   костыль по удалению пробелов
        fun_str[i] = fun_str[i].replace(" ","")
        #   добавление знаков сразу в конечную строку во избежание применения numpy к ним
        if fun_str[i] == '+'or fun_str[i] == '*' or fun_str[i] == '/' or fun_str[i] == '-' or fun_str[i] == '**':
            fun += fun_str[i]
        else:
            try:
                #   всё, что можно считать функцией без numpy
                eval(fun_str[i])
                fun += fun_str[i]
            except: 
                #   только с numpy
                fun += 'np.' + fun_str[i]
    return fun


f = np.vectorize(norm)

model = joblib.load("cls.pkl")
path = "C:\\Program Files\\Epic Games\\UE_4.18\\Engine\\Binaries\\Win64\\RenderTarget.png"

img = cv2.bitwise_not(cv2.imread(path))
    
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = cv2.medianBlur(gray,5)

thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
thresh_color = cv2.cvtColor(thresh,cv2.COLOR_GRAY2BGR)

thresh = cv2.dilate(thresh,None,iterations = 3)
thresh = cv2.erode(thresh,None,iterations = 2)

_,contours,_ = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)


normal_contours = np.array([], dtype='int32')

for ind,cnt in enumerate(contours):
    x,y,w,h = cv2.boundingRect(cnt)
  
    if ind == 0:
        normal_contours = np.array([[x,y,w,h]])
    else:
        normal_contours = chek2(x,y,w,h,normal_contours)
    
sorr_con = sorted(normal_contours, key= lambda row : row[0])
for ind, ar in enumerate(sorr_con):
    x,y,w,h = ar
    t_img = img[y:y+h,x:x+w]
    t_img = cv2.resize(t_img, (32,32))
    if not os.path.exists("data"):
        os.mkdir("data")
    save("data\\{}.png".format(ind),f(t_img))
    
res = np.array([], dtype = "str")
for elem in os.listdir("data"):
    t_img = cv2.imread("data\\{}".format(elem))
    res = np.append(res, model.predict(t_img[:,:,0].reshape((1,32*32))))

import shutil
shutil.rmtree("data")

formula = ""
for c in res:
    formula += c
print(formula)

evaluation_of_func(formula, "C:\\Program Files\\Epic Games\\UE_4.18\\Engine\\Binaries\\Win64\\model.bin")

