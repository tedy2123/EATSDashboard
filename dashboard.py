from flask import Flask, render_template, request, session
import io
from matplotlib.figure import Figure
import base64
import urllib.request
import json
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from datetime import date

app = Flask(__name__)
app.secret_key = "manbearpig_MUDMAN8882"
app.config["SESSION_COOKIE_NAME"] = "myCOOKIE_monSTER5282"
#getting weather data from different city
@app.route('/get_weather', methods=['GET','POST'])
def get_weather():
    ###  THIS IS THE CALL TO GET THE MET OFFICE FILE FROM THE INTERNET
    response = urllib.request.urlopen('http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/3281?res=hourly&?key=8f8ddd87-8564-49d3-8cca-57a6692eabf6')

    FCData = response.read()
    FCDataStr = FCData.decode('utf-8')
    #END OF THE CALL TO GET MET OFFICE FILE FROM THE INTERNET
    # Converts JSON data to a dictionary object
    FCData_Dic = json.loads(FCDataStr)
    # # Open output file for appending
    # fName = 'weather.csv'
    # if (not os.path.exists(fName)):
    #     print(fName, ' does not exist')
    #     exit()
    # fOut = open(fName, 'a')

    # Loop through each day, will nearly always be 2 days,
    # unless run at midnight.
    # get a list of dictionary to run in server
    keys = ["index", "dateZ", "hhmm", "temperature", "humidity"]  # keys for dictionary

    data_values = []
    get_request = []

    i = 0
    j = 0
    for k in range(24):
        datas = dict() #initialized new dictionary
        # there will be 24 values altogether
        # find the first hour value for the first day
        DateZ = (FCData_Dic['SiteRep']['DV']['Location']['Period'][i]['value'])
        hhmm = (FCData_Dic['SiteRep']['DV']['Location']['Period'][i]['Rep'][j]['$'])
        Temperature = (FCData_Dic['SiteRep']['DV']['Location']['Period'][i]['Rep'][j]['T'])
        Humidity = (FCData_Dic['SiteRep']['DV']['Location']['Period'][i]['Rep'][j]['H'])
        # DewPoint = (FCData_Dic['SiteRep']['DV']['Location']['Period'][i]['Rep'][j]['Dp'])
        # recordStr = '{},{},{},{},{}\n'.format(DateZ, hhmm, Temperature, Humidity, DewPoint)
        # append to list
        hhmm1 = float(hhmm) / 60  # Change date to hours
        hhmm1 = str(hhmm1) + '0 hrs'
        date = DateZ[:-1] # to remove Z character at the end of date
        get_request.append(k)
        get_request.append(date)
        get_request.append(hhmm1)
        get_request.append(Temperature)
        get_request.append(Humidity)

        for k in get_request:
            print(k)

        # #update the dictionary
        for key, value in zip(keys, get_request):
            datas.update({key: value})

        # append to list
        data_values.append(datas)

        for k in data_values:
            print(k)

        # clear list
        get_request.clear()
        #
        # fOut.write(recordStr)
        j = j + 1
        if (hhmm == '1380'):
            i = i + 1
            j = 0
    # fOut.close()
    # print('Records added to ', fName)
    data_values = reversed(data_values)
    return render_template('weather.html',weatherdata=data_values)

    # define pages
@app.route("/")
@app.route('/maindashboard')
def maindashboard_page():
    historical = [
        {'days': 'Mon', 'flow': 117.2, 'tempout': 8.694, 'humout': 87.673, 'tempin': 15.26, 'humin':  86.45125,  'sm': 38.70, 'st': 14.09, 'apr': 564.542},
        {'days': 'Tuse', 'flow': 165.2, 'tempout': 7.97, 'humout': 79.45, 'tempin': 20.40, 'humin': 76.00,  'sm': 39.01, 'st':14.57, 'apr': 479.94},
        {'days': 'Wed', 'flow': 85.8, 'tempout': 9.05, 'humout': 90.58, 'tempin': 16.18, 'humin':  86.74, 'sm': 37.81, 'st': 15.77,'apr': 391.43},
        {'days': 'Thurs', 'flow': 124, 'tempout': 8.38, 'humout': 83.97, 'tempin': 17.10, 'humin':71.76,  'sm': 35.99, 'st': 15.49, 'apr': 528},
        {'days': 'Fri', 'flow': 154.7, 'tempout': 8.59, 'humout': 95.09, 'tempin': 16.88, 'humin': 83.71,  'sm': 38.05, 'st': 38.05, 'apr': 228},
        {'days': 'Sat', 'flow': 162.4, 'tempout': 8.67, 'humout': 99.83, 'tempin': 15.91, 'humin': 75.95,  'sm': 39.82, 'st': 13.88, 'apr': 196.11},
        {'days': 'Sun', 'flow': 129.7, 'tempout': 9.21, 'humout': 99.74, 'tempin': 16.54, 'humin': 68.13,  'sm': 37.48, 'st': 14.66, 'apr': 527.94},
    ]


    future = [
        {'days': 'Mon', 'flow': 119.2, 'tempout': 9.694, 'humout': 89.673, 'tempin': 17.26, 'humin': 88.45125,'sm': 39.70, 'st': 14.09, 'apr': 568.542},
        {'days': 'Tuse', 'flow': 169.2, 'tempout': 6.97, 'humout': 80.45, 'tempin': 21.40, 'humin': 78.00, 'sm': 40.01, 'st': 15.57, 'apr': 490.94},
        {'days': 'Wed', 'flow': 86.8, 'tempout': 8.05, 'humout': 91.58, 'tempin': 17.18, 'humin': 87.74, 'sm': 38.81,'st': 16.77, 'apr': 393.43},
        {'days': 'Thurs', 'flow': 127, 'tempout': 9.38, 'humout': 84.97, 'tempin': 18.10, 'humin': 72.76, 'sm': 36.99, 'st': 16.49, 'apr': 529},
        {'days': 'Fri', 'flow': 156.7, 'tempout': 9.59, 'humout': 96.09, 'tempin': 17.88, 'humin': 84.71, 'sm': 39.05, 'st': 39.05, 'apr': 229},
        {'days': 'Sat', 'flow': 166.4, 'tempout': 9.67, 'humout': 99.89, 'tempin': 16.91, 'humin': 76.95, 'sm': 40.82,'st': 14.88, 'apr': 198.11},
        {'days': 'Sun', 'flow': 139.7, 'tempout': 10.21, 'humout': 99.76, 'tempin': 17.54, 'humin': 69.13, 'sm': 38.48,'st': 15.66, 'apr': 520.94},

    ]
    data, current, color = dynamicdays(historical, future)

    session["data"] =data
    session["current"] = current
    session["color"] = color

    session["number_of_tunnels_forcast"] = [{'name': 'Tunnel 17'}, {'name': 'Tunnel 19B'}, {'name': 'Tunnel 44'},
                                         {'name': 'Tunnel 45'}]


    session["optimize_value"] = [{'name': ''}, {'name': ''}, {'name': ''},
                                  {'name': ''},{'name': ''}]

    session["bgcolor"]=""
    session["weeks"] = [{'name': 'Current'}, {'name': 'Previous'}]
    session["readonly"]=""



    return render_template('maindashboard.html', data= session["data"],number_of_tunnels = session["number_of_tunnels_forcast"],
                           weeks=session["weeks"],bgcolor = session["bgcolor"],optimize_value=session["optimize_value"],today=session["current"],color= session["color"])
@app.route("/tunnels")
def tunnels_page():

    return render_template('tunnels.html')
@app.route("/temperture")
def temp_page():
    session["number_of_tunnels_soil"] = [{'name': 'Tunnel 17'}, {'name': 'Tunnel 19B'}, {'name': 'Tunnel 44'},
                                         {'name': 'Tunnel 45'}]
    return render_template('temp.html', number_of_tunnels=session["number_of_tunnels_soil"])
@app.route("/humidity")
def humidity_page():
    session["number_of_tunnels_soil"] = [{'name': 'Tunnel 17'}, {'name': 'Tunnel 19B'}, {'name': 'Tunnel 44'},
                                     {'name': 'Tunnel 45'}]
    return render_template('humidity.html', number_of_tunnels=session["number_of_tunnels_soil"])
@app.route("/soil")
def soil_page():
    session["number_of_tunnels_soil"] = [{'name': 'Tunnel 17'}, {'name': 'Tunnel 19B'}, {'name': 'Tunnel 44'},{'name': 'Tunnel 45'}]
    return render_template('soil.html', number_of_tunnels = session["number_of_tunnels_soil"])
@app.route("/flow")
def flow_page():
    session["number_of_tunnels_soil"] = [{'name': 'Tunnel 17'}, {'name': 'Tunnel 19B'}, {'name': 'Tunnel 44'},
                                         {'name': 'Tunnel 45'}]
    return render_template('flow.html', number_of_tunnels=session["number_of_tunnels_soil"])
@app.route("/par")
def par_page():
    session["number_of_tunnels_soil"] = [{'name': 'Tunnel 17'}, {'name': 'Tunnel 19B'}, {'name': 'Tunnel 44'},
                                         {'name': 'Tunnel 45'}]
    return render_template('par.html', number_of_tunnels=session["number_of_tunnels_soil"])
@app.route("/yield", methods =["POST", "GET"])
def yield_page():
    # get data from  combobox of temp page
    start_date = ""
    end_date = ""

    select = request.form.get('comp_select')
    tunnel = str(select)
    start_date = request.form.get("from")
    end_date = request.form.get("to")

    # start_date=str(start_date)
    # end_date=str(end_date)

    path1 = " "
    path2 = " "
    title1 = ""
    title2 = " "
    start_date = "2023-06-26"
    end_date = " 2023-07-11"



    if tunnel == "Tunnel 17":
        path = r'H:\Notebook\clean data\yield'
        path1 = path + '\yield_cleaned_17.csv'
    elif tunnel == "Tunnel 19B":
        path = r'H:\Notebook\clean data\yield'
        path1 = path + '\yield_cleaned_t9b.csv'
    elif tunnel == "Tunnel 44":
        path = r'H:\Notebook\clean data\yield'
        path1 = path + '\yield_cleaned_t45.csv'
    else:
        path = r'H:\Notebook\clean data\yield'
        path1 = path + '\yield_cleaned_t45.csv'


    df_yield = pd.read_csv(path1)

    df_yield['Submission_Date'] = pd.to_datetime(df_yield['Submission_Date'],
                                                               errors='coerce')

    # retrieved based on start and end dates
    df_yield = df_yield.loc[(df_yield['Submission_Date'] >= start_date)
                            & (df_yield['Submission_Date'] < end_date)]

    df_yield = df_yield.sort_values('Submission_Date')
    result_list = []
    for index, row in df_yield.iterrows():
        temp = {'ID': row['ID'],
                'Submission_Date': row['Submission_Date'],
                'Class1_Yield': row['Class1_Yield'],
                'Class2_Yield': row['Class2_Yield']
                }
        result_list.append(temp)

    return render_template('yield.html',number_of_tunnels = session["number_of_tunnels_forcast"],yielddata=result_list)
@app.route("/carbon")
def carbon_page():
    return render_template('carbon.html')
# the path is needed  for ploting graphs of each tunnels.
@app.route("/test" , methods=['GET', 'POST'])
def test():
    select = request.form.get('comp_select')
    session["get_tunnels_soil"]=str(select)
    return render_template('soil.html', number_of_tunnels = session["number_of_tunnels_soil"], get_tunnels=session["get_tunnels_soil"])

@app.route("/temp_plot" , methods=['GET', 'POST'])
def temp_plot():
    #get data from  combobox of temp page
    select = request.form.get('comp_select')
    tunnel=str(select)
    start_date = request.form.get("from")
    end_date = request.form.get("to")

    path1 = " "
    path2 = " "
    title1 = ""
    title2 = " "

    if tunnel== "Tunnel 17":
        path = r'H:\Notebook\clean data\17_may_to_july_2023'
        path1 = path + '\Tunnel_17_Hum_inside_may_to_july.csv'
        path2 = path + '\Tunnel_17_Hum_outside_may_to_july.csv'
        title1 = "Tunnel 17 Inside Temperature"
        title2 = "Tunnel 17 outside Temperature"
        # call figure function
        # fig = create_figure(path1,path2, title1,title2)
    elif tunnel == "Tunnel 19B":
        path = r'H:\Notebook\clean data\t9b_may_to_july_2023'
        path1 = path + '\Tunnel_T9B-R3_Hum_inside_may_to_july.csv'
        path2 = path + '\Tunnel_T9B-R3_Hum_outside_may_to_july.csv'
        title1 = "T9B Inside Temperature"
        title2 = "T9B outside Temperature"
        #call figure function
        # fig = create_figure(path1,path2, title1,title2)
    elif tunnel == "Tunnel 44":
        path = r'H:\Notebook\clean data\44_may_to_july_2023'
        path1 = path + '\Tunnel_44_Hum_inside_may_to_july.csv'
        path2 = path + '\Tunnel_44_Hum_outside_may_to_july.csv'
        title1 = "Tunnel 44 Inside Temperature"
        title2 = "Tunnel 44 outside Temperature"
        # call figure function
        # fig = create_figure(path1, path2, title1, title2)
    else:
        path = r'H:\Notebook\clean data\45_may_to_july_2023'
        path1 = path + '\Tunnel_45_Hum_inside_may_to_july.csv'
        path2 = path + '\Tunnel_45_Hum_outside_may_to_july.csv'
        title1 = "Tunnel 45 Inside Temperature"
        title2 = "Tunnel 45 outside Temperature"
        # fig = create_figure(path1, path2, title1, title2)

    df_internal = pd.read_csv(path1)
    df_external = pd.read_csv(path2)

    df_internal['Timestamp(Europe/London)'] = pd.to_datetime(df_internal['Timestamp(Europe/London)'],
                                                             errors='coerce')
    df_external['Timestamp(Europe/London)'] = pd.to_datetime(df_external['Timestamp(Europe/London)'],
                                                             errors='coerce')
    #retrived based on start and end dates
    df_internal = df_internal.loc[(df_internal['Timestamp(Europe/London)'] >= start_date)
                                  & (df_internal['Timestamp(Europe/London)'] < end_date)]
    df_external= df_external.loc[(df_external['Timestamp(Europe/London)'] >= start_date)
                                         & (df_external['Timestamp(Europe/London)'] < end_date)]

    df_internal = df_internal.sort_values('Timestamp(Europe/London)')
    df_external = df_external.sort_values('Timestamp(Europe/London)')

    # second image
    fig = Figure(figsize=(9, 10))

    axis = fig.add_subplot(2, 1, 1)

    axis.plot(df_internal['Timestamp(Europe/London)'], df_internal['Temperature'])
    axis.set_xlabel('')
    axis.set_ylabel("Temperature (°C)")
    axis.set_title(title1)
    # date_form = DateFormatter("%m-%d")
    # axis.xaxis.set_major_formatter(date_form)
    for tick in axis.get_xticklabels():
        tick.set_rotation(15)

    axis = fig.add_subplot(2, 1, 2)
    axis.plot(df_external['Timestamp(Europe/London)'], df_external['Temperature'],'r')
    axis.set_xlabel('Timestamps')
    axis.set_ylabel("Temperature (°C)")
    axis.set_title(title2)
    # date_form = DateFormatter("%m-%d")
    # x=axis.xaxis.set_major_formatter(date_form)
    # axis.set_xticks(x,rotation=90)
    for tick in axis.get_xticklabels():
        tick.set_rotation(15)

    # plotting images
    output = io.BytesIO()
    fig.savefig(output, format="png")
    # FigureCanvas(fig).print_png(output)
    # Embed the result in the html output.
    data = base64.b64encode(output.getbuffer()).decode("ascii")
    # encoded_img_data.decode('utf-8')

    # return Response(output.getvalue(), mimetype='image/png')
    # return f"<img src='data:image/png;base64,{data}'/>"


    return render_template('temp.html', number_of_tunnels = session["number_of_tunnels_soil"], image=data)

#humidity plotting
@app.route("/humidity_plot" , methods=['GET', 'POST'])
def humidity_plot():
    #get data from  combobox of temp page
    select = request.form.get('comp_select')
    tunnel=str(select)
    start_date = request.form.get("from")
    end_date = request.form.get("to")

    path1 = " "
    path2 = " "
    title1 = ""
    title2 = " "

    if tunnel== "Tunnel 17":
        path = r'H:\Notebook\clean data\17_may_to_july_2023'
        path1 = path + '\Tunnel_17_Hum_inside_may_to_july.csv'
        path2 = path + '\Tunnel_17_Hum_outside_may_to_july.csv'
        title1 = "Tunnel 17 Inside Humidity"
        title2 = "Tunnel 17 outside Humidity"
        # call figure function
        # fig = create_figure(path1,path2, title1,title2)
    elif tunnel == "Tunnel 19B":
        path = r'H:\Notebook\clean data\t9b_may_to_july_2023'
        path1 = path + '\Tunnel_T9B-R3_Hum_inside_may_to_july.csv'
        path2 = path + '\Tunnel_T9B-R3_Hum_outside_may_to_july.csv'
        title1 = "T9B Inside Humidity"
        title2 = "T9B outside Humidity"
        #call figure function
        # fig = create_figure(path1,path2, title1,title2)
    elif tunnel == "Tunnel 44":
        path = r'H:\Notebook\clean data\44_may_to_july_2023'
        path1 = path + '\Tunnel_44_Hum_inside_may_to_july.csv'
        path2 = path + '\Tunnel_44_Hum_outside_may_to_july.csv'
        title1 = "Tunnel 44 Inside Humidity"
        title2 = "Tunnel 44 outside Humidity"
        # call figure function
        # fig = create_figure(path1, path2, title1, title2)
    else:
        path = r'H:\Notebook\clean data\45_may_to_july_2023'
        path1 = path + '\Tunnel_45_Hum_inside_may_to_july.csv'
        path2 = path + '\Tunnel_45_Hum_outside_may_to_july.csv'
        title1 = "Tunnel 45 Inside Humidity"
        title2 = "Tunnel 45 outside Humidity"
        # fig = create_figure(path1, path2, title1, title2)



    df_internal = pd.read_csv(path1)
    df_external = pd.read_csv(path2)

    df_internal['Timestamp(Europe/London)'] = pd.to_datetime(df_internal['Timestamp(Europe/London)'],
                                                             errors='coerce')
    df_external['Timestamp(Europe/London)'] = pd.to_datetime(df_external['Timestamp(Europe/London)'],
                                                             errors='coerce')
    #retrived based on start and end dates
    df_internal = df_internal.loc[(df_internal['Timestamp(Europe/London)'] >= start_date)
                                  & (df_internal['Timestamp(Europe/London)'] < end_date)]
    df_external= df_external.loc[(df_external['Timestamp(Europe/London)'] >= start_date)
                                         & (df_external['Timestamp(Europe/London)'] < end_date)]

    df_internal = df_internal.sort_values('Timestamp(Europe/London)')
    df_external = df_external.sort_values('Timestamp(Europe/London)')

    # second image
    fig = Figure(figsize=(9, 10))

    axis = fig.add_subplot(2, 1, 1)

    axis.plot(df_internal['Timestamp(Europe/London)'], df_internal['Humidity'])
    axis.set_xlabel('')
    axis.set_ylabel("Humidity (°C)")
    axis.set_title(title1)
    for tick in axis.get_xticklabels():
        tick.set_rotation(15)

    axis = fig.add_subplot(2, 1, 2)
    axis.plot(df_external['Timestamp(Europe/London)'], df_external['Humidity'],'r')
    axis.set_xlabel('Timestamps')
    axis.set_ylabel(" Humidity (°C)")
    axis.set_title(title2)
    for tick in axis.get_xticklabels():
        tick.set_rotation(15)
    # plotting images
    output = io.BytesIO()
    fig.savefig(output, format="png")
    # FigureCanvas(fig).print_png(output)
    # Embed the result in the html output.
    data = base64.b64encode(output.getbuffer()).decode("ascii")
    # encoded_img_data.decode('utf-8')

    # return Response(output.getvalue(), mimetype='image/png')
    # return f"<img src='data:image/png;base64,{data}'/>"


    return render_template('humidity.html', number_of_tunnels = session["number_of_tunnels_soil"], image=data)

#Soil plotting
@app.route("/soil_plot" , methods=['GET', 'POST'])
def soil_plot():
    #get data from  combobox of temp page
    select = request.form.get('comp_select')
    tunnel=str(select)
    start_date = request.form.get("from")
    end_date = request.form.get("to")

    path1 = " "
    path2 = " "
    title1 = ""
    title2 = " "

    if tunnel== "Tunnel 17":
        path = r'H:\Notebook\clean data\17_may_to_july_2023'
        path1 = path + '\Tunnel_17_Soil_Moisture_may_to_july.csv'
        path2 = path + '\Tunnel_17_Soil_Moisture_may_to_july.csv'
        title1 = "Tunnel 17 Soil Moisture"
        title2 = "Tunnel 17 Soil Temperature"
        # call figure function
        # fig = create_figure(path1,path2, title1,title2)
    elif tunnel == "Tunnel 19B":
        path = r'H:\Notebook\clean data\t9b_may_to_july_2023'
        path1 = path + '\Tunnel_T9B-R3_Soil_Moisture_may_to_july.csv'
        path2 = path + '\Tunnel_T9B-R3_Soil_Moisture_may_to_july.csv'
        title1 = "T9B Soil Moisture"
        title2 = "T9B Soil Temperature"
        #call figure function
        # fig = create_figure(path1,path2, title1,title2)
    elif tunnel == "Tunnel 44":
        path = r'H:\Notebook\clean data\44_may_to_july_2023'
        path1 = path + '\Tunnel_44_Soil_Moisture_may_to_july.csv'
        path2 = path + '\Tunnel_44_Soil_Moisture_may_to_july.csv'
        title1 = "Tunnel 44 Soil Moisture"
        title2 = "Tunnel 44 Soil Temperature"
        # call figure function
        # fig = create_figure(path1, path2, title1, title2)
    else:
        path = r'H:\Notebook\clean data\45_may_to_july_2023'
        path1 = path + '\Tunnel_45_Soil_Moisture_may_to_july.csv'
        path2 = path + '\Tunnel_45_Soil_Moisture_may_to_july.csv'
        title1 = "Tunnel 45 Soil Moisture"
        title2 = "Tunnel 45 Soil Temperature"
        # fig = create_figure(path1, path2, title1, title2)



    df_soil_moisture = pd.read_csv(path1)
    df_soil_temperature = pd.read_csv(path2)

    df_soil_moisture['Timestamp(Europe/London)'] = pd.to_datetime(df_soil_moisture['Timestamp(Europe/London)'],
                                                             errors='coerce')
    df_soil_temperature['Timestamp(Europe/London)'] = pd.to_datetime(df_soil_temperature['Timestamp(Europe/London)'],
                                                             errors='coerce')
    #retrived based on start and end dates
    df_soil_moisture = df_soil_moisture.loc[(df_soil_moisture['Timestamp(Europe/London)'] >= start_date)
                                  & (df_soil_moisture['Timestamp(Europe/London)'] < end_date)]
    df_soil_temperature=  df_soil_temperature.loc[( df_soil_temperature['Timestamp(Europe/London)'] >= start_date)
                                         & ( df_soil_temperature['Timestamp(Europe/London)'] < end_date)]

    df_soil_moisture =   df_soil_moisture.sort_values('Timestamp(Europe/London)')
    df_soil_temperature = df_soil_temperature.sort_values('Timestamp(Europe/London)')

    # second image
    fig = Figure(figsize=(9, 10))

    axis = fig.add_subplot(2, 1, 1)

    axis.plot(df_soil_moisture['Timestamp(Europe/London)'], df_soil_moisture['Soil Moisture'])
    axis.set_xlabel('')
    axis.set_ylabel("Soil Moisture (°C)")
    axis.set_title(title1)
    for tick in axis.get_xticklabels():
        tick.set_rotation(15)

    axis = fig.add_subplot(2, 1, 2)
    axis.plot(df_soil_temperature['Timestamp(Europe/London)'], df_soil_temperature['Soil Temperature'],'r')
    axis.set_xlabel('Timestamps')
    axis.set_ylabel(" Soil Temperature (°C)")
    axis.set_title(title2)
    for tick in axis.get_xticklabels():
        tick.set_rotation(15)

    # plotting images
    output = io.BytesIO()
    fig.savefig(output, format="png")
    # FigureCanvas(fig).print_png(output)
    # Embed the result in the html output.
    data = base64.b64encode(output.getbuffer()).decode("ascii")
    # encoded_img_data.decode('utf-8')

    # return Response(output.getvalue(), mimetype='image/png')
    # return f"<img src='data:image/png;base64,{data}'/>"


    return render_template('soil.html', number_of_tunnels = session["number_of_tunnels_soil"], image=data)

#Flow plotting
@app.route("/flow_plot" , methods=['GET', 'POST'])
def flow_plot():
    #get data from  combobox of temp page
    select = request.form.get('comp_select')
    tunnel=str(select)
    start_date = request.form.get("from")
    end_date = request.form.get("to")

    path1 = " "
    path2 = " "
    title1 = ""
    title2 = " "

    if tunnel== "Tunnel 17":
        path = r'H:\Notebook\clean data\17_may_to_july_2023'
        path1 = path + '\Tunnel_17_Flow_Sensor_may_to_july.csv'
        title1 = "Tunnel 17 Water flow"
    elif tunnel == "Tunnel 19B":
        path = r'H:\Notebook\clean data\t9b_may_to_july_2023'
        path1 =  path + '/Tunnel_T9B-R3_Flow_Sensor_may_to_sept.csv'
        title1 = "Flow meter overtime"
    elif tunnel == "Tunnel 44":
        path = r'H:\Notebook\clean data\44_may_to_july_2023'
        path1 = path + '\Tunnel_44_Flow_Sensor_may_to_july.csv'
        title1 = "Flow meter overtime"
    else:
        path = r'H:\Notebook\clean data\45_may_to_july_2023'
        path1 = path + '\Tunnel_45_Flow_Sensor_may_to_july.csv'
        title1 = "Flow meter overtime"

    df_flow_meter = pd.read_csv(path1)

    df_flow_meter['Timestamp(Europe/London)'] = pd.to_datetime(df_flow_meter['Timestamp(Europe/London)'],
                                                             errors='coerce')

    #retrieved based on start and end dates
    df_flow_meter =  df_flow_meter.loc[(df_flow_meter['Timestamp(Europe/London)'] >= start_date)
                                  & (df_flow_meter['Timestamp(Europe/London)'] < end_date)]

    df_flow_meter =    df_flow_meter.sort_values('Timestamp(Europe/London)')

    # second image
    fig = Figure(figsize=(9, 10))

    axis = fig.add_subplot(1, 1, 1)

    axis.plot( df_flow_meter['Timestamp(Europe/London)'],  df_flow_meter['Total Water Flow Since Factory'])
    axis.set_xlabel('Timestamps')
    axis.set_ylabel("Flow rate (L)")
    axis.set_title(title1)
    for tick in axis.get_xticklabels():
        tick.set_rotation(15)
    # plotting images
    output = io.BytesIO()
    fig.savefig(output, format="png")
    # FigureCanvas(fig).print_png(output)
    # Embed the result in the html output.
    data = base64.b64encode(output.getbuffer()).decode("ascii")
    # encoded_img_data.decode('utf-8')

    return render_template('flow.html', number_of_tunnels = session["number_of_tunnels_soil"], image=data)


#Par plotting
@app.route("/par_plot", methods=['GET', 'POST'])
def par_plot():
    #get data from  combobox of temp page
    select = request.form.get('comp_select')
    tunnel=str(select)
    start_date = request.form.get("from")
    end_date = request.form.get("to")

    path1 = " "
    path2 = " "
    title1 = ""
    title2 = " "

    if tunnel== "Tunnel 17":
        path = r'H:\Notebook\clean data\17_may_to_july_2023'
        path1 = path + '\Tunnel_17_Light_inside_may_to_july.csv'
        title1 = "Tunnel 17 PAR Value "
    elif tunnel == "Tunnel 19B":
        path = r'H:\Notebook\clean data\t9b_may_to_july_2023'
        path1 =  path + '\Tunnel_T9B-R3_Light_inside_may_to_july.csv'
        title1 = " Tunnel 19B PAR Value"
    elif tunnel == "Tunnel 44":
        path = r'H:\Notebook\clean data\44_may_to_july_2023'
        path1 = path + '\Tunnel_44_Light_inside_may_to_july.csv'
        title1 = "Tunnel 44 PAR Value"
    else:
        path = r'H:\Notebook\clean data\45_may_to_july_2023'
        path1 = path + '\Tunnel_45_Light_inside_may_to_july.csv'
        title1 = "Tunnel 45 PAR Value"

    df_flow_meter = pd.read_csv(path1)

    df_flow_meter['Timestamp(Europe/London)'] = pd.to_datetime(df_flow_meter['Timestamp(Europe/London)'],
                                                             errors='coerce')

    #retrieved based on start and end dates
    df_flow_meter =  df_flow_meter.loc[(df_flow_meter['Timestamp(Europe/London)'] >= start_date)
                                  & (df_flow_meter['Timestamp(Europe/London)'] < end_date)]

    df_flow_meter =    df_flow_meter.sort_values('Timestamp(Europe/London)')

    # second image
    fig = Figure(figsize=(9, 10))

    axis = fig.add_subplot(1, 1, 1)

    axis.plot( df_flow_meter['Timestamp(Europe/London)'],  df_flow_meter['PAR'])
    axis.set_xlabel('Timestamps')
    axis.set_ylabel("PAR Value")
    axis.set_title(title1)
    for tick in axis.get_xticklabels():
        tick.set_rotation(15)

    # plotting images
    output = io.BytesIO()
    fig.savefig(output, format="png")
    # FigureCanvas(fig).print_png(output)
    # Embed the result in the html output.
    data = base64.b64encode(output.getbuffer()).decode("ascii")
    # encoded_img_data.decode('utf-8')

    return render_template('par.html', number_of_tunnels = session["number_of_tunnels_soil"], image=data)

#control the forcating button to get data from each tunnels
#Par plotting
@app.route("/data_retrieve" , methods=['GET', 'POST'])
def data_retrieve():
    #get data from  combobox of temp page
    get_tunnel = request.form.get('comp_select_tunnels')
    get_week = request.form.get('comp_select_week')
    tunnel=str(get_tunnel)
    week = str(get_week)

    #tunnels data
    tunnel17 = [
        {'days': 'Mon', 'flow': 117.2, 'tempout': 8.694, 'humout': 87.673, 'tempin': 15.26, 'humin': 86.45125,'sm': 38.70, 'st': 14.09, 'apr': 564.542},
        {'days': 'Tuse', 'flow': 165.2, 'tempout': 7.97, 'humout': 79.45, 'tempin': 20.40, 'humin': 76.00, 'sm': 39.01,'st': 14.57, 'apr': 479.94},
        {'days': 'Wed', 'flow': 85.8, 'tempout': 9.05, 'humout': 90.58, 'tempin': 16.18, 'humin': 86.74, 'sm': 37.81,'st': 15.77, 'apr': 391.43},
        {'days': 'Thurs', 'flow': 124, 'tempout': 8.38, 'humout': 83.97, 'tempin': 17.10, 'humin': 71.76, 'sm': 35.99,'st': 15.49, 'apr': 528},
        {'days': 'Fri', 'flow': 154.7, 'tempout': 8.59, 'humout': 95.09, 'tempin': 16.88, 'humin': 83.71, 'sm': 38.05,'st': 38.05, 'apr': 228},
        {'days': 'Sat', 'flow': 162.4, 'tempout': 8.67, 'humout': 99.83, 'tempin': 15.91, 'humin': 75.95, 'sm': 39.82,'st': 13.88, 'apr': 196.11},
        {'days': 'Sun', 'flow': 129.7, 'tempout': 9.21, 'humout': 99.74, 'tempin': 16.54, 'humin': 68.13, 'sm': 37.48,'st': 14.66, 'apr': 527.94},
        ]
    tunnel19 = [
        {'days': 'Mon', 'flow': 117.2, 'tempout': 8.694, 'humout': 87.673, 'tempin': 15.26, 'humin': 86.45125,'sm': 38.70, 'st': 14.09, 'apr': 564.542},
        {'days': 'Tuse', 'flow': 165.2, 'tempout': 7.97, 'humout': 79.45, 'tempin': 20.40, 'humin': 76.00, 'sm': 39.01,'st': 14.57, 'apr': 479.94},
        {'days': 'Wed', 'flow': 85.8, 'tempout': 9.05, 'humout': 90.58, 'tempin': 16.18, 'humin': 86.74, 'sm': 37.81,'st': 15.77, 'apr': 391.43},
        {'days': 'Thurs', 'flow': 124, 'tempout': 8.38, 'humout': 83.97, 'tempin': 17.10, 'humin': 71.76, 'sm': 35.99,'st': 15.49, 'apr': 528},
        {'days': 'Fri', 'flow': 154.7, 'tempout': 8.59, 'humout': 95.09, 'tempin': 16.88, 'humin': 83.71, 'sm': 38.05,'st': 38.05, 'apr': 228},
        {'days': 'Sat', 'flow': 162.4, 'tempout': 8.67, 'humout': 99.83, 'tempin': 15.91, 'humin': 75.95, 'sm': 39.82,'st': 13.88, 'apr': 196.11},
        {'days': 'Sun', 'flow': 129.7, 'tempout': 9.21, 'humout': 99.74, 'tempin': 16.54, 'humin': 68.13, 'sm': 37.48,'st': 14.66, 'apr': 527.94},
        ]
    tunnel44 = [
        {'days': 'Mon', 'flow': 117.2, 'tempout': 8.694, 'humout': 87.673, 'tempin': 15.26, 'humin': 86.45125,'sm': 38.70, 'st': 14.09, 'apr': 564.542},
        {'days': 'Tuse', 'flow': 165.2, 'tempout': 7.97, 'humout': 79.45, 'tempin': 20.40, 'humin': 76.00, 'sm': 39.01,'st': 14.57, 'apr': 479.94},
        {'days': 'Wed', 'flow': 85.8, 'tempout': 9.05, 'humout': 90.58, 'tempin': 16.18, 'humin': 86.74, 'sm': 37.81,'st': 15.77, 'apr': 391.43},
        {'days': 'Thurs', 'flow': 124, 'tempout': 8.38, 'humout': 83.97, 'tempin': 17.10, 'humin': 71.76, 'sm': 35.99,'st': 15.49, 'apr': 528},
        {'days': 'Fri', 'flow': 154.7, 'tempout': 8.59, 'humout': 95.09, 'tempin': 16.88, 'humin': 83.71, 'sm': 38.05,'st': 38.05, 'apr': 228},
        {'days': 'Sat', 'flow': 162.4, 'tempout': 8.67, 'humout': 99.83, 'tempin': 15.91, 'humin': 75.95, 'sm': 39.82,'st': 13.88, 'apr': 196.11},
        {'days': 'Sun', 'flow': 129.7, 'tempout': 9.21, 'humout': 99.74, 'tempin': 16.54, 'humin': 68.13, 'sm': 37.48,'st': 14.66, 'apr': 527.94},

        ]
    tunnel45 = [
        {'days': 'Mon', 'flow': 117.2, 'tempout': 8.694, 'humout': 87.673, 'tempin': 15.26, 'humin': 86.45125,'sm': 38.70, 'st': 14.09, 'apr': 564.542},
        {'days': 'Tuse', 'flow': 165.2, 'tempout': 7.97, 'humout': 79.45, 'tempin': 20.40, 'humin': 76.00, 'sm': 39.01,'st': 14.57, 'apr': 479.94},
        {'days': 'Wed', 'flow': 85.8, 'tempout': 9.05, 'humout': 90.58, 'tempin': 16.18, 'humin': 86.74, 'sm': 37.81,'st': 15.77, 'apr': 391.43},
        {'days': 'Thurs', 'flow': 124, 'tempout': 8.38, 'humout': 83.97, 'tempin': 17.10, 'humin': 71.76, 'sm': 35.99,'st': 15.49, 'apr': 528},
        {'days': 'Fri', 'flow': 154.7, 'tempout': 8.59, 'humout': 95.09, 'tempin': 16.88, 'humin': 83.71, 'sm': 38.05,'st': 38.05, 'apr': 228},
        {'days': 'Sat', 'flow': 162.4, 'tempout': 8.67, 'humout': 99.83, 'tempin': 15.91, 'humin': 75.95, 'sm': 39.82,'st': 13.88, 'apr': 196.11},
        {'days': 'Sun', 'flow': 129.7, 'tempout': 9.21, 'humout': 99.74, 'tempin': 16.54, 'humin': 68.13, 'sm': 37.48,'st': 14.66, 'apr': 527.94},
    ]
    #data from other,metoficce data, predicted and sessors
    tunnel17mps = [
        {'days': 'Mon', 'flow': 119.2, 'tempout': 9.694, 'humout': 89.673, 'tempin': 17.26, 'humin': 88.45125,'sm': 39.70, 'st': 14.09, 'apr': 568.542},
        {'days': 'Tuse', 'flow': 169.2, 'tempout': 6.97, 'humout': 80.45, 'tempin': 21.40, 'humin': 78.00, 'sm': 40.01,'st': 15.57, 'apr': 490.94},
        {'days': 'Wed', 'flow': 86.8, 'tempout': 8.05, 'humout': 91.58, 'tempin': 17.18, 'humin': 87.74, 'sm': 38.81,'st': 16.77, 'apr': 393.43},
        {'days': 'Thurs', 'flow': 127, 'tempout': 9.38, 'humout': 84.97, 'tempin': 18.10, 'humin': 72.76, 'sm': 36.99,'st': 16.49, 'apr': 529},
        {'days': 'Fri', 'flow': 156.7, 'tempout': 9.59, 'humout': 96.09, 'tempin': 17.88, 'humin': 84.71, 'sm': 39.05,'st': 39.05, 'apr': 229},
        {'days': 'Sat', 'flow': 166.4, 'tempout': 9.67, 'humout': 99.89, 'tempin': 16.91, 'humin': 76.95, 'sm': 40.82,'st': 14.88, 'apr': 198.11},
        {'days': 'Sun', 'flow': 139.7, 'tempout': 10.21, 'humout': 99.76, 'tempin': 17.54, 'humin': 69.13, 'sm': 38.48,'st': 15.66, 'apr': 520.94},
    ]
    tunnel19Bmps = [
        {'days': 'Mon', 'flow': 119.2, 'tempout': 9.694, 'humout': 89.673, 'tempin': 17.26, 'humin': 88.45125,'sm': 39.70, 'st': 14.09, 'apr': 568.542},
        {'days': 'Tuse', 'flow': 169.2, 'tempout': 6.97, 'humout': 80.45, 'tempin': 21.40, 'humin': 78.00, 'sm': 40.01,'st': 15.57, 'apr': 490.94},
        {'days': 'Wed', 'flow': 86.8, 'tempout': 8.05, 'humout': 91.58, 'tempin': 17.18, 'humin': 87.74, 'sm': 38.81,'st': 16.77, 'apr': 393.43},
        {'days': 'Thurs', 'flow': 127, 'tempout': 9.38, 'humout': 84.97, 'tempin': 18.10, 'humin': 72.76, 'sm': 36.99,'st': 16.49, 'apr': 529},
        {'days': 'Fri', 'flow': 156.7, 'tempout': 9.59, 'humout': 96.09, 'tempin': 17.88, 'humin': 84.71, 'sm': 39.05,'st': 39.05, 'apr': 229},
        {'days': 'Sat', 'flow': 166.4, 'tempout': 9.67, 'humout': 99.89, 'tempin': 16.91, 'humin': 76.95, 'sm': 40.82,'st': 14.88, 'apr': 198.11},
        {'days': 'Sun', 'flow': 139.7, 'tempout': 10.21, 'humout': 99.76, 'tempin': 17.54, 'humin': 69.13, 'sm': 38.48,'st': 15.66, 'apr': 520.94},
    ]
    tunnel44mps = [
        {'days': 'Mon', 'flow': 119.2, 'tempout': 9.694, 'humout': 89.673, 'tempin': 17.26, 'humin': 88.45125,'sm': 39.70, 'st': 14.09, 'apr': 568.542},
        {'days': 'Tuse', 'flow': 169.2, 'tempout': 6.97, 'humout': 80.45, 'tempin': 21.40, 'humin': 78.00, 'sm': 40.01,'st': 15.57, 'apr': 490.94},
        {'days': 'Wed', 'flow': 86.8, 'tempout': 8.05, 'humout': 91.58, 'tempin': 17.18, 'humin': 87.74, 'sm': 38.81,'st': 16.77, 'apr': 393.43},
        {'days': 'Thurs', 'flow': 127, 'tempout': 9.38, 'humout': 84.97, 'tempin': 18.10, 'humin': 72.76, 'sm': 36.99,'st': 16.49, 'apr': 529},
        {'days': 'Fri', 'flow': 156.7, 'tempout': 9.59, 'humout': 96.09, 'tempin': 17.88, 'humin': 84.71, 'sm': 39.05,'st': 39.05, 'apr': 229},
        {'days': 'Sat', 'flow': 166.4, 'tempout': 9.67, 'humout': 99.89, 'tempin': 16.91, 'humin': 76.95, 'sm': 40.82,'st': 14.88, 'apr': 198.11},
        {'days': 'Sun', 'flow': 139.7, 'tempout': 10.21, 'humout': 99.76, 'tempin': 17.54, 'humin': 69.13, 'sm': 38.48,'st': 15.66, 'apr': 520.94},
    ]
    tunnel45mps =[
        {'days': 'Mon', 'flow': 119.2, 'tempout': 9.694, 'humout': 89.673, 'tempin': 17.26, 'humin': 88.45125,'sm': 39.70, 'st': 14.09, 'apr': 568.542},
        {'days': 'Tuse', 'flow': 169.2, 'tempout': 6.97, 'humout': 80.45, 'tempin': 21.40, 'humin': 78.00, 'sm': 40.01,'st': 15.57, 'apr': 490.94},
        {'days': 'Wed', 'flow': 86.8, 'tempout': 8.05, 'humout': 91.58, 'tempin': 17.18, 'humin': 87.74, 'sm': 38.81,'st': 16.77, 'apr': 393.43},
        {'days': 'Thurs', 'flow': 127, 'tempout': 9.38, 'humout': 84.97, 'tempin': 18.10, 'humin': 72.76, 'sm': 36.99,'st': 16.49, 'apr': 529},
        {'days': 'Fri', 'flow': 156.7, 'tempout': 9.59, 'humout': 96.09, 'tempin': 17.88, 'humin': 84.71, 'sm': 39.05,'st': 39.05, 'apr': 229},
        {'days': 'Sat', 'flow': 166.4, 'tempout': 9.67, 'humout': 99.89, 'tempin': 16.91, 'humin': 76.95, 'sm': 40.82,'st': 14.88, 'apr': 198.11},
        {'days': 'Sun', 'flow': 139.7, 'tempout': 10.21, 'humout': 99.76, 'tempin': 17.54, 'humin': 69.13, 'sm': 38.48,'st': 15.66, 'apr': 520.94},
    ]

    if tunnel== "Tunnel 17":
        if week == "Previous":
            session["bgcolor"]="green"
            session["data"]=tunnel17
        else:
            session["bgcolor"] = ""
            data, current, color = dynamicdays(tunnel17, tunnel17mps)
            session["data"] = data
            session["current"] = current
            session["color"] = color
    elif tunnel == "Tunnel 19B":
        if week == "Previous":
            session["bgcolor"] = "green"
            session["data"] = tunnel19
        else:
            session["bgcolor"] = ""
            data, current, color = dynamicdays(tunnel19, tunnel19Bmps)
            session["data"] = data
            session["current"] = current
            session["color"] = color
    elif tunnel == "Tunnel 44":
        if week == "Previous":
            session["bgcolor"] = "green"
            session["data"] =  tunnel44
        else:
            session["bgcolor"] = ""
            data, current, color = dynamicdays(tunnel44, tunnel44mps)
            session["data"] = data
            session["current"] = current
            session["color"] = color
    else:
        if week == "Previous":
            session["bgcolor"] = "green"
            session["data"] = tunnel45
        else:
            session["bgcolor"] = ""
            data, current, color = dynamicdays(tunnel45, tunnel45mps)
            session["data"] = data
            session["current"] = current
            session["color"] = color

    # To change to display today word in historical data
    if week=="Previous":
        session["current"] = ""
    else:
        session["current"] = current



    return render_template('maindashboard.html', waterflow=session["water_flow"], data=session["data"],
                           number_of_tunnels=session["number_of_tunnels_forcast"], weeks=session["weeks"],
                           bgcolor=session["bgcolor"], color=session["color"], today=session["current"]) #

@app.route('/decision', methods=['GET', 'POST'])
def decision():
    # # put here functionality of the predict
    # days = ["Mon", "Tuse", "Wed", "Thurs", "Fri", "Sat", "Sun"]  # used for naming textfield
    # keys = ["tempout", "humout","tempin", "humin", "sm", "st", "apr"]  # keys for dictionary
    # temp = ""
    # data_values = []
    # get_request = []
    # for index in range(len(days)):
    #     datas = dict()
    #     days_value = days[index]
    #     for i in range(8):
    #         temp = days_value + str(i)
    #         value = request.form.get(temp)  # get values from textfield
    #         get_request.append(value)
    #
    #     # #update the dictionary
    #     for key, value in zip(keys, get_request):
    #         datas.update({key: value})
    #
    #     # append to list
    #     data_values.append(datas)
    #
    #     # clear list
    #     get_request.clear()
    #
    # #drop the days in a dic and get the remaining values
    # key = ["days"]
    # sum = 0
    # for dic in data_values:
    #     for key in keys:
    #         dic.pop(key, None)
    #         for val, cal in dic.items():
    #             sum = sum + int(cal)

    get_recommend = request.form.get('comp_select_recommend')
    get_recommend=str(get_recommend)
    predicted_class1=0
    predicted_class2 =0
    carbon_usage = 0
    water_usage=0

    if get_recommend=="Optimal yield":
        predicted_class1 = 500
        predicted_class2 = 400
        carbon_usage = 90
        water_usage = 600
    else:
        predicted_class1 = 400
        predicted_class2 = 300
        carbon_usage = 95
        water_usage =500



    return render_template('maindashboard.html', data=session["data"],
                           number_of_tunnels=session["number_of_tunnels_forcast"],
                           weeks=session["weeks"], color=session["color"],today=session["current"], bgcolor=session["bgcolor"],optimize_value=session["optimize_value"],
                           predicted_class1=predicted_class1,
                           predicted_class2=predicted_class2,
                           carbon_usage=carbon_usage,
                           water_usage=water_usage

                           )

@app.route('/optimize', methods=['GET', 'POST'])
def optimize():
    # put functionality of optimize
    days = ["Mon", "Tuse", "Wed", "Thurs", "Fri", "Sat", "Sun"]  # used for naming textfield
    keys = ["flow", "tempin", "tempout", "humin", "humout", "sm", "st", "apr"]  # keys for dictionary
    temp = ""

    # session["water_flow"]= {"D1":1,"D2":2, "D3":3, "D4":4, "D5":5, "D6":6, "D7":7}
    session["optimize_value"] = [{'name': 'Optimal yield'}, {'name': 'Optimal waterUsage'}]
    return render_template('maindashboard.html', data=session["data"],
                           number_of_tunnels=session["number_of_tunnels_forcast"], weeks=session["weeks"],
                           bgcolor=session["bgcolor"],optimize_value=session["optimize_value"], color=session["color"],today=session["current"])
#AI model section
@app.route('/model', methods=['GET', 'POST'])
def model():
    # call all functions
    dfs_45 = get_data()
    # dfs_45=pd.DataFrame.from_dict(dfs_45,orient='index')
    # print(dfs_45)
    dfs_45 = data_preprocessing(dfs_45)
    #print(dfs_45)
    path = r'H:\Notebook\clean data\45_may_to_sept_2023\merged_df_45_new3.csv'
    write_to_file(dfs_45, path)
    X, y = read_from_file(path)
    mse_n, results = train_forcast(X, y)
    #to send a list of dictionary to client
    result_list = []
    for index, row in results.iterrows():
        temp = {'Predicted_Class1_Yield': row['Predicted_Class1_Yield'],
                'Class1_Yield': row['Class1_Yield'],
                'Predicted_Class2_Yield': row['Predicted_Class2_Yield'],
                'Class2_Yield': row['Class2_Yield']
                }
        result_list.append(temp)
    session["mse_n"]=mse_n
    session["results"]= result_list
    return render_template('model.html', results=session["results"],msen=session["mse_n"])


def get_data():
    path = r'H:\Notebook\clean data\45_may_to_sept_2023'
    soil_conditions_45 = path + '\Tunnel_45_Soil_Moisture_may_to_sept.csv'
    light_45 = path + '\Tunnel_45_Light_inside_may_to_sept.csv'
    external_env_45 = path + '\Tunnel_45_Hum_outside_may_to_sept.csv'
    internal_env_45 = path + '\Tunnel_45_Hum_inside_may_to_sept.csv'
    flow_meter_45 = path + '\Tunnel_45_Flow_Sensor_may_to_sept.csv'

    df_soil_conditions_45 = pd.read_csv(soil_conditions_45)
    df_light_45 = pd.read_csv(light_45)
    df_external_env_45 = pd.read_csv(external_env_45)
    df_internal_env_45 = pd.read_csv(internal_env_45)
    df_water_meter_45 = pd.read_csv(flow_meter_45)

    df_soil_conditions_45['Timestamp(Europe/London)'] = pd.to_datetime(
        df_soil_conditions_45['Timestamp(Europe/London)'])
    df_soil_conditions_45.set_index('Timestamp(Europe/London)', inplace=True)

    df_soil_conditions_45.sort_index(inplace=True)
    df_soil_conditions_45 = pd.read_csv(soil_conditions_45)
    df_light_45 = pd.read_csv(light_45)
    df_external_env_45 = pd.read_csv(external_env_45)
    df_internal_env_45 = pd.read_csv(internal_env_45)
    df_water_meter_45 = pd.read_csv(flow_meter_45)

    dfs_45 = {
        "Soil Conditions": df_soil_conditions_45,
        "Light": df_light_45,
        "External Environment": df_external_env_45,
        "Internal Environment": df_internal_env_45,
        "Flow Meter": df_water_meter_45
    }

    return dfs_45
def convert_to_datetime(df, column_name):
    # just extract the date
    df[column_name] = pd.to_datetime(df[column_name].str.extract(r'([A-Za-z]{3} \d{1,2}, \d{4})')[0])
    return df
def compute_daily_average(df, column_names, timestamp_col):
    return df.groupby(timestamp_col)[column_names].mean().reset_index()

def compute_daily_sum(df, column_name, timestamp_col):
    daily_sum = df.groupby(timestamp_col).apply(lambda x: x[column_name].iloc[-1] - x[column_name].iloc[0]).reset_index()
    daily_sum.columns = [timestamp_col, column_name]
    return daily_sum


def data_preprocessing(df):
    dfs_45 = df
    # Convert timestamp columns to datetime format for all datasets
    dfs_45['Soil Conditions'] = convert_to_datetime(dfs_45['Soil Conditions'], 'Timestamp(Europe/London)')
    dfs_45['Light'] = convert_to_datetime(dfs_45['Light'], 'Timestamp(Europe/London)')
    dfs_45['External Environment'] = convert_to_datetime(dfs_45['External Environment'], 'Timestamp(Europe/London)')
    dfs_45['Internal Environment'] = convert_to_datetime(dfs_45['Internal Environment'], 'Timestamp(Europe/London)')
    dfs_45['Flow Meter'] = convert_to_datetime(dfs_45['Flow Meter'], 'Timestamp(Europe/London)')

    df_flow_meter_daily_45 = compute_daily_sum(dfs_45['Flow Meter'], 'Total Water Flow Since Factory',
                                               'Timestamp(Europe/London)')
    df_flow_meter_daily_45['Total Water Flow Since Factory'] = df_flow_meter_daily_45[
        'Total Water Flow Since Factory'].abs()
    df_flow_meter_daily_45.rename(columns={'Total Water Flow Since Factory': 'Water Usage'}, inplace=True)
    print(df_flow_meter_daily_45)

    # compute  averages for other variables
    df_internal_env_daily_45 = compute_daily_average(dfs_45['Internal Environment'], ['Temperature', 'Humidity'],
                                                     'Timestamp(Europe/London)')
    df_external_env_daily_45 = compute_daily_average(dfs_45['External Environment'], ['Temperature', 'Humidity'],
                                                     'Timestamp(Europe/London)')
    df_soil_conditions_daily_45 = compute_daily_average(dfs_45['Soil Conditions'],
                                                        ['Soil Moisture', 'Soil Temperature'],
                                                        'Timestamp(Europe/London)')
    df_light_daily_45 = compute_daily_average(dfs_45['Light'], ['PAR'], 'Timestamp(Europe/London)')

    # merge into single dataframe
    merged_df_45 = df_flow_meter_daily_45.copy()
    merged_df_45 = merged_df_45.merge(df_internal_env_daily_45, on='Timestamp(Europe/London)', how='outer')
    merged_df_45 = merged_df_45.merge(df_external_env_daily_45, on='Timestamp(Europe/London)', how='outer',
                                      suffixes=('_Internal', '_External'))
    merged_df_45 = merged_df_45.merge(df_soil_conditions_daily_45, on='Timestamp(Europe/London)', how='outer')
    merged_df_45 = merged_df_45.merge(df_light_daily_45, on='Timestamp(Europe/London)', how='outer')

    merged_df_45 = merged_df_45.sort_values('Timestamp(Europe/London)')

    # merged_df_45.sort_index().head()

    yield_data_path_45 = r'H:\Notebook\clean data\yield_cleaned_t45.csv'
    df_yield_45 = pd.read_csv(yield_data_path_45)
    df_yield_45['Submission_Date'] = pd.to_datetime(df_yield_45['Submission_Date'])
    merged_df_45 = merged_df_45.merge(df_yield_45, left_on='Timestamp(Europe/London)', right_on='Submission_Date',
                                      how='left')
    merged_df_45.head()

    features_to_cluster = ['Water Usage', 'Temperature_Internal', 'Humidity_Internal',
                           'Temperature_External', 'Humidity_External', 'Soil Moisture', 'Soil Temperature']

    merged_df_45 = merged_df_45.fillna(0)

    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(merged_df_45[features_to_cluster])
    # k-means
    optimal_k = 3
    kmeans = KMeans(n_clusters=optimal_k, init='k-means++', max_iter=300, n_init=10, random_state=1337)

    # Adding cluster labels to the DataFrame
    cluster_labels = kmeans.fit_predict(data_scaled)
    merged_df_45['Cluster'] = cluster_labels

    return merged_df_45
def write_to_file(df, path):
    df=df
    path = path
    df.to_csv(path)

def read_from_file(path):
    df2 = pd.read_csv(path)
    sensor_features = ['Water Usage', 'Temperature_Internal', 'Humidity_Internal', 'Temperature_External',
                       'Humidity_External', 'Soil Moisture', 'Soil Temperature', 'PAR']
    # Create 7-day lagged features
    for feature in sensor_features:
        for lag in range(1, 8):  # 7 days
            df2[f"{feature}_lag_{lag}"] = df2[feature].shift(lag)

    df2.dropna(inplace=True)

    # Drop rows with NaN values in 'Class1_Yield' and 'Class2_Yield'
    df2['Class1_Yield'].replace(0, np.nan, inplace=True)
    df2['Class2_Yield'].replace(0, np.nan, inplace=True)
    df_model_2 = df2.dropna(subset=['Class1_Yield', 'Class2_Yield'])

    # Create X and y for the merged dataframe
    X = df_model_2.drop(['Class1_Yield', 'Class2_Yield'], axis=1)
    y = df_model_2[['Class1_Yield', 'Class2_Yield']]
    #y=df_model_merged['Class1_Yield'] single out put
    lagged_features = [f"{feature}_lag_{lag}" for feature in sensor_features for lag in range(1, 8)]
    X = df_model_2[lagged_features]

    return X, y


def train_forcast(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # normalize
    scaler = StandardScaler()
    X_train_n = scaler.fit_transform(X_train)
    X_test_n = scaler.transform(X_test)

    lin_reg = LinearRegression()
    lin_reg.fit(X_train_n, y_train)
    y_pred_n = lin_reg.predict(X_test_n)

    mse_n = mean_squared_error(y_test, y_pred_n)

    X_test_display = X_test.reset_index(drop=True)
    y_pred_display = pd.DataFrame(y_pred_n, columns=['Predicted_Class1_Yield', 'Predicted_Class2_Yield'])
    # y_pred_display = pd.DataFrame(y_pred_n, columns=['Predicted_Class1_Yield'])
    y_test_reset = y_test.reset_index(drop=True)

    result = pd.concat([y_pred_display, y_test_reset], axis=1)
    #result = result.to_dict(orient='list')

    return mse_n, result
#change dynamic day to the dashboard
def dynamicdays(historical, future):
    # inputList.reverse()
    today = {0: 'Mon',
             1: 'Tuse',
             2: 'Wed',
             3: 'Thurs',
             4: 'fri',
             5: 'Sat',
             6: 'Sun'}
    temphis = []
    tempfut = []

    color = []
    #     givenIndices = []  # define pop indices
    day = date.today().weekday()  # get curret date 0 mon,1 Tus .....
    # day=3
    current = today[day]
    # day=2

    for i in range(day):
        temphis.append(historical[i])
        # givenIndices.append(i)

    for i in range(day, 7):
        tempfut.append(future[i])

    for i in range(0, 7):
        if i < day:
            color.append(1)
        else:
            color.append(0)

    inputlist = temphis + tempfut

    return inputlist, current, color

