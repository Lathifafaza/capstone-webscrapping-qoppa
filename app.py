from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('table', attrs={'class':'table table-striped table-hover table-hover-solid-row table-simple history-data'})
tr = table.find_all('tr',attrs={'class':""})

row = table.find_all('tr')
row_length = len(row)

temp = [] #initiating a list 

temp = [] #initiating a tuple

for i in range(1, len(tr)):
    row = table.find_all('tr',attrs={'class':""})[i]
    
    #tanggal
    date = row.find_all('td')[0].text
    date = date.strip()

    
    #nilai uang
    value = row.find_all('td')[2].text
    value = value.strip()
    
    
    temp.append((date, value))

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns = ('date', 'value'))
df['value'] = df['value'].replace('IDR',"",regex=True).replace(',',"",regex=True)
df['value'] = df['value'].astype('float64')

#insert data wrangling here
exchange=df[['value']].set_index(df.date)

#end of data wranggling 

@app.route("/")
def index(): 
	
		card_data = f'USD {round(exchange["value"].mean(),2)}' #be careful with the " and ' 

		# generate plot
		ax = exchange.plot(figsize = (20,9)) 
	
		# Rendering plot
		# Do not change this
		figfile = BytesIO()
		plt.savefig(figfile, format='png', transparent=True)
		figfile.seek(0)
		figdata_png = base64.b64encode(figfile.getvalue())
		plot_result = str(figdata_png)[2:-1]

		# render to html
		return render_template('index.html',
				card_data = card_data, 
				plot_result=plot_result
				)


if __name__ == "__main__": 
    app.run(debug=True)