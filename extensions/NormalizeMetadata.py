import json

def get_flattened_meta():

    flattened = dict()
    for m in document.get_meta_data():
        for metadata_name, metadata_values in m.values.iteritems():
            flattened[metadata_name.lower()] = metadata_values

    normalized = dict()
    for metadata_name, metadata_values in flattened.iteritems():
        if len(metadata_values) == 1:
            normalized[metadata_name] = metadata_values[0]
        elif len(metadata_values) > 1:
            normalized[metadata_name] = ";".join([str(value) for value in metadata_values])
    return normalized

def normalize_document_based_on_meta(targeted_metadata_name, targeted_metadata_values, new_metadata_name, new_metadata_value, new_metadata_field):

    try:
        values = json.loads(targeted_metadata_values)
        metadata = get_flattened_meta()
        metadata_values = metadata[targeted_metadata_name].split(";")

        not_affected_metadata_values = ";".join(list(set(metadata_values).difference(values)))
        
        if not not_affected_metadata_values:
          new_value = (new_metadata_value or metadata[new_metadata_field])
          log('Setting values on {} with : {}'.format(new_metadata_name, new_value.encode('utf8')))
          document.add_meta_data({new_metadata_name:new_value.encode('utf8')})
    
    except Exception as e:
        log(str(e))

if 'targeted_metadata_name' not in parameters:
    log('targeted_metadata_name has not been specified, please supply a parameter targeted_metadata_name')
    raise Exception('Supply a targeted_metadata_name in the parameters of ext')
if 'targeted_metadata_values' not in parameters:
    log('targeted_metadata_values has not been specified, please supply a parameter targeted_metadata_values')
    raise Exception('Supply a targeted_metadata_values in the parameters of ext')
if 'new_metadata_name' not in parameters:
    log('new_metadata_name has not been specified, please supply a parameter new_metadata_name')
    raise Exception('Supply a new_metadata_name in the parameters of ext')
if 'new_metadata_value' not in parameters and 'new_metadata_field' not in parameters:
    log('new_metadata_value or new_metadata_field have not been specified, please supply a parameter new_metadata_value or new_metadata_field')
    raise Exception('Supply a new_metadata_value or new_metadata_field in the parameters of ext')
if 'new_metadata_value' in parameters and 'new_metadata_field' in parameters:
    log('new_metadata_value and new_metadata_field have been specified, please supply a parameter new_metadata_value or new_metadata_field')
    raise Exception('Supply a new_metadata_value or new_metadata_field in the parameters of ext')

new_metadata_value = ''
if 'new_metadata_value' in parameters:
    new_metadata_value = parameters['new_metadata_value']

new_metadata_field = ''
if 'new_metadata_field' in parameters:
    new_metadata_field = parameters['new_metadata_field']

normalize_document_based_on_meta(parameters['targeted_metadata_name'], parameters['targeted_metadata_values'], parameters['new_metadata_name'], new_metadata_value, new_metadata_field)