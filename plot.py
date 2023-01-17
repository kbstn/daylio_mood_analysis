import plotly.express as px
import pandas as pd

def create_lineplot(data: pd.DataFrame, y_col: str, title: str, target_line: 
    float = None,target_plot_color: str = '#E1BE6A', target_line_color: str = 'salmon', target_line_width: int = 3,
     target_line_dash: str = 'dot', plot_bgcolor: str = 'rgba(0,0,0,0)', 
     grid: bool = True):
    """
    Create a line plot using plotly express
    
    Parameters:
    - data (pd.DataFrame): The dataframe containing the data
    - x_col (str): The name of the column to be used as x-axis
    - y_col (str): The name of the column to be used as y-axis
    - title (str): Title for the plot
    - target_line (float, optional): Value for the target line. If not provided, target line will not be plotted
    - target_line_color (str, optional): Color for the target line
    - target_line_width (int, optional): Width of the target line
    - target_line_dash (str, optional): Dash style of the target line
    - plot_bgcolor (str, optional): Background color of the plot
    - grid (bool, optional): Show grid or not
    """
    fig = px.line(data, x=data.index, y=y_col, template="simple_white", title=title)
    fig.update_traces(line_color=target_plot_color, line_width=5)
    if target_line is not None:
        fig.add_shape(
            # add a horizontal "target" line
    #              type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
    #  x0=0, x1=1, xref="paper", y0=0, y1=0, yref="y"
             type="line", line_color=target_line_color, line_width=target_line_width, opacity=1, line_dash=target_line_dash,
             x0=0, x1=1, xref="paper", y0=target_line, y1=target_line, yref="y"
        )
    fig.update_layout(
        plot_bgcolor=plot_bgcolor,
        xaxis=dict(showgrid=grid),
    )
    return fig

def plot_two_df(data1: pd.DataFrame,data2: pd.DataFrame, y_col: str, title: str, plot_bgcolor: str = 'rgba(0,0,0,0)', grid: bool = True):

    # Find the overlapping date range
    overlap_range = pd.merge(data1, data2, left_index=True, right_index=True).index

    # Get the minimum and maximum values of the overlapping date range
    min_index = overlap_range.min()
    max_index = overlap_range.max()

    # Get the range of datetimeindex for both dataframes
    x_range = [min_index, max_index]
    # Plot the two dataframes
    fig = px.line(data1, x=data1.index, y=y_col, range_x=x_range)
    fig.update_traces(line_color='#E1BE6A', line_width=5)


    fig.add_trace(px.line(data2, x=data2.index, y=y_col,range_x=x_range).update_traces(line_color='#40B0A6', line_width=5).data[0])
    fig.update_layout(
        plot_bgcolor=plot_bgcolor,
        xaxis=dict(showgrid=grid),
    )
    return fig
   