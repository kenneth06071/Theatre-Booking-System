import pyodbc
from PIL import Image, ImageDraw, ImageFont
from datetime import date
from datetime import datetime
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem
from login import*
from menu import*
from blocking import*
from booking import *
from search import*
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class login (QDialog):
    def __init__ (self):
        super(QDialog , self).__init__()
        self.ui = Ui_Dialog_login()
        self.ui.setupUi(self)
        self.ui.login.clicked.connect(self.login_button)
        self.cs=(
            "Driver={SQL Server};"
            "Server=svr-cmp-01;"
            "Database=21ChungK69;"
            "Trusted_Connection=yes;"
            "UID=COLLYERS\21ChungK69;"
            "PWD=SY219769"
            )
        self.staff_detail=[]
    def start(self):
        try:
            cnxn=pyodbc.connect(self.cs)
            if self.cs is not None:
                cursor = cnxn.cursor()
                statementSQL_login = 'SELECT* FROM login'
                cursor.execute(statementSQL_login)
                self.staff_detail = cursor.fetchall()
        except pyodbc.DatabaseError as err:
            print("Error:{0}".format(error))
            print(err)
        finally:
            cnxn.close()
            print("Connection Closed")

    def login_button (self):
        
        staff_ID = self.ui.staff_ID.text()
        password = self.ui.password.text()
        if (len(staff_ID)>0 and staff_ID.isspace()==False) and (len(password)>0 and password.isspace()==False):
            
            for i in range (len(self.staff_detail)):
                if staff_ID == self.staff_detail[i][0] and password == self.staff_detail[i][1]:
                    c.show()
                    c.start()
                    d.close()
                    break
                        
                else:
                    self.ui.validation.setText('Incorrect Staff_ID or Password')
        else:
            self.ui.validation.setText('Please enter all data')
            
                        

            



class menu(QDialog):
    def __init__ (self):
        super(QDialog , self).__init__()
        self.ui = Ui_Dialog_menu()
        self.ui.setupUi(self)
        self.ui.combobox_day.currentIndexChanged.connect(self.change_date)
        self.ui.booking_system.clicked.connect(self.booking)
        self.ui.search_engine.clicked.connect(self.search)
        self.ui.block.clicked.connect(self.block)
        self.booked_day1=[]
        self.booked_day2=[]
        self.booked_day3=[]
        self.blocked_day1=[]
        self.blocked_day2=[]
        self.blocked_day3=[]
        
        
        for day in range(1,4):
            for z in range(2):
                y=90+(180*z)
                for j in range (2):
                    x=30+(340*j)
                    for k in range(65,70):
                        for i in range(1,11):
                            exec("self.label{0}{1}_{2} = QtWidgets.QLabel(self.ui.page{2})".format((chr(k+(5*z))),((i)+(10*j)),day))
                            exec("self.label{0}{1}_{4}.setGeometry(QtCore.QRect({2},{3},31,31))".format((chr(k+(5*z))),((i)+(10*j)),(x+(30*(i-1))),(y+(30*(k-65))),(day)))
                            exec("""self.label{0}{1}_{2}.setStyleSheet('image: url(:/empty/available.png)')""".format((chr(k+(5*z))),((i)+(10*j)),(day)))
                            exec("self.label{0}{1}_{2}.setText('')".format((chr(k+(5*z))),((i)+(10*j)),(day)))
                            exec("self.label{0}{1}_{2}.setObjectName('checkBox{0}{1}')".format((chr(k+(5*z))),((i)+(10*j)),(day)))
        self.statementSQL_booked = "SELECT seat.[Row],seat.[Column],booking.[Day] FROM ticket\
                                    INNER JOIN seat ON ticket.seat_ID = seat.seat_ID\
                                    INNER JOIN booking ON ticket.Booking_ID = booking.Booking_ID\
                                    LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
                                    WHERE ticket.[type]='Standard' OR ticket.[type]='Reduced'"
        
        self.statementSQL_blocked = "SELECT seat.[Row],seat.[Column],booking.[Day] FROM ticket\
                                     INNER JOIN seat ON ticket.seat_ID = seat.seat_ID\
                                     INNER JOIN booking ON ticket.Booking_ID = booking.Booking_ID\
                                     LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
                                     WHERE ticket.[type]='Blocked'"

        self.statementSQL_day1_count = "SELECT COUNT(*) FROM ticket\
                                        INNER JOIN seat ON ticket.seat_ID = seat.seat_ID\
                                        INNER JOIN booking ON ticket.Booking_ID = booking.Booking_ID\
                                        LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
                                        WHERE booking.[Day]=1"
        self.statementSQL_day2_count = "SELECT COUNT(*) FROM ticket\
                                   INNER JOIN seat ON ticket.seat_ID = seat.seat_ID\
                                   INNER JOIN booking ON ticket.Booking_ID = booking.Booking_ID\
                                   LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
                                   WHERE booking.[Day]=2"
        self.statementSQL_day3_count = "SELECT COUNT(*) FROM ticket\
                                   INNER JOIN seat ON ticket.seat_ID = seat.seat_ID\
                                   INNER JOIN booking ON ticket.Booking_ID = booking.Booking_ID\
                                   LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
                                   WHERE booking.[Day]=3"
        
        self.statementSQL_day1_reduced = "SELECT COUNT(*) FROM ticket\
                                    INNER JOIN seat ON ticket.seat_ID = seat.seat_ID\
                                    INNER JOIN booking ON ticket.Booking_ID = booking.Booking_ID\
                                    LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
                                    WHERE booking.[Day]=1 AND ticket.[Type]='Reduced'"
        self.statementSQL_day2_reduced = "SELECT COUNT(*) FROM ticket\
                                    INNER JOIN seat ON ticket.seat_ID = seat.seat_ID\
                                    INNER JOIN booking ON ticket.Booking_ID = booking.Booking_ID\
                                    LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
                                    WHERE booking.[Day]=2 AND ticket.[Type]='Reduced'"
        self.statementSQL_day3_reduced = "SELECT COUNT(*) FROM ticket\
                                    INNER JOIN seat ON ticket.seat_ID = seat.seat_ID\
                                    INNER JOIN booking ON ticket.Booking_ID = booking.Booking_ID\
                                    LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
                                    WHERE booking.[Day]=3 AND ticket.[Type]='Reduced'"
        self.statementSQL_day1_standard = "SELECT COUNT(*) FROM ticket\
                                    INNER JOIN seat ON ticket.seat_ID = seat.seat_ID\
                                    INNER JOIN booking ON ticket.Booking_ID = booking.Booking_ID\
                                    LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
                                    WHERE booking.[Day]=1 AND ticket.[Type]='Standard'"
        self.statementSQL_day2_standard = "SELECT COUNT(*) FROM ticket\
                                    INNER JOIN seat ON ticket.seat_ID = seat.seat_ID\
                                    INNER JOIN booking ON ticket.Booking_ID = booking.Booking_ID\
                                    LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
                                    WHERE booking.[Day]=2 AND ticket.[Type]='Standard'"
        self.statementSQL_day3_standard = "SELECT COUNT(*) FROM ticket\
                                    INNER JOIN seat ON ticket.seat_ID = seat.seat_ID\
                                    INNER JOIN booking ON ticket.Booking_ID = booking.Booking_ID\
                                    LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
                                    WHERE booking.[Day]=3 AND ticket.[Type]='Standard'"
        self.statementSQL_day1_sold = "SELECT COUNT(*) FROM ticket\
                                   INNER JOIN seat ON ticket.seat_ID = seat.seat_ID\
                                   INNER JOIN booking ON ticket.Booking_ID = booking.Booking_ID\
                                   LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
                                   WHERE booking.[Day]=1 AND (ticket.[Type]='Standard' OR ticket.[Type]='Reduced')"
        self.statementSQL_day2_sold = "SELECT COUNT(*) FROM ticket\
                                   INNER JOIN seat ON ticket.seat_ID = seat.seat_ID\
                                   INNER JOIN booking ON ticket.Booking_ID = booking.Booking_ID\
                                   LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
                                   WHERE booking.[Day]=2 AND (ticket.[Type]='Standard' OR ticket.[Type]='Reduced')"
        self.statementSQL_day3_sold = "SELECT COUNT(*) FROM ticket\
                                       INNER JOIN seat ON ticket.seat_ID = seat.seat_ID\
                                       INNER JOIN booking ON ticket.Booking_ID = booking.Booking_ID\
                                       LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
                                       WHERE booking.[Day]=3 AND (ticket.[Type]='Standard'OR ticket.[Type]='Reduced')"
        self.cs=(
            "Driver={SQL Server};"
            "Server=svr-cmp-01;"
            "Database=21ChungK69;"
            "Trusted_Connection=yes;"
            "UID=COLLYERS\21ChungK69;"
            "PWD=SY219769"
            )
    def start(self):                         
        try:
            
            cnxn=pyodbc.connect(self.cs)
            if self.cs is not None:
                cursor = cnxn.cursor()
                cursor.execute(self.statementSQL_booked)
                booked_seats = cursor.fetchall()
                cursor.execute(self.statementSQL_blocked)
                blocked_seats = cursor.fetchall()
                cursor.execute(self.statementSQL_day1_count)
                day1_unavailable=cursor.fetchone()
                cursor.execute(self.statementSQL_day2_count)
                day2_unavailable=cursor.fetchone()
                cursor.execute(self.statementSQL_day3_count)
                day3_unavailable=cursor.fetchone()

                cursor.execute(self.statementSQL_day1_sold)
                day1_sold=cursor.fetchone()
                cursor.execute(self.statementSQL_day2_sold)
                day2_sold=cursor.fetchone()
                cursor.execute(self.statementSQL_day3_sold)
                day3_sold=cursor.fetchone()

                
                cursor.execute(self.statementSQL_day1_reduced)
                day1_reduced = cursor.fetchone()
                cursor.execute(self.statementSQL_day2_reduced)
                day2_reduced = cursor.fetchone()
                cursor.execute(self.statementSQL_day3_reduced)
                day3_reduced = cursor.fetchone()
                cursor.execute(self.statementSQL_day1_standard)
                day1_standard = cursor.fetchone()
                cursor.execute(self.statementSQL_day2_standard)
                day2_standard = cursor.fetchone()
                cursor.execute(self.statementSQL_day3_standard)
                day3_standard = cursor.fetchone()
        


                for i in range (len(booked_seats)):
                    exec("""self.label{0}{1}_{2}.setStyleSheet('image: url(:/booked/booked.png)')""".format((booked_seats[i][0]),(booked_seats[i][1]),(booked_seats[i][2])))
                    exec("self.booked_day{0}.append(('{1}',{2}))".format(((booked_seats[i][2])),(booked_seats[i][0]),(booked_seats[i][1])))
                   

                for i in range (len(blocked_seats)):
                    exec("""self.label{0}{1}_{2}.setStyleSheet('image: url(:/blocked/blocked.png)')""".format((blocked_seats[i][0]),(blocked_seats[i][1]),(blocked_seats[i][2])))
                    exec("self.blocked_day{0}.append(('{1}',{2}))".format(((blocked_seats[i][2])),(blocked_seats[i][0]),(blocked_seats[i][1])))
                    print((blocked_seats[i][2]))
                print(self.blocked_day1)
                #Day1
                self.ui.sold_day1.setText(str(day1_sold[0]))
                self.ui.available_day1.setText(str(200-day1_unavailable[0]))
                self.ui.revenue_day1.setText('£'+str((day1_reduced[0]*5)+(day1_standard[0]*10)))
                #Day2
                self.ui.sold_day2.setText(str(day2_sold[0]))
                self.ui.available_day2.setText(str(200-day2_unavailable[0]))
                self.ui.revenue_day2.setText('£'+str((day2_reduced[0]*5)+(day2_standard[0]*10)))
                #Day3
                self.ui.sold_day3.setText(str(day3_sold[0]))
                self.ui.available_day3.setText(str(200-day3_unavailable[0]))
                self.ui.revenue_day3.setText('£'+str((day3_reduced[0]*5)+(day3_standard[0]*10)))
                    
                    
   
        
    
                         
        except pyodbc.DatabaseError as err:
            print("Error:{0}".format(error))
            print(err)
        finally:
            cnxn.close()
            print("Connection Closed")
                
    def change_date(self):
        day=(self.ui.combobox_day.currentIndex()+1)
        exec("self.ui.stackedWidget.setCurrentWidget(self.ui.page{0})".format(day))
    def booking(self):
        b.close()
        a.close()
        w.standard=''
        w.reduced= ''
        w.first=''
        w.last=''
        w.total=''
        w.phone=''
        w.day = ''
        w.ui.lineEdit_first.clear()
        w.ui.lineEdit_last.clear()
        w.ui.stackedWidget.setCurrentIndex(0)
        w.ui.lineEdit_phone.clear()
        w.ui.spinBox_standard.setValue(0)
        w.ui.spinBox_reduced.setValue(0)
        w.ui.day.setCurrentIndex(0)
        w.show()
        
    def search(self):
        w.close()
        b.close()
        a.ui.stackedWidget.setCurrentIndex(0)
        a.show()
    def block (self):
        w.close()
        a.close()
        b.show()
        b.start()
    
    def update (self,day):
        booked_day=[]
        exec("booked_day=self.booked_day{0}".format(day))
        for i in range(len(booked_day)):
            exec("""self.label{0}{1}_{2}.setStyleSheet('image: url(:/empty/available.png)')""".format((booked_day[i][0]),(booked_day[i][1]),(booked_day[i][2])))
        blocked_day=[]
        exec("blocked_day=self.blocked_day{0}".format(day))
        for i in range(len(blocked_day)):
            exec("""self.label{0}{1}_{2}.setStyleSheet('image: url(:/empty/available.png)')""".format((blocked_day[i][0]),(blocked_day[i][1]),(blocked_day[i][2])))      
            

        try:
            
            cnxn=pyodbc.connect(self.cs)
            if self.cs is not None:
                cursor = cnxn.cursor()
                cursor.execute(self.statementSQL_booked)
                booked_seats = cursor.fetchall()
                cursor.execute(self.statementSQL_blocked)
                blocked_seats = cursor.fetchall()
                
                exec("cursor.execute(self.statementSQL_day{0}_count)".format(day))
                unavailable=cursor.fetchone()

                exec("cursor.execute(self.statementSQL_day{0}_sold)".format(day))
                sold=cursor.fetchone()

                
                exec("cursor.execute(self.statementSQL_day{0}_reduced)".format(day))
                reduced = cursor.fetchone()
                

                exec("cursor.execute(self.statementSQL_day{0}_standard)".format(day))
                standard = cursor.fetchone()

                for i in range (len(booked_seats)):
                    exec("""self.label{0}{1}_{2}.setStyleSheet('image: url(:/booked/booked.png)')""".format((booked_seats[i][0]),(booked_seats[i][1]),(booked_seats[i][2])))
                

                for i in range (len(blocked_seats)):
                    exec("""self.label{0}{1}_{2}.setStyleSheet('image: url(:/blocked/blocked.png)')""".format((blocked_seats[i][0]),(blocked_seats[i][1]),(blocked_seats[i][2])))

                
                exec("self.ui.sold_day{0}.setText(str(sold[0]))".format(day))
                exec("self.ui.available_day{0}.setText(str(200-unavailable[0]))".format(day))
                exec("self.ui.revenue_day{0}.setText('£'+str((reduced[0]*5)+(standard[0]*10)))".format(day))
                print('fuck')
        except pyodbc.DatabaseError as err:
            print("Error:{0}".format(error))
            print(err)
        finally:
            cnxn.close()
            print("Connection Closed")
        
        
        
        
        
        
        
        
        

class block(QDialog):
    def __init__ (self):
        super(QDialog , self).__init__()
        self.ui = Ui_Blocking()
        self.ui.setupUi(self)
        self.ui.day_block.currentIndexChanged.connect(self.change_date)
        self.ui.block_unblock.clicked.connect(self.block_unblock)
        for z in range(2):
            y=60+(180*z)
            for j in range (2):
                x=50+(340*j)
                for k in range(65,70):
                    for i in range(1,11):
                        exec("self.checkBox{0}{1} = QtWidgets.QCheckBox(self.ui.page_2)".format((chr(k+(5*z))),((i)+(10*j))))
                        exec("self.checkBox{0}{1}.setGeometry(QtCore.QRect({2},{3},31,31))".format((chr(k+(5*z))),((i)+(10*j)),(x+(30*(i-1))),(y+(30*(k-65)))))
                        exec("""self.checkBox{0}{1}.setStyleSheet('QCheckBox::indicator:unchecked {{image: url(:/empty/available.png)}}\\n'
'QCheckBox::indicator:checked {{image: url(:/search/search.png)}}')""".format((chr(k+(5*z))),((i)+(10*j))))
                        exec("self.checkBox{0}{1}.setInputMethodHints(QtCore.Qt.ImhNone)".format((chr(k+(5*z))),((i)+(10*j))))
                        exec("self.checkBox{0}{1}.clicked.connect(lambda:b.selected_block('{0}',{1}))".format((chr(k+(5*z))),((i)+(10*j))))
                        exec("self.checkBox{0}{1}.setText('')".format((chr(k+(5*z))),((i)+(10*j))))
                        exec("self.checkBox{0}{1}.setIconSize(QtCore.QSize(20,20))".format((chr(k+(5*z))),((i)+(10*j))))
                        exec("self.checkBox{0}{1}.setCheckable(True)".format((chr(k+(5*z))),((i)+(10*j))))
                        exec("self.checkBox{0}{1}.setChecked(False)".format((chr(k+(5*z))),((i)+(10*j))))
                        exec("self.checkBox{0}{1}.setTristate(False)".format((chr(k+(5*z))),((i)+(10*j))))
                        exec("self.checkBox{0}{1}.setObjectName('checkBox{0}{1}')".format((chr(k+(5*z))),((i)+(10*j))))
        self.unblock=False
        self.blocked_seats=[]
        self.selected=[]
        self.booked_seats=[]
        self.cs=(
            "Driver={SQL Server};"
            "Server=svr-cmp-01;"
            "Database=21ChungK69;"
            "Trusted_Connection=yes;"
            "UID=COLLYERS\21ChungK69;"
            "PWD=SY219769"
            )
    def start (self):
        day= (self.ui.day_block.currentIndex()+1)
        self.selected=[]
        statementSQL_booked = "SELECT seat.[Row],seat.[Column] FROM ticket\
        INNER JOIN seat ON ticket.seat_ID = seat.seat_ID\
        INNER JOIN booking ON ticket.Booking_ID = booking.Booking_ID\
        LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
        WHERE booking.Day={0} AND (ticket.[type]='Standard' OR ticket.[type]='Reduced')".format(day)
        
        statementSQL_blocked = "SELECT seat.[Row],seat.[Column] FROM ticket\
        INNER JOIN seat ON ticket.seat_ID = seat.seat_ID\
        INNER JOIN booking ON ticket.Booking_ID = booking.Booking_ID\
        LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
        WHERE booking.Day={0} AND ticket.[type]='Blocked'".format(day)
                                
        try:
            
            cnxn=pyodbc.connect(self.cs)
            if self.cs is not None:
                
                cursor = cnxn.cursor()
                cursor.execute(statementSQL_booked)
                self.booked_seats = cursor.fetchall()
                cursor.execute(statementSQL_blocked)
                self.blocked_seats = cursor.fetchall()
                
            for i in range (len(self.blocked_seats)):
                exec("""self.checkBox{0}{1}.setStyleSheet('QCheckBox::indicator:unchecked {{image: url(:/blocked/blocked.png)}}\\n'
'QCheckBox::indicator:checked {{image: url(:/search/search.png)}}')""".format((self.blocked_seats[i][0]),(self.blocked_seats[i][1])))
                exec("self.checkBox{0}{1}.setChecked(False)".format((self.blocked_seats[i][0]),(self.blocked_seats[i][1])))
                

            for i in range (len(self.booked_seats)):
                    exec("""self.checkBox{0}{1}.setStyleSheet('QCheckBox::indicator:disabled {{image: url(:/booked/booked.png)}}\\n'
)""".format((self.booked_seats[i][0]),(self.booked_seats[i][1])))
                    exec("self.checkBox{0}{1}.setEnabled(False)".format((self.booked_seats[i][0]),(self.booked_seats[i][1])))
        except pyodbc.DatabaseError as err:
            print("Error:{0}".format(error))
            print(err)
        finally:
            cnxn.close()
            print("Connection Closed")
        
    def selected_block (self,row,column):
        x= eval("self.checkBox{0}{1}.isChecked()".format((row),(column)))
        
        if x== True:
            self.selected.append((row,column))
            print('blocked',self.blocked_seats)
            if len(self.selected)>1:
                exec("self.checkBox{0}{1}.setChecked(False)".format((self.selected[0][0]),(self.selected[0][1])))
                self.selected.pop(0)
                
            for i in range(len(self.blocked_seats)):
                if row== str(self.blocked_seats[i][0]) and column== self.blocked_seats[i][1]:
                    print('true:',row,column)
                    self.unblock=True
                    break
                else:
                    print(str(self.blocked_seats[i][0]),str(self.blocked_seats[i][1]))
                    self.unblock=False
                    
            if self.unblock==True:
                self.ui.block_unblock.setText('UNBLOCK')
            else:
                self.ui.block_unblock.setText('BLOCK')

        else:
            self.selected.remove((row,column))
        print(self.unblock)
    def change_date (self):
        for i in range (len(self.blocked_seats)):
            exec("""self.checkBox{0}{1}.setStyleSheet('QCheckBox::indicator:unchecked {{image: url(:/empty/available.png)}}\\n'
'QCheckBox::indicator:checked {{image: url(:/search/search.png)}}')""".format((self.blocked_seats[i][0]),(self.blocked_seats[i][1])))
            exec("self.checkBox{0}{1}.setChecked(False)".format((self.blocked_seats[i][0]),(self.blocked_seats[i][1])))
        
        for i in range (len(self.selected)):
            exec("self.checkBox{0}{1}.setChecked(False)".format((self.blocked_seats[i][0]),(self.blocked_seats[i][1])))
        for i in range (len(self.booked_seats)):
            print(self.booked_seats[i][0])
            exec("""self.checkBox{0}{1}.setStyleSheet('QCheckBox::indicator:unchecked {{image: url(:/empty/available.png)}}\\n'
'QCheckBox::indicator:checked {{image: url(:/search/search.png)}}')""".format((self.booked_seats[i][0]),(self.booked_seats[i][1])))
            exec("self.checkBox{0}{1}.setChecked(False)".format((self.booked_seats[i][0]),(self.booked_seats[i][1])))
            exec("self.checkBox{0}{1}.setEnabled(True)".format((self.booked_seats[i][0]),(self.booked_seats[i][1])))

        day= (self.ui.day_block.currentIndex()+1)
        self.selected=[]
        statementSQL_booked = "SELECT seat.[Row],seat.[Column] FROM ticket\
        INNER JOIN seat ON ticket.seat_ID = seat.seat_ID\
        INNER JOIN booking ON ticket.Booking_ID = booking.Booking_ID\
        LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
        WHERE booking.Day={0} AND (ticket.[type]='Standard' OR ticket.[type]='Reduced')".format(day)
        
        statementSQL_blocked = "SELECT seat.[Row],seat.[Column] FROM ticket\
        INNER JOIN seat ON ticket.seat_ID = seat.seat_ID\
        INNER JOIN booking ON ticket.Booking_ID = booking.Booking_ID\
        LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
        WHERE booking.Day={0} AND ticket.[type]='Blocked'".format(day)
                                
        try:
            
            cnxn=pyodbc.connect(self.cs)
            if self.cs is not None:
                
                cursor = cnxn.cursor()
                cursor.execute(statementSQL_booked)
                self.booked_seats = cursor.fetchall()
                cursor.execute(statementSQL_blocked)
                self.blocked_seats = cursor.fetchall()
                print('after',self.booked_seats)
                
                for i in range (len(self.blocked_seats)):
                    exec("""self.checkBox{0}{1}.setStyleSheet('QCheckBox::indicator:unchecked {{image: url(:/blocked/blocked.png)}}\\n'
'QCheckBox::indicator:checked {{image: url(:/search/search.png)}}')""".format((self.blocked_seats[i][0]),(self.blocked_seats[i][1])))
                    exec("self.checkBox{0}{1}.setChecked(False)".format((self.blocked_seats[i][0]),(self.blocked_seats[i][1])))
                

                for i in range (len(self.booked_seats)):
                    exec("""self.checkBox{0}{1}.setStyleSheet('QCheckBox::indicator:disabled {{image: url(:/booked/booked.png)}}\\n'
)""".format((self.booked_seats[i][0]),(self.booked_seats[i][1])))
                    exec("self.checkBox{0}{1}.setEnabled(False)".format((self.booked_seats[i][0]),(self.booked_seats[i][1])))
        except pyodbc.DatabaseError as err:
            print("Error:{0}".format(error))
            print(err)
        finally:
            cnxn.close()
            print("Connection Closed")
        self.selected=[]
        
    def block_unblock (self):
        day= (self.ui.day_block.currentIndex()+1) 
        try:
            
            cnxn=pyodbc.connect(self.cs)
            if self.cs is not None:
                cursor = cnxn.cursor()
                if len(self.selected)>0:
                    if self.unblock==True:
                

        
                        day=(self.ui.day_block.currentIndex()+1)
                        statementSQL_booking_ID ="SELECT booking.Booking_ID FROM ticket\
                                                  INNER JOIN seat ON ticket.seat_ID = seat.seat_ID\
                                                  INNER JOIN booking ON ticket.Booking_ID = booking.Booking_ID\
                                                  WHERE ticket.seat_ID = '{0}' AND booking.Day = {1}".format((str(self.selected[0][0])+str(self.selected[0][1])),(day))
                        cursor.execute(statementSQL_booking_ID)
                        booking_ID = cursor.fetchone()
                        booking_ID = booking_ID[0]
                        print (booking_ID)
                        statementSQL_unblock_ticket = "DELETE ticket\
                                                       FROM ticket\
                                                       WHERE Booking_ID={0}".format(booking_ID)
                        cursor.execute(statementSQL_unblock_ticket)
                    

                        statementSQL_unblock_booking =   "DELETE booking\
                                                          FROM booking\
                                                          WHERE Booking_ID={0}".format(booking_ID)
                        cursor.execute(statementSQL_unblock_booking)
                        exec("""self.checkBox{0}{1}.setStyleSheet('QCheckBox::indicator:unchecked {{image: url(:/empty/available.png)}}\\n'
'QCheckBox::indicator:checked {{image: url(:/search/search.png)}}')""".format((self.selected[0][0]),(self.selected[0][1])))
                        exec("self.checkBox{0}{1}.setChecked(False)".format((self.selected[0][0]),(self.selected[0][1])))
                        
                        for i in range(len(self.blocked_seats)):
                            if self.selected[0][0]== str(self.blocked_seats[i][0]) and self.selected[0][1]== self.blocked_seats[i][1]:
                                print('remove',self.blocked_seats[i][0],self.blocked_seats[i][1])
                                self.blocked_seats.pop(i)
                        
                                break
                            else:
                                pass

                    
                    
                    
        
                    else:
                        #booking
                        statementSQL_last_booking= 'SELECT TOP 1 Booking_ID FROM Booking ORDER BY Booking_ID  DESC'
                        cursor.execute(statementSQL_last_booking)
                        last_Booking_ID = cursor.fetchone()
                        new_Booking_ID = last_Booking_ID[0]+1
                        statementSQL_block = "INSERT INTO Booking (Booking_ID,Day) VALUES ({0},{1})".format((new_Booking_ID),(day))
                        cursor.execute(statementSQL_block)

                        #ticket
                        statementSQL_ticket= "INSERT INTO ticket (Booking_ID,seat_ID,type) VALUES ({0},'{1}','Blocked')".format((new_Booking_ID),(str(self.selected[0][0])+str(self.selected[0][1])))
                        cursor.execute(statementSQL_ticket)
                        exec("""self.checkBox{0}{1}.setStyleSheet('QCheckBox::indicator:unchecked {{image: url(:/blocked/blocked.png)}}\\n'
'QCheckBox::indicator:checked {{image: url(:/search/search.png)}}')""".format((self.selected[0][0]),(self.selected[0][1])))
                        exec("self.checkBox{0}{1}.setChecked(False)".format((self.selected[0][0]),(self.selected[0][1])))
                        self.blocked_seats.append(self.selected[0])
                    self.selected=[]
                    cnxn.commit()
                    c.update(day)
                else:
                    pass
                
        except pyodbc.DatabaseError as err:
                print("Error:{0}".format(error))
                print(err)
        finally:
            cnxn.close()
            print("Connection Closed")
            
        
                                    

        
        
        

        

class booking(QDialog):
    def __init__ (self):
        super(QDialog , self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.Confirm.clicked.connect(self.confirm)
        self.ui.Book.clicked.connect(self.book)
        self.ui.ticket.clicked.connect(self.print)
        self.ui.new_booking.clicked.connect(self.new)
        self.ui.home.clicked.connect(self.close)
        self.ui.undo.clicked.connect(self.undo)
        self.standard=''
        self.reduced= ''
        self.first=''
        self.last=''
        self.total=''
        self.phone=''
        self.day = ''
        self.selected =[]
        self.booked_seats=[]
        self.blocked_seats=[]
        for z in range(2):
                y=160+(180*z)
                for j in range (2):
                    x=90+(340*j)
                    for k in range(65,70):
                        for i in range(1,11):
                            exec("self.checkBox{0}{1} = QtWidgets.QCheckBox(self.ui.page_2)".format((chr(k+(5*z))),((i)+(10*j))))
                            exec("self.checkBox{0}{1}.setGeometry(QtCore.QRect({2},{3},31,31))".format((chr(k+(5*z))),((i)+(10*j)),(x+(30*(i-1))),(y+(30*(k-65)))))
                            exec("""self.checkBox{0}{1}.setStyleSheet('QCheckBox::indicator:unchecked {{image: url(:/empty/available.png)}}\\n'
'QCheckBox::indicator:checked {{image: url(:/chosen/chosen.png)}}')""".format((chr(k+(5*z))),((i)+(10*j))))
                            exec("self.checkBox{0}{1}.setInputMethodHints(QtCore.Qt.ImhNone)".format((chr(k+(5*z))),((i)+(10*j))))
                            exec("self.checkBox{0}{1}.clicked.connect(lambda:w.check('{0}','{1}'))".format((chr(k+(5*z))),((i)+(10*j))))
                            exec("self.checkBox{0}{1}.setText('')".format((chr(k+(5*z))),((i)+(10*j))))
                            exec("self.checkBox{0}{1}.setIconSize(QtCore.QSize(20,20))".format((chr(k+(5*z))),((i)+(10*j))))
                            exec("self.checkBox{0}{1}.setCheckable(True)".format((chr(k+(5*z))),((i)+(10*j))))
                            exec("self.checkBox{0}{1}.setChecked(False)".format((chr(k+(5*z))),((i)+(10*j))))
                            exec("self.checkBox{0}{1}.setTristate(False)".format((chr(k+(5*z))),((i)+(10*j))))
                            exec("self.checkBox{0}{1}.setObjectName('checkBox{0}{1}')".format((chr(k+(5*z))),((i)+(10*j))))
        self.cs=(
            "Driver={SQL Server};"
            "Server=svr-cmp-01;"
            "Database=21ChungK69;"
            "Trusted_Connection=yes;"
            "UID=COLLYERS\21ChungK69;"
            "PWD=SY219769"
            )
    def undo (self):
        self.standard=''
        self.reduced= ''
        self.first=''
        self.last=''
        self.total=''
        self.phone=''
        self.day = ''
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)
        

    def new (self):
        self.standard=''
        self.reduced= ''
        self.first=''
        self.last=''
        self.total=''
        self.phone=''
        self.day = ''
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)
        self.ui.lineEdit_first.clear()
        self.ui.lineEdit_last.clear()
        self.ui.lineEdit_phone.clear()
        self.ui.spinBox_standard.setValue(0)
        self.ui.spinBox_reduced.setValue(0)
        self.ui.day.setCurrentIndex(0)
        
        

    def print(self):
        standard=self.standard
        font70 = ImageFont.truetype("static\OpenSans\OpenSans-Bold.ttf",size=70)
        font30 = ImageFont.truetype("static\OpenSans\OpenSans-Bold.ttf",size=30)
        for i in range (len(self.selected)):
            ticket=Image.open("ticket.jpg")
            draw = ImageDraw.Draw(ticket)
            draw.text((63,190),self.selected[i][0],font=font70, fill='black')
            draw.text((244,190),self.selected[i][1],font=font70, fill='black')
            draw.text((212,347),("DAY"+" "+str(self.day)),font=font30, fill='black')
            if standard>0:
                draw.text((510,190),'Standard',font=font70, fill='black')
                draw.text((61,347),("£10.00"),font=font30, fill='black')
                standard-=1
            else:
                draw.text((510,190),'Reduced',font=font70, fill='black')
                draw.text((61,347),'£5.00',font=font30, fill='black')
            ticket.show()
            
        
    def check(self,row,column):
        x= eval("self.checkBox{0}{1}.isChecked()".format((row),(column)))
        print ('x is ',x)
        if x== True:
            self.selected.append([row,column])
            if len(self.selected)>(self.standard+self.reduced):
                exec("self.checkBox{0}{1}.setChecked(False)".format((self.selected[0][0]),(self.selected[0][1])))
                self.selected.pop(0)
            else:
                pass
                     
        else:
            self.selected.remove([row,column])
        print(self.selected)

    def confirm (self):     
        self.standard= self.ui.spinBox_standard.value()
        self.reduced= self.ui.spinBox_reduced.value()
        self.first=self.ui.lineEdit_first.text()
        self.last=self.ui.lineEdit_last.text()
        self.total=(10*self.standard)+(5*self.reduced)
        self.phone=self.ui.lineEdit_phone.text()
        self.day = (self.ui.day.currentIndex()+1)
        print(self.day)
        if len(self.first)==0 or self.first.isspace() or len(self.last)==0 or self.last.isspace() or len(self.phone)==0 or self.phone.isspace() :
            self.ui.label_validation_check.setText('Please enter all the data')
        elif len(self.phone)!= 10 and len(self.phone)!=11 :
            self.ui.label_validation_check.setText('Phone number must be 10 digits')
        elif (self.standard+ self.reduced)==0:
            self.ui.label_validation_check.setText('Please choose your tickets')
        else:
            for i in range (len(self.booked_seats)):
                print(self.booked_seats[i][0])
                exec("""self.checkBox{0}{1}.setStyleSheet('QCheckBox::indicator:unchecked {{image: url(:/empty/available.png)}}\\n'
'QCheckBox::indicator:checked {{image: url(:/chosen/chosen.png)}}')""".format((self.booked_seats[i][0]),(self.booked_seats[i][1])))
                exec("self.checkBox{0}{1}.setEnabled(True)".format((self.booked_seats[i][0]),(self.booked_seats[i][1])))
                exec("self.checkBox{0}{1}.setChecked(False)".format((self.booked_seats[i][0]),(self.booked_seats[i][1])))
            
            for i in range (len(self.blocked_seats)):
                exec("""self.checkBox{0}{1}.setStyleSheet('QCheckBox::indicator:unchecked {{image: url(:/empty/available.png)}}\\n'
'QCheckBox::indicator:checked {{image: url(:/chosen/chosen.png)}}')""".format((self.blocked_seats[i][0]),(self.blocked_seats[i][1])))
                exec("self.checkBox{0}{1}.setEnabled(True)".format((self.blocked_seats[i][0]),(self.booked_seats[i][1])))
                exec("self.checkBox{0}{1}.setChecked(False)".format((self.blocked_seats[i][0]),(self.blocked_seats[i][1])))
            for i in range (len(self.selected)):
                exec("self.checkBox{0}{1}.setChecked(False)".format((self.selected[i][0]),(self.selected[i][1])))
            self.selected =[]
            
            statementSQL_booked = "SELECT seat.[Row],seat.[Column] FROM ticket\
                                   INNER JOIN seat ON ticket.seat_ID = seat.seat_ID\
                                   INNER JOIN booking ON ticket.Booking_ID = booking.Booking_ID\
                                   LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
                                   WHERE booking.Day={0} AND (ticket.[type]='Standard' OR ticket.[type]='Reduced')".format(self.day)
            statementSQL_blocked = "SELECT seat.[Row],seat.[Column] FROM ticket\
                                   INNER JOIN seat ON ticket.seat_ID = seat.seat_ID\
                                   INNER JOIN booking ON ticket.Booking_ID = booking.Booking_ID\
                                   LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
                                   WHERE booking.Day={0} AND ticket.[type]='Blocked'".format(self.day)
                        
            try:
            
                cnxn=pyodbc.connect(self.cs)
                if self.cs is not None:
                
                    cursor = cnxn.cursor()
                    cursor.execute(statementSQL_booked)
                    self.booked_seats = cursor.fetchall()
                    cursor.execute(statementSQL_blocked)
                    self.blocked_seats = cursor.fetchall()

                    for i in range (len(self.booked_seats)):
                        exec("""self.checkBox{0}{1}.setStyleSheet('QCheckBox::indicator:disabled{{image: url(:/booked/booked.png)}}')""".format((self.booked_seats[i][0]),(self.booked_seats[i][1])))
                        exec("self.checkBox{0}{1}.setEnabled(False)".format((self.booked_seats[i][0]),(self.booked_seats[i][1])))
                    for i in range (len(self.blocked_seats)):
                        exec("""self.checkBox{0}{1}.setStyleSheet('QCheckBox::indicator:disabled{{image: url(:/blocked/blocked.png)}}')""".format((self.blocked_seats[i][0]),(self.blocked_seats[i][1])))
                        exec("self.checkBox{0}{1}.setEnabled(False)".format((self.blocked_seats[i][0]),(self.blocked_seats[i][1])))

            except pyodbc.DatabaseError as err:
                print("Error:{}".format(error))
                print(err)
            finally:
                cnxn.close()
                print("Connection Closed")
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)
    def book (self):
        standard=self.standard
        
        try:
            cnxn=pyodbc.connect(self.cs)
            
            if self.cs is not None:
                if len(self.selected)==0:
                    self.ui.label_validation.setText('Please pick your seat')
                elif len(self.selected)!=(self.standard+self.reduced):
                    self.ui.label_validation.setText('Please pick '+str(self.standard+self.reduced)+' seats')
                else:
                    cursor = cnxn.cursor()
                    #customer
                    statementSQL_last_customer= 'SELECT TOP 1 Cust_ID FROM customer ORDER BY Cust_ID  DESC'
                    cursor.execute(statementSQL_last_customer)
                    last_cust_ID = cursor.fetchone()
                    new_cust_ID = last_cust_ID[0]+1
                    statementSQL_customer = "INSERT INTO [customer] (Cust_ID,First_name,Last_name,Phone_num) VALUES({0},'{1}','{2}','{3}')".format((new_cust_ID),(self.first),(self.last),(self.phone))
                    cursor.execute(statementSQL_customer)
                    #booking
                    today = date.today()
                    current_date= today.strftime("%d/%m/%Y")
                    now = datetime.now()
                    time = now.strftime("%H:%M:%S")
                    statementSQL_last_booking= 'SELECT TOP 1 Booking_ID FROM Booking ORDER BY Booking_ID  DESC'
                    cursor.execute(statementSQL_last_booking)
                    last_Booking_ID = cursor.fetchone()
                    new_Booking_ID = last_Booking_ID[0]+1
                    statementSQL_booking = "INSERT INTO Booking (Booking_ID,Cust_ID,Day,Total_Cost,Date,Time) VALUES ({0},{1},{2},{3},'{4}','{5}')".format((new_Booking_ID),(new_cust_ID),(self.day),(self.total),str(current_date),str(time))
                    cursor.execute(statementSQL_booking)

        
                    
                    
                    

                    for i in range (len(self.selected)):

                        #ticket
                        if standard>0:
                            statementSQL_ticket= "INSERT INTO ticket (Booking_ID,seat_ID,type) VALUES ({0},'{1}','Standard')".format((new_Booking_ID),(str(self.selected[i][0])+str(self.selected[i][1])))
                            cursor.execute(statementSQL_ticket)
                            standard-=1
                            print('standard')
                        else:
                            statementSQL_ticket= "INSERT INTO ticket (Booking_ID,seat_ID,type) VALUES ({0},'{1}','Reduced')".format((new_Booking_ID),(str(self.selected[i][0])+str(self.selected[i][1])))
                            cursor.execute(statementSQL_ticket)
                    cnxn.commit()



                        

                    #recipt
                    self.ui.standard_quantity.setText('standard x'+str(self.standard))
                    self.ui.reduced_quantity.setText('reduced x'+str(self.reduced))
                    self.ui.label_first.setText(self.first)
                    self.ui.label_last.setText(self.last)
                    self.ui.label_phone.setText(self.phone)
                    self.ui.performance.setText('Day'+str(self.day))
                    seats = []
                    for i in range (len(self.selected)):
                        row= self.selected[i][0]
                        column= self.selected[i][1]
                        seat_num=(row+column)
                        seats.append(seat_num)
                    new_seats=(','.join(seats))     
                    self.ui.seats.setText(new_seats)
                    self.ui.total_cost.setText('£'+str(self.total))
                    self.ui.booking_date.setText(str(current_date))
                    self.ui.booking_time.setText(str(time))
                    self.ui.stackedWidget.setCurrentWidget(self.ui.page_3)
                    c.update(self.day)
                    
                    
                    
                    
            
                
                

        except pyodbc.DatabaseError as err:
            print("Error:{}".format(error))
            print(err)
        finally:
            cnxn.close()
            print("Connection Closed")


###search###



        
class search_engine(QDialog):
    def __init__ (self):
        super(QDialog , self).__init__()
        self.ui = Ui_Dialog_search()
        self.ui.setupUi(self)
        self.ui.search_cust.clicked.connect(self.search_cust)
        self.ui.show_all_cust.clicked.connect(self.show_all_cust)
        self.ui.customer.clicked.connect(self.cust)
        self.ui.seat.clicked.connect(self.seat)
        self.ui.booking.clicked.connect(self.booking)
        self.ui.day_seat.currentIndexChanged.connect(self.change_date)
        self.ui.search_seat.clicked.connect(self.search_seat)
        self.ui.search_booking.clicked.connect(self.search_booking)
        self.ui.calendarWidget.clicked.connect(self.calender)
        self.ui.pushButton.clicked.connect(self.reset)
        self.ui.print.clicked.connect(self.print)
        
        self.selected =[]
        self.booked_seats=[]
        self.blocked_seats=[]
        self.date = []
        for z in range(2):
                y=60+(180*z)
                for j in range (2):
                    x=60+(340*j)
                    for k in range(65,70):
                        for i in range(1,11):
                            exec("self.checkBox{0}{1} = QtWidgets.QCheckBox(self.ui.seat_page)".format((chr(k+(5*z))),((i)+(10*j))))
                            exec("self.checkBox{0}{1}.setGeometry(QtCore.QRect({2},{3},31,31))".format((chr(k+(5*z))),((i)+(10*j)),(x+(30*(i-1))),(y+(30*(k-65)))))
                            exec("""self.checkBox{0}{1}.setStyleSheet('QCheckBox::indicator:disabled {{image: url(:/empty/available.png)}}\\n'
)""".format((chr(k+(5*z))),((i)+(10*j))))
                            exec("self.checkBox{0}{1}.clicked.connect(lambda:a.chosen('{0}','{1}'))".format((chr(k+(5*z))),((i)+(10*j))))
                            exec("self.checkBox{0}{1}.setInputMethodHints(QtCore.Qt.ImhNone)".format((chr(k+(5*z))),((i)+(10*j))))
                            exec("self.checkBox{0}{1}.setText('')".format((chr(k+(5*z))),((i)+(10*j))))
                            exec("self.checkBox{0}{1}.setIconSize(QtCore.QSize(20,20))".format((chr(k+(5*z))),((i)+(10*j))))
                            exec("self.checkBox{0}{1}.setEnabled(False)".format((chr(k+(5*z))),((i)+(10*j))))
                            exec("self.checkBox{0}{1}.setTristate(False)".format((chr(k+(5*z))),((i)+(10*j))))
                            exec("self.checkBox{0}{1}.setObjectName('checkBox{0}{1}')".format((chr(k+(5*z))),((i)+(10*j))))

        
        self.cs=(
            "Driver={SQL Server};"
            "Server=svr-cmp-01;"
            "Database=21ChungK69;"
            "Trusted_Connection=yes;"
            "UID=COLLYERS\21ChungK69;"
            "PWD=SY219769"
            )
    def print (self):
        count=self.ui.tableWidget_seat.rowCount()
        if count>0:
        
            font70 = ImageFont.truetype("static\OpenSans\OpenSans-Bold.ttf",size=70)
            font30 = ImageFont.truetype("static\OpenSans\OpenSans-Bold.ttf",size=30)
            for i in range (count):
                ticket=Image.open("ticket.jpg")
                draw = ImageDraw.Draw(ticket)
                draw.text((63,190),self.ui.tableWidget_seat.item(i,2).text(),font=font70, fill='black')
                draw.text((244,190),self.ui.tableWidget_seat.item(i,3).text(),font=font70, fill='black')
                draw.text((212,347),self.ui.tableWidget_seat.item(i,4).text(),font=font30, fill='black')
                if self.ui.tableWidget_seat.item(i,5).text()=='Standard':
                    draw.text((510,190),'Standard',font=font70, fill='black')
                    draw.text((61,347),("£10.00"),font=font30, fill='black')
                else:
                    draw.text((510,190),'Reduced',font=font70, fill='black')
                    draw.text((61,347),'£5.00',font=font30, fill='black')
                ticket.show()
        else:
            pass
        
    
    def reset(self):
        self.date = []
        self.ui.day_booking.setCurrentIndex(0)
        today = date.today()
    def calender (self):
        self.date=str(self.ui.calendarWidget.selectedDate().toString("dd/MM/yyyy"))
        print(self.date)
        
        

    def search_booking (self):
        self.ui.tableWidget_booking.clearContents()
        col = ["Booking_ID","First Name","Last Name","Performance","Total","Date","Time"]
        self.ui.tableWidget_booking.setColumnCount(len(col))
        self.ui.tableWidget_booking.setHorizontalHeaderLabels(col)

        day= (self.ui.day_booking.currentIndex())
        
        statementSQL_day_date = "SELECT booking.Booking_ID,customer.First_name,customer.Last_name,booking.Day,booking.Total_Cost,booking.Date,booking.Time FROM booking\
                                 LEFT JOIN customer ON booking.Cust_ID = customer.Cust_ID\
                                 WHERE  booking.Day= {0} AND booking.Date='{1}' AND booking.Cust_ID IS NOT NULL".format((day),(self.date))


        statementSQL_day = "SELECT booking.Booking_ID,customer.First_name,customer.Last_name,booking.Day,booking.Total_Cost,booking.Date,booking.Time FROM booking\
                            LEFT JOIN customer ON booking.Cust_ID = customer.Cust_ID\
                            WHERE  booking.Day= {0} AND booking.Cust_ID IS NOT NULL".format(day)
        
        
        statementSQL_date = "SELECT booking.Booking_ID,customer.First_name,customer.Last_name,booking.Day,booking.Total_Cost,booking.Date,booking.Time FROM booking\
                             LEFT JOIN customer ON booking.Cust_ID = customer.Cust_ID\
                             WHERE booking.Date='{0}' AND booking.Cust_ID IS NOT NULL".format(self.date)
        
        statementSQL_all = "SELECT booking.Booking_ID,customer.First_name,customer.Last_name,booking.Day,booking.Total_Cost,booking.Date,booking.Time FROM booking\
                             LEFT JOIN customer ON booking.Cust_ID = customer.Cust_ID\
                            WHERE booking.Cust_ID IS NOT NULL"
                             
        try:
            cnxn=pyodbc.connect(self.cs)
            if self.cs is not None:
                cursor = cnxn.cursor()
                if self.date!=[] and day!=0:
                    cursor.execute(statementSQL_day_date)
                elif self.date!=[]:
                    cursor.execute(statementSQL_date)
                elif day!=0:
                    cursor.execute(statementSQL_day)
                else:
                    cursor.execute(statementSQL_all)
               
                    
                rows = cursor.fetchall()
                noRow = 0
                self.ui.tableWidget_booking.setRowCount(len(rows))

                for tuple in rows:
                    noCol=0                                                                                                                                          
                    for column in tuple:
                        satuKolum=QTableWidgetItem(str(column))
                        self.ui.tableWidget_booking.setItem(noRow,noCol,satuKolum)
                        noCol+=1
                    noRow+=1
                self.rowcount=self.ui.tableWidget_booking.rowCount()


           

        except pyodbc.DatabaseError as err:
            print("Error:{}".format(error))
            self.ui.tableWidget_booking.clearContents()
            print(err)
            
        finally:
            cnxn.close()
            print("Connection Closed")
        

        
        
    def chosen(self,row,column):
        x= eval("self.checkBox{0}{1}.isChecked()".format((row),(column)))
        print(self.selected)
        if x== True:
            self.selected.append([row,column])       
        else:
            self.selected.remove([row,column])
        print('after',self.selected)
        
    
    def change_date(self):
            
        for i in range (len(self.booked_seats)):
            print(self.booked_seats[i][0])
            exec("self.checkBox{0}{1}.setChecked(False)".format((self.booked_seats[i][0]),(self.booked_seats[i][1])))
            exec("""self.checkBox{0}{1}.setStyleSheet('QCheckBox::indicator:disabled {{image: url(:/empty/available.png)}}\\n'
)""".format((self.booked_seats[i][0]),(self.booked_seats[i][1])))
            exec("self.checkBox{0}{1}.setEnabled(False)".format((self.booked_seats[i][0]),(self.booked_seats[i][1])))
        for i in range (len(self.blocked_seats)):
            exec("""self.checkBox{0}{1}.setStyleSheet('QCheckBox::indicator:disabled {{image: url(:/empty/available.png)}}\\n'
)""".format((self.blocked_seats[i][0]),(self.blocked_seats[i][1])))
        
        

        day= (self.ui.day_seat.currentIndex()+1)
        statementSQL_booked = "SELECT seat.[Row],seat.[Column] FROM ticket\
                               INNER JOIN seat ON ticket.seat_ID = seat.seat_ID\
                               INNER JOIN booking ON ticket.Booking_ID = booking.Booking_ID\
                               LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
                               WHERE booking.Day={0} AND (ticket.[type]='Standard' OR ticket.[type]='Reduced')".format(day)

        statementSQL_blocked = "SELECT seat.[Row],seat.[Column] FROM ticket\
                                INNER JOIN seat ON ticket.seat_ID = seat.seat_ID\
                                INNER JOIN booking ON ticket.Booking_ID = booking.Booking_ID\
                                LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
                                WHERE booking.Day={0} AND ticket.[type]='Blocked'".format(day)

        
                        
        try:
            
            cnxn=pyodbc.connect(self.cs)
            if self.cs is not None:
                
                cursor = cnxn.cursor()
                cursor.execute(statementSQL_booked)
                self.booked_seats = cursor.fetchall()
                cursor.execute(statementSQL_blocked)
                self.blocked_seats = cursor.fetchall()
                print('change',self.blocked_seats)


                for i in range (len(self.booked_seats)):
                    exec("""self.checkBox{0}{1}.setStyleSheet('QCheckBox::indicator:unchecked {{image: url(:/booked/booked.png)}}\\n'
'QCheckBox::indicator:checked {{image: url(:/search/search.png)}}')""".format((self.booked_seats[i][0]),(self.booked_seats[i][1])))
                    exec("self.checkBox{0}{1}.setEnabled(True)".format((self.booked_seats[i][0]),(self.booked_seats[i][1])))
                for i in range (len(self.blocked_seats)):
                    exec("""self.checkBox{0}{1}.setStyleSheet('QCheckBox::indicator:disabled {{image: url(:/blocked/blocked.png)}}\\n'
)""".format((self.blocked_seats[i][0]),(self.blocked_seats[i][1])))

 
            
        except pyodbc.DatabaseError as err:
            print("Error:{0}".format(error))
            print(err)
        finally:
            cnxn.close()
            print("Connection Closed")
        self.selected=[]
        self.ui.tableWidget_seat.clearContents()
        self.ui.tableWidget_seat.setColumnCount(0)
        self.ui.tableWidget_seat.setRowCount(0)
        
        
        
    
    def cust(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.cust_page)
        
    def seat(self):
            
        for i in range (len(self.booked_seats)):
            exec("""self.checkBox{0}{1}.setStyleSheet('QCheckBox::indicator:disabled {{image: url(:/empty/available.png)}}\\n'
)""".format((self.booked_seats[i][0]),(self.booked_seats[i][1])))
            exec("self.checkBox{0}{1}.setChecked(False)".format((self.booked_seats[i][0]),(self.booked_seats[i][1])))
            exec("self.checkBox{0}{1}.setEnabled(False)".format((self.booked_seats[i][0]),(self.booked_seats[i][1])))
        for i in range (len(self.blocked_seats)):
            exec("""self.checkBox{0}{1}.setStyleSheet('QCheckBox::indicator:disabled {{image: url(:/empty/available.png)}}\\n'
)""".format((self.booked_seats[i][0]),(self.booked_seats[i][1])))
        

        day= (self.ui.day_seat.currentIndex()+1)
        statementSQL_booked = "SELECT seat.[Row],seat.[Column] FROM ticket\
                                INNER JOIN seat ON ticket.seat_ID = seat.seat_ID\
                                INNER JOIN booking ON ticket.Booking_ID = booking.Booking_ID\
                                LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
                                WHERE booking.Day={0} AND (ticket.[type]='Standard' OR ticket.[type]='Reduced')".format(day)
        statementSQL_blocked = "SELECT seat.[Row],seat.[Column] FROM ticket\
                                INNER JOIN seat ON ticket.seat_ID = seat.seat_ID\
                                INNER JOIN booking ON ticket.Booking_ID = booking.Booking_ID\
                                LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
                                WHERE booking.Day={0} AND ticket.[type]='Blocked'".format(day)
                        
        try:
            
            cnxn=pyodbc.connect(self.cs)
            if self.cs is not None:
                
                cursor = cnxn.cursor()
                cursor.execute(statementSQL_booked)
                self.booked_seats = cursor.fetchall()
                cursor.execute(statementSQL_blocked)
                self.blocked_seats = cursor.fetchall()
                print('seat',self.blocked_seats)

                for i in range (len(self.booked_seats)):
                    exec("""self.checkBox{0}{1}.setStyleSheet('QCheckBox::indicator:unchecked {{image: url(:/booked/booked.png)}}\\n'
'QCheckBox::indicator:checked {{image: url(:/search/search.png)}}')""".format((self.booked_seats[i][0]),(self.booked_seats[i][1])))
                    exec("self.checkBox{0}{1}.setEnabled(True)".format((self.booked_seats[i][0]),(self.booked_seats[i][1])))
                for i in range (len(self.blocked_seats)):
                    exec("""self.checkBox{0}{1}.setStyleSheet('QCheckBox::indicator:disabled {{image: url(:/blocked/blocked.png)}}\\n'
)""".format((self.blocked_seats[i][0]),(self.blocked_seats[i][1])))
        except pyodbc.DatabaseError as err:
            print("Error:{0}".format(error))
            print(err)
        finally:
            cnxn.close()
            print("Connection Closed")
        self.selected=[]
        self.ui.tableWidget_seat.clearContents()
        self.ui.tableWidget_seat.setRowCount(0)
        self.ui.tableWidget_seat.setColumnCount(0)
        self.ui.stackedWidget.setCurrentWidget(self.ui.seat_page)
        
        

    def booking(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.booking_page)
#search button
    def search_seat(self):
        self.ui.tableWidget_seat.clearContents()
        col = ["First Name","Last Name","Row","Column","Performance","Type"]
        self.ui.tableWidget_seat.setColumnCount(len(col))
        self.ui.tableWidget_seat.setHorizontalHeaderLabels(col)
        day= (self.ui.day_seat.currentIndex()+1)
        rows=[]

        try:
            cnxn=pyodbc.connect(self.cs)
            if self.cs is not None:
                cursor = cnxn.cursor()
                for i in range (len(self.selected)):
                    statementSQL_ticket = "SELECT customer.First_name,customer.Last_name,seat.[Row],seat.[Column],booking.Day,ticket.Type FROM ticket\
                                           INNER JOIN seat ON ticket.seat_ID = seat.seat_ID\
                                           INNER JOIN booking ON ticket.Booking_ID = booking.Booking_ID\
                                           LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
                                           WHERE booking.Day={0} AND (seat.[Row] ='{1}' AND seat.[Column]='{2}')".format((day),(self.selected[i][0]),(self.selected[i][1]))
           
                    cursor.execute(statementSQL_ticket)
                    row = cursor.fetchone()
                    rows.append(row)

                    
                print(rows)
                noRow = 0
                self.ui.tableWidget_seat.setRowCount(len(rows))

                for tuple in rows:
                    noCol=0                                                                                                                                          
                    for column in tuple:
                        satuKolum=QTableWidgetItem(str(column))
                        self.ui.tableWidget_seat.setItem(noRow,noCol,satuKolum)
                        noCol+=1
                    noRow+=1
                self.rowcount=self.ui.tableWidget_seat.rowCount()
        except pyodbc.DatabaseError as err:
            print("Error:{}".format(error))
            self.ui.tableWidget_seat.clearContents()
            print(err)
            
        finally:
            cnxn.close()
            print("Connection Closed")
            
            
        
            

            
        
        
    def show_all_cust(self):
        self.ui.tableWidget_cust.clearContents()
        col = ["Customer_ID","First Name","Last Name","Phone"]
        self.ui.tableWidget_cust.setColumnCount(len(col))
        self.ui.tableWidget_cust.setHorizontalHeaderLabels(col)
        statementSQL_show_all_cust = "SELECT* FROM customer WHERE Cust_ID IS NOT NULL"

        try:
            cnxn=pyodbc.connect(self.cs)
            if self.cs is not None:
                cursor = cnxn.cursor()
                cursor.execute(statementSQL_show_all_cust)
                rows = cursor.fetchall()
                noRow = 0
                self.ui.tableWidget_cust.setRowCount(len(rows))

                for tuple in rows:
                    noCol=0                                                                                                                                          
                    for column in tuple:
                        satuKolum=QTableWidgetItem(str(column))
                        self.ui.tableWidget_cust.setItem(noRow,noCol,satuKolum)
                        noCol+=1
                    noRow+=1
                self.rowcount=self.ui.tableWidget_cust.rowCount()

           

        except pyodbc.DatabaseError as err:
            print("Error:{}".format(error))
            self.ui.tableWidget_cust.clearContents()
            print(err)
            
        finally:
            cnxn.close()
            print("Connection Closed")
        
        
        
    def search_cust (self):
        self.ui.tableWidget_cust.clearContents()
        col = ["Customer_ID","First Name","Last Name","Phone","Performance"]
        self.ui.tableWidget_cust.setColumnCount(len(col))
        self.ui.tableWidget_cust.setHorizontalHeaderLabels(col)

        first=self.ui.first_cust.text()
        last = self.ui.last_cust.text()
        phone = self.ui.phone_cust.text()
        day= (self.ui.day_cust.currentIndex()+1)

        statementSQL_full_phone_day = "SELECT customer.Cust_ID,customer.First_name,customer.Last_name,customer.Phone_num,booking.Day FROM booking\
                                       LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
                                       WHERE customer.First_name = '{0}' AND booking.Day= {1} AND customer.Phone_num = {2} AND booking.Cust_ID IS NOT NULL".format((first),(day),(phone))
        
        statementSQL_first_day= "SELECT customer.Cust_ID,customer.First_name,customer.Last_name,customer.Phone_num,booking.Day FROM booking\
                             LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
                             WHERE customer.First_name = '{0}' AND booking.Day= {1} AND booking.Cust_ID IS NOT NULL".format((first),(day))
        statementSQL_last_day = "SELECT customer.Cust_ID,customer.First_name,customer.Last_name,customer.Phone_num,booking.Day FROM booking\
                             LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
                             WHERE customer.Last_name = '{0}' AND booking.Day= {1} AND booking.Cust_ID IS NOT NULL".format((last),(day))
 
        statementSQL_phone_day = "SELECT customer.Cust_ID,customer.First_name,customer.Last_name,customer.Phone_num,booking.Day FROM booking\
                                  LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
                                  WHERE customer.Phone_num = '{0}' AND booking.Day= {1} AND booking.Cust_ID IS NOT NULL".format((phone),(day))
        statementSQL_day = "SELECT customer.Cust_ID,customer.First_name,customer.Last_name,customer.Phone_num,booking.Day FROM booking\
                            LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
                            WHERE booking.Day = {0} AND booking.Cust_ID IS NOT NULL".format(day)
        statementSQL_full_day = "SELECT customer.Cust_ID,customer.First_name,customer.Last_name,customer.Phone_num,booking.Day FROM booking\
                                 LEFT JOIN customer ON Booking.Cust_ID = customer.Cust_ID\
                                 WHERE customer.First_name = '{0}' AND customer.Last_name='{1}' AND booking.Day= {2} AND booking.Cust_ID IS NOT NULL".format((first),(last),(day))

        try:
            cnxn=pyodbc.connect(self.cs)
            if self.cs is not None:
                cursor = cnxn.cursor()
                if (len(first)>0 and first.isspace()==False) and (len(last)>0 and last.isspace()==False) and (len(phone)>0 and phone.isspace()==False):
                    cursor.execute(statementSQL_full_phone_day)
                elif (len(first)>0 and first.isspace()==False) and (len(last)>0 and last.isspace()==False):
                    cursor.execute(statementSQL_full_day)
                elif len(phone)>0 and phone.isspace()==False:
                    cursor.execute(statementSQL_phone_day)
                elif len(first)>0 and first.isspace()==False:
                    cursor.execute(statementSQL_first_day)
                elif len(last)>0 and last.isspace()==False:
                    cursor.execute(statementSQL_last_day)
                else:
                    cursor.execute(statementSQL_day)
                    
                rows = cursor.fetchall()
                noRow = 0
                self.ui.tableWidget_cust.setRowCount(len(rows))

                for tuple in rows:
                    noCol=0                                                                                                                                          
                    for column in tuple:
                        satuKolum=QTableWidgetItem(str(column))
                        self.ui.tableWidget_cust.setItem(noRow,noCol,satuKolum)
                        noCol+=1
                    noRow+=1
                self.rowcount=self.ui.tableWidget_cust.rowCount()


           

        except pyodbc.DatabaseError as err:
            print("Error:{}".format(error))
            self.ui.tableWidget_cust.clearContents()
            print(err)
            
        finally:
            cnxn.close()
            print("Connection Closed")
                    
            
            
        
        
        

        
        


if __name__ == '__main__':
    import sys
    sys._excepthook = sys.excepthook
    def exception_hook(exctype,value,traceback):
        sys._excepthook(exctype,value,traceback)
        sys.exit(1)
    sys.excepthook = exception_hook
    app = QApplication(sys.argv)
    w = booking()
    a = search_engine()
    b = block()
    c = menu()
    d = login()
    d.show()
    d.start()
    sys.exit(app.exec())
        
        
        

