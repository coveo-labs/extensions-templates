# Title: FAST Feed handler
# Description: Output the GSA feed to a dropbox share (or a file share, a gdrive, etc), change the extension settings so you retrieve the files, create a push source, configure the extension with the organizationId, sourceId, apiKey, and you will index FAST feeds.
# Required data: Body TEXT

import xml.etree.ElementTree as ElTree
import requests
import base64
from json import dumps, loads

################################################################################
# Formatters and encoders for the feed's metadatas
################################################################################
def format_for_addition(record):
    metadata = record.find("metadata")
    content = record.get("content", "")

    if content != "":
        content = content.text

    document = {
        "DocumentId": record.get("url"),
        "uri": record.get("url"),
        "Data": encode_ascii(content),
        "body": encode_ascii(content)
    }

    for meta in metadata.findall("meta"):
        encoding = meta.attrib.get("encoding", "default")
        name = encoding_mapping[encoding](meta.attrib.get("name"))
        content = encoding_mapping[encoding](meta.attrib.get("content"))

        document[name] = content

    return document

def format_for_deletion(record):
    return {
        "DocumentId": record.get("url"),
        "deleteChildren": False
    }

def decode_base64_string(base64_string):
    return encode_ascii(
        base64.b64decode(base64_string).decode("ascii", "ignore")
    )

def encode_ascii(any_string):
    return unicode(any_string).encode('ascii','xmlcharrefreplace')

################################################################################
# Coveo Push API URL and headers configuration
################################################################################
base_url = "https://push.cloud.coveo.com/v1/organizations/{organization_id}/".format(
    organization_id="myorg"
)
coveo_get_batch_file_id_url = base_url + "files"
coveo_batch_document_api_url = base_url + "sources/{source_id}/documents/batch?fileId={file_id}"

push_header = {
    "Content-Type": "application/json",
    "Authorization": "Bearer xx9999xxxx-999x-9x9x-9999-x9x9xxxxxx99"
}

s3_header = {
    'content-type': 'application/octet-stream',
    'x-amz-server-side-encryption': 'AES256'
}

################################################################################
# Mapping for sources (in case you'd like to use the same extension/source
# to crawl multiple sources from GSA
################################################################################
source_mapping = {
    "other_source": "rzwvzpq4ngwpe4lx4g5hwkshoe-myorg",
    "default": "rzwvzpq4ngwpe4lx4g5hwkshoe-myorg"
}

operation_mapping = {
    "add": format_for_addition,
    "delete": format_for_deletion
}

encoding_mapping = {
    "base64binary": decode_base64_string,
    "UTF-8": encode_ascii,
    "default": encode_ascii
}

################################################################################
# Extraction of the feed's data and batch formatting
################################################################################
f = document.get_data_stream('documentdata')
root = ElTree.fromstring(f.read())

header = root.find("header")
source = header.find("datasource").text
source_id = source_mapping[source]
feed_type = header.find("feedtype").text

log("Source={}|SourceId={}|Operation={}".format(source, source_id, feed_type), severity="normal")

add_or_update = []
delete = []

for group in root.findall("group"):
    for record in group.findall("record"):
        print "operation={}|uri={}".format(
            record.get("action"),
            record.get("url")
        )

        document = operation_mapping[record.get("action", "add")](record)

        if record.get("action") == "delete":
            delete.append(document)
        else:
            add_or_update.append(document)

batch = {
    "AddOrUpdate": add_or_update,
    "Delete": delete
}

################################################################################
# Push the batch to Coveo
################################################################################
r = loads(
    requests.post(
        coveo_get_batch_file_id_url,
        headers=push_header
    ).content
)

upload_uri = r["uploadUri"]
file_id = r["fileId"]

# Upload the batch
r = requests.put(
    upload_uri,
    headers=s3_header,
    data=dumps({"AddOrUpdate": batch})
)

if r.status_code == 200:
    pass
else:
    log("ERROR: {}".format(r.text), severity="error")

# Request the push api to process the batch
coveo_batch_document_api_url = coveo_batch_document_api_url.format(
    source_id=source_id,
    file_id=file_id
)

r = requests.put(
    coveo_batch_document_api_url,
    headers=push_header
)

if r.status_code == 202:
    # If the batch went through properly, reject the feed as it will be processed by the Push API
    log("SUCCESS {}".format(file_id), severity="normal")
    document.reject()
else:
    # If the batch went wrong, let the feed go through... it will end in the source and, at the same time, provide a
    # failsafe mechanism (everything in the source didn't get through and should be looked at/re-pushed)
    log("ERROR: {}".format(r.text), severity="error")