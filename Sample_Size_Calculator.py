import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.tools as tls
from dash.dependencies import Input, Output
from scipy import arange
import scipy.stats as st
import math

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


app = dash.Dash(__name__)
server = app.server
app.title = 'Sample Size Calculator'


app.config['suppress_callback_exceptions']=True

app.layout = html.Div([

                html.Div([
                    html.Div(
                        'Sample Size Calculator',
                        style={
                            'font-size': '1.5em', 
                            'font-weight': 'bolder', 'text-align': 'center',
                            'display': 'inline-block', 'width': '100%', 'padding': '10px 0px 10px 0px'
                        })
                    ],
                    style={
                        'position': 'fixed','top': '0', 'left': '0', 'width': '100%', 'height': '45px'
                        }),
                    
                html.Div([
                    html.Hr(style={'width': '90%'})],
                    style={
                        'position': 'absolute','top': '45', 'left': '0', 'width': '100%'
                        }),

                html.Div([

                	html.Div([

                		html.H3('Input the following parameters'),

                		html.Div('Type of Test:'),
                		dcc.RadioItems(
                			id='test',
                			options=[{'label': i, 'value': i} for i in ['z-test', 't-test']],
                			value='z-test',
                			labelStyle={'display': 'inline-block', 'padding': '3%'}
                			),

                		html.Div('Alternative:'),
                		dcc.RadioItems(
                			id='alternative',
                			options=[{'label': i, 'value': i} for i in ['one-sided', 'two-sided']],
                			value='two-sided',
                			labelStyle={'display': 'inline-block', 'padding': '3%'}
                			),

                		html.Div('Allow-to-vary Parameter:'),
                		dcc.RadioItems(
                			id='allow-to-vary',
                			options=[{'label': i, 'value': i} for i in ['none', 'alpha', 'power', 'delta']],
                			value='delta',
                			labelStyle={'display': 'inline-block', 'padding': '3%'}
                			),

                		html.Div(id='parameters'),

                		html.Div('Multiplicative Factor (𝑘 = n1/n2):'),
						html.Div([
							html.Div('n1 : n2 = ', style={'display': 'inline-block'}),
				    		html.Div([dcc.Input(
				    			id='n1',
							    type='number',
							    inputmode='numeric',
							    value='1',
							    min=1
							)], style={'display': 'table-cell'}),
							html.Div(' : ', style={'display': 'table-cell'}),
							html.Div([dcc.Input(
				    			id='n2',
							    type='number',
							    inputmode='numeric',
							    value='1',
							    min=1,
							)], style={'display': 'table-cell'})
							],
							style={
								'width': '90%',
								'display': 'inline-block',
								'padding': '2%'
							})
                		],
                		style={
                			'width': '40%', 
                			'display': 'table-cell',
                			'padding': '0 3% 0 0'
                			}),

                	html.Div([
                		
                		html.Div(id='output-container')

                		], 
                		style={
                			'display': 'table-cell',
                			'width': '50%'
                			})
                	],
                	style={
            			'position': 'absolute',
            			'top': '60', 
            			'left': '7%',
            			'width': '86%',
            			'height': '80%'
            			})
                ])


def calculate_sample_size(test="z-test", alpha=0.05, power=0.8, delta=0.5, sides="two-sided", k=1):
    """
    This function calculates the required sample size to conduct the A/B test given the parameters.
    ARGUMENTS:
        test: either 'z-test' or 't-test'
        alpha: the significance level of the test
        power: the power of the test 1-beta, where beta is defined as Type II error rate
        delta: effect size of the test, defined as (mu_1 - mu_2)/std
        sides: either 'one-sided' or 'two-sided'
        k: the multiplicative factor relating n_a to n_b, (i.e. n_a = k * n_b)
    It will return a single number if k=1, and (n_a, n_b) otherwise.
    NOTE: one of (alpha, power, delta, k) could be a list of elements, and a plot will generated.
    """
    
    if sides == 'one-sided':
        sig = alpha
    elif sides == 'two-sided':
        if isinstance(alpha, list): sig = [val/2 for val in alpha]
        else: sig = alpha / 2
    else:
        print("ERROR: Please specified whether it's a one-sided or two-sided test.")
        return
    
    num_lists = sum([isinstance(o, list) for o in (sig, power, delta, k)])
    if num_lists > 1:
        print("ERROR: At most one of (alpha, power, delta, k) could be a list.")
        return
    
    if test == "z-test":
        test_to_use = z_test_helper
    elif test == "t-test":
        test_to_use = t_test_helper
    else:
        print("ERROR: Please specified the test type, choose from: z-test, t-test.")
        return

    if num_lists == 0:
        n = test_to_use(sig, power, delta, k)
    elif isinstance(sig, list):
        x_list, x_label = get_range(alpha), 'significance level'
        n_list = [test_to_use(s, power, delta, k) for s in get_range(sig)]
    elif isinstance(power, list):
        x_list, x_label = get_range(power), 'power'
        n_list = [test_to_use(sig, p, delta, k) for p in get_range(power)]
    elif isinstance(delta, list):
        x_list, x_label = get_range(delta), 'effect size'
        n_list = [test_to_use(sig, power, d, k) for d in get_range(delta)]
    else:
        x_list, x_label = k, 'multiplicative factor'
        n_list = [test_to_use(sig, power, delta, c) for c in k]
        
    # Plot of n v.s. the given input
    if num_lists == 1:
        return plot_relation(x_list, n_list, x_label, k)
        
    if k == 1: return n[0]
    return n


def get_range(param_list):
	return list(arange(param_list[0], param_list[1], (param_list[1]-param_list[0])/10)) + [param_list[1]]


def z_test_helper(sig, power, delta, k):
    n = (1/k + 1) * (st.norm.ppf(sig) - st.norm.ppf(power))**2 / delta**2
    return k*n, n


def t_test_helper(sig, power, delta, k):
    df = max(sum(z_test_helper(sig, power, delta, k)) - 2, 0)
    n = 10
    while abs(n + k*n - df - 2) > 1e-6:
        df = n + k*n - 2
        n = (1/k + 1) * (st.t.ppf(sig, df) - st.norm.ppf(power))**2 / delta**2
    return k*n, n


def plot_relation(x_list, n, x_label, k):
    x_list,n = zip(*sorted(zip(x_list,n), key=lambda x: x[0]))
    n1,n2 = zip(*n)
    mpl_fig = plt.figure()
    plt.plot(x_list, n1, 'r')
    plt.plot(x_list, n2, 'b')
    plt.xlabel(x_label)
    plt.ylabel("sample size")
    if k != 1: plt.legend(["sample 1", "sample 2"])
    return mpl_fig


alpha_control = {'alpha': [
	html.Div('Significance Level (𝛼):'),
	html.Div([
		dcc.RangeSlider(
			id='alphaalpha',
			min=0,
			max=0.1,
			step=0.001,
			value=[0.01, 0.05],
			marks={i:round(i,2) for i in arange(0.01, 0.11, 0.01)}
		)], 
		style={
			'width': '90%',
			'display': 'inline-block',
			'padding': '5%'
		})
]}

power_control = {'power':[
	html.Div('Power (1-𝛽):'),
	html.Div([
		dcc.RangeSlider(
			id='powerpower',
			min=0.75,
			max=1,
			step=0.01,
			value=[0.8, 0.9],
			marks={i:round(i,2) for i in arange(0.75, 1.01, 0.05)}
		)], 
		style={
			'width': '90%',
			'display': 'inline-block',
			'padding': '5%'
		})
]}

delta_control = {'delta':[
	html.Div('Effective Size (𝛿 = (μ1-μ2)/σ):'),
	html.Div([
		dcc.RangeSlider(
			id='deltadelta',
			min=0,
			max=3,
			step=0.01,
			value=[0.5, 1],
			marks={i:round(i,2) for i in arange(0, 3.01, 0.3)}
		)], 
		style={
			'width': '90%',
			'display': 'inline-block',
			'padding': '5%'
		})
]}


for o in app.layout['allow-to-vary'].options:
	control = o['value']
	if control not in alpha_control:
		alpha_control[control] = [
		html.Div('Significance Level (𝛼):'),
		html.Div([
			dcc.Slider(
				id=control+'alpha',
				min=0,
				max=0.1,
				step=0.001,
				value=0.05,
				included=False,
				marks={i:round(i,2) for i in arange(0.01, 0.11, 0.01)}
			)], 
			style={
				'width': '90%',
				'display': 'inline-block',
				'padding': '5%'
			})
		]
	if control not in power_control:
		power_control[control] = [
		html.Div('Power (1-𝛽):'),
		html.Div([
			dcc.Slider(
				id=control+'power',
				min=0.75,
				max=1,
				step=0.01,
				value=0.8,
				included=False,
				marks={i:round(i,2) for i in arange(0.75, 1.01, 0.05)}
			)], 
			style={
				'width': '90%',
				'display': 'inline-block',
				'padding': '5%'
			})
		]
	if control not in delta_control:
		delta_control[control] = [
		html.Div('Effective Size (𝛿 = (μ1-μ2)/σ):'),
		html.Div([
			dcc.Slider(
				id=control+'delta',
				min=0,
				max=3,
				step=0.01,
				value=0.5,
				included=False,
				marks={i:round(i,2) for i in arange(0, 3.01, 0.3)}
			)], 
			style={
				'width': '90%',
				'display': 'inline-block',
				'padding': '5%'
			})
		]


def generate_control_id(value):
    return 'Control {}'.format(value)


@app.callback(
    dash.dependencies.Output('parameters', 'children'),
    [dash.dependencies.Input('allow-to-vary', 'value')
     ])
def update_vary_param(allow_to_vary):
	return alpha_control[allow_to_vary] + power_control[allow_to_vary] + delta_control[allow_to_vary]


def generate_output_id(value):
    return '{} container'.format(value)

@app.callback(
    Output('output-container', 'children'),
    [Input('allow-to-vary', 'value')])
def output_controls(allow_to_vary):
    # create a unique output container for each dyanmic control
    return html.Div(id=generate_output_id(
        allow_to_vary
    ))

def update_param_type(allow_to_vary):
	def update_params(test, alternative, n1, n2, alpha, power, delta):
		k = float(n1)/float(n2)
		md = dcc.Markdown('''
			Type of Test: %s
			Alternative: %s
			Significance Level: %s
			Power: %s
			Effective Size: %s
			Sample Size Ratio: %.2f
			''' % (test, alternative, alpha, power, delta, k))
		if allow_to_vary !='none':
			mpl_fig = calculate_sample_size(test=test, alpha=alpha, power=power, delta=delta, sides=alternative, k=k)
			plotly_fig = tls.mpl_to_plotly(mpl_fig, verbose=True)
			plotly_fig['layout']['margin'] = go.Margin(l=50, r=50, t=10, b=50)
			fig = dcc.Graph(figure=plotly_fig, id='plot', config={'displayModeBar': False})
			return md, fig
		else:
			n = calculate_sample_size(test=test, alpha=alpha, power=power, delta=delta, sides=alternative, k=k)
			if isinstance(n, float):
				n = math.ceil(n)
			else:
				n = (math.ceil(n[0]), math.ceil(n[1]))
			size = html.H4('Calculated Sample Size: %s' % str(n))
			return md, size
	return update_params

for o in app.layout['allow-to-vary'].options:
	app.callback(
    dash.dependencies.Output(generate_output_id(o['value']), 'children'),
    [dash.dependencies.Input('test', 'value'),
     dash.dependencies.Input('alternative', 'value'),
     dash.dependencies.Input('n1', 'value'),
     dash.dependencies.Input('n2', 'value'),
     dash.dependencies.Input(o['value']+'alpha', 'value'),
     dash.dependencies.Input(o['value']+'power', 'value'),
     dash.dependencies.Input(o['value']+'delta', 'value')
     ])(update_param_type(o['value']))


if __name__ == '__main__':
    app.run_server(debug=True)
