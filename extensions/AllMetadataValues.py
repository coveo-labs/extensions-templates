# Title: All metadata values
# Description: This extension is useful for development and debugging (https://developers.coveo.com/x/UQgvAg)
# Required data:

import json
from sets import Set

values = dict()
fields = Set([])
type = ''

for m in document.get_meta_data():
    type = ':' + m.origin
    for metadata_name, metadata_value in m.values.iteritems():
        values[metadata_name + type] = metadata_value
        fields.add(metadata_name)

# Add the allmetadatafields metadata: allows discovery of all available meta in a source
document.add_meta_data({"allmetadatafields": ';'.join(fields)})

# Add the allmetadatavalues metadata
document.add_meta_data({"allmetadatavalues": json.dumps(values)})
