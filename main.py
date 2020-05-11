#from PyQt5.QtWidgets import QApplication,QDialog
#from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from mplwidget import * 
import numpy as np
import random
import PlotHelper
import pandas as pd
from DataManagment import *
import os
import numpy
from operator import add
import plotly.express as px
from collections import namedtuple
from PyQt5.QtCore import pyqtSlot
from PIL import Image

import dash
import dash_core_components as dcc
import dash_html_components as html
     
class MainWindow(QMainWindow):
    
    def __init__(self):
        
        QMainWindow.__init__(self)
        loadUi('loginpage.ui',self)
        self.setWindowTitle('login page')
        self.BtnLogin.clicked.connect(self.on_pushButton_clicked)
        self.move_to_center()

    @pyqtSlot()
    def on_pushButton_clicked(self):
        db=DataManagment()        
        result=db.is_authenticate(self.txtUserName.text(),self.txtPassword.text())
        db.connect_close()
        if not result:
            self.lblError.setText("The username/Password is incorrect, please try again!")
            return

        self.open_home()

    def move_to_center(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def open_admin_panel(self):

        loadUi("adminpanelsummary.ui",self)
        self.move_to_center()
        self.setWindowTitle("Query designer for Covid19 Dataset")
        self.load_filters_data_summary()
            #self.showFullScreen();


    def open_user_page(self):
        loadUi("userpage.ui",self)
        self.setWindowTitle("View graphs")
        self.move_to_center()
        self.create_buttons()
    
    def clickMethod(self):
        sender = self.sender()
        x=sender.text()
        db=DataManagment()        
        plots=db.get_plotpath(x)
        filepath=plots[0][2]
        im = Image.open(filepath)
        im.show()

    def create_buttons(self):
        db=DataManagment()        
        plots=db.get_plots()
        left=20
        top=80
        i=1
        for plot in plots:
            #creating pushbutton
            pybutton = QCommandLinkButton(plot[1], self)
            QCommandLinkButton.objectName='btn'+str(plot[0])
            pybutton.clicked.connect(self.clickMethod) 
            pybutton.resize(len(plot[1])*15,50)
            if i%11==0:
                left+=400
                top=80
            pybutton.move(left, top)  
            pybutton.show()
            top+=50
            i+=1


    def select_dataset(self):
        self.drpDataset.show()
        self.labelDataset.show()
        self.pushButtonAdmin.hide()
        self.pushButtonUser.hide()
        self.pushButtonContinue.show()


    def load_filters_data_summary(self):
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))
        df = PlotHelper.getSummaryDataset()
        
        # load date data
        self.drpDate.addItem('Any')
        lst=sorted(PlotHelper.get_Dates(df))
        for i in lst:
            self.drpDate.addItem(str(i))


        #Load Country Data
        lst=sorted(PlotHelper.get_Countries(df))
        self.drpCountry.addItem('Any')
        for i in lst:
            self.drpCountry.addItem(i)

        #Load Province Data
        lst=sorted(PlotHelper.get_Province(df))
        self.drpProvince.addItem('Any')
        for i in lst:
            self.drpProvince.addItem(i)

        self.df=df
        #################################################
        self.BtnApply.clicked.connect(lambda: self.update_summary_graph(self.drpTopX.currentText(),self.drpX.currentText(),self.listWidgetY.selectedItems(),self.drpPlotType.currentText(),Date=self.drpDate.currentText(),Country=self.drpCountry.currentText(),Province=self.drpProvince.currentText() ))
        self.BtnSave.clicked.connect(lambda: self.export_plot(self.txtName.text(),self.txtDescription.toPlainText()))
        #self.pushButtonHome.clicked.connect(self.open_home)

    def open_home(self):
        db=DataManagment()        
        roles=db.get_Role(self.txtUserName.text())
        loadUi("Main.ui",self)
        self.setWindowTitle("Main Window")
        self.move_to_center()
        if roles[0][0].lower()=='user':           
            self.actionCreate_Summary_chart.setVisible(False)

        #menu bar actions 
        self.actionCreate_Summary_chart.triggered.connect(self.open_admin_panel)
        self.actionCreate_Geographical_Charts.triggered.connect(self.create_GeoMap)
        self.actionView_Charts.triggered.connect(self.open_user_page)
        self.actionOpen_US_Geographical_Map.triggered.connect(self.create_US_GeoMap)
        self.actionOpen_US_Geographical_Map_Death_Cases.triggered.connect(self.create_US_GeoMap_Death)            
        self.df=None



    def update_summary_graph(self,topx,x,y,plottype,**kwargs):
        df=self.df
        df = PlotHelper.filterDataFrame(df,**kwargs)
        dfy=[]
        self.MplWidget.canvas.axes.clear()

        for i in range(len(y)):
            dfy=df.groupby(x).sum()[y[i].text()].reset_index()
            dfy=dfy.sort_values(by=[y[i].text()], ascending=False)
            dfy=dfy.iloc[0:int(topx)]
               
            if plottype=='bar':
                self.MplWidget.canvas.axes.bar(dfy[x],dfy[y[i].text()],label=y[i].text())
            else:
                self.MplWidget.canvas.axes.plot(dfy[x],dfy[y[i].text()])

        self.MplWidget.canvas.axes.set_xlabel(x, fontsize=10)
        #self.MplWidget.canvas.axes.set_ylabel(y+' cases', fontsize='medium')  
        self.MplWidget.canvas.axes.set_xticklabels(dfy[x], rotation=90)
        self.MplWidget.canvas.axes.legend()
        self.MplWidget.canvas.draw()


    def new_map(self):
        df = pd.read_csv('../novel-corona-virus-2019-dataset/covid_19_data.csv',parse_dates=['Last Update'])
        df.rename(columns={'ObservationDate':'Date', 'Country/Region':'Country' }, inplace=True)
        df_confirmed = pd.read_csv("../novel-corona-virus-2019-dataset/time_series_covid_19_confirmed.csv")
        df_confirmed.rename(columns={'Country/Region':'Country'}, inplace=True)
        df_confirmed = df_confirmed[["Province/State","Lat","Long","Country"]]
        df_temp = df.copy()
        df_temp['Country'].replace({'Mainland China': 'China'}, inplace=True)
        df_latlong = pd.merge(df_temp, df_confirmed, on=["Country", "Province/State"])
        fig = px.density_mapbox(df_latlong, 
                        lat="Lat", 
                        lon="Long", 
                        hover_name="Province/State", 
                        hover_data=["Confirmed","Deaths","Recovered"], 
                        animation_frame="Date",
                        color_continuous_scale="Portland",
                        radius=7, 
                        zoom=0,height=700)
        fig.update_layout(title='Worldwide Corona Virus Cases Time Lapse - Confirmed, Deaths, Recovered',
                          font=dict(family="Courier New, monospace",
                                    size=18,
                                    color="#7f7f7f")
                         )
        fig.update_layout(mapbox_style="open-street-map", mapbox_center_lon=0)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        #self.MplWidget.canvas.figure=fig
        fig.show()


    def export_plot(self,name,description):
        try:
             root_directory = os.path.dirname(os.path.abspath(__file__))
             filepath = root_directory+'\\Graphs\\'+name+'.png'
             self.MplWidget.canvas.figure.savefig(filepath)
             d=DataManagment()
             d.save_plot(name,description,filepath)
        except:
            print("Ops. Something wrong. try again!")
         
    def create_GeoMap(self):
        df = pd.read_csv('../novel-corona-virus-2019-dataset/covid_19_data.csv',parse_dates=['Last Update'])
        df.rename(columns={'ObservationDate':'Date', 'Country/Region':'Country'}, inplace=True)


        df_confirmed = pd.read_csv("../novel-corona-virus-2019-dataset/time_series_covid_19_confirmed.csv")
        df_confirmed_US = pd.read_csv("../novel-corona-virus-2019-dataset/time_series_covid_19_confirmed_US.csv")
        df_recovered = pd.read_csv("../novel-corona-virus-2019-dataset/time_series_covid_19_recovered.csv")
        df_deaths = pd.read_csv("../novel-corona-virus-2019-dataset/time_series_covid_19_deaths.csv")
        df_deaths_US = pd.read_csv("../novel-corona-virus-2019-dataset/time_series_covid_19_deaths_US.csv")

        df_confirmed.rename(columns={'Country/Region':'Country'}, inplace=True)
        df_confirmed_US.rename(columns={'Country_Region':'Country'}, inplace=True)
        df_confirmed_US.rename(columns={'Province_State':'Province/State' ,'Long_':'Long'}, inplace=True)
        df_recovered.rename(columns={'Country/Region':'Country'}, inplace=True)
        df_deaths.rename(columns={'Country/Region':'Country'}, inplace=True)
        df_deaths_US.rename(columns={'Country/Region':'Country'}, inplace=True)

        df_confirmed = df_confirmed[["Province/State","Lat","Long","Country"]]
        df_confirmed_US = df_confirmed_US[["Province/State","Lat","Long","Country"]]
        #pd.concat([df_confirmed,df_confirmed_US])

        df_temp = df.copy()
        df_temp['Country'].replace({'Mainland China': 'China'}, inplace=True)
        df_latlong = pd.merge(df_temp, df_confirmed, on=["Country", "Province/State"])


        fig = px.density_mapbox(df_latlong, 
                                lat="Lat", 
                                lon="Long", 
                                hover_name="Province/State", 
                                hover_data=["Confirmed","Deaths","Recovered"], 
                                animation_frame="Date",
                                color_continuous_scale="Portland",
                                radius=7, 
                                zoom=0,height=700)
        fig.update_layout(title='Worldwide Lapse - Confirmed, Deaths, Recovered',
                          font=dict(family="Courier New, monospace",
                                    size=18,
                                    color="#7f7f7f")
                         )
        fig.update_layout(mapbox_style="open-street-map", mapbox_center_lon=0)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        fig.show()


        app = dash.Dash()
        app.layout = html.Div([
            dcc.Graph(figure=fig)
        ])

        app.run_server(debug=True, use_reloader=False) 


    def create_US_GeoMap(self):
        df_confirmed_US = pd.read_csv("../novel-corona-virus-2019-dataset/time_series_covid_19_confirmed_US.csv")
        df_confirmed_US=df_confirmed_US.drop(['UID', 'iso2','iso3','code3','FIPS','Admin2','Combined_Key'], axis=1)
        df_confirmed_US.rename(columns={'Country_Region':'Country','Province_State':'Province/State' ,'Long_':'Long'}, inplace=True)
        df_confirmed_US=pd.melt(df_confirmed_US,id_vars=['Province/State','Country','Lat','Long'], var_name='Date', value_name='Confirmed')
        df_confirmed_US=df_confirmed_US[df_confirmed_US['Confirmed']>0]

        fig = px.density_mapbox(df_confirmed_US, 
                        lat="Lat", 
                        lon="Long", 
                        hover_name="Province/State", 
                        hover_data=["Confirmed"], 
                        animation_frame="Date",
                        color_continuous_scale="Portland",
                        radius=7, 
                        zoom=0,height=700)
        fig.update_layout(title='Worldwide Confirmed Cases',
                          font=dict(family="Courier New, monospace",
                                    size=18,
                                    color="#7f7f7f")
                         )
        fig.update_layout(mapbox_style="open-street-map", mapbox_center_lon=0)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.show()

        app = dash.Dash()
        app.layout = html.Div([
            dcc.Graph(figure=fig)
        ])

        app.run_server(debug=True, use_reloader=False) 


    def create_US_GeoMap_Death(self):
        df_confirmed_US = pd.read_csv("../novel-corona-virus-2019-dataset/time_series_covid_19_deaths_US.csv")
        df_confirmed_US=df_confirmed_US.drop(['UID', 'iso2','iso3','code3','FIPS','Admin2','Combined_Key','Population'], axis=1)
        df_confirmed_US.rename(columns={'Country_Region':'Country','Province_State':'Province/State' ,'Long_':'Long'}, inplace=True)
        df_confirmed_US=pd.melt(df_confirmed_US,id_vars=['Province/State','Country','Lat','Long'], var_name='Date', value_name='Deaths')
        df_confirmed_US=df_confirmed_US[df_confirmed_US['Deaths']>0]

        fig = px.density_mapbox(df_confirmed_US, 
                        lat="Lat", 
                        lon="Long", 
                        hover_name="Province/State", 
                        hover_data=["Deaths"], 
                        animation_frame="Date",
                        color_continuous_scale="Portland",
                        radius=7, 
                        zoom=0,height=700)
        fig.update_layout(title='Worldwide Deaths Cases',
                          font=dict(family="Courier New, monospace",
                                    size=18,
                                    color="#7f7f7f")
                         )
        fig.update_layout(mapbox_style="open-street-map", mapbox_center_lon=0)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.show()

        app = dash.Dash()
        app.layout = html.Div([
            dcc.Graph(figure=fig)
        ])

        app.run_server(debug=True, use_reloader=False) 


app = QApplication([])
window = MainWindow()

window.show()
app.exec_()
