# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 09:40:50 2022

@author: rahul
"""
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import tkinter.messagebox
from tkinter import messagebox as mb 
import os
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

global input_service,input_years,input_avgcst,input_resource,input_dtime,df,df2

class Homepage:
    def __init__(self,master,*args,**kwargs):
        self.master=master
        master.title("Seller foreteller")
        self.heading=Label(master,text="Welcome to SELLER FORETELLER",font=('arial 35 bold italic'),fg='teal')
        self.heading.place(x=300,y=0)
        #button for navigating to prediction page
        self.btn_add=Button(master,text='PREDICT',width=10,height=2,font=('arial 10 bold italic'),bg='steelblue',fg='white',command=self.predict)
        self.btn_add.place(x=600,y=600)
        
        self.name_l=Label(master,text="Location of Dataset",font=('arial 18 bold'))
        self.name_l.place(x=0,y=140)
        
        Button(master,text='BROWSE',width=10,height=2,font=('arial 10 bold italic'),fg='white',bg='violet',command=self.open_file).place(x=620,y=130)
        Button(master,text='IMPORT',width=10,height=2,font=('arial 10 bold italic'),fg='white',bg='red',command=self.import_data).place(x=400,y=195)

        self.heading=Label(master,text="Provide Inputs:",font=('arial 25 bold italic'),fg='teal')
        self.heading.place(x=200,y=275)
 
        self.cp_l = Label(master, text="Type of service ", font=('arial 18 bold'))
        self.cp_l.place(x=0, y=345)
         
        self.cp_l = Label(master, text="Use records, since year ", font=('arial 18 bold'))
        self.cp_l.place(x=0, y=395)
         
        self.cp_l = Label(master, text="Cost of investment ", font=('arial 18 bold'))
        self.cp_l.place(x=0, y=445)
         
        self.cp_l = Label(master, text="No.of.resources req ", font=('arial 18 bold'))
        self.cp_l.place(x=0, y=495)
         
        self.cp_l = Label(master, text="Expected delivery time ", font=('arial 18 bold'))
        self.cp_l.place(x=0, y=545)
         
 
        #enteries for extraction
        
        self.source_path_etry = Entry(master, width=25, font=('arial 18 bold'))
        self.source_path_etry.place(x=280, y=140)
 
        self.type_service = Entry(master, width=25, font=('arial 18 bold'))
        self.type_service.place(x=280, y=345)
         
        self.since_year = Entry(master, width=25, font=('arial 18 bold'))
        self.since_year.place(x=280, y=395)
         
        self.cost_invst = Entry(master, width=25, font=('arial 18 bold'))
        self.cost_invst.place(x=280, y=445)
         
        self.count_resource = Entry(master, width=25, font=('arial 18 bold'))
        self.count_resource.place(x=280, y=495)
         
        self.del_time = Entry(master, width=25, font=('arial 18 bold'))
        self.del_time.place(x=280, y=545)

        #text box for the log
        self.tbBox=Text(master,width=60,height=35)
        self.tbBox.place(x=750,y=75)
        self.tbBox.insert(END,"\n\n1.Use browse button and chose the data file\n\n2.cilck on IMPORT to get data and preprocess it \n\n3 Fill all the input fields\n\n4.click on PREDICT to get the plots\n\n5.The plot shows companies in ranked order with best\n from the left")
        self.name_l=Label(master,text="scroll down in the dialog box\n in case of too much data",font=('arial 13 bold'))
        self.name_l.place(x=900,y=650)
        
        self.master.bind('&lt;Return&gt;', self.open_file)
        self.master.bind('&lt;Return&gt;', self.import_data)
        self.master.bind('&lt;Return&gt;', self.predict)
        
    def open_file(self):
        file=filedialog.askopenfile(mode='r')
        if file:
            filepath = os.path.abspath(file.name)
            self.source_path_etry.insert(0,filepath)
            
    def import_data(self):
        global df
        path = self.source_path_etry.get()
        ext = None
        #Getting file as input
        for ch in path:
        
            if ch=='.':
                ext = path[path.index(ch)+1:]
                
            if ext == 'csv':
                try:
                    df= pd.read_csv(path,na_values=['NULL'])
                    self.tbBox.delete('1.0', END)
                    self.tbBox.insert(END,'Data has been imported sucessfully\n')

                except:
                    
                    self.tbBox.insert(END,'Error while reading csv file ')
                    
            elif ext == 'tsv':
                try:
                    df= pd.read_csv(path,sep='\t')
                    self.tbBox.delete('1.0', END)
                    self.tbBox.insert(END,'Data has been imported sucessfully\n')
                except:
                   self.tbBox.insert(END,'Error while reading tsv file ')  
                    
            elif ext == 'json':
                try:
                    df = pd.read_json(path,encoding='utf-8-sig')
                    self.tbBox.delete('1.0', END)
                    self.tbBox.insert(END,'Data has been imported sucessfully\n')
                except:
                    self.tbBox.insert(END,'Error while reading json file ') 
            try:
                df.dropna(inplace=True)
                df.drop_duplicates(inplace=True)
                service = list(set(df["Service"]))
                year = list(set(df["Years"]))
                self.tbBox.insert(END,'\n\t SERVICES\n')
                for s in service:
                    self.tbBox.insert(END,'\n')
                    self.tbBox.insert(END,s)
                    self.tbBox.insert(END,'\n')
                self.tbBox.insert(END,'\n\t YEARS\n')
                for y in year:
                    self.tbBox.insert(END,'\n')
                    self.tbBox.insert(END,y)
                    self.tbBox.insert(END,'\n')
            except:
        
                self.tbBox.insert(END,"Error while reteving data")
    def predict(self):
        
        global input_service,input_years,input_avgcst,input_resource,input_dtime ,df,df2
        
        input_service = self.type_service.get()
        self.tbBox.delete('1.0', END)
        try:
            
            input_years = int(self.since_year.get())
        except:
           self.tbBox.insert(END,"\nInteger values are expected for years")
        try:    
            input_avgcst = int(self.cost_invst.get())
        except:
           self.tbBox.insert(END,"\nInteger values are expected for cost of invstmt ")
        try:
            input_resource = int(self.count_resource.get())
        except:
            self.tbBox.insert(END,"\nInteger values are expected count of resources")
        try: 
            input_dtime = int(self.del_time.get())
        except:
           self.tbBox.insert(END,"\nInteger values are expected delivery time")
           
        avgcst_max = df['Avg_Cost'].max()
        avgdtime_max = df['Average_Delivery_Time'].max()
        escalation_max = df['Number_of_Escalations'].max()
        cstperqty_max = df['Avg_Cost']/df['Resources'] 
        cstperqty_max = cstperqty_max.max()
        #year_max = df['Years'].max()

        #Calculation of weight for each record
        df["Weight"] =  100-((df["Avg_Cost"]/df["Resources"])/cstperqty_max)*100 +(100-((df["Average_Delivery_Time"]/avgdtime_max)*100))+100-(df["Number_of_Escalations"]/escalation_max)*100+df["Rating"]
        df["Weight"] = df["Weight"]/4
        
        df2 = df[df["Service"]==input_service]
        flag_plot = True
        if len(df2)==0:
            flag_plot=False
            self.tbBox.insert(END,"\nNo data matched for the given service")
        df2 = df2[df2["Years"]>=input_years]
        if len(df2)==0:
            flag_plot=False
            self.tbBox.insert(END,"\nNo data matched for the given range of years")
        df2 = df2[df2['Avg_Cost']/df2['Resources'] <= input_avgcst/input_resource] 
        if len(df2)==0:
            flag_plot=False
            self.tbBox.insert(END,"\nNo data of feasible solution for the given budget and no.of.resources")
       
        df2["Costperunit"] = df2['Avg_Cost']/df2['Resources']
        df2.sort_values(by=['Weight'],ascending=False,inplace=True)
        if df2.shape[0]>=5:
             df2 = df2.head(5)
       
        if flag_plot:
            self.master=gotopredict(self.master)
        
        


class Prediction:
    
    def __init__(self,master,*args,**kwargs):
        
            
        figure1 = plt.Figure(figsize=(5,4), dpi=100)
        ax1 = figure1.add_subplot(111)
        plt1 = FigureCanvasTkAgg(figure1, root)
        plt1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        df2.plot(kind='line',x="Supplier_Name",y='Costperunit' ,color='red',ax=ax1)
        ax1.set_title('CostperUnit Vs. Supplier')

        figure2 = plt.Figure(figsize=(5,4), dpi=100)
        ax2 = figure2.add_subplot(111)
        plt2 = FigureCanvasTkAgg(figure2, root)
        plt2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        df2.plot(kind='line',x="Supplier_Name",y='Average_Delivery_Time' ,color='yellow',ax=ax2)
        ax2.set_title('Delivery time Vs. Supplier')

        figure3 = plt.Figure(figsize=(5,4), dpi=100)
        ax3 = figure3.add_subplot(111)
        df2.plot(kind='bar',x="Supplier_Name",y='Rating' ,ax=ax3)
        plt3 = FigureCanvasTkAgg(figure3, root) 
        plt3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        ax3.set_title('Rating Vs. Supplier')
        
        
def gotopredict(master):    
    master.geometry("1366x768+0+0")
    master.title("RANKED VISUVALIZATION(BEST BEING AT LEFTMOST)")
    b=Prediction(master)
    master.mainloop()

root=Tk()
b=Homepage(root)
root.geometry("1366x768+0+0")
root.mainloop()