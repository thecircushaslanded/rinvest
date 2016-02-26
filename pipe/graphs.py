import datetime as dt
from dateutil.relativedelta import relativedelta

from pandas_datareader import data as wb
from bokeh.plotting import figure, output_file
from bokeh.io import gridplot, show

ticker = "CLRI"
EventDates = [dt.date(2010,01,28), dt.date(2010,03,02), dt.date(2010,03,26)]
# EventDates = [dt.date(2010, 02, 9), dt.date(2010, 3, 10), dt.date(2010,3,30)]
# ticker = "ALME"

# ticker = "PSEC"

start = min(EventDates) + relativedelta(years=-1)
end = max(EventDates) + relativedelta(years=1)


data = wb.DataReader(ticker, 'yahoo', start, end).reset_index()



output_file("graph.html")

price = figure(title=ticker, x_axis_type='datetime', y_axis_label="Price", height=250, width=800)
volume = figure(x_axis_type='datetime', y_axis_label="Volume", height=250, width=800)


price.line(data["Date"], data["Adj Close"], line_width=2)
volume.line(data["Date"], data["Volume"]/1000., line_width=2, color='green')

price.ray(x=EventDates, y=0, length=0, angle=3.14159/2, color='red')
price.ray(x=EventDates, y=0, length=0, angle=-3.14159/2, color='red')
volume.ray(x=EventDates, y=0, length=0, angle=3.14159/2, color='red')
volume.ray(x=EventDates, y=0, length=0, angle=-3.14159/2, color='red')

show(gridplot([[price], [volume]]))

