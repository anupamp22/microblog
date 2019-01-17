# from datetime import datetime
# from flask import render_template, flash, redirect, url_for, request, g, \
#     jsonify, current_app, Flask
# from flask_login import current_user, login_required
# from flask_babel import _, get_locale
# from guess_language import guess_language
# from app import db
# from app.main.forms import EditProfileForm, PostForm, SearchForm, MessageForm
# from app.models import User, Post, Message, Notification
# from app.translate import translate
# from app.dashboard import bp
# from flask_babel import _, lazy_gettext as _l

# from bokeh.embed import components
# from bokeh.plotting import figure
from bokeh.resources import INLINE
# from bokeh.util.string import encode_utf8
# from bokeh.plotting import figure, show, output_file
# from bokeh.sampledata.iris import flowers

# from numpy import histogram
# import pandas as pd
# import os

# import numpy as np
# from datetime import timedelta
# from functools import update_wrapper, wraps
# from math import sin, cos
# from random import random
# from six import string_types

# from bokeh.plotting import figure
# from bokeh.models.sources import AjaxDataSource, CustomJS
from bokeh.embed import components


from flask import Flask, jsonify, make_response, request, current_app, render_template
from app.dashboard import bp


from collections import Counter
from math import pi

import numpy as np
import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, DataTable, RangeTool, TableColumn, \
                         NumberFormatter, StringFormatter
from bokeh.palettes import Spectral11
from bokeh.plotting import figure
from bokeh.transform import cumsum
# from bokeh.charts import Histogram
from numpy import histogram, linspace
#from scipy.stats.kde import gaussian_kde

from bokeh.sampledata.autompg2 import autompg2 as mpg
from bokeh.sampledata.stocks import AAPL
from bokeh.embed import server_document
from numpy import histogram, linspace


# from app.dashboard import delay_histogram



# @bp.route('/data', methods=['GET','OPTIONS','POST'])
# # @crossdomain(origin="*", methods=['GET', 'POST'], headers=None)
# def data():
#     x = list(np.arange(0, 6, 0.1))
#     y = list(np.sin(x) + np.random.random(len(x)))
#     x.append(x[-1]+0.1)
#     y.append(np.sin(x[-1])+np.random.random())
#     return jsonify(points=list(zip(x,y)))


# def read_csv_file():
#     dir_name="/home/anupam/.bokeh/data/"
#     df = pd.read_csv(dir_name+"AAPL.csv")
#     return df

iris_df = pd.read_csv("/home/anupam/eclipse-workspace/microblog-0.15/app/data/iris.data", 
                names=["Sepal Length", "Sepal Width", "Petal Length", "Petal Width", "Species"])

feature_names = iris_df.columns[0:-1].values.tolist()



def create_figure(current_feature_name, bins):

    # iris_df1 = iris_df.sort_values([current_feature_name])

    # p = Histogram(iris_df, current_feature_name, title=current_feature_name, color='Species', 
    #     bins=bins, legend='top_right', width=600, height=400)

    # # Set the x axis label
    # p.xaxis.axis_label = current_feature_name

    # # Set the y axis label
    # p.yaxis.axis_label = 'Count'

    #pdf = gaussian_kde(iris_df.current_feature_name)

    #x = linspace(0,250,200)

    # p = figure(x_axis_type="log", plot_height=300)

    # #p.line(x, pdf(x))

    # # plot actual hist for comparison
    # hist, edges = histogram(iris_df.current_feature_name, density=True, bins=bins)

    # p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], alpha=0.4)

    # hist, edges = np.histogram(np.array(iris_df[current_feature_name]), density=True, bins=bins)

    # # x = np.linspace(-2, 2, 1000)

    # p = figure()

    # p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], line_color="red")

    
    x = linspace(0,250,200)

    p = figure(plot_height=300)

    hist, edges = histogram(iris_df[current_feature_name], density=True, bins=bins)

    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], alpha=0.4,

           # same technique and properties for every Bokeh Glyph
           line_color="red", line_width=2)


    return p

# @bp.route("/dashboard1")
# def dashboard1():
#     # script=autoload_server(model=None,app_path="/bokeh-sliders",url="http://localhost:5000")
#     script=server_document("http://localhost:5000/bokeh-sliders")
#     return render_template('dashboard/index.html',bokS=script)

# @bp.route("/dashboard1")
# def dashboard1():
#     # script=autoload_server(model=None,app_path="/bokeh-sliders",url="http://localhost:5000")
#     script=server_document("http://localhost:5000/dashboard/delay_histogram")
#     return render_template('dashboard/index.html',bokS=script)


@bp.route("/dashboard1")
def dashboard1():
    current_feature_name = request.args.get("feature_name")
    if current_feature_name == None:
        current_feature_name = "Sepal Length"

    # Create the plot
    plot = create_figure(current_feature_name, 10)
        
    # Embed plot into HTML via Flask Render
    script, div = components(plot)

    # js_resources = INLINE.render_js()
    # css_resources = INLINE.render_css()    
    

    return render_template("dashboard/index.html", script=script, div=div,
        feature_names=feature_names,  current_feature_name=current_feature_name)

@bp.route("/dashboard")
def dashboard():
    # AAPL = read_csv_file()
    dates = np.array(AAPL['date'], dtype=np.datetime64)
    source = ColumnDataSource(data=dict(date=dates, close=AAPL['adj_close']))

    p = figure(plot_height=110, tools="", toolbar_location=None, #name="line",
               x_axis_type="datetime", x_range=(dates[1500], dates[2500]), sizing_mode="scale_width")

    p.line('date', 'close', source=source, line_width=2, alpha=0.7)
    p.yaxis.axis_label = 'Traffic'
    p.background_fill_color="#f5f5f5"
    p.grid.grid_line_color="white"

    script0, div0 = components(p)

    select = figure(plot_height=50, plot_width=800, y_range=p.y_range,
                    x_axis_type="datetime", y_axis_type=None,
                    tools="", toolbar_location=None, sizing_mode="scale_width")

    range_rool = RangeTool(x_range=p.x_range)
    range_rool.overlay.fill_color = "navy"
    range_rool.overlay.fill_alpha = 0.2

    select.line('date', 'close', source=source)
    select.ygrid.grid_line_color = None
    select.add_tools(range_rool)
    select.toolbar.active_multi = range_rool
    select.background_fill_color="#f5f5f5"
    select.grid.grid_line_color="white"
    select.x_range.range_padding = 0.01

    layout = column(p, select, sizing_mode="scale_width", name="line")

    curdoc().add_root(layout)

    script1, div1 = components(select)

    # Donut chart

    x = Counter({ 'United States': 157, 'United Kingdom': 93, 'Japan': 89, 'China': 63,
                  'Germany': 44, 'India': 42, 'Italy': 40, 'Australia': 35, 'Brazil': 32,
                  'France': 31, 'Taiwan': 31  })

    data = pd.DataFrame.from_dict(dict(x), orient='index').reset_index().rename(index=str, columns={0:'value', 'index':'country'})
    data['angle'] = data['value']/sum(x.values()) * 2*pi
    data['color'] = Spectral11

    region = figure(plot_height=350, toolbar_location=None, outline_line_color=None, sizing_mode="scale_both", name="region", x_range=(-0.4, 1))

    region.annular_wedge(x=-0, y=1, inner_radius=0.2, outer_radius=0.32,
                      start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                      line_color="white", fill_color='color', legend='country', source=data)

    region.axis.axis_label=None
    region.axis.visible=False
    region.grid.grid_line_color = None
    region.legend.label_text_font_size = "0.7em"
    region.legend.spacing = 1
    region.legend.glyph_height = 15
    region.legend.label_height = 15

    curdoc().add_root(region)
    script2, div2 = components(region)

    # Bar chart

    plats = ("IOS", "Android", "OSX", "Windows", "Other")
    values = (35, 22, 13, 26, 4)
    platform = figure(plot_height=350, toolbar_location=None, outline_line_color=None, sizing_mode="scale_both", name="platform",
                      y_range=list(reversed(plats)), x_axis_location="above")
    platform.x_range.start = 0
    platform.ygrid.grid_line_color = None
    platform.axis.minor_tick_line_color = None
    platform.outline_line_color = None

    platform.hbar(left=0, right=values, y=plats, height=0.8)

    curdoc().add_root(platform)
    script3, div3 = components(platform)

    # Table

    source = ColumnDataSource(data=mpg[:6])
    columns = [
        TableColumn(field="cyl", title="Counts"),
        TableColumn(field="cty", title="Uniques",
                    formatter=StringFormatter(text_align="center")),
        TableColumn(field="hwy", title="Rating",
                    formatter=NumberFormatter(text_align="right")),
    ]
    table = DataTable(source=source, columns=columns, height=210, width=330, name="table", sizing_mode="scale_both")

    curdoc().add_root(table)

    # Setup

    curdoc().title = "Bokeh Dashboard"
    curdoc().template_variables['stats_names'] = ['users', 'new_users', 'time', 'sessions', 'sales']
    curdoc().template_variables['stats'] = {
        'users'     : {'icon': 'user',        'value': 11200, 'change':  4   , 'label': 'Total Users'},
        'new_users' : {'icon': 'user',        'value': 350,   'change':  1.2 , 'label': 'New Users'},
        'time'      : {'icon': 'clock-o',     'value': 5.6,   'change': -2.3 , 'label': 'Total Time'},
        'sessions'  : {'icon': 'user',        'value': 27300, 'change':  0.5 , 'label': 'Total Sessions'},
        'sales'     : {'icon': 'dollar-sign', 'value': 8700,  'change': -0.2 , 'label': 'Average Sales'},
    }
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()    
    
    return render_template("dashboard/dashboard.html",
                           div0=div0, script0=script0,
                           div1=div1, script1=script1,
                           div2=div2, script2=script2,
                           div3=div3, script3=script3,
                           js_resources=js_resources,
                           css_resources=css_resources
                           )




# @bp.route("/dashboard")
# def dashboard():

#     js_resources = INLINE.render_js()
#     css_resources = INLINE.render_css()

#     adapter = CustomJS(code="""
#     const result = {x: [], y: []}
#     const pts = cb_data.response.points
#     for (i=0; i<pts.length; i++) {
#         result.x.push(pts[i][0])
#         result.y.push(pts[i][1])
#     }
#     return result
#     """)

#     source = AjaxDataSource(data_url='http://localhost:5000/data',
#                             polling_interval=1000, adapter=adapter)

#     p = figure(plot_height=300, plot_width=800, background_fill_color="lightgrey",
#                title="Streaming Noisy sin(x) via Ajax")
#     p.circle('x', 'y', source=source)

#     p.x_range.follow = "end"
#     p.x_range.follow_interval = 10

#     script1, div1 = components(p)

#     # -------------------------------------
#     # p = figure()
#     # p.line(x='x', y='y2', source=source)

#     # p.x_range.follow = "end"
#     # p.x_range.follow_interval = 10

#     # script2, div2 = components(p)

#     return render_template("dashboard/dashboard.html",
#                            div1=div1, script1=script1,
#                            # div2=div2, script2=script2,
#                            js_resources=js_resources,
#                            css_resources=css_resources
#                            )

# @bp.route('/dashboard')
# @login_required
# def dashboard():



    # chart defaults
    # color = '#FF0000'
    # start = 0
    # finish = 10

    # Create a polynomial line graph with those arguments
    # x = list(range(start, finish + 1))
    # fig = figure(title='Polynomial')
    # fig.line(x, [i ** 2 for i in x], color=color, line_width=2)

    # grab the static resources
    # js_resources = INLINE.render_js()
    # css_resources = INLINE.render_css()

    # Determine the selected feature
    # current_feature_name = request.args.get("feature_name")
    # if current_feature_name == None:
    #     current_feature_name = "Sepal Length"

    # # Create the plot
    # plot = create_figure(current_feature_name, 10)
        
    # # Embed plot into HTML via Flask Render
    # script, div = components(plot)

    # render template
    # script, div = components(fig)
    # html = render_template(
    #     'dashboard/dashboard.html',
    #     plot_script=script,
    #     plot_div=div,
    #     js_resources=js_resources,
    #     css_resources=css_resources,
    # )
    # return encode_utf8(html)
    # return render_template('dashboard/view.html')

    # colormap1 = {'setosa': 'rgb(255, 0, 0)',
    #          'versicolor': 'rgb(0, 255, 0)',
    #          'virginica': 'rgb(0, 0, 255)'}
    # colors1 = [colormap1[x] for x in flowers['species']]

    # colormap2 = {'setosa': '#0f0', 'versicolor': '#0f0', 'virginica': '#f00'}
    # colors2 = [colormap2[x] for x in flowers['species']]

    # p = figure(title = "Iris Morphology", output_backend="webgl")
    # p.xaxis.axis_label = 'Petal Length'
    # p.yaxis.axis_label = 'Petal Width'

    # p.diamond(flowers["petal_length"], flowers["petal_width"],
    #           color=colors1, line_alpha=0.5, fill_alpha=0.2, size=25, legend='diamonds')

    # p.circle(flowers["petal_length"], flowers["petal_width"],
    #          color=colors2, line_alpha=0.5, fill_alpha=0.2, size=10, legend='circles')

    # output_file("iris_blend.html", title="iris_blend.py example")

    # show(p)



   
                          