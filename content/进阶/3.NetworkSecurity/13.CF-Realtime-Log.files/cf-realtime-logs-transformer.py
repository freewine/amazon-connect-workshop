import base64
import json
from datetime import datetime
 
print('Loading function')
 
 
def lambda_handler(event, context):
    output = []
 
    # Based on the fields chosen during the creation of the 
    # Real-time log configuration.
    # The order is important and please adjust the function if you have removed 
    # certain default fields from the configuration. 
    realtimelog_fields_dict = {
    "timestamp" : "date", 
    "c-ip" : "str", 
    "time-to-first-byte" : "float", 
    "sc-status" : "int", 
    "sc-bytes" : "int", 
    "cs-method" : "str", 
    "cs-protocol" : "str",
    "cs-host" : "str", 
    "cs-uri-stem" : "str", 
    "cs-bytes" : "int",
    "x-edge-location" : "str", 
    "x-edge-request-id" : "str", 
    "x-host-header" : "str", 
    "time-taken" : "float", 
    "cs-protocol-version" : "str",
    "c-ip-version" : "str", 
    "cs-user-agent" : "str", 
    "cs-referer" : "str", 
    "cs-cookie" : "str", 
    "cs-uri-query" : "str", 
    "x-edge-response-result-type" : "str", 
    "x-forwarded-for" : "str", 
    "ssl-protocol" : "str", 
    "ssl-cipher" : "str", 
    "x-edge-result-type" : "str", 
    "fle-encrypted-fields": "str", 
    "fle-status" : "str",
    "sc-content-type" : "str", 
    "sc-content-len" : "int", 
    "sc-range-start" : "int", 
    "sc-range-end" : "int", 
    "c-port" : "int", 
    "x-edge-detailed-result-type" : "str", 
    "c-country" : "str", 
    "cs-accept-encoding" : "str",
    "cs-accept" : "str",
    "cache-behavior-path-pattern" : "str",
    "cs-headers" : "str", 
    "cs-header-names" : "str", 
    "cs-headers-count" : "int"
    }
 
    for record in event['records']:
    
        # Extracting the record data in bytes and base64 decoding it
        payload_in_bytes = base64.b64decode(record['data'])
        
        # Converting the bytes payload to string
        payload = "".join(map(chr, payload_in_bytes))
 
        # dictionary where all the field and record value pairing will end up
        payload_dict = {}
        
        # counter to iterate over the record fields
        counter = 0
        
        # generate list from the tab-delimited log entry
        payload_list = payload.strip().split('\t')
        
        # perform the field, value pairing and any necessary type casting.
        # possible types are: int, float and str (default)
        for field, field_type in realtimelog_fields_dict.items():
            #overwrite field_type if absent or '-'
            if(payload_list[counter].strip() == '-'):
                field_type = "str"
            if(field_type == "int"):
                payload_dict[field] = int(payload_list[counter].strip())
            if(field_type == "date"):
                timeint = float(payload_list[counter].strip())
                payload_dict[field] = datetime.fromtimestamp(timeint).strftime('%Y-%m-%d %H:%M:%S')
            elif(field_type == "float"):
                payload_dict[field] = float(payload_list[counter].strip())
            else:
                payload_dict[field] = payload_list[counter].strip()
            counter = counter + 1
                
        # JSON version of the dictionary type
        payload_json = json.dumps(payload_dict)
        
        # Preparing JSON payload to push back to Firehose
        payload_json_ascii = payload_json.encode('ascii')
        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': base64.b64encode(payload_json_ascii).decode("utf-8")
        }
        output.append(output_record)
 
    print('Successfully processed {} records.'.format(len(event['records'])))
 
    return {'records': output}