import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas_datareader.data as web
from datetime import datetime

app = dash.Dash()

import pandas as pd

nsdq = pd.read_csv('https://old.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download')
nsdq = nsdq.set_index('Symbol')
options = []
for ticker in nsdq.index:
	#{'Label': 'user sees', 'Value': 'script sees')
	myDict = {}
	myDict['label'] = str(nsdq.loc[ticker]['Name']) + ' ' + ticker
	myDict['value'] = ticker
	options.append(myDict)


app.layout = html.Div([
	html.H1('Stock Ticker Dashboard'),
	html.Div(
		[
			html.H3('Enter a stock symbol:', style={'paddingRight': '30px'}),
			dcc.Dropdown(
				id='my_stock_picker',
				value=['TSLA'],
				options= options,
				multi=True
			)
		], style={'display': 'inline-block', 'verticalAlign': 'top', 'width': '30%'}
	),
	html.Div(
		[
			html.H3('Select a start and end date:'),
			dcc.DatePickerRange(
				id='my_date_picker',
				min_date_allowed=datetime(2000, 1, 1),
				max_date_allowed=datetime.today(),
				start_date=datetime(2020, 1, 1),
				end_date=datetime.today())
		], style={'display': 'inline-block'}
	),
	html.Div(
		[
			html.Button(
				id='submit-button',
				n_clicks=0,
				children='Submit',
				style={'fontSize':24, 'marginLeft':'30px'}
			)
		],
		style={'display': 'inline-block'}
	),
	dcc.Graph(
		id='my_graph',
		figure = {
			'data': [{'x':[1,2], 'y':[3,1]}],
			'layout': {'title':'Default Title'}
		}
	)
])

# update title
@app.callback(
	Output('my_graph','figure'),
	[Input('submit-button','n_clicks')],
	[
		State('my_stock_picker','value'),
		State('my_date_picker', 'start_date'),
		State('my_date_picker', 'end_date')
	]
)
def update_graph(n_clicks, stock_ticker, start_date, end_date):
	start = datetime.strptime(start_date[:10], '%Y-%m-%d')
	end = datetime.strptime(end_date[:10], '%Y-%m-%d')

	#create traces for each ticker in option list

	traces = []
	for ticker in stock_ticker:
		df = web.DataReader(ticker, 'yahoo', start, end)
		traces.append({'x':df.index, 'y':df['Adj Close'], 'name': ticker})
	fig = {
		'data': traces,
		'layout': {'title':stock_ticker}
	}
	return fig

if __name__ == '__main__':
	app.run_server()