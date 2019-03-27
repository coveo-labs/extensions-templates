from dateutil import parser

# Title: Normalize Fuzzy Date
# Description: This extension is useful to normalize a document date based on an existing fuzzy date value
# Required data:
# Parameters: targeted_metadata_name, new_metadata_name

def get_safe_meta_data(meta_data_name):
    safe_meta = ''
    meta_data_value = document.get_meta_data_value(meta_data_name)
    if len(meta_data_value) > 0:
        safe_meta = meta_data_value[-1]
    return safe_meta

def normalizeDate(targeted_metadata_name, new_metadata_name):
    try:
        targeted_meta = get_safe_meta_data(targeted_metadata_name)
        
        if targeted_meta:
            meta_parseddate = parser.parse(targeted_meta, fuzzy=True)
            document.add_meta_data({new_metadata_name: meta_parseddate})
    
    except Exception as e:
        log(str(e), 'Error')

if 'targeted_metadata_name' not in parameters:
    log('targeted_metadata_name has not been specified, please supply a parameter targeted_metadata_name')
    raise Exception('Supply a targeted_metadata_name in the parameters of ext')
if 'new_metadata_name' not in parameters:
    log('new_metadata_name has not been specified, please supply a parameter new_metadata_name')
    raise Exception('Supply a new_metadata_name in the parameters of ext')

normalizeDate(parameters['targeted_metadata_name'],parameters['new_metadata_name'])