import datetime
import itertools
import json
import os

#Create a Object

notes=[];

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
        date=todays_date = datetime.datetime.now()
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
        exit();   
    else:
        print("wrong input");
        Main();

def Add():
    print("Add a New Note");
    title=input("Add a title:");
    content=input("Add a content:");
    newNote=Notes(title,content);
    confirm(Add,"save this note?",False);
    notes.append(newNote);
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


Main()

