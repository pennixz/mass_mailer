import smtplib
import re
from tkinter import *
from email.message import EmailMessage

msg = EmailMessage()
sender = ''
pw = ''
smtp_data = ''
smtp_port = 587

recipientList = []

errors = 0
succez = 0


class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid(padx=15, pady=15)

        self.emne = StringVar()
        self.beskjed = StringVar()
        self.email = StringVar()
        self.pw = StringVar()

        self.email_label = Label(self, text="Skriv inn din e-post og ditt passord.")
        self.email_input = Entry(self, textvariable=self.email)
        self.pw_input = Entry(self, textvariable=self.pw, show="*")
        self.info_button = Button(self, text="ok", command=self.checkit, width=5)

        self.email_label.grid(pady=5, padx=5)
        self.email_input.grid(pady=5, ipadx=31)
        self.pw_input.grid(ipadx=31)
        self.info_button.grid(pady=(18, 0))

    def checkit(self):
        global sender
        global pw
        global smtp_data
        global smtp_port
        is_emailerror_hidden = False
        sender = self.email_input.get().lower()
        if re.match(r"[^@]+@[^@]+\.[^@]+", sender):
            gmail_check = re.search("gmail.com", sender)
            pw = self.pw_input.get().rstrip()
            if gmail_check:
                smtp_data = 'smtp.gmail.com'
                is_emailerror_hidden = True
                self.wreckem()
                self.createWidgets()

            outlook_check = re.search("outlook", sender)
            hotmail_check = re.search("hotmail.com", sender)
            live_check = re.search("live.no", sender)
            if outlook_check or hotmail_check or live_check:
                smtp_data = 'smtp-mail.outlook.com'
                self.wreckem()
                self.createWidgets()
                is_emailerror_hidden = True

            online_check = re.search("online.no", sender)
            if online_check:
                smtp_data = 'smtp.online.no'
                smtp_port = 465
                self.wreckem()
                self.createWidgets()
                is_emailerror_hidden = True

            if not gmail_check or hotmail_check or outlook_check or live_check or online_check and is_emailerror_hidden:
                if not hasattr(self, 'unsupported_mail_label'):
                    self.unsupported_mail_label = Label(self,
                                                        text="Programmet støtter ikke din e-post leverandør.")
                    self.unsupported_mail_label.grid()

                    if hasattr(self, 'invalid_email_label'):
                        self.invalid_email_label.destroy()

        else:
            if not hasattr(self, 'invalid_email_label'):
                self.invalid_email_label = Label(self,
                                                 text="Forsikre deg om at du har oppgitt en gyldig e-post adresse")
                self.invalid_email_label.grid()

    def createWidgets(self):
        self.email_label.destroy()
        self.email_input.destroy()
        self.pw_input.destroy()
        self.info_button.destroy()

        try:
            smtp_obj = smtplib.SMTP(smtp_data, smtp_port)
            smtp_obj.ehlo()
            smtp_obj.starttls()
            smtp_obj.login(sender, pw)
            print("Koblet til SMTP server")
            self.instruksLabel = Label(self, text="Fyll inn ønsket emne på epost")
            self.emneKnagg = Entry(self, textvariable=self.emne)
            self.instruksLabelTo = Label(self, text="Fyll så inn ønsket beskjed")
            self.beskjedKnagg = Text(self)
            self.sendButton = Button(self, text="Send e-poster", command=self.send_mail)
            self.quitButton = Button(self, text="Avslutt", command=self.quit)

            self.instruksLabel.grid()
            self.emneKnagg.grid()
            self.instruksLabelTo.grid()
            self.beskjedKnagg.grid()
            self.sendButton.grid()
            self.quitButton.grid()

        except:
            self.cerror_label = Label(self,
                                      text="Noe gikk galt under tilkobling til mail server, kan være feil passord.\n Avslutt programmet og prøv på nytt.")
            self.cerror_label.grid()

    def wreckem(self):
        self.pw_input.destroy()
        self.info_button.destroy()
        self.email_input.destroy()
        self.email_label.destroy()
        if hasattr(self, 'invalid_email_label'):
            self.invalid_email_label.destroy()
        if hasattr(self, 'unsupported_mail_label'):
            self.unsupported_mail_label.destroy()

    def get_email_list(self):
        f = open('mail_list.txt', 'r')
        lines = f.readlines()
        for x in lines:
            recipientList.append(x.rstrip())

    def send_mail(self):
        global succez
        global errors
        try:
            self.get_email_list()
        except:
            print("Noe gikk galt i å lese mail listen. Sjekk at du har mail_list.txt i samme mappe som mailer.exe")

        msg.set_content(self.beskjedKnagg.get('1.0', END))
        msg['Subject'] = self.emne.get()
        msg['From'] = sender

        for x in range(len(recipientList)):
            try:
                smtp_obj.sendmail(sender, recipientList[x], msg.as_string())
                print('E-post sendt til ' + recipientList[x])
                succez += 1
            except:
                print('Noe gikk galt ved sendingen av e-post til ' + recipientList[x])
                errors += 1

        self.statusLabel = Label(self, text=str(succez) + " eposter sendt. " + str(
            errors) + " eposter ikke sendt, sjekk terminalen for å se hvilke.")

        self.statusLabel.grid(pady=10)
        print('Avslutter forbindelse med SMTP server')
        smtp_obj.quit()


app = Application()
app.master.title('Masseutsendelse av E-post')
app.mainloop()
