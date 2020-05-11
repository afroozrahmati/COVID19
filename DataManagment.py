import pyodbc 
class DataManagment(object):
    """Manage conncetivity with SQL Server"""

    def __init__(self):
        self.connection=pyodbc.connect('Driver={SQL Server};'
                      'Server=.;'
                      'Database=Covid19;'
                      'Trusted_Connection=yes;')

    def is_authenticate(self,user,password):
        conn = self.connection
        cursor = conn.cursor()
        cursor.execute("select * from users where UserName='"+user+"' and password='"+password+"'")
        
        for row in cursor:
            return True
        else:
            return False


    def get_Role(self,user):
        try:
            conn = self.connection
            with (conn.cursor()) as c:
                c.execute("select Role from users where  UserName='"+user+"'")
                plots=c.fetchall()
                return plots
        except ex as Exception:
            print(str(ex))


    def connect_close(self):
        if self.connection:
            self.connection.close()


    def save_plot(self,name,description,path):
        try:
            conn = self.connection
            sql="insert into PlotInformation(PlotName,PlotDescription,filePath) values ('"+name+"','"+description+"','"+path+"')"
            with (conn.cursor()) as c:
                c.execute(sql)
                conn.commit()
        except ex as Exception:
            print(str(ex))


    def get_plots(self):
        try:
            conn = self.connection
            with (conn.cursor()) as c:
                c.execute('select PlotID,PlotName,filePath from PlotInformation')
                plots=c.fetchall()
                return plots
        except ex as Exception:
            print(str(ex))




    def get_plotpath(self,x):
        try:
            conn = self.connection
            with (conn.cursor()) as c:
                c.execute("select PlotID,PlotName,filePath from PlotInformation where PlotName='"+x+"'")
                plots=c.fetchall()
                return plots
        except ex as Exception:
            print(str(ex))