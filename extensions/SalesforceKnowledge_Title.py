# Title: Salesforce Knowledge Title
# Description: This extension is useful to use sftitle meta as the document title
# Required data:
# Parameters:

try:
    meta_sftitle = document.get_meta_data_value("sftitle")
    if len(meta_sftitle) > 0:
        document.add_meta_data({"title": meta_sftitle[-1]})
except Exception as e:
    log(str(e))
