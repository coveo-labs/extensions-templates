# Title: Reject document metadata
# Description: This extension is useful to a reject document (or remove values) based on existing metadata values
# Required data:
# Parameters: metadata_name, valuesToBeRejected, removeValuesFromMetaOnly


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
            normalized[metadata_name] = ";".join(
                [str(value) for value in metadata_values])
    return normalized


def reject_document_based_on_meta(metadata_name, jsonValues, removeValuesFromMetaOnly=False):

    try:
        values = json.loads(jsonValues)
        meta_data = get_flattened_meta()
        meta_data_values = meta_data[metadata_name].split(";")

        if removeValuesFromMetaOnly:
            log("removing values from meta only ...")
            cleaned_meta_data_values = ";".join(
                list(set(meta_data_values).difference(values)))
            log('Replacing values on {} with : {}'.format(
                metadata_name, cleaned_meta_data_values.encode('utf8')))
            document.add_meta_data(
                {metadata_name: cleaned_meta_data_values.encode('utf8')})
        else:
            for v in values:
                if v in meta_data_values:
                    log("rejecting document ...")
                    document.reject()
                    break

    except Exception as e:
        log(str(e))


if 'metadata_name' not in parameters:
    log('metadata_name has not been specified, please supply a parameter metadata_name')
    raise Exception('Supply a metadata_name in the parameters of ext')
if 'valuesToBeRejected' not in parameters:
    log('valuesToBeRejected has not been specified, please supply a parameter valuesToBeRejected')
    raise Exception('Supply a valuesToBeRejected in the parameters of ext')

removeValuesFromMetaOnly = False if 'removeValuesFromMetaOnly' not in parameters else parameters[
    'removeValuesFromMetaOnly']
reject_document_based_on_meta(
    parameters['metadata_name'], parameters['valuesToBeRejected'], removeValuesFromMetaOnly)
