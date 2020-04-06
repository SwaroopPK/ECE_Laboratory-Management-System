# ECE_Laboratory-Management-System
This is a simple front end and a back end project to maintain equipments in an Electronics and Communication Laboratory.

  This project was created because most of the college laboratories face a common problem i.e. who borrowed which equipment from the lab? Did he return it or not? This project gives a basic idea of how we can reduce the number of ICs being stolen from the laboratory.
  
The project contains 2 parts

1) Front end i.e. the Graphical User Interface.
2) Back end i.e. the Database.

### Front End

* The GUIs are created using a software called *Qt Designer* ([Instructions to install](https://www.youtube.com/watch?v=isZYlUINWiM))
* The GUIs in Qt Designer are made as [follows](Designer_GUI). After creating the GUIs in Designer, open *Command Prompt* and type **pyqt5 -x your_GUI.ui -o PythonFileNameYouWant.py**

**NOTE:** This command will convert *your_GUI.ui* into its respective python code and saves it in a seperate  file named *PythonFileNameYouWant.py*

* The GUIs are converted and are shown [here](/GUI)

### Back End

1) The database includes 4 tables namely **STUDENT,COMPONENTS,BORROW,SECURITY**.

2) *STUDENT* is a global table made by the college. It has attributes like **FNAME, LNAME, USN, DOB, SEM, BATCH**.

3) *COMPONENTS* is a table which has the details of the ICs (**ICNUM, COST_INR, COUNT**) available in the laboratory.

4) *BORROW* table contains the details including **USN, IC, COUNT**.

5) *SECURITY* table contains **USN_ID,PASSWORD,USER_TYPE** for STUDENT as well as FACULTY

* To create a DB and include all the data in them [SQLite Sudio](https://sqlitestudio.pl/index.rvt)([Instruction to Install](https://www.youtube.com/watch?v=X4Bqkez9BRM)) is used. 
* The [codes](/DB.txt) for creation of tables and data are included in the repository.
* The functions for accessing the DB using python are created using *sqlite3* package and cursor method. The codes are included [here](/functions.py)
* The codes of all three GUIs are combined into a single file called [Security.py](/Security.py)

### Some Constraints Followed

1) The IC num in the BORROW table is a foreign key which references the ICNUM from the COMPONENTS table.

2) STUDENTS are not allowed to LOGIN, but are only allowed to check their borrowed ICs and count.

3) Updating the BORROW list can only be done by FACULTY and only after the FACULTY logins.

4) IC list and its details are only visible to the  FACULTY.

This project can be improvised by including a lot of other features like making it online or other updates as such. But this project is made just for a basic reference of a better idea.
