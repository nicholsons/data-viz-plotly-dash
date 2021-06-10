# Workshop: How to make a COVID-19 web dashboard in under an hour using Plotly Dash

## Basic structure of a web app

This is a very quick overview of how web apps works. You need to understand the basic flow and technologies in order to
create a web app.

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

When a browser receives a web page to display, it generates a tree structure to represent the page called the Domain
Object Model, DOM. The DOM has methods that allow programmatic access to elements in this tree.

CSS is applied to one or more HTML elements using 'selectors'. A selector is a mechanism to locate a particular HTML
element on a web page and apply styling to it.

For today, you just need to know that the look and feel of the page is mostly determined by styles that are defined
using CSS. You programmatically select one or more elements to apply the defined styles to.

### JavaScript: Adds interactivity to a web page

JavaScript is a programming language. It (mostly) runs in the browser and is used to support interactivity. We are not
going to use any JavaScript directly. Plotly Dash abstracts this away for us by provides python methods that we will
use.

For now you can forget that JavaScript exists!

### Web server

Most websites use some kind of server technology to dynamically generate data to be displayed. There are numerous
languages and technologies you can use for this, we are going to use the Python version of Plotly Dash. 

Dash itself makes use of another framework called Flask which is used to create web apps. We might have
a look at this in another session and see how you can include visualisations and machine learning models in a web app.

### HTTP: A protocol that supports communication between the web broswer and web server

HyperText Transfer Protocol (HTTP) is a protocol (a set of rules) for transferring images, text and audio between a web
browser and a web server.

For now you can forget about HTTP as we won't need to code anything that directly expresses HTTP.

### Summary

![Structure of a web app](web_app.jpeg)
[Source Mark Dabbs, 2019]: https://reinvently.com/blog/fundamentals-web-application-architecture/

- HTML provides the page structure.
- CSS provides the styling.
- JavaScript provides interactivity in the browser.
- Python (or other) code runs on the server to generate the charts and other page content.
- HTTP is the set of rules used to communicate between the browser and our server. The browser makes a request and the server sends a
  response.

The good news is, you don't need to learn any of the above as we are going to use Python methods in Plotly Dash for all
of these!

Sounds like a lot to learn? Not if you use frameworks and libraries to help you! We are going to use all of these in the
next 45 minutes!

## How to use python Plotly Dash to create a simple web data dashboard

### What is Plotly Dash?

Plotly Dash is a high level library that provides a way for you to create a web app dashboard using Python (as well as R
and Julia). It is designed for creating "web analytics applications" [Plotly dash](https://dash.plotly.com/introduction).

Under the covers Dash builds on Plotly.js, React.js and Flask.

You can build dash apps with multiple pages, however to do that you will need to understand a little more about HTTP 
and routing. For today, we are going to build a single page app.

### Create the basic web page
Create a new python file called `app.py`.
Add the following code:
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

The code now looks like this:
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

Experiment with different [themes](https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/) and choose one 
you like. You may need to refresh the browser to see the changes but you shouldn't need to stop and restart the Dash app.

> Stretch:
Bootstrap provides a way to make your design 'responsive', that is it tries to alter the style appropriately for 
browsers on different size devices (think difference between small portrait mobile phone and larger landscape laptop).
To support the responsive design you need to move HTML elements into a container.
Alter your layout to this:
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
Firstly we need to generate the chart. The following code recreates the chart from Albert's {TODO: add correct reference}
Add this code to app.py (or you could create a separate code file if you prefer).
```python
def make_chart():
data = pd.read_csv("https://cdn.opensource.faculty.ai/world-phones/data.csv")
```


To add a chart we need to import dash_core_components:
```python
import dash_core_components as dcc
```

We then need to add the chart control to the layout:


### Voila! A web app

## How to add chart interactivity using callbacks

