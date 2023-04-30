import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
import dash_table as dt
from jupyter_dash import JupyterDash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

web_text = '''
Pew Research Center (https://www.pewresearch.org/short-reads/2023/03/01/gender-pay-gap-facts/) talks about the disparity in women wage and its existence for the past 20 years. It also provides interesting metrics about the differences in choices made at work by gender and how it may affect the pay between genders.
'''

gss_text = ''' 
The General Social Survey (GSS) is a sociological/attitudinal survey conducted since 1972 by NORC (The National Opinion Research Center) in collaboration with National Science Foundation. These surveys aims to understand complex trends of American society. The survey covers a wide range of topics, including political behavior, social inequality, race relations, gender roles, and religion. Surveys are conducted for a sample of US population through face-to-face or telephone interviews. The data collected is available to the public(https://gssdataexplorer.norc.org/) and can help in research and analysis in related fields.

We will explore gss_clean data  that contains the following features:

id - a numeric unique ID for each person who responded to the survey

weight - survey sample weights

sex - male or female

education - years of formal education

region - region of the country where the respondent lives

age - age

income - the respondent's personal annual income

job_prestige - the respondent's occupational prestige score, as measured by the GSS using the methodology described above

mother_job_prestige - the respondent's mother's occupational prestige score, as measured by the GSS using the methodology described above

father_job_prestige -the respondent's father's occupational prestige score, as measured by the GSS using the methodology described above

socioeconomic_index - an index measuring the respondent's socioeconomic status

satjob - responses to "On the whole, how satisfied are you with the work you do?"

relationship - agree or disagree with: "A working mother can establish just as warm and secure a relationship with her children as a mother who does not work."

male_breadwinner - agree or disagree with: "It is much better for everyone involved if the man is the achiever outside the home and the woman takes care of the home and family."

men_bettersuited - agree or disagree with: "Most men are better suited emotionally for politics than are most women."

child_suffer - agree or disagree with: "A preschool child is likely to suffer if his or her mother works."

men_overwork - agree or disagree with: "Family life often suffers because men concentrate too much on their work.

'''

gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

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


df2 = gss_clean.groupby('sex').agg({'socioeconomic_index':'mean',
                                        'income':'mean',
                                      'education':'mean',
                                      'job_prestige':'mean'})
df2 = df2.reset_index().rename({'sex':'Gender','socioeconomic_index':'Avg Socioeconomic Index','income':'Avg Income','education':'Avg Years of Education','job_prestige':'Avg Job Prestige'}, axis=1)
round(df2, 2)

table = ff.create_table(round(df2, 2))


gss_scatter = gss_clean[~gss_clean.income.isnull()]
fig_scatter = px.scatter(gss_scatter, x='job_prestige', y='income', 
                 color = 'sex', 
                 trendline='ols',
                title = 'Occupational Prestige Vs Income',
                 height=600, width=600,
                 labels={'job_prestige':'Occupational Prestige', 
                        'income':'Income'},
                 hover_data=['education', 'socioeconomic_index'],
                        color_discrete_map = {'male':'blue', 'female':'green'},)
fig_scatter.update(layout=dict(title=dict(x=0.5)))



fig_income = px.violin(gss_clean, y='income', x = 'sex', color = 'sex',
                   labels={'income':'Income', 'sex':''},
                       title = 'Distribution of Income by Gender',
                      color_discrete_map = {'male':'blue', 'female':'green'},)
fig_income.update(layout=dict(title=dict(x=0.5)))
fig_income.update_layout(showlegend=False)



fig_prestige = px.violin(gss_clean, y='job_prestige', x = 'sex', color = 'sex',
                   labels={'job_prestige':'Occupational Prestige', 'sex':''},
                         title = 'Distribution of Occupation Prestige by Gender',
                        color_discrete_map = {'male':'blue', 'female':'green'},)
fig_prestige.update(layout=dict(title=dict(x=0.5)))
fig_prestige.update_layout(showlegend=False)



df6 = gss_clean[['income','sex','job_prestige']]
df6['job_prestige_cat']=pd.cut(df6.job_prestige, 6,labels=['15 to 27','27 to 37','37 to 48','48 to 59','59 to 69','69 to 80'])
df6['job_prestige_cat'] = df6['job_prestige_cat'].astype('category')
df6 = df6.dropna()


fig_box = px.box(df6, x='income', y='sex', color='sex', 
             facet_col='job_prestige_cat',facet_col_wrap=2,
             color_discrete_map = {'male':'blue', 'female':'green'},
            labels={'job_prestige_cat':'Occupational Prestige Category','sex':'Gender','income':'Income'},
            title = 'Occupational Prestige Categories by Gender',
            width=1000, height=600)
fig_box.update(layout=dict(title=dict(x=0.5)))
fig_box.update_layout(showlegend=True)
fig_box.for_each_annotation(lambda a: a.update(text=a.text.replace("vote=", "")))


x_columns = ['satjob', 'relationship', 'male_breadwinner', 'men_bettersuited', 'child_suffer', 'men_overwork']
y_columns = ['sex','region','education'] 
gss_ft = gss_clean[x_columns + y_columns].dropna()


app = JupyterDash(__name__, external_stylesheets=external_stylesheets)
selections = dbc.Card(
        children=[
            html.Div(
                [
                    dbc.Label("x-axis feature"),            
                    dcc.Dropdown(id='x-axis',
                             options=[{'label': i, 'value': i} for i in x_columns],
                             value='male_breadwinner',className="dropdown"),
                ]
            ),
            html.Div(
                [
                    dbc.Label("y-axis feature"),
                    dcc.Dropdown(id='y-axis',
                             options=[{'label': i, 'value': i} for i in y_columns],
                             value='sex', className="dropdown"),
                ]
            ),
        ],
)

app.layout = html.Div(children=[
    html.Div(children=[
        html.H3(children='Exploring General Social Survey'),
        html.H6(children='Data year - 2019', style={'marginTop': '-15px', 'marginBottom': '30px'}),
        
    ], style={'textAlign': 'center'}),
    
    html.Div(className='parent2',children=[  
        dcc.Markdown(children = web_text),
        dcc.Markdown(children = gss_text),
    ], style={'textAlign': 'left'}),
    
   
    html.H2("Number of men and women with each level of agreement to male breadwinner"),
        
        html.Div([
            
            html.H3("x-axis feature"),
            
            dcc.Dropdown(id='x-axis',
                         options=[{'label': i, 'value': i} for i in x_columns],
                         value='male_breadwinner'),
            
            html.H3("y-axis feature"),
            
            dcc.Dropdown(id='y-axis',
                         options=[{'label': i, 'value': i} for i in y_columns],
                         value='sex'),
                      
                ]
            ),
       dcc.Graph(id="graph"),
    
    html.H2("Comparing mean income, occupational prestige, socioeconomic index, and years of education for men and for women"),
    html.Div(className='parent', children=[
            dcc.Graph(figure=table, className='plot'),
        ]),

    html.H2("Distribution of Income"),
    html.Div(className='parent', children=[
            dcc.Graph(figure=fig_income, className='plot',style={'display': 'inline-block'}),
            dcc.Graph(figure=fig_prestige, className='plot', style={'display': 'inline-block'}),
        ]),
    
    html.Div(className='parent', children=[
            dcc.Graph(figure=fig_box, className='plot',style={'display': 'inline-block','width': '48%'}),
             dcc.Graph(figure=fig_scatter, className='plot', style={'display': 'inline-block','width': '52%'}),
        ]),    

], style={'padding': '2rem'})

@app.callback(Output(component_id="graph",component_property="figure"), 
                  [Input(component_id='x-axis',component_property="value"),
                   Input(component_id='y-axis',component_property="value")])

def make_figure(x, y):
    df = pd.crosstab(gss_ft[x], gss_ft[y]).reset_index()
    
    df = pd.melt(df, id_vars = x, value_vars = gss_ft[y].unique().tolist() )
    df = df.rename({'value':'Count'}, axis=1)

    fig_bar = px.bar(df, x=x, y='Count', color=y,
            text='Count',
            barmode = 'group')
    fig_bar.update_layout(showlegend=True)
    fig_bar.update(layout=dict(title=dict(x=0.5)))

    return fig_bar

if __name__ == '__main__':
    app.run_server(mode='inline', debug=True, port=8051)
