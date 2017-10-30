import re

# Title: Replace text in QuickView
# Description: This extension is useful to replace or clean up the HTML used for the QuickView.
# Required data: Body HTML


def replace_text(re_to_replace, new_text, text):
    return re.sub(re_to_replace, new_text, text, flags=re.I)


# get quickview representation
html = document.get_data_stream('body_html').read()

# remove all "display:none!important"
html = replace_text(r'\s*\bdisplay\s*:\s*none\s*!important\s*;?', '', html)

# override height for an element with id FOO
html = replace_text(r'\s+id="FOO"', ' id="FOO" style="height:auto"', html)


# update quickview
body_html = document.DataStream('body_html')
body_html.write(html)
document.add_data_stream(body_html)
