import smtplib
import numpy as np
import datetime
import requests
import warnings
warnings.filterwarnings("ignore")

carriers = {'verizon':'vzwpix.com', 'att':'mms.att.net', 'tmobile':'tmomail.net'}
# pw = open("pw.txt").read()


print("Welcome to LMS, Luke Message Service")
username = input('Enter SMTP username: \n')
pw = input('Enter SMTP password: \n')
host = input('Enter host address:\n')

contacts = {}
f = open('contacts.txt', 'a')
# f.write('Luke, 5718880684@mms.att.net\nAlso Luke, 5718880684@mms.att.net\n')
f.close()


def login(usr, pwd, h=host, p=465):
    e = smtplib.SMTP_SSL(host=h, port=p)
    e.login(user=usr, password=pwd)
    return e
def loadContact(name):
    return contacts[name]

def findCarrier(num, carriers, log):
    for crr in carriers:
        try:
            email_address = num + '@' + carriers[crr]
            response = requests.get(
                "https://isitarealemail.com/api/email/validate",
                params={'email': email_address})
            status = response.json()['status']
            if status == 'valid':
                print('Carrier is ' + crr)
        except:
            pass
def logout(em):
    em.quit()
def sendmsg(subj, txt, to, frm, em):
    mssg = 'Subject: {}\n\n{}'.format(subj, txt)
    stmt = em.sendmail(from_addr=frm, to_addrs=to, msg=mssg)
    # em.quit()
    return stmt
def enterContact(name, number, carrier):
    contacts[name] = str(number) + '@' + carrier
    l = open("contacts.txt", "a")
    l.write(name + ', ' + contacts[name] + '\n')
#def loadContact(name):
    return contacts[name]
def importContacts(fileName):
    global contacts
    print("fileName: ", fileName)
    raw_data = open(fileName, 'rt')
    # loadtxt defaults to floats
    dict = {}
    # dict[raw_data[0,0]] = raw_data[0,1]
    try:
        data = np.loadtxt(raw_data, usecols=(0, 1), dtype='str', delimiter=",")
        if len(data) == 0:
            ipt = input('Enter contact name:\n')
            name = ipt
            ipt = input('Enter contact number:\n')
            number = int(ipt)
            while ipt not in carriers.keys():
                print("Carrier options: ")
                for car in carriers.keys():
                    print("{}".format(car), end=', ')
                ipt = input('\nEnter contact carrier:\n')
            enterContact(name, number, carriers[ipt])
            return contacts
    except:
        pass
    for i in range(len(data)):
        dict[data[i,0]] = data[i, 1]
    return dict


contacts = importContacts('contacts.txt')
#enterContact("Atharva", )
print('Logging in...')
log = login(username, pw)
ipt = ''
ctct = ''
messg = ''
name = ''
number = 0
newcarrier = ''
def resync(log, pw):
    logout(log)
    return login(username, pw)
while ipt != 'done':
    ipt = input('Type \'send\' to send a message\nType \'add\' to add a contact\nType \'resync\' to resync\n')
    if(ipt == 'send'):
        while ipt not in contacts.keys():
            print("\nContacts:\n")
            for ctt in contacts.keys():
                print("{}".format(ctt), end=', ')
            print('\n')
            ipt = input('Enter contact name:\n')
        ctct = ipt
        ipt = input('Enter msg:\n')
        messg = ipt
        try:
            a = sendmsg('',messg,loadContact(ctct),username,log)
            now = datetime.datetime.now()
            out = 'Message failed to send ' + str(a)
            if str(a) == '{}':
                out = 'Message sent at: ' + str(now)
            print(out)
        except:
            print('Send Failed. Please resync and try again.')
    if(ipt == 'add'):
        ipt = input('Enter contact name:\n')
        name = ipt
        ipt = input('Enter contact number:\n')
        number = int(ipt)
        while ipt not in carriers.keys():
            print("Carrier options: ")
            for car in carriers.keys():
                print("{}".format(car), end =', ')
            ipt = input('\nEnter contact carrier:\n')
        enterContact(name, number, carriers[ipt])
    if(ipt == 'resync'):
        resync(log, pw)
    if ipt == 'find carrier':
        num = input('Enter number: \n')
        findCarrier(num, carriers, log)


logout(log);

#Me - 5718880684@txt.att.net
#Pavan - 7035980278@vtext.com
#Aadi - 7038701218@tmomail.net
#Varun - 7038176529@vtext.com000
#Ian - 703-4207783