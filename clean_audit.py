#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
import audit_street


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
mapping = { "St": "Street",
            "St.": "Street",
            "Ave":"Avenue",
            "Rd.":"Road",
            "PKWY":"Parkway",
            "Dr.":"Drive",
            "Blvd.":"Boulevard",
            "Ct.":"Court",
            "Ln":"Lane",
            "Centre":"Center"}
expected=['Street','Road','Lane','Court','Avenue','Drive','Grove','Way',
          'Boulevard','Center','Highway']


def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        list_keys=element.attrib.keys()
        node['created']={}
        node['pos']=[]
        for k in list_keys:
            if k not in CREATED:
                if k not in ['lat','lon']:
                    node[k]=element.attrib[k]
                else:
                    node['pos']=[float(element.get("lat")),float(element.get("lon"))]
                    
            else:
                node['created'][k]=element.attrib[k]
       
        if element.tag=="way":
            node['node_refs']=[]
            for tag in element.iter("nd"):
                node['node_refs'].append(tag.attrib["ref"])
            node['type']='way'
        else:
            node['type']='node'
        address={}
        for tag in element.iter("tag"):
            if lower.match(tag.attrib['k']):
                node[tag.attrib['k']]=tag.attrib['v']
            elif lower_colon.match(tag.attrib['k']):
                list_new2=re.split(':',tag.attrib['k'])
                if list_new2[0]=='addr':
                    if lower_colon.match(list_new2[1]):
                        pass
                    else:
                        if list_new2[1]=='street':
                            name=audit_street.update_street_name(tag.attrib['v'], mapping)
                            address['street']=name
                        elif list_new2[1]=='state':
                             name=audit_street.update_state_name(tag.attrib['v'])
                             address['state']=name
                        elif list_new2[1]=='country':
                             name=audit_street.update_country_name(tag.attrib['v'])
                             address['country']=name
                            
                        else:
                             address[list_new2[1]]=tag.attrib['v']
                        
        if address:
            node['address']=address
        return node
    else:
        return None
            

def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    data = process_map('sample_file.osm', False)
    


     

if __name__ == "__main__":
    test()
