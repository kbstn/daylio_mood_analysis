import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

def plot_two_df(data1: pd.DataFrame,data2: pd.DataFrame, y_col: str, title: str,color1: str ='#DE7E21',color2: str ='#3481C5', plot_bgcolor: str = 'rgba(0,0,0,0)', grid: bool = True):

    # Find the overlapping date range
    overlap_range = pd.merge(data1, data2, left_index=True, right_index=True).index

    # Get the minimum and maximum values of the overlapping date range
    min_index = overlap_range.min()
    max_index = overlap_range.max()

    # Get the range of datetimeindex for both dataframes
    x_range = [min_index, max_index]
    # Plot the two dataframes

    # todo: replace px line with go.scatter to add names and have a legend plotted
    fig = px.line(data1, x=data1.index, y=y_col, range_x=x_range)
    fig.update_traces(line_color=color2, line_width=5)


    fig.add_trace(px.line(data2, x=data2.index, y=y_col,range_x=x_range).update_traces(line_color=color1, line_width=5).data[0])
    fig.update_layout(
        plot_bgcolor=plot_bgcolor,
        title_text="Plot of Z-Scores Weight (orange) against Mood (blue)",
        xaxis=dict(showgrid=grid),)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='grey')
    # changing orientation of the legend
    fig.update_layout(legend=dict(
    orientation="h",

    ))  
    return fig
   
def plot_double_axis(df,col1,col2,color1='#3481C5',color2='#B5B5B5'):
    """
    This function plots two graphs on the same figure with a secondary y-axis.
    The first graph is plotted on the primary y-axis (left) and the second graph is plotted on the secondary y-axis (right).
    The user can enable or disable each graph by clicking on the label.

    Parameters:
    df (DataFrame): DataFrame containing the data for plotting.
    col1 (str): Column name of the data for the first graph.
    col2 (str): Column name of the data for the second graph.

    Returns:
    Plotly figure object
    """
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add trace for the first graph (col1) to the primary y-axis
    fig.add_trace(
        go.Scatter(x=df.index, y=df[col2], name=col2,line=dict(
                    color=color1,
                    width=5)), secondary_y=True)

    # Add trace for the second graph (col2) to the secondary y-axis
    fig.add_trace(
            go.Scatter(x=df.index, y=df[col1], name=col1,line_color=color2),
            secondary_y=False)

    # Add figure title
    fig.update_layout(
        title_text="Plot of <b>"+col1+"</b> and <b>"+col2+"</b>")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>"+col2+"</b>", secondary_y=True)
    fig.update_yaxes(title_text="<b>"+col1+"</b>", secondary_y=False)

    #make the background transparent
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='grey')
    # Set the range of primary y-axis to [min(col1), max(col1)]
    fig.update_yaxes(range=[min(df[col1]), max(df[col1])], secondary_y=False)
    # Add horizontal line at y=0 of the primary y-axis
    fig.update_layout(shapes=[dict(y0=0, y1=0, x0=min(df.index), x1=max(df.index), line_dash='dot',line_color='grey', yref='y2', xref='x')])
    fig.update_yaxes(showgrid=False, gridwidth=1, gridcolor='grey')
    fig.update_layout(legend=dict(
    orientation="h",xanchor = "center",  # use center of legend as anchor
                     x = 0.5)) 

    return fig
