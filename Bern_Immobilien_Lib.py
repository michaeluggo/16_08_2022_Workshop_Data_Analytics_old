import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.io import output_notebook, show, output_file
from bokeh.models import ColumnDataSource, HoverTool, Panel
from bokeh.models.widgets import Tabs
from bokeh.models import  HoverTool, ColumnDataSource
import itertools
from bokeh.palettes import Dark2_5 as palette

def bardiagram_anzeigen(Nicht_versteuerter_Gewinn_gefunden, Nicht_versteuerter_Gewinn_nicht_gefunden):

    width = 0.35
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar([0], [Nicht_versteuerter_Gewinn_gefunden], width, color='b')
    ax.bar([0], [Nicht_versteuerter_Gewinn_nicht_gefunden], width, bottom=[Nicht_versteuerter_Gewinn_gefunden], color='r')
    ax.set_ylabel('Nicht versteuerter Gewinn [Fr]')
    ax.set_title('Nicht versteuerter Gewinn gefunden und nicht gefunden')
    ax.set_xlim([-0.45,0.45])
    ax.set_ylim([0,100000000])

    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['top'].set_visible(False)


    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False) # labels along the bottom edge are off

    ax.legend(labels=['Gefunden', 'Nicht gefunden'])
    plt.show()

def numerical_hist_hover(dataframe, column, colors=["SteelBlue", "Tan"], bins=30, plot_height = 300, plot_width = 600, log_scale=False, show_plot=True):

    # build histogram data with Numpy
    hist, edges = np.histogram(dataframe[column], bins = bins)
    hist_df = pd.DataFrame({column: hist,
                             "left": edges[:-1],
                             "right": edges[1:]})
    hist_df["interval"] = ["%d to %d" % (left, right) for left, 
                           right in zip(hist_df["left"], hist_df["right"])]

    # bokeh histogram with hover tool
    if log_scale == True:
        hist_df["log"] = np.log(hist_df[column])
        src = ColumnDataSource(hist_df)
        plot = figure(plot_height = plot_height, plot_width = plot_width,
              title = "Histogram {}".format(column.capitalize()),
              x_axis_label = column.capitalize(),
              y_axis_label = "Log Count")    
        plot.quad(bottom = 0, top = "log",left = "left", 
            right = "right", source = src, fill_color = colors[0], 
            line_color = "black", fill_alpha = 0.7,
            hover_fill_alpha = 1.0, hover_fill_color = colors[1])
    else:
        src = ColumnDataSource(hist_df)
        plot = figure(plot_height = plot_height, plot_width = plot_width,
              title = "Histogram {}".format(column.capitalize()),
              x_axis_label = column.capitalize(),
              y_axis_label = "Count")    
        plot.quad(bottom = 0, top = column,left = "left", 
            right = "right", source = src, fill_color = colors[0], 
            line_color = "black", fill_alpha = 0.7,
            hover_fill_alpha = 1.0, hover_fill_color = colors[1])
    # hover tool
    hover = HoverTool(tooltips = [('Interval', '@interval'),
                              ('Anzahl', str("@" + column))])
    plot.add_tools(hover)
    # output
    if show_plot == True:
        show(plot)
    else:
        return plot
    
def kategorical_hist_hover(dataframe, column, plot_height = 300, plot_width = 600):
    colors=["SteelBlue", "Tan"]

    grouped_df = dataframe.groupby(column)

    source = ColumnDataSource(grouped_df)

    p = figure(plot_height = plot_height, plot_width = plot_width, x_range=grouped_df, title=column,
               toolbar_location=None, tooltips=[("Anzahl", "@Id_count")])

    p.vbar(x=column, top = 'Id_count' , width=0.9, source=grouped_df)

    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    #p.xaxis.axis_label = column
    #p.xaxis.major_label_orientation = 1.2
    p.outline_line_color = None
    p.xaxis.major_label_orientation = "vertical"

    show(p)
    
def plot_line(dataframe, column, aggr = "count", plot_height = 300, plot_width = 600):
    column_str = column + '_' + aggr
    source = ColumnDataSource(dataframe.groupby(["DatumVerkauft"]))
    p = figure(plot_width=plot_width, plot_height=plot_height, x_axis_type="datetime",title=column, toolbar_location=None, tooltips=[(column_str, "@"+column_str), ('Monat', "@MonatVerkauft_mean")])
    p.line(x="DatumVerkauft", y=column_str, source=source, line_width=2)
    p.left[0].formatter.use_scientific = False
    show(p)
    
def plot_line_year(dataframe, column, aggr = "count", plot_height = 300, plot_width = 600):
    column_str = column + '_' + aggr
    source = ColumnDataSource(dataframe.groupby(["JahrVerkauft"]))
    p = figure(plot_width=plot_width, plot_height=plot_height,title=column, toolbar_location=None, tooltips=[(column_str, "@"+column_str)])
    p.line(x="JahrVerkauft", y=column_str, source=source, line_width=2)
    p.left[0].formatter.use_scientific = False
    show(p)
    
def plot_line_kategorical(dataframe, column, aggr = "count", Zeit_dauer = "Jahr", plot_height = 300, plot_width = 600):

    colors = itertools.cycle(palette) 
    
    if Zeit_dauer == "Jahr":
    
        Z_Spalte = "JahrVerkauft"
        
        if aggr == "mean":
            df = dataframe.groupby([Z_Spalte, column])['Preis'].mean().unstack()
        else: 
            df = dataframe.groupby([Z_Spalte, column])['Preis'].count().unstack()
        p = figure(plot_width=plot_width, plot_height=plot_height, title=column, tooltips=[("Name","$name"), ("Preis"+"_"+aggr, "@$name")])
        source = ColumnDataSource(df)
        for column_id, color in zip(df,colors):
            p.line(Z_Spalte, column_id, source=source, name=column_id, legend='Name = {}'.format(column_id), color=color)

        show(p)
    elif Zeit_dauer == "Monat":
    
        Z_Spalte = "DatumVerkauft"
        
        if aggr == "mean":
            df = dataframe.groupby([Z_Spalte, column])['Preis'].mean().unstack()
        else: 
            df = dataframe.groupby([Z_Spalte, column])['Preis'].count().unstack()
        p = figure(plot_width=plot_width, plot_height=plot_height, title=column, tooltips=[("Name","$name"), ("Preis"+"_"+aggr, "@$name")])
        source = ColumnDataSource(df)
        for column_id, color in zip(df,colors):
            p.line(Z_Spalte, column_id, source=source, name=column_id, legend='Name = {}'.format(column_id), color=color)

        show(p)