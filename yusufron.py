import streamlit as st
import firebase_admin
from firebase_admin import db
import pandas as pd
from datetime import datetime
@st.cache
def runonce():
    cred=firebase_admin.credentials.Certificate('key.json')
    app=firebase_admin.initialize_app(cred,{'databaseURL':'https://python-cccbe-default-rtdb.firebaseio.com/'})
runonce()

mymenu=st.sidebar.selectbox("Menu",("Home","Admin Login","Student Login","Create New Account"))
st.title('Library Management System')
if(mymenu=="Admin Login"):
    if'adminlogin' not in st.session_state:
        st.session_state['adminlogin']=False
    data=db.reference("/Admin").get()
    with st.form('Login Form'):
        id=st.text_input('Enter Admin Id')
        password=st.text_input('Enter Admin Password') 
        loginbutton=st.form_submit_button('Login')
        if loginbutton:
            for i,p in data.items():
                if(i==id and p==password):
                    st.session_state['adminlogin']=True
            if(st.session_state['adminlogin']==False):
                st.write("Incorrect ID or password")
 
    if(st.session_state['adminlogin']==True):
        st.write("Login Successful")
        choice=st.selectbox("Options",("None","Issued Book","Add New Book"))
        if(choice=="Issued Book"):
            ref2=db.reference("/Issue Book/").get()
            df=pd.DataFrame.from_dict(ref2,orient='index')
            st.table(data=df)
        elif(choice=="Add New Book"):
            with st.form("Add Book"):
                bookid=st.text_input("Enter Book ID")
                bookname=st.text_input("Enter Book Name")
                authorname=st.text_input("Enter Author Name")
                button=st.form_submit_button("Add Book")
                if button:
                    ref3=db.reference("/Books/"+bookname)
                    ref3.update({"Bookid":bookid,"Author":authorname})
     
elif(mymenu=="Student Login"):
    if 'login' not in st.session_state:
        st.session_state['login']=False
        st.session_state['studentid']=''
    data=db.reference("/Student").get()
    with st.form('Login Form'):
        st.session_state['studentid']=st.text_input("Enter Student ID")
        password=st.text_input("Enter Password")
        loginbutton=st.form_submit_button("Login")
        if loginbutton:
            for i,p in data.items():
                if(i==st.session_state['studentid'] and p==password):
                    st.session_state['login']=True
            if(st.session_state['login']==False):
                st.write("Incorrect ID or password")
    if(st.session_state['login']==True):
        st.write("Login Successful")
        choice=st.selectbox("Options",("None","Search Book","Issue Book"))
        if(choice=="Search Book"):
            ref2=db.reference("Books").get()
            df=pd.DataFrame.from_dict(ref2,orient='index')
            st.table(data=df)
        elif(choice=="Issue Book"):
            with st.form("Book Issue"):
                bookid=st.text_input("Enter Book ID")
                btn2=st.form_submit_button("Issue Book")
                if btn2:
                    x=''
                    for i in str(datetime.now()):
                        if i not in [':','-','.']:
                            x=x+str(''.join(i))
                    ref3=db.reference("/Issue Book/"+x)
                    ref3.update({"Student ID":st.session_state['studentid'],"Book ID":bookid})
