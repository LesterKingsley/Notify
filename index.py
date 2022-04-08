#testing
import datetime
import itertools
import json
import os
import pymysql


#Global Variables
notes=[];
logged=False;
_user="";
_pass="";

#Class of Word Object
class Notes:
    id_iter = itertools.count()
  
    def __init__(self, title, content):
       
        self.id = next(Notes.id_iter)
        self.title = title
        self.content = content
     
    def __repr__(self): #ung itsura sa array o kaya pinrint
        return str(self.id)+":"+self.title;
    def obj_dict(obj):
        return obj.__dict__;
    def show(self):
        date= datetime.datetime.now()
        print("\nNOTE DETAILS","\ntitle:", self.title, "\ncontent:", self.content , "\ndate added:",date);  #pag comma automatic space na


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
        print("");

    
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
            sign();
        elif(res=="l"):
            login();
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
                newNote=Notes(x['title'],x['content']);
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

def browse():
    print("You choose to Browse a Note");
    print(notes);
    openId=input("input the id that will be open: ");
    if openId.isdigit(): #check of the string answer are digits
        openId=int(openId);
        filteredNote=list(filter(lambda x: x.id == openId, notes));
        if(len(filteredNote)>=1):
            filteredNote[0].show();
            tryAgain=input("\nsearch again?");
            if(tryAgain=="y"):
                browse();
            else:
                Main();
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
                newNote=Notes(x['title'],x['content']);
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
