# Title: Question Folding
# Description: This extension is useful to create a folding relation between a Feed Item and its comments.
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
            normalized[metadata_name] = ";".join([str(value) for value in metadata_values])
    return normalized

meta_data = get_flattened_meta()

try:
    if meta_data["objecttype"] == "FeedItem":
        document.add_meta_data({'foldfoldingfield':meta_data["sffeeditemid"]})
        document.add_meta_data({'foldparentfield':meta_data["sffeeditemid"]})
    elif meta_data["objecttype"] == "FeedComment":
        document.add_meta_data({'foldfoldingfield':meta_data["sffeeditemid"]})
        document.add_meta_data({'foldchildfield':meta_data["sffeeditemid"]})

except Exception as e:
    log(str(e))