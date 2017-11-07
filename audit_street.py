import xml.etree.ElementTree as ET
from collections import defaultdict
import re
import pprint



#Here the main goal is to replace the short names of streets, state and city by their respective full names.street_type_re 
#looks for the string at the end of the street name.

osm_file="sample_file.osm"
street_type_re=re.compile(r'\b\S+\.?$',re.IGNORECASE)
#street_type_start=re.compile(r'^\S+\.?\b', re.IGNORECASE)

#street_types=defaultdict(set)

expected=['Street','Road','Lane','Court','Avenue','Drive','Grove','Way',
          'Boulevard','Center','Highway']

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



def audit_street_type(street_types, street_name):
  """ We group the street names in a dictionary, the key being the short version of street name, e.g. St. or Rd."""
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
            
def audit_state_type(state_types, state_name):
    m = street_type_re.search(state_name)
    if m:
        state_type = m.group()
        state_types[state_type].add(state_name)
            
def audit_country_type(country_types, country_name):
    m = street_type_re.search(country_name)
    if m:
        country_type = m.group()
        country_types[country_type].add(country_name)



def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def is_state_name(elem):
    return (elem.attrib['k'] == "addr:state")

def is_country_name(elem):
    return (elem.attrib['k'] == "addr:country")

def audit(osmfile):
    osm_file = open(osmfile, encoding="utf8")
    street_types = defaultdict(set)
    state_types = defaultdict(set)
    country_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                elif is_state_name(tag):
                    audit_state_type(state_types, tag.attrib['v'])
                elif is_country_name(tag):
                    audit_country_type(country_types, tag.attrib['v'])
                
                    
    osm_file.close()
    return [street_types,state_types,country_types]

def update_street_name(name, mapping):
    """ the street name update is carried here. Using the mapping dictionary, we replace the shorter version by their full length
    counterparts. The key of the maping dictionary is shorter version, e.g. St and the value is the longer version, e.g. Street."""

    name=name.split()
    if name[len(name)-1] in mapping.keys():
        name[len(name)-1]=mapping[name[len(name)-1]]
        name = ' '.join(name)

    return name

def update_state_name(name):
    if name=="VIC":
        name="Victoria"
    return name

def update_country_name(name):
    if name=="AU":
        name="Australia"
    return name

def test():
    output_list = audit(osm_file)
    st_types=output_list[0]
    state_types=output_list[1]
    country_types=output_list[2]
    

    for st_type, ways in st_types.items():
        for name in ways:
            better_name = update_street_name(name, mapping)
    for st_type, ways in state_types.items():
        for name in ways:
            better_state_name=update_state_name(name)
    for st_type, ways in country_types.items():
        for name in ways:
            better_country_name = update_country_name(name)
    
                              
                        
                   
if __name__ == '__main__':
    test()
