# Title: Use Https Protocol
# Description: This extension is useful to use HTTPS protocol instead of HTTP protocol in the URI
# Required data: originaluri, clickableuri
# Parameters:

try:
    originaluri = document.get_meta_data_value("originaluri")[-1]
    clickableuri = document.get_meta_data_value("clickableuri")[-1]

    document.add_meta_data(
        {"originaluri": originaluri.replace("http:", "https:")})
    document.add_meta_data(
        {"clickableuri": clickableuri.replace("http:", "https:")})
except Exception as e:
    log(str(e))
