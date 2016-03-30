"""Variables for plots html report generator"""

tmp = 'c:\tmp'            # temporary folder to move corrupt files to
index = r'index.html'  # filename for html files

br = '<br>'
footer = '\n</div></body></html>'
img_src = '\n<img height="%s" src="%s">'
timestamp = 'REGION: <span style="color:red; weight=bold">%s</span> '
url_dir = '\n<p><a href="%s" target="_blank">%s</a></p>'
url_img = '\n<a href="%s" ><img height="%s" title="%s" src="%s"></a>' # target="_blank"
thum_size=150
plots_per_row=4

header = ("""<!doctype html>
<html>
<head>
  <title>%s</title>
  <meta charset="utf-8" />
  <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style type="text/css">
    body {
      background-color: #002b36;
      color: #FFFFFF;
      font-family: "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;
      margin: 0;
      padding: 0;
    }
    div {
      background-color: #073642;
      border-radius: 0.25em;
      margin: 1em auto;
      padding: 2em;
      width: %spx;
    }
    p {
      font-size: 16px;
      padding-bottom: 1.5em;
    }
    a:link, a:visited {
      color: #93a1a1;
      font-size: 24px;
      text-decoration: underline;
    }
	
    img {
      padding: 0.1em;
      border-radius: 0.25em;
    }
	table{
    table-layout: fixed;
	}
	td{
    word-wrap:break-word
	}
  </style>
</head>
<body>
<div>
""")

