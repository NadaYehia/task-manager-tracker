#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import pandas as pd
import numpy as np
import tkinter as tk
import time
from datetime import datetime
from  tkinter import ttk


# In[2]:


# add task

class Add_task:
    
    def __init__(self,data,username,password):
        
        self.data=data
        self.username=username
        self.password=password
        self.window1=tk.Tk()
        self.window1.geometry("400x400")

        self.task_name_var=tk.StringVar()
        self.task_descrip_var=tk.StringVar()

        self.task_name_label = tk.Label(self.window1, text = 'Task name', font=('calibre',10, 'bold'))

        self.task_name_entry = tk.Entry(self.window1,textvariable = self.task_name_var, font=('calibre',10,'normal'))

        self.task_descrip_label = tk.Label(self.window1, text = 'Task description', font = ('calibre',10,'bold'))

        self.task_descrip_entry=tk.Entry(self.window1, textvariable =self.task_descrip_var, font = ('calibre',10,'normal'))

        self.add_btn=tk.Button(self.window1,text = 'Add', command = self.add_record)


        self.task_name_label.grid(row=0,column=0)
        self.task_name_entry.grid(row=0,column=1)
        self.task_descrip_label.grid(row=1,column=0)
        self.task_descrip_entry.grid(row=1,column=1)
        self.add_btn.grid(row=2,column=1)

    def add_record(self):

        task_name=self.task_name_var.get()
        task_descrip=self.task_descrip_var.get()

        now = datetime.now()
        formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        task_creation_date=formatted_date_time
        task_status='ongoing'

        df=self.data[(self.data.User_name==self.username)&(self.data.Password==self.password)]


        if (df.Date_created.isna().all()):
            # the user has no assigned tasks then add data to an existing row

            self.data.loc[(self.data.User_name==self.username)&(self.data.Password==self.password),'Task_name']=task_name
            self.data.loc[(self.data.User_name==self.username)&(self.data.Password==self.password),'Task_description']=task_descrip
            self.data.loc[(self.data.User_name==self.username)&(self.data.Password==self.password),'Date_created']=task_creation_date
            self.data.loc[(self.data.User_name==self.username)&(self.data.Password==self.password),'Status']=task_status
            


        else: # add new row
            self.data=self.data.append({'User_name':self.username,'Password':self.password,
                             'Task_name':task_name, 'Task_description':task_descrip,
                              'Date_created':task_creation_date, 'Status':task_status},ignore_index=True)
            

        
        # if the user missed any of the task enteries, but they created a task
        # fill the '' with missing not nans
        self.data.replace('', 'missing', inplace=True)
        self.data.to_csv('users_credentials.csv',index=False)
        self.window1.destroy()
        
    
               


# In[3]:


# view tasks for this user
class View_task:
    def __init__(self,data,username,password):
        
        self.data=data
        self.username=username
        self.password=password
        
        self.df=self.data[(self.data.User_name==username)&(self.data.Password==password)]
                
        self.window1=tk.Tk()
        self.window1.geometry("400x400")
        self.my_table=tk.ttk.Treeview()
        self.my_table['columns'] = ('Task_name', 'Task_description', 'Date_created', 'Status')

        self.my_table.column("#0", width=10,  stretch=False)
        self.my_table.column("Task_name",anchor=tk.CENTER, width=80)
        self.my_table.column("Task_description",anchor=tk.CENTER,width=120)
        self.my_table.column("Date_created",anchor=tk.CENTER,width=80)
        self.my_table.column("Status",anchor=tk.CENTER,width=80)

        self.my_table.heading("#0",text="",anchor=tk.CENTER)
        self.my_table.heading("Task_name",text="Task_name",anchor=tk.CENTER)
        self.my_table.heading("Task_description",text="Task_description",anchor=tk.CENTER)
        self.my_table.heading("Date_created",text="Date_created",anchor=tk.CENTER)
        self.my_table.heading("Status",text="Status",anchor=tk.CENTER)
        
        # Create a context menu
        self.context_menu = tk.Menu(self.window1, tearoff=0)
        self.context_menu.add_command(label="delete task", command=self.menu_action_delete)
        self.context_menu.add_command(label="mark task completed", command=self.menu_action_mark)
        
        # Bind the right-click event to the Treeview
        self.my_table.bind("<Button-1>", self.on_right_click)

        
        for i in range (len(self.df)):
            
            
            self.my_table.insert(parent='',index='end',iid=i,text='',
            values=(self.df.iloc[i]['Task_name'],self.df.iloc[i]['Task_description'],self.df.iloc[i]['Date_created'],self.df.iloc[i]['Status']) )
            

        self.my_table.pack()
        
    def on_right_click(self,event):
        
        # Select the item under the mouse
        item = self.my_table.identify_row(event.y)
        if item:
            self.my_table.selection_set(item)
            # Display the context menu
            self.context_menu.post(event.x_root, event.y_root)

    def menu_action_delete(self):
        
        selected_item = self.my_table.selection()[0]
        d_index=self.df.index[int(selected_item)]
        self.data.drop(d_index,inplace=True)
        
        #delete it from the cvs file too
        self.data.to_csv('users_credentials.csv',index=False)
        
        self.my_table.delete(selected_item)
        
    def menu_action_mark(self):
        
        selected_item = self.my_table.selection()[0]
        d_index=self.df.index[int(selected_item)]
        
        self.data.loc[d_index,'Status']='completed'
        
        #delete it from the cvs file too
        self.data.to_csv('users_credentials.csv',index=False)
        
        self.my_table.set(selected_item,'Status','completed')
        
        
        

        
   


# In[4]:


class Login:
       
       def __init__(self,root):
           self.attempts=0
           self.root=root
           self.root.geometry("400x400") 
           # declaring string variable
           # for storing name and password
           self.name_var=tk.StringVar()
           self.pass_var=tk.StringVar()
           # creating a label for 
           # name using widget Label
           self.name_label = tk.Label(root, text = 'Username', font=('calibre',10, 'bold'))

           # creating a entry for input
           # name using widget Entry
           self.name_entry = tk.Entry(root,textvariable = self.name_var, font=('calibre',10,'normal'))

           # creating a label for password
           self.passw_label = tk.Label(root, text = 'Password', font = ('calibre',10,'bold'))

           # creating a entry for password
           self.passw_entry=tk.Entry(root, textvariable = self.pass_var, font = ('calibre',10,'normal'), show = '*')

           # creating a button using the widget 
           # Button that will call the submit function 
           self.sub_btn=tk.Button(root,text = 'Submit', command = self.user_authentication)

           # placing the label and entry in
           # the required position using grid
           # method
           self.name_label.grid(row=0,column=0)
           self.name_entry.grid(row=0,column=1)
           self.passw_label.grid(row=1,column=0)
           self.passw_entry.grid(row=1,column=1)
           self.sub_btn.grid(row=2,column=1)


           
       def user_authentication(self):
           username=self.name_var.get()
           password=self.pass_var.get()

           data=pd.read_csv('users_credentials.csv')
           df_user= data[(data.User_name==username) & (data.Password==password)]
           
           if (df_user.empty):
               self.attempts += 1
               print(self.attempts)
               
               if(self.attempts>3): 
                   
                   self.sub_btn.destroy()
                   self.register_label=tk.Label(root,text= 'Please register', font=('calibre',20,'bold'))
                   self.reg_btn=tk.Button(root,text='register',command=self.register_func)
                   
                   self.name_label.grid(row=1,column=0)
                   self.name_entry.grid(row=1,column=1)
                   self.passw_label.grid(row=2,column=0)
                   self.passw_entry.grid(row=2,column=1)
                   self.reg_btn.grid(rows=3,column=1)
                   

           else:
               print('access granted')
               action_obj=Action(data,username,password)
               action_obj.select_action()
               
               
       def register_func(self):
           username=self.name_var.get()
           password=self.pass_var.get()
           data=pd.read_csv('users_credentials.csv')
           #write the new user to the csv file
           data=data.append({'User_name':username,'Password':password},ignore_index=True)
           data.replace('',np.nan,inplace=True)
           data.to_csv('users_credentials.csv',index=False)
           action_obj=Action(data,username,password)
           action_obj.select_action()
  
   


# In[5]:


class Action:
    
    def __init__(self, data, username,password):
        
        self.data = data
        self.username = username
        self.password=password
        self.root2=tk.Tk()
        
    def select_action(self):
        root.destroy()
        
        self.root2.geometry("400x400") 
        listbox = tk.Listbox(self.root2, height = 10, 
                  width = 50)
        # insert elements by their
        # index and names.
        listbox.pack()
        listbox.insert(1, "add task")
        listbox.insert(2, "view my tasks (delete/mark complete)")
        
        listbox.bind('<Double-1>',self.selected_item)
        

    def selected_item(self,evt):
        
        w = evt.widget
        action = int(w.curselection()[0])
        self.data=pd.read_csv('users_credentials.csv')
        
        if(action==0):
            
            add_task_obj=Add_task(self.data,self.username,self.password)
            
        elif (action==1):
            View_task(self.data,self.username,self.password)
            
  


# In[6]:


root=tk.Tk()
login_obj=Login(root)

# performing an infinite loop 
# for the window to display
root.mainloop()         


# In[ ]:




