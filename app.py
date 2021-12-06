import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# For this lab, we will be working with the 2019 General Social Survey one last time.
%%capture
gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

# Here is code that cleans the data and gets it ready to be used for data visualizations:
mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')


# Markdown Text -- Summary
markdown_text = "WILL WRITE THIS LATER"



# Problem 2
import plotly.graph_objects as go
import pandas as pd

df = prob2

prob2_fig = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df['Mean Income'], df['Mean Occupational Prestige'], df['Mean Socioeconomic Index'], df['Mean Years of Education']],
               fill_color='lavender',
               align='left'))
])
prob2_fig.show()



# Problem 3
# this groups by male_breadwinner and sex and then returns only the count of male_breadwinner by sex
prob3 = gss_clean.groupby(['male_breadwinner','sex']).agg({'male_breadwinner':'count'})#.reset_index()

# rename column to distinguish from original column name
prob3 = prob3.rename(columns={"male_breadwinner":"male_breadwinner_count"})

# reset multiindex back to single
prob3 = prob3.reset_index(level=[0,1])


# add x and y-axis labels but not a title
# use barmode='group' to group the data 
prob3_fig = px.bar(prob3, x='male_breadwinner', y='male_breadwinner_count', color='sex',
      barmode='group', labels={'male_breadwinner':'Level of Agreement', 'male_breadwinner_count':'Count'})

prob3_fig.show()





# Problem 4
prob4_fig = px.scatter(gss_clean.head(200), x='job_prestige', y='income', 
                 color='sex',
                 trendline='ols',
                 #trendline='lowess',
                 height=600, width=600,
                 labels={'job_prestige':'Job Prestige', 
                        'income':'Income'},
                 hover_data=['education','socioeconomic_index'])
prob4_fig.update(layout=dict(title=dict(x=0.5)))
prob4_fig.show()




# Problem 5
# A
prob5a_fig = px.box(gss_clean, x='income', y = 'sex', color = 'sex',
                   labels={'income':'Income', 'sex':''})
prob5a_fig.update(layout=dict(title=dict(x=0.5)))
prob5a_fig.update_layout(showlegend=False)
prob5a_fig.show()

# B
prob5b_fig = px.box(gss_clean, x='job_prestige', y = 'sex', color = 'sex',
                   labels={'job_prestige':'Job Prestige', 'sex':''})
prob5b_fig.update(layout=dict(title=dict(x=0.5)))
prob5b_fig.update_layout(showlegend=False)
prob5b_fig.show()




# Problem 6
# create new dataframe containing 3 columns
prob6 = gss_clean[['income','sex','job_prestige']]
# create new feature that breaks 'job_prestige' into six categories with equally sized ranges
prob6['split_JP_cat'] = pd.cut(prob6['job_prestige'],6)
# drop all rows with any missing values 
prob6 = prob6.dropna()
# create facet grid with 3 rows and 2 columns where each cell contains
# an interactive box plot comparing the income distributions of men and women
# for each of these new categories 

prob6_fig = px.box(prob6, x='income', y='sex', color='sex', 
             facet_col='split_JP_cat', facet_col_wrap=2,
#              hover_data = ['votes', 'Biden thermometer', 'Trump thermometer'],
            labels={'income':'Income', 'sex':''},
             color_discrete_map = {'male':'blue', 'female':'red'},
#             title = 'Vote choice as of December 2019',
#             text='rowtext', 
             width=1000, height=600
            )
prob6_fig.update(layout=dict(title=dict(x=0.5)))
prob6_fig.update_layout(showlegend=False)
# fig.for_each_annotation(lambda a: a.update(text=a.text.replace("vote=", "")))
prob6_fig.show()





# Problem 7
# external style sheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# Collect all of the code needed to run an app, including the package import, data loading, and 
# cleaning steps, and the code to generate the individual elements that populate the dashboard. 
# Start a new Jupyter notebook and paste all of this code into a single cell. If you used jupyterdash, 
# change the code to regular dash by changing app = dash.Dash(__name__, external_stylesheets=external_stylesheets) 
# to app = JupyterDash(__name__, external_stylesheets=external_stylesheets) and 
# app.run_server(mode='inline', debug=True) to app.run_server(debug=True).


# To create the dashboard app using jupyterdash, we write instead:
# app = JupyterDash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.H1("Exploring the GSS Data"),
        dcc.Markdown(children = markdown_text),
        
        html.H2("Table Comparing Mean Income, Occupational Prestige, Socioeconomic Index, and Years of Education between Men and Women"),
        dcc.Graph(figure=prob2_fig),
        
        html.H2("Barplot of Count of Men and Women per Level of Agreement to male_breadwinner"),
        dcc.Graph(figure=prob3_fig),
        
        html.H2("Scatterplot of Job Prestige and Income (color-coded by gender) with Best-Fit Lines"),
        dcc.Graph(figure=prob4_fig),
        
        html.Div([            
            html.H2("Boxplot of Distribution of Income for Men and Women"),
            dcc.Graph(figure=prob5a_fig)
        ], style = {'width':'48%', 'float':'left'}),
        html.Div([
            html.H2("Boxplot of Distribution of Job Prestige for Men and Women"),
            dcc.Graph(figure=prob5b_fig)
        ], style = {'width':'48%', 'float':'right'}),

        html.H2("Scatterplot of Job Prestige and Income (color-coded by gender) with Best-Fit Lines"),
        dcc.Graph(figure=prob6_fig)
        
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True, port=8050, host='0.0.0.0')
    # app.run_server(debug=True, port=8050)
    
