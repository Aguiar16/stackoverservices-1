import pygal
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go


from pygal.style import LightStyle



def csv_to_boxplot(input_path, output_path, column_id=None, title=None):
    df = pd.read_csv(input_path)
    df.set_index('Id', inplace=True)

    box_plot = pygal.Box()

    if title:
        box_plot.title = title

    if column_id:
        box_plot.add(column_id, df[column_id])
    else:
        for column in df:
            box_plot.add(column, df[column])

    box_plot.render_to_file(output_path)


def metrics_boxplot(input_path, metrics):
    df = pd.read_csv(input_path)
    df.set_index('Id', inplace=True)

    # box_plot = pygal.Box()

    # if title:
    #     box_plot.title = title

    data = [
        go.Box(
            y=df[column],
            name=column
        ) for column in metrics
    ] 
    
    fig = go.Figure(data=data)
    py.plot(fig, filename='test')

    # box_plot.add(column, df[column])
    # box_plot.render_to_file(output_path)
    # box_plot.render_to_png(output_path)


def stacked_time_serie(data, x_labels, chart_name):
    """docstring"""

    series_chart = pygal.StackedBar()

    series_chart.title = chart_name
    series_chart.x_labels = x_labels

    for item in data:
        series_chart.add(item, data[item])

    series_chart.render_to_file('new_discussions_by_year.svg')
    series_chart.render_to_png('new_discussions_by_year.png')


def topics_treemap(data, output):
    treemap = pygal.Treemap(style=LightStyle)
    treemap.title = "Tech Topics"

    for branch in data:
        treemap.add(branch, data[branch])
    
    treemap.render_to_file(output + '.svg')
    treemap.render_to_png(output + '.png')


