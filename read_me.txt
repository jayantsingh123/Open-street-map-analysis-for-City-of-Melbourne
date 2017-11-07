In this project, following files have been submitted:

1. 'clean_audit.py' : This code is similar to the code submitted for the Open Street Map case study in the MongoDB Course. In this code, following tasks have been performed:

a) The function 'shape_element' has been implemented. This function aims at
  i) Updating the street names as well as state names; replacing the abbreviations by ther full length counterparts. We have used the module functionality in Python to access the update function from audit_street.py. 
  ii) Converting all attributes of "node" and "way" into regular key/value pairs, except:
    - attributes in the CREATED array are added under a key "created"
    - attributes for latitude and longitude are added to a "pos" array, for use in geospatial indexing.
    - if the second level tag "k" value starts with "addr:", it should be added to a dictionary "address"	
	
b) The function 'update_street_name' has been executed. The input parameters are mapping dictionary and the street or state names.   It aims at replacing the abbreviated names by their full length counterparts. Similarly, 'update_state_name' has been used to replace abbreviations of state.

b) The function 'process_map' is responsible for loading the JSON file as output. Its input is the XML file, sample_file.osm, and th eoutput will be a JSON file.

2.'audit_street.py': This code performs the cleaning of the input XML file, like replacing abbreviated street names and state names by their full length counterparts. In this file, following funcions have been implemened:

 i) 'audit_street_type' : It looks for the end of the string using regular expressions and groups them dpending on the text found at end of the string. the output is a dictionary, with key being the text found a the end of the string, for example; {'Esperence': {'The Esperence'},'Summit': {'The Summit'}}. Similarly, we have also implemented audit_state_type and audit_country_type.
 ii)'is_street_name': This function identifies the elements with attribute names "addr:street", similar to "addr:state", and "addr:country".
 iii)'update_street_name': This function updates the street names, asper the abbreviation and mapping dicionary. The state and country abbreviations are also modified.  

3. 'load_data.py' : This code has been executed to load the JSON output, obtained from 'clean_audit.py', into the MongoDB database.

4. 'query_mongodb.py' : Once the JSON file has been loaded into the database, we query it using this file. Different types of queries have been implemented including,

   i) finding number of ways and nodes,
   ii) getting a count of  distinct users,
   iii) Getting the user who has contributed the highest number of documents, and
   iv) Retrieving the most common amenity.
   Please note that, other information can also be retrieved.
 
5. open_street_map_project.pdf: This file documents the different types of wrangling steps, that have been carried out in the python files. 

6. sample_file_new.osm: it is a sample XML file of approx size 10 MB.

7. Melbourne_link_information: It contains the link for the city data.

8.resources_used.txt: This file enlists the resources used for the completion of this project.