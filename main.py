from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QFileDialog, QDialog
import queue
import requests
import json
import threading
from PyQt5.QtGui import QIcon
import sys
from instabot_py import InstaBot
from checker import InstaChecker
import license
import time, random
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import objgraph


class Ui(QtWidgets.QMainWindow):
    max_threads = 1
    proxyqueue = queue.Queue()
    username_queue = queue.Queue()
    threadCount = 1
    running = False
    names = []
    count = 0
    proxiescount = 0
    proxies = []
    claiming_flag = False
    restartRequiredFlag = 0
    checked_count = 1
    error_count = 0
    sandbox_flag = False
    prev_count = 1
    claim_name = ""

    if (license.licence_check() != 1):
        print("check failed")
        time.sleep(5)
        sys.exit(0)

    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('gui.ui', self) # Load the .ui file

      
        self.login_status = False
        
        #Buttons
        self.login_Btn = self.findChild(QtWidgets.QPushButton, 'loginButton')
        self.login_Btn.clicked.connect(self.loginButtonPressed) # Remember to pass the definition/method, not the return value!

        self.start_Btn = self.findChild(QtWidgets.QPushButton, 'claimButton')
        self.start_Btn.clicked.connect(self.MainLoop)

        self.stop_Btn = self.findChild(QtWidgets.QPushButton, 'stopButton')
        self.stop_Btn.clicked.connect(self.StopLoop)
        
        self.import_userlist_Btn = self.findChild(QtWidgets.QPushButton, 'usernameButton')
        self.import_userlist_Btn.clicked.connect(self.importUserList)


        self.proxy_Btn = self.findChild(QtWidgets.QPushButton, 'proxyButton')
        self.proxy_Btn.clicked.connect(self.proxyLoad)


        self.sandbox_Btn = self.findChild(QtWidgets.QPushButton, 'sandbox_Btn')
        self.sandbox_Btn.clicked.connect(self.sandbox)

        self.mthreads_Btn = self.findChild(QtWidgets.QPushButton, 'pushButton_maxthreads')
        self.mthreads_Btn.clicked.connect(self.updateMaxThreads)
        

        self.check_LineEdit = self.findChild(QtWidgets.QLineEdit, 'lineEdit_checking')
        self.username_LineEdit = self.findChild(QtWidgets.QLineEdit, 'lineEdit_username')
        self.password_LineEdit = self.findChild(QtWidgets.QLineEdit, 'lineEdit_password')
        self.email_LineEdit = self.findChild(QtWidgets.QLineEdit, 'lineEdit_email')
        self.listSize_LineEdit = self.findChild(QtWidgets.QLineEdit, 'lineEdit_listSize')
        self.maxThreads_LineEdit = self.findChild(QtWidgets.QLineEdit, 'lineEdit_maxThreads')
        
    
        self.proxy_LineEdit = self.findChild(QtWidgets.QLineEdit, 'lineEdit_proxyNo')
        self.checkedNo_LineEdit = self.findChild(QtWidgets.QLineEdit, 'lineEdit_checkedNo')
        self.errorNo_LineEdit = self.findChild(QtWidgets.QLineEdit, 'lineEdit_errorcount')
        self.day_LineEdit = self.findChild(QtWidgets.QLineEdit, 'lineEdit_day')
        self.hour_LineEdit = self.findChild(QtWidgets.QLineEdit, 'lineEdit_hour')
        self.second_LineEdit = self.findChild(QtWidgets.QLineEdit, 'lineEdit_second')
        self.threadpool_LineEdit = self.findChild(QtWidgets.QLineEdit, 'lineEdit_threadpool')


        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1) #30

        self.consoleUpdate = QtCore.QTimer()
        self.consoleUpdate.timeout.connect(self.ConsoleUpdate)
        self.consoleUpdate.start(30) #30

        self.timer3 = QtCore.QTimer()
        self.timer3.timeout.connect(self.speedCounter)
        self.timer3.start(20000)

        self.console = self.findChild(QtWidgets.QTextEdit, 'textEdit_console')
        
        self.show() # Show the GUI
        
    def updateMaxThreads(self):

        self.max_threads = int(self.maxThreads_LineEdit.text())
        print("UPDATED MAX THREADS TO: " + str(self.max_threads))

        
    def speedCounter(self):
        try:
            per_second = (self.checked_count - self.prev_count) / 20
            per_hour = per_second*3600
            per_day = per_hour * 24

            self.day_LineEdit.setText(str(per_day))
            self.hour_LineEdit.setText(str(per_hour))
            self.second_LineEdit.setText(str(per_second))
            self.prev_count = self.checked_count
         
            
        except:
            print("DIV 0 ERROR")
   
   
    def sandbox(self):
        if self.sandbox_flag == False:
            self.sandbox_flag = True
        else:
            self.sandbox_flag = False
        
        self.console.append("Sandbox - " + str(self.sandbox_flag))


    def proxyLoad(self):
        if (self.restartRequiredFlag < 2):
            self.proxies = []
            dlg = QFileDialog()
            dlg.setFileMode(QFileDialog.ExistingFile)
            dlg.setNameFilters(["Text files (*.txt)"])
            
            
            self.console.append("Reading proxies list file...")
        
            if dlg.exec_():
                filenames = dlg.selectedFiles()
                f = open(filenames[0], 'r')

                Lines = f.readlines() 
                self.proxiescount = 0
                # Strips the newline character 
                self.proxies.clear()

                for line in Lines: 
                    
                    line = line.strip()

                    self.proxyqueue.put(line)
                    self.proxies.append(line) 
                    
                    self.proxiescount += 1
            else:
                self.console.append("Invalid file selected...")
            random.shuffle(self.proxies)   
            # for p in self.proxies:
            #     self.proxyqueue.put(p)

            self.proxy_LineEdit.setText(str(self.proxiescount))
            self.console.append("File read - " + str(self.proxiescount) + " proxies loaded")
     
            self.restartRequiredFlag += 1
        else:
            self.console.append("RESTART REQUIRED TO EDIT PROXY LIST - already imported")
      

    def importUserList(self):
        if (self.restartRequiredFlag < 2):
            self.names = []
            dlg = QFileDialog()
            dlg.setFileMode(QFileDialog.ExistingFile)
            dlg.setNameFilters(["Text files (*.txt)"])
            
                
            self.console.append("Reading username list file...")
        
            if dlg.exec_():
                filenames = dlg.selectedFiles()
                f = open(filenames[0], 'r')

                Lines = f.readlines() 
                self.count = 0
                # Strips the newline character 
                for line in Lines: 
                    self.names.append(line.strip()) 
                    self.count += 1
            else:
                self.console.append("Invalid file selected...")
            random.shuffle(self.names) 
            for n in self.names:
                self.username_queue.put(n)

            self.listSize_LineEdit.setText(str(self.count))
            self.console.append("File read - " + str(self.count) + " words loaded")
            self.restartRequiredFlag += 1
        else:
            self.console.append("RESTART REQUIRED TO EDIT USERNAME LIST - already imported")

    def sendEmail(self,Cname,subjects):
        
        print("Sending Email Notification")
        try:
            sender_email = "valesamores4@gmail.com"
            receiver_email = "percy.edward74@gmail.com"
            password = "xp2QZEk95F9"

            message = MIMEMultipart("alternative")
            message["Subject"] = subjects
            message["From"] = "IGClaimer 2020"
            message["To"] = receiver_email

            now = datetime.datetime.now()

            # Create the plain-text and HTML version of your message
            text = ("An attempt to claim the following username has been made " + Cname + "\n" + now.strftime("%Y-%m-%d %H:%M:%S")) 
            

            # Turn these into plain/html MIMEText objects
            part1 = MIMEText(text, "plain")


            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            message.attach(part1)


            # Create secure connection with server and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(
                    sender_email, receiver_email, message.as_string()
                )
        except:
            print("Failed to send email - GOOGLE SECURITY\nLOGIN to your GMAIL account using chrome to fix\n\nCheck *Less secure apps* is ENABLED too @ \nhttps://myaccount.google.com/lesssecureapps?pli=1")

    def loginButtonPressed(self):
        try:
            if(self.login_status == False):
                global bot

                #LOGIN BIT
                if ( self.sandbox_flag == False):
                    bot = InstaBot(login=self.username_LineEdit.text().strip(),  password=self.password_LineEdit.text().strip(), console=self.console, apps = app, email_a = self.email_LineEdit.text().strip())
                    bot.login()

                self.console.append("Creating threads") #Create object threads
                self.checker = InstaChecker(proxiesL=self.proxies)
                    
                
                self.login_status = True
                
            else:
                self.console.append("Already Logged In") #Create object threads
        except:
            self.console.append("Login Function Crashed :/") #Create object threads
            print("Login Function Crashed :/")
        

    def StopLoop(self):
        #global bot
        self.console.append("****BOT STOPPING****")
      
        #bot.logout()
        self.running = False
    
        self.login_status = False

    def ThreadFunction(self,threadProxy):
        try:
            name_check = self.username_queue.get()
        except:
            name_check = random.choice(self.names)
            print("Name queue empty error")
        #prev = time.perf_counter()
       
        response = self.checker.check(check_name=name_check,Tproxy = threadProxy)
        #print(time.perf_counter() - prev)
        
        if response == 0: #Taken
            self.checked_count += 1
            
        elif response == 1: #CLAIMABLE
            print ("CLAIMING: " + name_check)
            self.claim_name = name_check   

            if (self.sandbox_flag != True):
                self.claiming_flag = True
            
        elif response == 2: #PROXY ERROR
            self.error_count += 1
            print("400 - BAD REQUEST")
        elif response == 3: #INSTA COOLDOWN
            print("INSTA COOLDOWN")
            time.sleep(10)
            self.error_count += 1
        elif response == 4: #PROXY ERROR
            self.error_count += 1
        elif response == 5: #PROXY ERROR
            print("UNKNOWN ERROR CODE")
            self.error_count += 1
        
        elif response == 6: #PROXY ERROR
            self.error_count += 1
    
        else:
            print("UNKNOWN ERROR")
            self.error_count += 1

            
        self.proxyqueue.put(threadProxy)
        try:
            self.username_queue.put(name_check)
        except:
            print("Name put error")
            

        
    def MainLoop(self):
        if (self.login_status == False):
            self.console.append("LOGIN FIRST")

        else:
            self.console.append("****STARTING BOT****")
            self.running = True
            self.claiming_flag = False
  


    def ConsoleUpdate(self):
        self.console.verticalScrollBar().setValue(self.console.verticalScrollBar().maximum())
        if(self.console.verticalScrollBar().value() > 0):
            self.console.clear()
        
        self.threadpool_LineEdit.setText(str(threading.active_count()))
        self.checkedNo_LineEdit.setText(str(self.checked_count))
        self.errorNo_LineEdit.setText(str(self.error_count))
        app.processEvents()


    def update(self):
        global bot
       
        if(self.running == True):
            if(self.claiming_flag == True):
                if (self.sandbox_flag == False):
                    if(self.login_status == True):
                        bot.claim(self.claim_name)
                        
                    else:
                        bot.login()
                        bot.claim(self.claim_name)

                    self.running = False
                    self.login_status = False
                    self.sendEmail(self.claim_name,"CLAIM ATTEMPT")
                    try:
                        self.console.append("Attempting to claim: " + str(self.claim_name))
                        app.processEvents()
                    except:
                        print ("console error")
                    while(1):
                        
                        time.sleep(1)
                    
            else:
                if (int(threading.active_count()) <= self.max_threads and (self.proxyqueue.empty() == False)):
                
                    threadProxy = self.proxyqueue.get()
                    thread = threading.Thread(target=self.ThreadFunction, args=(threadProxy,))
                    thread.start()



app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication

app.setWindowIcon(QIcon("/Claimer2020/icon.png"))
        
window = Ui() # Create an instance of our class
app.exec_() # Start the application
