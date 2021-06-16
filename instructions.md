# Workshop: Make a COVID-19 web dashboard in an hour using Plotly Dash

## 1 Understand the basic structure of a web app

_**5 mins**_

Aim: To be aware of the basic flow and technologies used in a web app. Hopefully this will help you put the workshops
activities in context.

### Browser: Provides the user interface

You all know what this is!

### HTML: Provides the structure of the web page

Defined using tags e.g.

```html
<!DOCTYPE html>
<html>
<head>
    <!-- This section mostly tells the browser info about the page --!>
</head>
<body>
<!-- This section is what the user sees in the web page --!>
<h1>This is a heading</h1>
<p>This is a paragraph</p>
</body>
</html>
```

There are plenty of references and tutorials on HTML. For today all you need to remember is that HTML tags provide the
structure of the page.

#### CSS: Styles the HTML (colours, fonts, spacing etc)

Here's an example of CSS styling for the ```<h1>``` tag:

```css
h1 {
    font-family: "American Typewriter";
    font-weight: bold;
    color: blueviolet;
    padding: 5em;
}
```

There are different ways to add the styles to your code. We wil stick to adding styles in a `.css` file. You tell
the `.html` file where the css file is in the head section of the page.

```html

<head>
    <link rel="stylesheet" href="mystyle.css">
</head>
```

To make it even easier we are going to use someone else's CSS, in this case a widely ised library
called [Bootstrap](https://getbootstrap.com/docs/5.0/getting-started/introduction/). They even give you the HTML code to
copy and paste.

```html

<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-+0n0xVW2eSR5OomGNYDnhzAbDsOXxcvSN1TPprVMTNDbiYZCxYbOOl7+AMvyTG2x" crossorigin="anonymous">
</head>
```

When a browser receives a web page to display, it generates a tree structure to represent the page called the Domain
Object Model, DOM. The DOM has methods that allow programmatic access to elements in this tree.

![The HTML DOM Tree of Objects](img_dom_tree.gif)
[Source w3schools.com]: https://www.w3schools.com/js/pic_htmltree.gif

CSS is applied to one or more HTML elements using 'selectors'. A selector is a mechanism to locate a particular HTML
element on a web page and apply styling to it.

For today, you just need to know that the look and feel of the page is mostly determined by styles that are defined
using CSS. You programmatically select one or more elements to apply the defined styles to.

### JavaScript: Adds interactivity to a web page

JavaScript is a programming language. It (mostly) runs in the browser and is used to support interactivity. We are not
going to use any JavaScript directly. Plotly Dash abstracts this away for us by provides python methods that we will
use.

### Web server

Most websites use some kind of server technology to dynamically generate data to be displayed. There are numerous
languages and technologies you can use for this, we are going to use the Python version of Plotly Dash.

Dash itself makes use of another framework called Flask which is used to create web apps. We might have a look at this
in another session and see how you can include visualisations and machine learning models in a web app.

### HTTP: A protocol that supports communication between the web broswer and web server

HyperText Transfer Protocol (HTTP) is a protocol (a set of rules) for transferring images, text and audio between a web
browser and a web server.

For now you can forget about HTTP as we won't need to code anything that directly expresses HTTP.

### Summary

![Structure of a web app](img_web_app.jpeg)
[Source Mark Dabbs, 2019]: https://reinvently.com/blog/fundamentals-web-application-architecture/

- HTML provides the page structure.
- CSS provides the styling.
- JavaScript provides interactivity in the browser.
- Python (or other) code runs on the server to generate the charts and other page content.
- HTTP is the set of rules used to communicate between the browser and our server. The browser makes a request and the
  server sends a response.

The good news is we are going to use Python methods in Plotly Dash for all of these so you don't need to learn HTML, CSS
and JavaScript.

## 2 Create a simple web dashboard

_**10 mins**_

Aim: Recreate Albert's COVID-19 chart and display it in a Dash web app that uses Bootstrap styling.

### What is Plotly Dash?

Plotly Dash is a high level library that provides a way for you to create a web app dashboard using Python (as well as R
and Julia). It is designed for creating "web analytics applications" [Plotly dash](https://dash.plotly.com/introduction)
.

Under the covers Dash builds on Plotly.js, React.js and Flask.

You can build dash apps with multiple pages, however to do that you will need to understand a little more about HTTP and
routing. For today, we are going to build a single page app.

### Create the basic web page

Create a new python file called `app.py`. Add the following code:

```python
# Import the dash libraries
import dash
import dash_html_components as html

# Creates the Dash web app
app = dash.Dash(__name__)

# Defines the layout of the page. Uses python methods to generate HTML.
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
])

# Runs the web app. By default you should be able to access it at http://127.0.0.1:8050/ in a web browser
if __name__ == '__main__':
    app.run_server(debug=True)
```

Run this app with `python app.py` and go to http://127.0.0.1:8050/ in your web browser.

### Add styling

Let's use bootstrap to provide the CSS stylesheet using the dash-bootstrap-components library.

You need to add the import:

```python
import dash_bootstrap_components as dbc
```

Then apply the stylesheet to the Dash app:

```python
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
```

The code in `app.py` now looks like this:

```python
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
])

if __name__ == '__main__':
    app.run_server(debug=True)
```

Run the app in your IDE or use the command line from the venv e.g. `python app.py`

Go to [http://127.0.0.1:8050/](http://127.0.0.1:8050/) in a browser to view the app.

Experiment with different [themes](https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/) and choose one
you like. You may need to refresh the browser to see the changes, though you shouldn't need to stop and restart the Dash
app.

<hr>
<i class="fa fa-lightbulb-o" aria-hidden="true"></i>
Responsive design

Bootstrap provides a way to make your design 'responsive', that is it tries to alter the style appropriately for browsers on different size devices (think difference between small portrait mobile phone and larger landscape laptop). To support the responsive design you need to move HTML elements into a container. Alter your layout to this:

  ```python
    app.layout = dbc.Container(children=
        [
            html.H1("Hello Dash"),
            html.P("This is my first Dash app")
        ],
    fluid=True,
)
  ```

### Add the chart

First we need to generate the chart. The following code recreates the chart from Albert's workshop. Code to prepare the
data and generate the charts is in `prepare_data.py`. The Plotly Dash component that we will use only supports the
Plotly graph libraries, Plotly Express and Plotly Graph Objects (GO).

Apologies, I'm not familiar with R so apologies if I haven't interpreted the chart correctly.

`create_chart(country_data, country_list)` takes two parameters, the prepared data and a list of countries. In Albert's
chart you used the top 10, however this method is written to allow a subset of the top 10 list to be used. We will need
this in activity 3 to generate an interactive chart.

Run `python prepare_data.py` to generate and display the chart.

Now let's create the chart in our Dash app.

First, add the following imports to `app.py`:

- `dash_core_components` provides a Python graph class with methods. We will use this to display the chart in the web
  page layout.
- `pandas` is used to read the data from a .csv file (you could use another library if you prefer).
- `plotly.graph_objects` is used to create a chart, this replaces `ggplot` that you used with R.
- `prepare_data` provides python code to create the chart using pandas and plotly go.

```python
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objects as go

import prepare_data
```

Now add the code to generate the charts. Since the focus is on the web app then I'm just giving you the code for the
charts.

It isn't vital to declare the global variables with defaults, I've done this so that if the data file can't be read then
at least something will still display on the web page.

The chart variable is `figure_static`.

Add the following code to the start of `app.py` after the imports.

```python
# Global variables for the static chart
msg_no_data = 'No chart to display'
fig_static = go.Figure(data=[go.Table(header=dict(values=[msg_no_data]))])
df_country_data = pd.DataFrame()
top_10_country_list = []

# Path to the John Hopkins dataset
csv_file = "https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series"
"/time_series_covid19_confirmed_global.csv"

# Use the functions in prepare_data.py to prepare the data and create the chart  
try:
    df_raw = pd.read_csv(csv_file)
    df_cleaned_data = prepare_data.clean_data(df_raw)
    df_country_data = prepare_data.consolidate_country_data(df_cleaned_data)
    top_10_country_list = prepare_data.get_top_10_country_list(df_country_data)
    fig_static = prepare_data.create_chart(df_country_data, top_10_country_list)
except (FileNotFoundError, error.HTTPError) as e:
    print(f'Could not find file {csv_file}. Error {e}')
```

To make the chart visible in your web page layout, add a Dash core components Graph object within the layout.

The value assigned to the `figure` parameter is the name of the variable for the chart, e.g.

```python
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    dcc.Graph(figure=fig_static)
])
```

### There you have it, a web app with a chart!

<hr>
<i class="fa fa-lightbulb-o" aria-hidden="true"></i> 
Experiment:

- add different chart types ([e.g. try adding example code for a PlotlyExpress chart](https://plotly.com/python/plotly-express/))
- use different HTML components ([try adding an image to the page](https://dash.plotly.com/dash-html-components/img))
- use different styles and layouts (try experimenting with [Bootstrap column and row layouts](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/), you will also need to use html.Col and html.Row)
<hr>

## 3 Add chart interactivity using callbacks

_**15 mins**_

Aim: Create a version of the chart that allows the user to select from the top 10 countries.

A person can select one or more countries using an drop down list. When they have made a selection the chart will update
to show only the countries selected.

To do this we will create:

- an HTML drop down list with the top 10 countries.
- a new Graph using a figure variable called `figure_select`
- a Dash callback function that listens for changes to the HTML drop down and then updates the Graph to display the
  traces for the selected countries

### What is a Dash callback?

A callback is a Python decorator (function) that is automatically called by Dash whenever a particular component's (
referred to as the Input) property changes and makes a change to another component (the Output) as a result.

The basic structure of a callback is:

```python
@app.callback(Output(component_id='my-output', component_property='a_property'),
              [Input(component_id='my-input', component_property='another_property')]
              )
def update_output_div(input_value):
    return 'Output: {}'.format(input_value)
```

- You can use any name for the function that is wrapped by the @app.callback decorator. The convention is that the name
  describes the callback output(s).

- You can use any name for the function arguments, but you must use the same names inside the callback function as you
  do in its definition, just like in a regular Python function. The arguments are positional: first the Input items and
  then any State items are given in the same order as in the decorator.

- You must use the same id you gave a Dash component in the app.layout when referring to it as either an Input or Output
  of the @app.callback decorator.

- The @app.callback decorator needs to be directly above the callback function declaration. If there is a blank line
  between the decorator and the function definition, the callback registration will not be successful.

### Add the new chart to the layout

Add the following to the global variables in `app.py`.

NB: This isn't strictly necessary. It just provides a default in case the desired chart isn't generated for any reason:

```python
fig_select = go.Figure(data=[go.Table(header=dict(values=[msg_no_data]))])
```

Within the layout add a new HTML H2 heading and a Graph component.

Notice that we are providing a value for `id` as well as a `figure`. The`id` is used to allow the element to be selected
for the callback.

```python
    html.H2("Example of an interactive chart (using Dash callbacks"),
dcc.Graph(id='fig_selected_countries', figure=fig_select),
```

Aside: You should be able to view the page source in your browser and find the element with the
id `fig_selected_countries`.

Check that the new heading and chart are visible in your Dash app.

### Add the HTML drop down

You would need to understand how
a [multi select HTML drop down](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select) works to know the
syntax.

The code you will need to create the dropdown is given to you in the interests of time.

`html.Label` provides text that will be displayed above the dropdown. It is linked to the dropdown by using the
dropdown's `id` as the value of `htmlFor`.

`dcc.Dropdown` creates a dropdown with the following properties:

- `id="dd_countries"` defines the `id`
- `options=[{"label": x, "value": x} for x in top_10_country_list],` uses the top_10_country_list variable which is a
  Python list we created in the global variables section
- `value=[]` provides an list to hold the values that have been selected in the dropdown, it iterates through the list
  adding a new option to the dropdown for each country
- `multi=True` makes this a multi select rather than a single item select dropdown

```python
    html.Label("Select country/countries:", htmlFor="dd_countries"),
    dcc.Dropdown(id="dd_countries",
             options=[{"label": x, "value": x} for x in top_10_country_list],
             value=[],
             multi=True),
```

Add the above code before the Graph in the layout.

Check the drop down is displayed in your Dash app.

### Create the callback

To create the callback we need to:

- Define the Input: identify the component id (e.g. id of an html element) and component property that the user will
  interact with

- Define the Outputs: identify the component id and property that will be updated after we make a change

- Write a Python function using the @callback decorator. The function will be run when the Input has been selected

The Input and Output are components provided in the dash.dependencies module so you will need the add the relevant
import to `app.py`:

```python
from dash.dependencies import Output, Input
```

The callback should be defined in `app.py` after the layout, add the following structure (it will result in errors in
your IDE for now):

```python
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
])


@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return 'Output: {}'.format(input_value)
```

Let's walk through the elements of the callback. For this example we will use only one Input and Output though it is
possible to use multiple.

**Output**:
The component that will be updated by the callback is the Graph with the id of `fig_selected_countries`. Specifically,
the 'figure' property of the Graph will be updated.

The Output is therefore:
`Output(component_id='fig_selected_countries', component_property='figure')`
which can be abbreviated so long as the arguments appear in the correct order:
`Output('fig_selected_countries', 'figure')`

**Input**
The id of the dropdown component is "dd_countries". The countries that are selected are held in the `value=` parameter,
which in this case is a list.

The Input is therefore:
`Input(component_id='dd_countries', component_property='value')` or `Input('dd_countries', 'value')`

**Callback function**:
The function will take the list of selected countries and pass this to the `create_chart` function in `prepare_data.py`.
This will return an updated figure.

The function might look like this:

```python
def update_figure_select(selected_countries):
    fig_select_updated = prepare_data.create_chart(df_country_data, selected_countries)
    return fig_select_updated
```

To put this all together our callback looks like this:

```python
@app.callback(Output('fig_selected_countries', 'figure'), Input('dd_countries', 'value'))
def update_fig_select(selected_countries):
    fig_select_updated = prepare_data.create_chart(df_country_data, selected_countries)
    return fig_select_updated
```

### There you have it, a web app with an interactive chart!

Test out your web app, select a few countries and see the chart change.

In case you haven't already seen it, there is a completed version of the code in `app_final.py.`


<hr>
<i class="fa fa-lightbulb-o" aria-hidden="true"></i> Use chart interactivitiy in Express or Go

Not all interactivity requires Dash. You can add some interaction in the chart itself using with Plotly Express or Plotly Go.  

Try and apply the slider to your interactive chart. There is a function called `add_range_slider(figure)` in `prepare_data.py` that you can use.

<hr>

_**The end (hopefully in under an hour)!**_
