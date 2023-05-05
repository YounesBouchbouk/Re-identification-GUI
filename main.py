from tkinter import  *
from tkinter import ttk
import pytesseract
import PIL
from PIL import ImageTk,Image
import os
import cv2
import numpy as np
from multiprocessing import Process
import exifread
from PIL.ExifTags import TAGS
import urllib.request
import datetime


sft = cv2.xfeatures2d.SIFT_create()

dt = datetime.datetime.now()
root=Tk()
root.bind('<Escape>', lambda e: root.quit())
root.title("Amoung Us ")
root.geometry('1850x920+33+24')
root.resizable(False,False)
path = 'people'

#----------3 camera Labels -----------------------------------------------
#notconncted = cv2.imread('cameranotconn.jpg',cv2.IMREAD_GRAYSCALE)
#myimg='cameranotconn.jpg'
notconncted = ImageTk.PhotoImage(Image.open('cameraprincipale.jpg'))
cam1notc = ImageTk.PhotoImage(Image.open('camera1.jpg'))
cam2notc = ImageTk.PhotoImage(Image.open('camera2.jpg'))
#resized = notconncted.resize((300,250) , Image.ANTIALIAS)
lmain = Label(root)


lmain.place(x=750,y=40,width=700,height=400)
#lmain.imgtk=notconncted
lmain.config(image=notconncted)
cam1frams = Label(root)
cam1frams.place(x=410,y=480,width=700,height=400)
cam1frams.config(image=cam1notc)
cam2frams = Label(root)
cam2frams.place(x=1120,y=480,width=700,height=400)
cam2frams.config(image=cam2notc)
#myList = os.listdir(path)





# read all images  ------------------------------------------------------------
imagesliste = []
classnames=[]
classnames2=[]
def extractdata(classnames,imagesliste,classnames2):
    global path
    classnames2.clear()

    classnames.clear()
    imagesliste.clear()
    myList = os.listdir(path)
    for myimg in myList:
        classnames.append(os.path.splitext(myimg)[0] + '.jpg')
        classnames2.append(os.path.splitext(myimg)[0])
        pic = Image.open(f'{path}/{myimg}')
        resized = pic.resize((300,250) , Image.ANTIALIAS)
        image2 = ImageTk.PhotoImage(resized)
        imagesliste.append(image2)

extractdata(classnames,imagesliste,classnames2)





# create 2 frame   ------------------------------------------------------------
leftframe = Frame(root ,bd=2 , relief=SUNKEN)
leftframe.place(x=0 , y=0 , width=400 , height =450 )


# text label status
statusfram = Frame(root , bg = "black" )
status = Label(root ,  text = " image 1 of " + str(len(imagesliste)),bd=2 , relief=SUNKEN)
status.place(x=50 , y=10 )


# back and next function ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# image viewer label  ------------------------------------------------------------
imageframe = Frame(root , bg = "WHITE")
imageframe.place(x=50 , y = 50 , width=300 , height=225)
imagelabel = Label(imageframe)
if len(classnames) != 0:

    imagelabel = Label(imageframe, image=imagesliste[0])

imagelabel.grid(row=0, column=2, columnspan=3)

imagenombre = 0

def refresh():
    liste = os.listdir(path)
    global backtbtn
    global nexttbtn
    global removetbtn
    global removealltbtn
    global imagelabel
    global trackbutton
    global classnames2
    global imagename
    global cam2trackdeslist,cam2trackclassname,cam2imgtotrack,cam2images,cam2desList
    if len(liste) != 0 :
        extractdata(classnames,imagesliste,classnames2)

        imagelabel.grid_forget()
        imagelabel = Label(imageframe, image=imagesliste[0])
        backtbtn = Button(framebuttonleft, text="back",fg='White',bg= 'dark green',  command=back, state=DISABLED).place(x=55, y=10)
        removetbtn = Button(framebuttonleft, text="Remove", fg='White',bg= 'dark red', command=lambda: deleteon(1)).place(x=165, y=10)
        if(len(liste)==1):
            nexttbtn = Button(framebuttonleft, text="next", fg='White', bg='dark green',
                              state=DISABLED).place(x=305, y=10)
        else:
            nexttbtn = Button(framebuttonleft, text="next", fg='White', bg='dark green',
                              command=lambda: forward(2)).place(x=305, y=10)

        removealltbtn = Button(framebuttonleft, text="Remove All",fg='White',bg= 'dark red',   command=lambda : deleteall() ).place(x=160, y=50)
        imagelabel.grid(row=0, column=2, columnspan=3)
        imagename = Button(root, text=classnames[0], bd=3, relief=SUNKEN, width=5, height=1,command=lambda: openlevel(0)).place(x=182, y=10)
        trackbutton = Button(root, text="track this person", bd=3, relief=SUNKEN, width=15, fg="white",bg="black",height=1 ,command= lambda :cam2whototrack(cam2trackdeslist,cam2trackclassname,cam2imgtotrack,classnames2[0])).place(x=138, y=277)
    Process(target=cam2checkonfolder(cam2classname, cam2images, cam2desList, cam2trackclassname, cam2trackdeslist,
                                     cam2imgtotrack)).start()


def deleteon(imagenum):
    global path
    global imagenombre
    global imagelabel
    global backtbtn
    global nexttbtn
    global imagename
    global classnames
    global nexttbtn
    global backtbtn
    global removetbtn
    global removealltbtn
    global classnames2
    global cam2trackdeslist, cam2trackclassname, cam2imgtotrack
    global trackbutton
    #print(imagenum)
    imagepath = path + '/' + classnames[imagenum-1]
    #print(imagepath)
    os.remove(imagepath)
    Process(target=extractdata(classnames, imagesliste,classnames2)).start()
    imagelabel.grid_forget()
    if  imagenum == len(imagesliste)+1:
        if(len(classnames)!=0):
            imagelabel = Label(imageframe, image=imagesliste[0])
            imagename = Button(root, text=classnames[0], bd=3, relief=SUNKEN, width=5, height=1,command=lambda: openlevel(0)).place(x=182, y=10)
            trackbutton = Button(root, text="track this person", bd=3, fg="white",bg="black",relief=SUNKEN, width=15, height=1 ,command=lambda :cam2whototrack(cam2trackdeslist,cam2trackclassname,cam2imgtotrack,classnames2[0])).place(x=138, y=277)

        else:
            backtbtn = Button(framebuttonleft, text="back", fg='White', bg='dark green', command=back,state=DISABLED).place(x=55, y=10)
            removetbtn = Button(framebuttonleft, text="Remove", fg='White', bg='dark red', state=DISABLED).place(x=165,y=10)
            nexttbtn = Button(framebuttonleft, text="next", fg='White', bg='dark green', state=DISABLED).place(x=305,y=10)
            removealltbtn = Button(framebuttonleft, text="Remove All", fg='White', bg='dark red', state=DISABLED).place(x=160, y=50)

    else:
        imagelabel = Label(imageframe, image=imagesliste[imagenum-1])
        imagename = Button(root, text=classnames[imagenum-1], bd=3, relief=SUNKEN, width=5, height=1,command=lambda: openlevel(imagenum-1)).place(x=182, y=10)
        trackbutton = Button(root, text="track this person", bd=3, relief=SUNKEN, width=15, height=1,fg="white",bg="black",
                             command=lambda :cam2whototrack(cam2trackdeslist, cam2trackclassname, cam2imgtotrack,
                                                    classnames2[imagenum-1])).place(x=138, y=277)

    imagelabel.grid(row=0, column=2, columnspan=3)

    #forward(imagenum + 1)


def deleteall():
    global path
    global nexttbtn
    global backtbtn
    global removetbtn
    global removealltbtn
    global imagename
    global  trackbutton
    myList = os.listdir(path)
    for each in myList:
        os.remove(path+'/'+each)

    Process(target=extractdata(classnames, imagesliste,classnames2)).start()
    backtbtn = Button(framebuttonleft, text="back",fg='White',bg= 'dark green',  command=back, state=DISABLED).place(x=55, y=10)
    removetbtn = Button(framebuttonleft, text="Remove", fg='White',bg= 'dark red', state=DISABLED).place(x=165, y=10)
    nexttbtn = Button(framebuttonleft, text="next", fg='White',bg= 'dark green',  state=DISABLED).place(x=305, y=10)
    removealltbtn = Button(framebuttonleft, text="Remove All", fg='White',bg= 'dark red',  state=DISABLED).place(x=160, y=50)


    imagename = Button(root, text=0, bd=3, relief=SUNKEN, width=5, height=1,command=lambda: openlevel(imagenum-1),state=DISABLED).place(x=182, y=10)
    trackbutton = Button(root, text="track this person", bd=3, relief=SUNKEN, width=15, height=1,fg="white",bg="black",
                         state=DISABLED).place(x=138, y=277)

def forward(imagenum):
    global imagelabel
    global backtbtn
    global nexttbtn
    global imagenombre
    global removetbtn
    global status
    global imagename
    global classnames
    global classnames2
    global cam2trackdeslist, cam2trackclassname, cam2imgtotrack
    global trackbutton
    imagelabel.grid_forget()
    print(imagenum)
    if (len(classnames) == 1):
        backtbtn = Button(framebuttonleft, text="back", fg='White', bg='dark green', command=back, state=DISABLED).place(x=55, y=10)

        nexttbtn = Button(framebuttonleft, text="next", fg='White', bg='dark green', state=DISABLED).place(x=305, y=10)
    else:

        imagelabel = Label(imageframe,image = imagesliste[imagenum-1])


    nexttbtn = Button(framebuttonleft, text="next",fg='White',bg= 'dark green',  command=lambda: forward(imagenum+1)).place(x=305, y=10)
    backtbtn = Button(framebuttonleft, text="back",fg='White',bg= 'dark green',  command=lambda: back(imagenum-1)).place(x=55, y=10)

    if imagenum == len(imagesliste) :
        #print("hahowa dkhl")
        nexttbtn = Button(framebuttonleft, text="next", state=DISABLED)
        nexttbtn.place(x=305, y=10)
        imagename = Button(root, text=classnames[imagenum-1] , bd=3, relief=SUNKEN,width=5, height=1 , command= lambda: openlevel(imagenum-1)).place(x=182, y=10)
        trackbutton = Button(root, text="track this person", bd=3, relief=SUNKEN, width=15, height=1,fg="white",bg="black",
                             command=lambda: cam2whototrack(cam2trackdeslist, cam2trackclassname, cam2imgtotrack,
                                                    classnames2[imagenum-1])).place(x=138, y=277)
    imagelabel.grid(row=0, column=2, columnspan=3)
    status = Label(root ,  text = " image " + str(imagenum) +" of " + str(len(imagesliste)),bd=2 , relief=SUNKEN)
    status.place(x=50 , y=10 )
    removetbtn = Button(framebuttonleft, text="Remove" ,fg='White',bg= 'dark red',  command=lambda: deleteon(imagenum)).place(x=165, y=10)
    if imagenum != len(imagesliste) and len(imagesliste) !=1 :
        imagename = Button(root, text=classnames[imagenum-1] , bd=3, relief=SUNKEN,width=5, height=1 , command= lambda: openlevel(imagenum-1)).place(x=182, y=10)
        trackbutton = Button(root, text="track this person", bd=3, relief=SUNKEN, width=15, height=1,fg="white",bg="black",
                             command=lambda :cam2whototrack(cam2trackdeslist, cam2trackclassname, cam2imgtotrack,
                                                    classnames2[imagenum - 1])).place(x=138, y=277)

    if (len(classnames) == 1):
        backtbtn = Button(framebuttonleft, text="back", fg='White', bg='dark green', command=back, state=DISABLED).place(x=55, y=10)

        nexttbtn = Button(framebuttonleft, text="next", fg='White', bg='dark green', state=DISABLED).place(x=305, y=10)


def back(imagenum):
    global imagelabel
    global backtbtn
    global nexttbtn
    global removetbtn
    global imagenombre
    global status
    global imagename
    global classnames
    global classnames2
    global cam2trackdeslist, cam2trackclassname, cam2imgtotrack
    global trackbutton
    imagelabel.grid_forget()
    imagelabel = Label(imageframe, image=imagesliste[imagenum - 1])
    imagelabel.grid(row=0, column=2, columnspan=3)
    nexttbtn = Button(framebuttonleft, text="next",fg='White',bg= 'dark green', command=lambda: forward(imagenum + 1)).place(x=305, y=10)
    backtbtn = Button(framebuttonleft, text="back",fg='White',bg= 'dark green', command=lambda: back(imagenum - 1)).place(x=55, y=10)
    if imagenum == 1:
        backtbtn = Button(framebuttonleft, text="back",fg='White',bg= 'dark green',  state=DISABLED)
        backtbtn.place(x=55,y=10)

    status = Label(root, text=" image " + str(imagenum) + " of " + str(len(imagesliste)), bd=2, relief=SUNKEN)
    status.place(x=50, y=10)

    imagename = Button(root, text=classnames[imagenum-1], bd=3, relief=SUNKEN, width=5, height=1,command= lambda: openlevel(imagenum-1)).place(x=182, y=10)
    trackbutton = Button(root, text="track this person", bd=3, relief=SUNKEN, width=15, height=1,fg="white",bg="black",
                         command= lambda : cam2whototrack(cam2trackdeslist, cam2trackclassname, cam2imgtotrack,
                                                classnames2[imagenum - 1])).place(x=138, y=277)
    removetbtn = Button(framebuttonleft, text="Remove",fg='White',bg= 'dark red',  command=lambda: deleteon(imagenum)).place(x=165, y=10)

    if (len(classnames) == 1):
        backtbtn = Button(framebuttonleft, text="back", fg='White', bg='dark green', command=back, state=DISABLED).place(x=55, y=10)

        nexttbtn = Button(framebuttonleft, text="next", fg='White', bg='dark green', state=DISABLED).place(x=305, y=10)


#---------------------------detaile Place personne -----------------------------------------------------
def listecamera():
    path = 'hasfoond'
    myList = os.listdir(path)
    return myList

def openfolder(path):
    comm = 'xdg-open ' + path
    os.system(comm)


def openlevel(numperson):
    top = Toplevel(root)
    top.geometry("600x800")
    top.title(classnames[numperson] + ' ' + "Traking info")

    prsnimage = Label(top , image = imagesliste[numperson])
    prsnimage.pack()
    namelabel = Label(top , text=classnames2[numperson] )
    namelabel.pack()
    listecamera()
    listecam = listecamera()
    #print(listecam)
    button_dict = {}
    i=0
    for fl in listecam:

        newpath = 'hasfoond/' + fl
        #print(newpath)
        #print(classnames2[numperson])
        listepath2 = os.listdir(newpath)
        #print(listepath2)
        if classnames2[numperson] in listepath2:
            classnameimg = []

            imgpathfils = newpath +'/'+classnames2[numperson]
            imglist = os.listdir(imgpathfils)
            for imgg in imglist:
                classnameimg.append(os.path.splitext(imgg)[0])

            print(max(classnameimg))
            camlabel = Label(top, text = 'Found It in  : ' + fl , fg="green")
            camlabel.pack()
            lastdt = Label(top,text="Last seen " + max(classnameimg) , fg="black")
            lastdt.pack()
            path3 = newpath + '/' + classnames2[numperson]
            #print("thi in path3" + path3)
            button_dict[i] = Button(top , text="Open Folder" ,fg='White',bg= 'dark red' ,command=lambda path3 = path3 :openfolder(path3))
            button_dict[i].pack()
        else:
            camlabel = Label(top, text = 'Not Found In  : ' + fl , fg ="red" )
            camlabel.pack()
            button_dict[i] = Button(top , text="Open Folder" ,fg='White',bg= 'dark red' ,state=DISABLED)
            button_dict[i].pack()
        i = i + 1





    top.mainloop()

#----------------------Camera 1 -----------------------------------------------------------------

#personne that already foond


cam1foondfolder =[]
def cam1foondfolderfun():
    global cam1foondfolder
    path2 = 'hasfoond/cam1'
    if not os.path.exists(path2):
        os.mkdir(path2)
    listedossier = os.listdir(path2)
    for ds in listedossier:
        cam1foondfolder.append(os.path.splitext(ds)[0])




def cam1findDes(images,cam1desList):


    for img in images:

        kp,des = sft.detectAndCompute(img,None)
        #kp2,des2 = sft.detectAndCompute(img,None)
        #desList.append(des)
        cam1desList.append(des)



def findID(img, cam1desList,thres=7):
    kp2,des2 = sft.detectAndCompute(img,None)
    bf = cv2.BFMatcher()
    matchList=[]
    finalVal = -1
    try:
        for des in cam1desList:
            matches = bf.knnMatch(des, des2, k=2)
            good = []
            for m, n in matches:
                if m.distance < 0.6 * n.distance:
                    good.append([m])
            matchList.append(len(good))
    except:
        pass
    print(matchList)
    if len(matchList)!=0:
        if max(matchList) > thres:
            finalVal = matchList.index(max(matchList))
    return finalVal



def checkwithorb(imgCur , img):
    #print("checking with ORB to get good result ......")
    orb = cv2.ORB_create()
    #imgclass = imgclass + '.jpg'

    #global path
    #imgCur = cv2.imread(f'{path}/{imgclass}',0)

    m = cv2.BFMatcher()
    kp,des = orb.detectAndCompute(img,None)
    kp2,des2 = orb.detectAndCompute(imgCur,None)

    goodpoint =[]
    matches = m.knnMatch(des , des2 , k=2)

    for m , n in matches:
        if m.distance < 0.7 * n.distance:
            goodpoint.append([m])
    print(len(goodpoint))
    if len(goodpoint)  > 3:
        return True
    else:
        return False

#-----------------------------------------------------------------------------------------------------

#### Import Images

cam1desList = []
cam1images = []
cam1classname= []


def cam1checkonfolder(myclassname , myimages,cam1desList):

    path = 'people'
    myList = os.listdir(path)
    myclassname.clear()
    myimages.clear()
    cam1desList.clear()
    for cl in myList:
        imgCur = cv2.imread(f'{path}/{cl}',0)
        #imgCur = cv2.cvtColor(imgCur, cv2.COLOR_BGR2GRAY)
        myimages.append(imgCur)
        myclassname.append(os.path.splitext(cl)[0])
    cam1findDes(myimages,cam1desList)

#-----------------------------------------------------------------------------------------------------

def cam1ifalreadychecked(cam1classname):
    global cam1foondfolder
    if(cam1classname in cam1foondfolder):
        return 1
    else:
        return 0



def cam1createfoolder(cam1classname):
    #global path2
    if(cam1ifalreadychecked(cam1classname) == 0):
        folder = "hasfoond/cam1/" + cam1classname# input nam
        if not os.path.exists(folder):
            os.mkdir(folder)


def  cam1saveimg(cam1classname , img  , count):
    dt = datetime.datetime.now()
    cam1createfoolder(cam1classname)
    cv2.imwrite("hasfoond/cam1/" + cam1classname + "/" + dt.strftime("%Y-%m-%d %H:%M:%S:%f") +  '.jpg', img)


k=0
cam1count = 0
cam1oldclass =""
cam1timer = 0
cam1t=0
cam1t2 = 10  # counter  pf people folder
#cap = cv2.VideoCapture(0)
def cam1show_frame():
    global cam1t2,cam1timer,cam1t,cam1oldclass,cam1ip,cam1ipvar,cam1count,cam2trackdeslist,cam2trackclassname,cam2imgtotrack
    #ip = '192.168.1.4'
    if k == 0:
        print("we cant")
        #lmain.destroy()
        #cap.release()
        return
    else:


        #ret, frame = cap.read()
        if True:
            #success, frame = cap.read()
            req = urllib.request.urlopen('http://' + cam1ipvar + ':8080/shot.jpg')

            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)

            frame = cv2.imdecode(arr, -1)  # 'Load it as it is'

            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            newframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            imgOriginal = newframe.copy()
            img2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if cam1t2 % 10 == 0:
                Process(target=cam2checkonfolder(cam1classname, cam1images, cam1desList,cam2trackclassname,cam2trackdeslist,cam2imgtotrack)).start()

            cam1t2 += 2

            id = findID(img2, cam2trackdeslist)



            if id != -1 and checkwithorb(cam2imgtotrack[id], img2) == True:
                #oldclass = cam1classname[id]
                # set  time to get few cuptureframe
                # print(t)

                if cam1t == 0:

                    #print("hani ndkhlt nsofgardi f cam 1 ")
                    #print(cam1count)
                    cam1saveimg(cam2trackclassname[id], frame, cam1count)

                    # print("has saved")
                cam1timer += 1
                cam1t = cam1timer % 3
                cam1count +=1

                cv2.putText(imgOriginal, cam2trackclassname[id], (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)
                # print("object found ")

            img = PIL.Image.fromarray(imgOriginal)
            resized = img.resize((700, 400), PIL.Image.ANTIALIAS)
            imgtk = ImageTk.PhotoImage(image=resized)


            cam1frams.imgtk=imgtk
            cam1frams.configure(image=imgtk)
            cam1frams.after(10, cam1show_frame)

def cam1startframe():
    global k,cam1ip,cam1ipvar
    k = 1
    cam1ipvar = str(cam1ip.get())
    cam1show_frame()

def cam1stoprecording():
    global k
    global cam1frams,cam1notc

    k = 0
    cam1frams.config(image=cam1notc)

#-----------------------------End of cam 1 ---------------------------------------------------------

#------------------------------- Cam 2 start --------------------------------------------------------


#personne that already foond


cam2foondfolder =[]
def cam2foondfolderfun():
    global cam2foondfolder
    path2 = 'hasfoond/cam2'
    if not os.path.exists(path2):
        os.mkdir(path2)
    listedossier = os.listdir(path2)
    for ds in listedossier:
        cam2foondfolder.append(os.path.splitext(ds)[0])




def cam2findDes(images,cam2desList):


    for img in images:

        kp,des = sft.detectAndCompute(img,None)
        #kp2,des2 = sft.detectAndCompute(img,None)
        #desList.append(des)
        cam2desList.append(des)



def findID(img, cam2desList,thres=7):
    kp2,des2 = sft.detectAndCompute(img,None)
    bf = cv2.BFMatcher()
    matchList=[]
    finalVal = -1
    try:
        for des in cam2desList:
            matches = bf.knnMatch(des, des2, k=2)
            good = []
            for m, n in matches:
                if m.distance < 0.6 * n.distance:
                    good.append([m])
            matchList.append(len(good))
    except:
        pass
    print(matchList)
    if len(matchList)!=0:
        if max(matchList) > thres:
            finalVal = matchList.index(max(matchList))
    return finalVal



def checkwithorb(imgCur , img):
    #print("checking with ORB to get good result ......")
    orb = cv2.ORB_create()
    #imgclass = imgclass + '.jpg'

    #global path
    #imgCur = cv2.imread(f'{path}/{imgclass}',0)

    m = cv2.BFMatcher()
    kp,des = orb.detectAndCompute(img,None)
    kp2,des2 = orb.detectAndCompute(imgCur,None)

    goodpoint =[]
    matches = m.knnMatch(des , des2 , k=2)

    for m , n in matches:
        if m.distance < 0.7 * n.distance:
            goodpoint.append([m])
    print(len(goodpoint))
    if len(goodpoint)  > 3:
        return True
    else:
        return False

#-----------------------------------------------------------------------------------------------------

#### Import Images

cam2desList = []
cam2images = []
cam2classname= []
cam2trackdeslist = []
cam2trackclassname = []
cam2imgtotrack = []
def deletefromtotrack(myclassname,cam2trackclassname,cam2trackdeslist,cam2imgtotrack):


    for arrb in cam2trackclassname:
        if arrb not in myclassname:
            index = cam2trackclassname.index(arrb)
            cam2trackclassname.remove(arrb)
            cam2trackdeslist.pop(index)
            cam2imgtotrack.pop(index)
            # print(arrb)


def cam2checkonfolder(myclassname , myimages,cam2desList,cam2trackclassname,cam2trackdeslist,cam2imgtotrack):

    path = 'people'
    myList = os.listdir(path)
    myclassname.clear()
    myimages.clear()
    cam2desList.clear()
    for cl in myList:
        imgCur = cv2.imread(f'{path}/{cl}',0)
        #imgCur = cv2.cvtColor(imgCur, cv2.COLOR_BGR2GRAY)
        myimages.append(imgCur)
        myclassname.append(os.path.splitext(cl)[0])
    cam2findDes(myimages,cam2desList)
    deletefromtotrack(myclassname ,cam2trackclassname,cam2trackdeslist,cam2imgtotrack)

cam2checkonfolder(cam2classname,cam2images,cam2desList,cam2trackclassname,cam2trackdeslist,cam2imgtotrack)
#-----------------------------------------------------------------------------------------------------

def cam2ifalreadychecked(cam2classname):
    global cam2foondfolder
    if(cam2classname in cam2foondfolder):
        return 1
    else:
        return 0



def cam2createfoolder(cam2classname):
    #global path2
    if(cam2ifalreadychecked(cam2classname) == 0):
        folder = "hasfoond/cam2/" + cam2classname# input nam
        if not os.path.exists(folder):
            os.mkdir(folder)


def cam2saveimg(cam2classname , img  , count):

    cam2createfoolder(cam2classname)
    dt = datetime.datetime.now()
    cv2.imwrite("hasfoond/cam2/" + cam2classname + "/" + dt.strftime("%Y-%m-%d %H:%M:%S:%f") +  '.jpg', img)



def cam2whototrack(cam2trackdeslist,cam2trackclassname,cam2imgtotrack,parsnclassname):
    global cam2desList,cam2classname,cam2images,classnames2

    if parsnclassname not in cam2trackclassname:

        index = classnames2.index(parsnclassname)
        #print(len(cam2desList))
        cam2trackdeslist.append(cam2desList[index])
        cam2trackclassname.append(parsnclassname)
        cam2imgtotrack.append(cam2images[index])
        print(cam2trackclassname)




z=0

cam2count = 0
cam2oldclass =""
cam2timer = 0
cam2t=0
cam2t2 = 10  # counter  pf people folder
#cap = cv2.VideoCapture(0)
def cam2show_frame():
    global cam2t2,cam2timer,cam2t,cam2oldclass,cam2count,cam2ip,cam2ipvar,cam2trackdeslist,cam2trackclassname,cam2imgtotrack
    #ip = '192.168.1.4'
    if z == 0:
        #print("we cant")

        return
    else:


        #ret, frame = cap.read()
        if True:
            #success, frame = cap.read()
            req = urllib.request.urlopen('http://' + cam2ipvar + ':8080/shot.jpg')

            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)

            frame = cv2.imdecode(arr, -1)  # 'Load it as it is'

            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            newframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            imgOriginal = newframe.copy()
            img2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if cam2t2 % 10 == 0:
                Process(target=cam2checkonfolder(cam2classname, cam2images, cam2desList,cam2trackclassname,cam2trackdeslist,cam2imgtotrack)).start()

            cam2t2 += 2

            id = findID(img2, cam2trackdeslist)




            if id != -1 and checkwithorb(cam2imgtotrack[id], img2) == True:
                oldclass = cam2classname[id]
                # set  time to get few cuptureframe
                # print(t)

                if cam2t == 0:
                    cam2saveimg(cam2trackclassname[id], frame, cam2count)
                    # print("has saved")
                cam2timer += 1
                cam2t = cam2timer % 3

                cam2count += 1
                cv2.putText(imgOriginal, cam2trackclassname[id], (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)
                # print("object found ")

            img = PIL.Image.fromarray(imgOriginal)
            resized = img.resize((700, 400), PIL.Image.ANTIALIAS)
            imgtk = ImageTk.PhotoImage(image=resized)
            cam2frams.imgtk = imgtk
            cam2frams.configure(image=imgtk)
            cam2frams.after(10, cam2show_frame)

def cam2startframe():
    global z,cam2ip,cam2ipvar
    z = 1
    cam2ipvar = str(cam2ip.get())
    cam2show_frame()

def cam2stoprecording():
    global z
    global cam2frams, cam2notc
    z = 0
    cam2frams.config(image=cam2notc)


# ----------------------------- End of Cam2 ---------------------------------------------------------

#___________________________Yolo Mask _______________________________________________________________
# ----------------------------------  Camera Label --------------------------------------
#lmain = Label(root).place(x=750,y=40,width=700,height=400)

#cam1frams = Frame(root,bg="red").place(x=410,y=480,width=700,height=400)
#cam2frams = Frame(root,bg="red").place(x=1120,y=480,width=700,height=400)
# ----------------------- Compartion Zone ------------------------------------------

desList = []
images = []

classes = []
with open("classes.txt", "r") as f:
    classes = f.read().splitlines()

net = cv2.dnn.readNet('yolov4-custom_last.weights', 'yolov4-custom.cfg')
font = cv2.FONT_HERSHEY_PLAIN
colors = np.random.uniform(0, 255, size=(100, 3))
count = 0
prsn_count = 10
t2 = 10

#mystring = StringVar(root)

yolocount=0



def yolofindDes(images,desList):

    for img in images:
        kp,des = sft.detectAndCompute(img,None)
        #kp2,des2 = sft.detectAndCompute(img,None)
        #desList.append(des)
        desList.append(des)

def newprsadd(img,dt):
    top = Toplevel(root)
    top.geometry("900x200")
    top.title( "someone isn't wearing a mask")
    warning = ImageTk.PhotoImage(Image.open('warning.png'))

    namelabel = Label(top, text="DATE : "+ dt ,font=("Arial", 25) ,fg ="red" )
    namelabel.pack()
    namelabel = Label(top, text="if you want to track this person please click on 'track this person' in the left side",font=("Arial", 15) )
    namelabel.pack()


def yolofindID(img,desList,count,thres=5):
    dt = datetime.datetime.now()
    kp2,des2 = sft.detectAndCompute(img,None)
    bf = cv2.BFMatcher()
    matchList=[]
    finalVal = -1
    maxv = 3
    try:
        for des in desList:
            matches = bf.knnMatch(des, des2, k=2)
            good = []
            for m, n in matches:
                if m.distance < 0.5 * n.distance:
                    good.append([m])
            matchList.append(len(good))
    except:
        pass
    print(matchList)
    if len(matchList)!= 0:
        if max(matchList) > thres:
            finalVal = matchList.index(max(matchList))
            #maxv = max(matchList)
    print("ha final val")
    print(finalVal)
    print("bin")
    if finalVal == -1:
        if maxv % 3 == 0:
            print("hani dkhlt")
            cv2.imwrite('people/' + dt.strftime("%Y-%m-%d%H:%M:%S:%f") + '.jpg', img)
            newprsadd(img , dt.strftime("%Y-%m-%d %H:%M:%S:%f"))
            print("chekc sofgarde")
        maxv += 1

def yolocheckonfolder(myimages,listedes):

    path = 'people'
    myList = os.listdir(path)
    myimages.clear()
    listedes.clear()
    for cl in myList:
        imgCur = cv2.imread(f'{path}/{cl}',0)
        myimages.append(imgCur)
        #myclassname.append(os.path.splitext(cl)[0])
    yolofindDes(myimages,desList)





def yoloshow_frame():

    global t2,prsn_count,count,yoloipvar
    global yolocount
    #ip = '192.168.1.4'
    print(yolocount)
    #cap = cv2.VideoCapture(0)
    if True and yolocount == 1:
        req = urllib.request.urlopen('http://' + yoloipvar + ':8080/shot.jpg')
        #print('http://' + yoloipvar + ':8080/shot.jpg')

        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)

        frame = cv2.imdecode(arr, -1)  # 'Load it as it is'
        #success, frame = cap.read()

        height, width, _ = frame.shape
        imgOriginal = frame.copy()

        if t2 % 10 == 0:
            Process(target=yolocheckonfolder(images, desList)).start()

        t2 += 2

        blob = cv2.dnn.blobFromImage(imgOriginal, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
        net.setInput(blob)
        output_layers_names = net.getUnconnectedOutLayersNames()
        layerOutputs = net.forward(output_layers_names)

        boxes = []
        confidences = []
        class_ids = []

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.2:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append((float(confidence)))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)
        # print(len(indexes))

        if len(indexes) > 0:

            for i in indexes.flatten():
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])

                if label == "bad":
                    # print("what is i {}".format(i) )
                    confidence = str(round(confidences[i], 2))
                    color = colors[i]
                    x1 = x - 100
                    x2 = x + w + 150
                    y1 = y - 70
                    y2 = y + h + 250

                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    img2 = frame.copy()



                    cv2.putText(frame, label + " " + confidence, (x, y + 20), font, 2, (255, 255, 255), 2)


                    if x1 > 0 and x2 > 0 and y1 > 0 and y2 > 0:
                        ROI = img2[y1:y2, x1:x2]


                        if prsn_count % 10 == 0:
                            Process(target=yolofindID(ROI, desList, count)).start()
                        prsn_count += 2
                        count += 1

        img = PIL.Image.fromarray(frame)
        resized = img.resize((700, 400), PIL.Image.ANTIALIAS)
        imgtk = ImageTk.PhotoImage(image=resized)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(10, yoloshow_frame)
    else:
        return

def yolostartframe():
    global yolocount,yoloip,yoloipvar
    yolocount = 1
    yoloipvar=str(yoloip.get())
    #print('http://' + yoloipvar + ':8080/shot.jpg')
    yoloshow_frame()

def yolostoprecording():
    global yolocount
    global lmain, notconncted

    yolocount = 0
    lmain.config(image=notconncted)








#_____________________end of yolomask func '-----------------------------------------------------------







if len(classnames) != 0 :

    imagename = Button(root, text=classnames[0], bd=3, relief=SUNKEN ,width=5, height=1 ,command= lambda: openlevel(0)).place(x=182, y=10)

#button we need for the veiwer palce ------------------------------------------------------------------------------------------------------------------------
framebuttonleft = Frame(root, bd=2 , relief=SUNKEN)
framebuttonleft.place(x=0,y=310,width=400 , height =100)
refreshbtn = Button(root,text="refresh" , fg='black',bg= 'yellow', command= lambda : refresh() ).place(x = 300 , y = 15)

if len(classnames) == 0  :


    backtbtn = Button(framebuttonleft, text="back",fg='White',bg= 'dark green', command=back, state=DISABLED).place(x=55, y=10)

    nexttbtn = Button(framebuttonleft, text="next",fg='White',bg= 'dark green',  state=DISABLED).place(x=305, y=10)
    removetbtn = Button(framebuttonleft, text="Remove", fg='White', bg='dark red', state=DISABLED).place(x=165, y=10)
    removealltbtn = Button(framebuttonleft, text="Remove All",fg='White',bg= 'dark red',  state=DISABLED).place(x=160, y=50)
    trackbutton = Button(root, text="track this person", bd=3, relief=SUNKEN, width=15, height=1,fg="white",bg="black",
                         state=DISABLED).place(x=138, y=277)
else:

    backtbtn = Button(framebuttonleft,text = "back" , fg='White',bg= 'dark green', command=back , state= DISABLED).place(x=55,y=10)
    removetbtn = Button(framebuttonleft,text = "Remove" , fg='White',bg= 'dark red',command=lambda: deleteon(1) ).place(x=165,y=10)
    nexttbtn = Button(framebuttonleft,text = "next",fg='White',bg= 'dark green', command=lambda: forward(2)).place(x=305,y=10)
    removealltbtn = Button(framebuttonleft,text = "Remove All" ,fg='White',bg= 'dark red', command=lambda : deleteall()).place(x=160,y=50)
    trackbutton = Button(root, text="track this person", bd=3, relief=SUNKEN, width=15, height=1,fg="white",bg="black",
                         command=lambda: cam2whototrack(cam2trackdeslist, cam2trackclassname, cam2imgtotrack,
                                                        classnames2[0])).place(x=138, y=277)
    if (len(classnames) == 1):
        backtbtn = Button(framebuttonleft, text="back", fg='White', bg='dark green', command=back, state=DISABLED).place(x=55, y=10)

        nexttbtn = Button(framebuttonleft, text="next", fg='White', bg='dark green', state=DISABLED).place(x=305, y=10)
#rightbottomframe.pack()

# Tree View Derectorie function __________________________________________________________

def SUBS(path2, parent):
    for p in os.listdir(path2):
        abspath = os.path.join(path2, p)
        parent_element = tree.insert(parent, 'end', text=p, open=True)
        if os.path.isdir(abspath):
            SUBS(abspath, parent_element)



# -------------------------  Camera Start Button
startcam1btn = Button(root , bg ="black" , text="Start " , fg="WHITE",command=yolostartframe).place(x=1000 , y=430)
startcam2btn = Button(root , bg ="black" , text="Start " , fg="WHITE",command=cam1startframe).place(x=630 , y=865)
startcam3btn = Button(root , bg ="black" , text="Start " , fg="WHITE",command=cam2startframe).place(x=1360 , y=865)
stopcam1btn = Button(root , bg ="Red" , text="Stop " , fg="WHITE",command=yolostoprecording).place(x=1190 , y=430)
stopcam2btn = Button(root , bg ="Red" , text="Stop " , fg="WHITE",command=cam1stoprecording).place(x=820 , y=865)
stopcam3btn = Button(root , bg ="Red" , text="Stop " , fg="WHITE",command=cam2stoprecording).place(x=1560 , y=865)


#button de suivie :


#----------------------------Camras Ip Entry -----------------------------------------------
yoloip=StringVar(root)
cam1ip=StringVar(root)
cam2ip=StringVar(root)
yoloipvar = ''
cam1ipvar = ''
cam2ipvar = ''
yoloipen = Entry(root,textvariable = yoloip,width=50 ,fg="blue",bd=3,selectbackground='violet').place(x=930 , y=410)
cam1ipen = Entry(root,textvariable = cam1ip,width=50,fg="blue",bd=3,selectbackground='violet').place(x=580 , y=845)
cam2ipen = Entry(root,textvariable = cam2ip,width=50,fg="blue",bd=3,selectbackground='violet').place(x=1300 , y=845)

leftframe2 = Frame(root ,bg="yellow")
leftframe2.place(x=0 , y=451 , width=400 , height = 500 )

path2 = "hasfoond"
tree = ttk.Treeview(leftframe2 ,height=15)
tree.pack(expand=YES,fill=BOTH)
tree.heading("#0" ,text="Directory")
root2 = tree.insert('', 'end', text=path2, open=True)
SUBS(path2, root2)


root.mainloop()










