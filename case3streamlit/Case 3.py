#!/usr/bin/env python
# coding: utf-8

# In[71]:


import pandas as pd
#import pycurl
import json
import plotly.express as px
import http.client
import streamlit as st


# # Importeren API dataset van OpenChargeMap

# In[2]:


import http.client
import csv

conn = http.client.HTTPSConnection("api.openchargemap.io")

headers = { 'Content-Type': "application/json" }

conn.request("GET", "/v3/poi/?key=c154fb8a-8bdf-4d6e-9800-3eb95fb347f4&output=csv&countrycode=NL&maxresults=200000&compact=true&verbose=false", headers=headers)
#key: c154fb8a-8bdf-4d6e-9800-3eb95fb347f4
res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))


# In[ ]:





# In[3]:


import io
df_li = pd.read_csv(io.StringIO(data.decode("utf-8")))
df_li.info()


# In[4]:


import http.client

conn = http.client.HTTPSConnection("api.openchargemap.io")

headers = { 'Content-Type': "application/json" }

conn.request("GET", "/v3/poi/?key=c154fb8a-8bdf-4d6e-9800-3eb95fb347f4&output=json&countrycode=NL&maxresults=200000&compact=true&verbose=false", headers=headers)
#key: c154fb8a-8bdf-4d6e-9800-3eb95fb347f4
res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))


# In[5]:


import json

data_json = json.loads(data)

li_adres = []
for item in data_json :
    li_adres.append(item["AddressInfo"])
    

df_li_adres = pd.DataFrame(li_adres)

df_li_adres


# In[6]:


li_connlist = []
for item in data_json :
    li_connlist.append(item["Connections"])
    
li_connectie = []

for m in range(len(li_connlist)):

   # using nested for loop, traversing the inner lists
   for n in range (len(li_connlist[m])):

      # Add each element to the result list
      li_connectie.append(li_connlist[m][n])
        
df_li_connectie = pd.DataFrame(li_connectie)

df_li_connectie


# In[7]:


df_li_merged = df_li_adres.merge(df_li_connectie, left_on = 'ID', right_on = 'ID')

df_li_merged


# In[8]:


conn = http.client.HTTPSConnection("opendata.rdw.nl")

headers = {}

conn.request("GET", "/resource/m9d7-ebf2.csv?$where=20200101<datum_eerste_toelating&$limit=100&$$app_token=WxRl58VIg5ybQ2cyCdTHcaUjE", headers=headers)
#token: WxRl58VIg5ybQ2cyCdTHcaUjE
res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))


# In[9]:


df_kenteken=pd.read_csv(io.StringIO(data.decode("utf-8")))


# In[10]:


df_kenteken['kenteken'][50]


# In[11]:


import urllib

conn = http.client.HTTPSConnection("opendata.rdw.nl")

#params = urllib.urlencode({"kenteken": {df_kenteken['kenteken']}})
headers = {}

ls = []
#ls['kenteken'] = df_kenteken['kenteken']
for items in df_kenteken['kenteken']:
    conn.request("GET", "/resource/8ys7-d773.csv?&kenteken=" + items + "&$$app_token=WxRl58VIg5ybQ2cyCdTHcaUjE", headers=headers)
#token: WxRl58VIg5ybQ2cyCdTHcaUjE
    res = conn.getresponse()
    data1 = res.read()
    #l = data1.decode("utf-8")
    l = pd.read_csv(io.StringIO(data1.decode("utf-8")))
    ls.append(l)
appended_data = pd.concat(ls)

    #print(data1.decode("utf-8"))


# In[12]:


appended_data


# In[13]:


df_kenteken_brandstof = df_kenteken.merge(appended_data, left_on='kenteken', right_on='kenteken')
df_kenteken_brandstof


# We hebben een functie nodig om unieke waarden in een kolom te vinden. Ik wil weten of er meerdere soorten getallen zitten 
# in DistanceUnit. Dat doen we met def unique hieronder.

# In[14]:


def unique(list1):
  
    # een null-lijst/lege lijst initialiseren
    unique_list = []
  
    # door alle elementen heengaan
    for x in list1:
        # controleren of het bestaat in unique_list of niet
        if x not in unique_list:
            unique_list.append(x)
    # print list
    for x in unique_list:
        print (x)
        
list1 = df_li_adres["DistanceUnit"]
unique(list1)


# In[15]:


df_li_adres.columns


# #conclusie: ook dit kolom kan gedropt worden

# In[16]:


# de gegeven lijst bevat duplicaten
mylist =  df_li_adres['ID']

newlist = [] # lege lijst om unieke elementen uit de lijst te bewaren
duplist = [] # lege lijst om de dubbele elementen uit de lijst te bewaren
for i in mylist:
    if i not in newlist:
        newlist.append(i)
    else:
        duplist.append(i) # deze methode vangt de eerste dup's op en voegt ze toe aan de lijst

# het printen van de dups
print("Lijst duplicates", duplist)
print("Unieke Item List", newlist) # print uiteindelijke list van unieke waarden


# # CSV files importeren 

# In[17]:


csv_file= 'laadpaaldata.csv'
df_1=pd.read_csv(csv_file)
csv_file2='Elektrische_voertuigen.csv'
df_2=pd.read_csv(csv_file2)


# In[18]:


df_2.info()

# We zien veel kolommen met NA waarden, deze worden hieronder eruit gehaald
# In[19]:


df_2filter=df_2.drop(['Aantal cilinders', 'Laadvermogen', 'Oplegger geremd', 'Aanhangwagen autonoom geremd', 
           'Aanhangwagen middenas geremd', 'Aantal staanplaatsen', 'Afwijkende maximum snelheid',
           'Europese uitvoeringcategorie toevoeging', 'Vervaldatum tachograaf', 'Vervaldatum tachograaf DT',
           'Maximum last onder de vooras(sen) (tezamen)/koppeling', 'Type remsysteem voertuig code',
           'Rupsonderstelconfiguratiecode', 'Wielbasis voertuig minimum', 'Wielbasis voertuig maximum',
           'Lengte voertuig minimum', 'Lengte voertuig maximum', 'Breedte voertuig minimum', 'Breedte voertuig maximum',
           'Hoogte voertuig minimum', 'Hoogte voertuig maximum', 'Massa bedrijfsklaar minimaal', 'Massa bedrijfsklaar maximaal',
           'Technisch toelaatbaar massa koppelpunt', 'Maximum massa technisch maximaal', 'Maximum massa technisch minimaal',
           'Subcategorie Nederland', 'Type gasinstallatie', 'Zuinigheidsclassificatie', 'API Gekentekende_voertuigen_carrosserie',
           'API Gekentekende_voertuigen_carrosserie_specifiek', 'Datum tenaamstelling DT', 'API Gekentekende_voertuigen_voertuigklasse',
                      'API Gekentekende_voertuigen_assen', 'API Gekentekende_voertuigen_brandstof', 'Europese voertuigcategorie toevoeging',
                      'Cilinderinhoud', 'Bruto BPM', 'Eerste kleur', 'Tweede kleur', 'Voertuigsoort'
                     ], axis=1)


# In[20]:


df_2filter.columns


# In[21]:


def unique(list2):
  
    # een null-lijst/lege lijst initialiseren
    unique_list = []
  
    # door alle elementen heengaan
    for x in list2:
        # controleren of het bestaat in unique_list of niet
        if x not in unique_list:
            unique_list.append(x)
    # print list
    for x in unique_list:
        print (x)
        
list2 = df_2filter['Tenaamstellen mogelijk']
unique(list2)



# In[22]:


df_1["ChargeTime"].min()


# In[23]:


#alleen positieve waardem behouden in ChargeTime

L=df_1['ChargeTime']

[x
   for x in L
   if x >= 0
]


# In[24]:


df_2filter.columns


# In[25]:


df_2filter['Datum eerste toelating DT']


# In[26]:


df_datum=df_2filter['Datum eerste toelating DT'] = pd.to_datetime(df_2filter['Datum eerste toelating DT'], errors='coerce')
df_datum


# In[27]:


df_maand= df_datum.dt.month
df_maand


# In[28]:


#df_jaar omzetten in een dataframe zodat t gemerged kan worden
df_month = pd.DataFrame({'Maand': df_maand})
df_month


# In[29]:


#extra tabel aanmaken  
df_2filter['Maand'] = df_month

df_2filter


# In[30]:


#Boxplot
#fig = px.box(df_2filter, x="Merk", y="Vermogen massarijklaar", color="Merk",
 #           labels={
  #                   "job_title": "Baan titel",
   #                  "salary_in_euro": "Salaris in Euro",
    #                 "job_title": "Baan titel"
     #            },
      #          title=""
#fig.show()


# In[31]:


#Histogram
#fig = px.histogram(x=df_1['TotalEnergy'])

#fig.update_layout(title='')
#fig.update_xaxes(title='')
#fig.update_yaxes(title='Hoeveelheid')

#fig.show()


# # Kaart in Geopandas

# In[32]:


import geopandas as gpd
import folium


# In[33]:


#df_li


# In[34]:


df_li.NumberOfPoints.unique()


# In[35]:


def unique(list3):
  
    # een null-lijst/lege lijst initialiseren
    unique_list = []
  
    # door alle elementen heengaan
    for x in list3:
        # controleren of het bestaat in unique_list of niet
        if x not in unique_list:
            unique_list.append(x)
    # print list
    for x in unique_list:
        print (x)
        
list3 = df_li['NumberOfPoints']
unique(list3)


# In[36]:


df_dropdowncolums=df_li[['StateOrProvince', 'NumberOfPoints']]
df_dropdowncolums


# In[37]:


def color_producer(type):
    
    if type == 1.0:
        return "Brown"
    if type == 2.0:
        return "green"
    if type == 3.0:
        return "blue"
    if type == 4.0:
        return "aqua"
    if type == 6.0:
        return "red"
    if type == 7.0:
        return "pink"
    if type == 8.0:
        return "orange"
    if type == 9.0:
        return "gray"
    if type == 10.0:
        return "lightskyblue"
    if type == 12.0:
        return "violet"
    if type == 13.0:
        return "olive"
    if type == 14.0:
        return "lightgreen"
    if type == 15.0:
        return "teal"
    if type == 16.0:
        return "gold"
    if type == 18.0:
        return "peru"
    if type == 20.0:
        return "lavender"
    if type == 24.0:
        return "crimson"
    if type == 28.0:
        return "slategray"
    if type == 29.0:
        return "indigo"
    if type == 32.0:
        return "lime"
    if type == 44.0:
        return "tan"
    if type == 72.0:
        return "mediumspringgreen"



# In[38]:


print(color_producer(df_li.NumberOfPoints[20]))


# In[39]:


def add_categorical_legend(folium_map, title, colors, labels):
    if len(colors) != len(labels):
        raise ValueError("colors and labels must have the same length.")

    color_by_label = dict(zip(labels, colors))
    
    legend_categories = ""     
    for label, color in color_by_label.items():
        legend_categories += f"<li><span style='background:{color}'></span>{label}</li>"
        
    legend_html = f"""
    <div id='maplegend' class='maplegend'>
      <div class='legend-title'>{title}</div>
      <div class='legend-scale'>
        <ul class='legend-labels'>
        {legend_categories}
        </ul>
      </div>
    </div>
    """
    script = f"""
        <script type="text/javascript">
        var oneTimeExecution = (function() {{
                    var executed = false;
                    return function() {{
                        if (!executed) {{
                             var checkExist = setInterval(function() {{
                                       if ((document.getElementsByClassName('leaflet-top leaflet-right').length) || (!executed)) {{
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.display = "flex"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.flexDirection = "column"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].innerHTML += `{legend_html}`;
                                          clearInterval(checkExist);
                                          executed = true;
                                       }}
                                    }}, 100);
                        }}
                    }};
                }})();
        oneTimeExecution()
        </script>
      """
   

    css = """

    <style type='text/css'>
      .maplegend {
        z-index:9999;
        float:right;
        background-color: rgba(255, 255, 255, 1);
        border-radius: 5px;
        border: 2px solid #bbb;
        padding: 10px;
        font-size:12px;
        positon: relative;
      }
      .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
      .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 0px solid #ccc;
        }
      .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend a {
        color: #777;
        }
    </style>
    """

    folium_map.get_root().header.add_child(folium.Element(script + css))

    return folium_map


# In[79]:


pip install streamlit_folium


# In[80]:


import streamlit as st
from streamlit_folium import folium_static
import folium


# In[81]:


#Gekleurde punten toevoegen aan map

"# streamlit-folium"



m = folium.Map(location=[df_li["Latitude"].mean(), df_li["Longitude"].mean()], zoom_start=8, control_scale=True)

for index, locatie_info in df_li.iterrows():
    color= color_producer(df_li.NumberOfPoints.iloc[index])
    folium.CircleMarker([locatie_info['Latitude'], locatie_info['Longitude']], fill=True, 
                        color = color, tooltip='Klik om het aantal laadpunten te zien',radius= 1.75,
                        popup=f"{df_li.NumberOfPoints.iloc[index]}").add_to(m)
#Legenda
add_categorical_legend(m, 'Legenda: aantal laadpunten', 
                       colors=['Brown', 'green', 'blue', 'aqua', 'red','pink', 'orange',
                                'gray', 'lightskyblue', 'violet', 'olive','lightgreen', 'teal',
                                'gold', 'peru', 'lavender', 'crimson','slategray', 'indigo',
                                'lime', 'tan', 'mediumspringgreen'], 
                       labels=[1.0, 2.0, 3.0,4.0, 6.0, 7.0, 8.0, 9.0, 10.0, 12.0, 13.0, 14.0, 15.0, 16.0,
                              18.0, 20.0, 24.0, 28.0, 29.0, 32.0, 44.0, 72.0])
folium_static(m)


# In[41]:


import plotly.express as px
import plotly.graph_objects as go


# In[42]:


df_dropdowncolums=df_li[['StateOrProvince', 'NumberOfPoints']]

df_dropdowncolums


# In[46]:


df_li.to_csv('laadpaalinfo.csv')


# In[53]:


df_1


# In[54]:


# alles positief maken
df_1["ChargeTime"] = df_1["ChargeTime"].abs()


# In[55]:


# waardes boven de 10 uur verwijderen
df_1= df_1[(df_1['ChargeTime'] <= 10)]


# In[56]:


fig = px.scatter(df_1, x="ChargeTime", y= 'ConnectedTime')
fig.show()


# In[59]:


data=df_1['ChargeTime']

[x
   for x in data
   if x >= 0
]


# In[60]:


import plotly.express as px

fig = px.histogram(x= data, title="Histogram", nbins= 30)
fig.update_xaxes(title_text='Tijd aan de oplader (uur)')
fig.update_yaxes(title_text='Aantal auto')

annotation = {'x': df_1.ChargeTime.mean(), 'y':100, 'showarrow': True, 'arrowhead': 4,
                    'font': {'color': 'black', 'size':10}, 'text': 'Gemiddelde'}
mediaan = {'x': df_1.ChargeTime.median(), 'y':0, 'showarrow': True, 'arrowhead': 4,
                    'font': {'color': 'red', 'size':10}, 'text': 'Mediaan'}

fig.update_layout({'annotations':[annotation, mediaan]})

fig.show()


# In[61]:


# Cleanen data laadpaal
import datetime
laadpaal= pd.read_csv('laadpaaldata.csv')
# Chargetime niet negatief
laadpaal = laadpaal[laadpaal['ChargeTime'] >= 0]

# Started en ended naar datum formaat
laadpaal['Started'] = pd.to_datetime(laadpaal['Started'], errors='coerce')
laadpaal['Ended'] = pd.to_datetime(laadpaal['Ended'], errors='coerce')

q1 = laadpaal.ChargeTime.quantile(0.25)
q3 = laadpaal.ChargeTime.quantile(0.75)

iqr = q3-q1

outlier = (laadpaal.ChargeTime <= q3 + 1.5*iqr)
laadpaal = laadpaal.loc[outlier]
laadpaal

#histogram
# Histogram van de ChargeTime tegen het aantal keer dat hij voorkomt
fig = px.histogram(laadpaal, x = 'ChargeTime')

# Annotatie bij het gemiddelde toevoegen
annotation = {'x': laadpaal.ChargeTime.mean(), 'y':200, 'showarrow': True, 'arrowhead': 4,
                    'font': {'color': 'black', 'size':10}, 'text': 'Gemiddelde'}

# Titel en labels toevoegen. 
fig.update_layout({'annotations':[annotation]})
fig.update_layout(title_text = 'Het aantal keer dat eenzelfde laadtijd voorkomt', xaxis_title = 'Laadtijd (uur)', yaxis_title = 'Aantal keer')

fig.show()


# In[63]:


# mediaan 
df_1['ChargeTime'].median()


# In[64]:


# gemiddelde
df_1['ChargeTime'].mean()


# In[65]:


elektrisch=  pd.read_csv('Elektrische_voertuigen.csv')
elektrisch


# In[66]:


df_2filter['Datum eerste toelating DT']

df_datum=df_2filter['Datum eerste toelating DT'] = pd.to_datetime(df_2filter['Datum eerste toelating DT'], 
                                                                  errors='coerce')
df_datum

df_jaar= df_datum.dt.year
df_jaar

#df_jaar omzetten in een dataframe zodat t gemerged kan worden
df_jaar = pd.DataFrame({'Maand': df_jaar})
df_jaar

df_2filter['Jaar'] = df_jaar
df_2filter


# In[68]:


jaar_nieuwe_auto= df_2filter['Jaar'].value_counts()
jaar_nieuwe_auto.head()


# In[69]:


df= pd.DataFrame(jaar_nieuwe_auto)


# In[ ]:




