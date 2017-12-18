# Title: FAST Feed handler
# Description: Output the FAST feed to a dropbox share (or a file share, a gdrive, etc), change the settings so you retrieve the files, configure the fields to index and you will index FAST feeds.
# Required data: Body TEXT

import xml.etree.ElementTree as ElTree
import json

# Do not forget to add a mapping for each of them...
fields_to_extract = [
    "collectionname",
    "categoryid",
    "id",
    "partpath",
    "category",
    "productnumber",
    "attrtranslations",
    "language",
    "attrspecs",
    "filetype",
    "ETC"
]

f = document.get_data_stream('documentdata')
if f:
    root = ElTree.fromstring(f.read())
    log("xml data successfully loaded", severity="Normal")

    fastmetadata = {}
    for attribute in root.findall("attribute"):
        val = unicode(attribute.text).encode('ascii', 'xmlcharrefreplace')
        # Add it to the full metadata list
        fastmetadata[attribute.attrib["name"]] = val

        # If present in the specific mapping list, add it as a mapping
        # We could also remove the condition, map everything and use
        # mappings to select what we want...
        # if attribute.attrib["name"] in fields_to_extract:
        # Adding all metadata - Sklava
        document.add_meta_data({attribute.attrib["name"]: val})
        log("Adding metadata: " + attribute.attrib["name"])

    document.add_meta_data({
        "categoryids": root.attrib["categoryids"],
        "fastmetadata": json.dumps(fastmetadata),
        "body": json.dumps(fastmetadata)
    })
    log("FAST metadata added", severity="Normal")
else:
    log('no documentdata', severity="Error")



