from pandas_datareader import data
import datetime
from bokeh.plotting import figure, show, output_file
from pandas.util.testing import assert_frame_equal

company_name="Apple"
name="AAPL"
start=datetime.datetime(2020,1,1)
end = datetime.datetime(2020,4,6)

#DateReader("Company_stock_symbol", data_source, start_date, end_date)
df = data.DataReader(name,data_source="yahoo",start=start,end=end) 
df

def status(c, o):
    if c > o:
        value="increase"
    elif c < o:
        value="decrease"
    else:
        value="equal"
    return value
    
df["status"] = [status(c,o) for c,o in zip(df.Close, df.Open)]
df["middle"] = (df.Open+df.Close)/2
df["height"] = abs(df.Close - df.Open)

p = figure(x_axis_type='datetime', width=1500, height=500, sizing_mode="scale_width")
p.title.text = company_name+" Stock Trend"
#p.title.align="center"

hours_12 = 12*60*60*1000

p.grid.grid_line_alpha=0.9

#break lines after ',' (comma) to avoid errors
p.rect(df.index[df.status=="increase"], df.middle[df.status=="increase"], hours_12,
       df.height[df.status=="increase"], fill_color="green", line_color="black")
p.rect(df.index[df.status=="decrease"], df.middle[df.status=="decrease"], hours_12,
       df.height[df.status=="decrease"], fill_color="red", line_color="black")

p.segment(df.index, df.High, df.index, df.Low, color="Black")
output_file("cs.html")
show(p)