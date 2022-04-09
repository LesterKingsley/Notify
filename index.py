#testing

from datetime import datetime
import itertools
import json
import os
from turtle import title
from unicodedata import category
import pymysql
from pyautogui import typewrite


#Global Variables
notes=[];
logged=False;
_user="";
_pass="";

#Class of Word Object
class Notes:
    now = datetime.now();
    id_iter = itertools.count();
    category=None;
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    def __init__(self, title, content,dateCreated=date_time):
       
        self.id = next(Notes.id_iter)
        self.title = title
        self.content = content
        self.dateCreated=dateCreated

     
    def __repr__(self): #ung itsura sa array o kaya pinrint
        return str(self.id)+":"+self.title;
    def obj_dict(obj):
        return obj.__dict__;
    def show(self):
        print("\nNOTE DETAILS","\ntitle:", self.title, "\ncontent:", self.content , "\ndate added:",self.dateCreated);  #pag comma automatic space na

def confirm(func,*args):
    ok=input(args[0]);
    #if magbaback
    if(ok=="n"):
        Main(); 
    #if irurun ulit sa start ung function
    elif(ok=="y" and args[1]==True):      
        func();
    #continue lang
    else:
        print("wrong button, going main...");
        Main();
    
def Main():
    if(logged==True):
        print("\nWelcome to Notify\n");
        res=input("Press 'A' to add notes, 'D' to delete notes, 'B' to open notes,'E' for export,'I' for import, 'X' to exit: ");
        if(res=="a"):
            Add();
        elif(res=="d"):
            Delete()
        elif(res=="b"):
            browse()
        elif(res=="e"):
            export()
        elif(res=="i"):
            confirm(importer,"this will import and clear current file, continue? ",False);
            importer()
        elif res=="x":
            save();
            exit();   
        else:
            print("wrong input");
            Main();
    else:
        res=input("Press 'S' to sign in, 'L' to log in: ");
        if(res=="s"):
            try:
                sign();
            except:
                print("no connection with the server, pls try again later...");
        elif(res=="l"):
            try:
                login();
            except:
                print("no connection with the server, pls try again later...");
        else:
            print("wrong input");
            Main();      

def fetchNotes():
    print("loading notes...");
    conn = pymysql.connect(host="localhost",user="root",passwd="",database="notify" );
    if conn.open:     
        cursor=conn.cursor();
        global _user;
        global _pass;
        username=_user;
        password=_pass;
        sql = "SELECT data FROM users WHERE username='{0}' and password='{1}'".format(username,password);
        cursor.execute(sql)
        result = cursor.fetchone()[0];
        if result!="[]":
            print(result);
            # json.dumps([ob.__dict__ for ob in notes]);
            imported=json.loads(result);
            for x in imported:
                newNote=Notes(x['title'],x['content'],x['dateCreated']);
                notes.append(newNote);
            print("account syncing succesfully executed \n");
            conn.commit();
            conn.close();
            Main();
        else:
            conn.commit();
            conn.close();

# Sign In
def sign():
    print("Signing In!");
    conn = pymysql.connect(host="localhost",user="root",passwd="",database="notify" );
    if conn.open:
        cursor = conn.cursor();
        username=input("Input your username: ");
        password=input("Input your password: ");
        
        # queries for inserting values
        username_exists = "SELECT * FROM users WHERE username='{0}'".format(username);
        cursor.execute(username_exists);
        result = cursor.fetchall();
     
        if(len(result)==0):
            sign_up= "INSERT INTO users(USERNAME,PASSWORD,DATA) VALUES('{0}', '{1}', '[]');".format(username,password);
            cursor.execute(sign_up);
            print("signed up succesfully");
            conn.commit();
            conn.close();
            login();
        else:
            conn.commit();
            conn.close();
            print("username already exists..pls try again...");
            sign();  

def login():
    print("Logging In");
    conn = pymysql.connect(host="localhost",user="root",passwd="",database="notify" );
    if conn.open:
        cursor = conn.cursor();
        username=input("Input your username: ");
        password=input("Input your password: ");
        #check if that exists;
        sql = "SELECT * FROM users WHERE username='{0}' and password='{1}'".format(username,password);
        
        cursor.execute(sql)
        result = cursor.fetchall();
        if(len(result)==0):
            print("account not detected. create a new account");
            conn.commit();
            conn.close();
            Main();
        else:
            global _user;
            global _pass;
            global logged;
            _user=username;
            _pass=password;
            logged=True;        
            print("account detected");
            conn.commit();
            conn.close();
            fetchNotes();
            
            
            Main();
         
#Log In
def Add():
    print("Add a New Note");
    title=input("Add a title:");
    content=input("Add a content:");
    newNote=Notes(title,content);
    confirm(Add,"save this note?",False);
    notes.append(newNote); # There is no need in global statement if there is no assignment.
    # print(notes);
    Main();

def Delete():
    delete=input("You choose to Delete a Note, 'S' to delete a single entry, 'A' to delete all entries ");
    if delete=="s":
        deleteId=input("input the id that will be deleted ") 
        if deleteId.isdigit():
            deleteId=int(deleteId);
            filteredNote=list(filter(lambda x: x.id != deleteId, notes))
            if(len(filteredNote)>=1):
                notes.clear()
                notes.extend(filteredNote);
                print("entry deleted");
            else:
                print("entry not detected");
                confirm(Delete,"try to delete again?",True);
    elif delete=="a":
        notes.clear();
    else:
        confirm(Delete,"wrong input, try to delete again?",True);
    Main();

def edit(editId):
    if type(editId)==int:
        editId=int(editId);
        editnote=list(filter(lambda x: x.id == editId, notes));

        editWhat=input("What will you edit. 't' for title, c for 'content'");
        if editWhat=="t":
            editnote[0].title="george";
            print("enter new title:");
            typewrite(editnote[0].title);
            newText=input();
            editnote[0].title=newText;
            Main();
        elif editWhat=="c":
            print("enter new content:");
            typewrite(editnote[0].content);
            newText=input();
            editnote[0].content=newText;
        else:
            confirm(edit(editId),"wrong input, try to edit again?",True);

    else:
        confirm(edit(editId),"wrong input, try to edit again?",True);

def browse():
    print("You choose to Browse a Note");
    print(notes);
    openId=input("input the id that will be open: ");
    if openId.isdigit(): #check of the string answer are digits
        openId=int(openId);
        filteredNote=list(filter(lambda x: x.id == openId, notes));
        if(len(filteredNote)>=1):
            filteredNote[0].show();
            action=input("'e' for Edit Note, 'X'for go back");
            if(action=="x"):
                confirm(browse,"browse again? ",True);
            elif(action=="e"):
                edit(openId);
            else:
                print("yeah");
        else:
            print("no entry detected");
            confirm(browse,"browse again? ",True);
    else:
        print("the input is not a number");
        confirm(browse,"browse again? ",True);
    Main();

def export():

    name=input("enter the file name: ");
    confirm(export,"a file named "+name+" will be created,continue? ",False);
    with open("C:/Users/LesterKingsley/OneDrive/Desktop/Business Analyst/Technical/Programming/My Projects/Notify/"+name+".json", "w") as f:
        json.dump([ob.__dict__ for ob in notes],f)
        print("file exported successfully")
    Main();
    
def importer():
    name=input("enter the file name: ");
    if os.path.isfile("C:/Users/LesterKingsley/OneDrive/Desktop/Business Analyst/Technical/Programming/My Projects/Notify/"+name+".json"):
        with open("C:/Users/LesterKingsley/OneDrive/Desktop/Business Analyst/Technical/Programming/My Projects/Notify/"+name+".json", "r") as f:
            notes.clear();
            jack=json.load(f); #para maging list ulit ung f gagamit ng json.load()
            for x in jack:
                newNote=Notes(x['title'],x['content'],x['dateCreated']);
                notes.append(newNote);
            print("importing",name,"succesfully executed \n");
    else:
        print("file not found");
        confirm(importer,"try again?",True);
        importer();
    Main();

def save():
    print("saving...");
    exported=json.dumps([ob.__dict__ for ob in notes]);
    conn = pymysql.connect(host="localhost",user="root",passwd="",database="notify" );
    if conn.open:
        global _user; 
        cursor=conn.cursor();
        updateSql = "UPDATE  users SET data= '{0}'  WHERE username = '{1}' ;".format(exported,_user);
        cursor.execute(updateSql);
    conn.commit();
    conn.close();
    print("saved");

Main()
