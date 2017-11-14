# Title: Salesforce Knowledge - Body Text
# Description: This extension is useful to create the body text of a document based on specific metadata values
# Required data:


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
            normalized[metadata_name] = ';'.join(
                [str(value) for value in metadata_values])
    return normalized


try:
    meta_data = get_flattened_meta()

    bodyTextFields = ['sftitle', 'sfsummary', 'sfdescriptionc',
                      'sfquestionc', 'sfanswerc', 'sfquestionproblemc', 'sfanswersolutionc']

    bodyContentText = ''
    for x in bodyTextFields:
        if x in meta_data.keys():
            bodyContentText = bodyContentText + ' ' + meta_data[x]

    bodyTextDataStream = document.DataStream('body_text')
    bodyTextDataStream.write(bodyContentText.encode('utf8'))
    document.add_data_stream(bodyTextDataStream)
except Exception as e:
    log(str(e))
