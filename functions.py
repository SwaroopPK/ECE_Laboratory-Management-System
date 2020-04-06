import sqlite3

class DB_functions(object):
    def initDB(self):
        self.dbms = sqlite3.connect('DBMS_SS.db')
        self.curdbms = self.dbms.cursor()

    def password_check(self,usn,password,user_type):
        # 0 -> correct password
        # 1 -> password incorrect
        # 2 -> No student with USN
        # 3 -> No match for entered ID
        if(self.curdbms.execute("SELECT * FROM SECURITY WHERE ? == SECURITY.USN_ID AND ? == SECURITY.USER_TYPE",(usn,user_type)).fetchone() is None):
            self.dbms.close()
            return 3
        elif(self.curdbms.execute("SELECT USER_TYPE FROM SECURITY WHERE SECURITY.USN_ID == ?",(usn,)).fetchone()[0] == "STUDENT"):
            if(self.curdbms.execute("SELECT * FROM STUDENT WHERE ? == STUDENT.USN",(usn,)).fetchone() is None):
                self.dbms.close()
                return 2  
        if(password == self.curdbms.execute('''SELECT PASSWORD FROM SECURITY
        WHERE ? == SECURITY.USN_ID;''',(usn,)).fetchone()[0]):
            self.dbms.close()
            return 0
        else:
            self.dbms.close()
            return 1


    def borrow(self,stusn,ic,count):     # Values come from when user clicks 'BORROW' button
        # Check for wrong or un-processable data
        if(self.curdbms.execute("SELECT * FROM STUDENT WHERE ? == STUDENT.USN",(stusn,)).fetchone() is None):
            self.dbms.close()
            return("No Student with the USN")
        elif(self.curdbms.execute("SELECT * FROM COMPONENTS WHERE ? == COMPONENTS.ICNUM",(ic,)).fetchone() is None):
            self.dbms.close()
            return("NO IC Found")
        elif(self.curdbms.execute("SELECT COUNT FROM COMPONENTS WHERE ? == COMPONENTS.ICNUM",(ic,)).fetchone()[0] < int(count)):
            s = "Available IC count is: " + str(self.curdbms.execute("SELECT COUNT FROM COMPONENTS WHERE ? == COMPONENTS.ICNUM",(ic,)).fetchone()[0])
            self.dbms.close()
            return(s)
        elif(int(count) < 0):
            self.dbms.close()
            return("Enter a non-negative count value")
        else:
            # Check if the USN and IC name are present in BORROW Table
            if(self.curdbms.execute("SELECT * FROM BORROW WHERE ? == BORROW.STUSN AND ? == BORROW.IC",(stusn,ic,)).fetchone() is None):
                # Insert if no prev entries
                self.curdbms.execute("INSERT INTO BORROW(STUSN,IC,COUNT) VALUES (?,?,?);",(stusn,ic,count,))
            else:
                # Existing count from the BORROW Table and increment
                self.c = count + (self.curdbms.execute("SELECT COUNT FROM BORROW WHERE ? == BORROW.STUSN AND ? == BORROW.IC",(stusn,ic,)).fetchone()[0])
                self.curdbms.execute("UPDATE BORROW SET COUNT = ? WHERE STUSN == ? AND ? == BORROW.IC;",(self.c,stusn,ic,))
            # Update available ICs in COMPONENTS Table
            self.c = self.curdbms.execute("SELECT COUNT FROM COMPONENTS WHERE ? == COMPONENTS.ICNUM",(ic,)).fetchone()[0]
            self.curdbms.execute("UPDATE COMPONENTS SET COUNT = ? WHERE ? == COMPONENTS.ICNUM;",(self.c-count,ic,))
        # Commit the changes to the DataBase
        self.dbms.commit()
        self.dbms.close()
        return("Change committed in the DataBase")


    def return_ic(self,stusn,ic,count):     # Values come from when user clicks 'BORROW' button
        # Check for wrong or un-processable data
        if(self.curdbms.execute("SELECT * FROM STUDENT WHERE ? == STUDENT.USN",(stusn,)).fetchone() is None):
            self.dbms.close()
            return("No Student with the USN")
        elif(self.curdbms.execute("SELECT * FROM COMPONENTS WHERE ? == COMPONENTS.ICNUM",(ic,)).fetchone() is None):
            self.dbms.close()
            return("NO IC Found")
        elif(self.curdbms.execute("SELECT * FROM BORROW WHERE ? == BORROW.STUSN AND ? == BORROW.IC",(stusn,ic,)).fetchone() is None):
            self.dbms.close()
            return("Student has no IC of the entered number") 
        elif(self.curdbms.execute("SELECT COUNT FROM BORROW WHERE ? == BORROW.STUSN AND ? == BORROW.IC",(stusn,ic,)).fetchone()[0] < count):
            c = "Student borrowed only " + str(self.curdbms.execute("SELECT COUNT FROM BORROW WHERE ? == BORROW.STUSN AND ? == BORROW.IC",(stusn,ic,)).fetchone()[0]) + " of ICNum " + ic
            self.dbms.close()
            return(c)
        else:
            c = self.curdbms.execute("SELECT COUNT FROM BORROW WHERE ? == BORROW.STUSN AND ? == BORROW.IC",(stusn,ic,)).fetchone()[0]
            if(c == count):
                # Delete the tuple from BORROW Table
                self.curdbms.execute("DELETE FROM BORROW WHERE ? == BORROW.STUSN AND ? == BORROW.IC",(stusn,ic,))
            else:
                # Update BORROW Table
               self.curdbms.execute("UPDATE BORROW SET COUNT = ? WHERE STUSN == ? AND ? == BORROW.IC;",(c-count,stusn,ic,)) 
            # Update COMPONENTS Table and Commit changes
            c = self.curdbms.execute("SELECT COUNT FROM COMPONENTS WHERE ? == COMPONENTS.ICNUM",(ic,)).fetchone()[0]
            self.curdbms.execute("UPDATE COMPONENTS SET COUNT = ? WHERE ? == COMPONENTS.ICNUM;",(c+count,ic,))
        self.dbms.commit()
        self.dbms.close()
        return("Change committed in the DataBase")


    def get_detail(self,usn_id):
        if(self.curdbms.execute("SELECT USER_TYPE FROM SECURITY WHERE SECURITY.USN_ID == ?",(usn_id,)).fetchone()[0] == "STUDENT"):
            self.borrowed = self.curdbms.execute("SELECT * FROM BORROW WHERE BORROW.STUSN == ?",(usn_id,)).fetchall()
        else:
            self.borrowed = self.curdbms.execute("SELECT * FROM BORROW WHERE 1").fetchall()
        if len(self.borrowed) is 0:
            print("No borrowed items")
        else:
            for rows in borrowed:
                print(rows)
        self.dbms.close()
        return

    def add_component(self,icnum,cost_inr,count):
        if(self.curdbms.execute("SELECT * FROM COMPONENTS WHERE ? == COMPONENTS.ICNUM",(icnum,)).fetchone() is None):
            self.curdbms.execute("INSERT INTO COMPONENTS(ICNUM,COST_INR,COUNT) VALUES(?,?,?)",(icnum,cost_inr,count,))
            self.c = "A new component has been added"
        else:
            self.c = self.curdbms.execute("SELECT COUNT FROM COMPONENTS WHERE COMPONENTS.ICNUM == ?",(icnum,)).fetchone()[0]
            self.curdbms.execute("UPDATE COMPONENTS SET COUNT = ? WHERE COMPONENTS.ICNUM == ?",(self.c+count,icnum,))
            self.c = "Existing component count has been updated"
        self.dbms.commit()
        self.dbms.close()
        return self.c

    def remove_component(self,icnum,cost_inr,count):
        if(self.curdbms.execute("SELECT * FROM COMPONENTS WHERE ? == COMPONENTS.ICNUM",(icnum,)).fetchone() is None):
            self.c = "No component of name/number " + icnum + " found"
        elif(self.curdbms.execute("SELECT COUNT FROM COMPONENTS WHERE ? == COMPONENTS.ICNUM",(icnum,)).fetchone()[0] < count):
            self.c = "The component number/name " + icnum + " has only " + str(self.curdbms.execute("SELECT COUNT FROM COMPONENTS WHERE ? == COMPONENTS.ICNUM",(icnum,)).fetchone()[0]) + " of its type"
        else:
            self.c = self.curdbms.execute("SELECT COUNT FROM COMPONENTS WHERE COMPONENTS.ICNUM == ?",(icnum,)).fetchone()[0]
            self.curdbms.execute("UPDATE COMPONENTS SET COUNT = ? WHERE COMPONENTS.ICNUM == ?",(self.c-count,icnum,))
            self.c = "Existing component count has been updated"
        self.dbms.commit()
        self.dbms.close()
        return self.c
 

