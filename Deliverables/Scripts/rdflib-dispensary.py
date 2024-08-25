##### Graph stuff
import rdflib
from rdflib import URIRef, Graph, Namespace, Literal
from rdflib import OWL, RDF, RDFS, XSD, TIME
import os
import csv

# Prefixes
name_space = "https://kastle-lab.org/"
pfs = {
"kl-res": Namespace(f"{name_space}lod/resource/"),
"kl-ont": Namespace(f"{name_space}lod/ontology/"),
"geo": Namespace("http://www.opengis.net/ont/geosparql#"),
"geof": Namespace("http://www.opengis.net/def/function/geosparql/"),
"sf": Namespace("http://www.opengis.net/ont/sf#"),
"wd": Namespace("http://www.wikidata.org/entity/"),
"wdt": Namespace("http://www.wikidata.org/prop/direct/"),
"dbo": Namespace("http://dbpedia.org/ontology/"),
"time": Namespace("http://www.w3.org/2006/time#"),
"ssn": Namespace("http://www.w3.org/ns/ssn/"),
"sosa": Namespace("http://www.w3.org/ns/sosa/"),
"cdt": Namespace("http://w3id.org/lindt/custom_datatypes#"),
"ex": Namespace("https://example.com/"),
"rdf": RDF,
"rdfs": RDFS,
"xsd": XSD,
"owl": OWL,
"time": TIME
}
# Initialization shortcut
def init_kg(prefixes=pfs):
    kg = Graph()
    for prefix in pfs:
        kg.bind(prefix, pfs[prefix])
    return kg

# predicate shortcuts
a = pfs["rdf"]["type"]

## xsd:string
license_number = pfs["kl-ont"]["hasLicenseNumber"]
license_type = pfs["kl-ont"]["hasLicenseType"]
business_as = pfs["kl-ont"]["isDoingBusinessAs"]
### Resource
license_name = pfs["kl-res"]["hasLicenseName"]
## xsd:date
issue_date = pfs["kl-ont"]["hasIssueDate"]
effective_date = pfs["kl-ont"]["hasEffectiveDate"]
expiration_date = pfs["kl-ont"]["hasExpirationDate"]


## not in csv
### xsd:string
dispensary_name = pfs["kl-ont"]["hasName"]
### xsd:boolean
license_status = pfs["kl-ont"]["isActive"]
### xsd:date
dispensary_license = pfs["kl-ont"]["hasLicense"]

# Create predicate mapping
predicate_mapping = {
    "License: Number": license_number,
    "Type": license_type,
    "Licensee Doing Business As": business_as,
    "Issue Date": issue_date,
    "Effective Date": effective_date,
    "Expiration Date": expiration_date,
    "Licensee": license_name,
}

# Initialize an empty graph
graph = init_kg()

# Load the roster_fips.csv file
roster_fips_file_path = os.path.join(os.path.dirname(__file__), "roster_fips.csv")

# Initialize from a file
with open(roster_fips_file_path, newline='', encoding='utf-8') as input_file:
    reader = csv.reader(input_file)


    # for row in reader:
    #     # Add a specific triple
    #     # graph.add( (subject_node, predicate_node, object_node) )
    #     graph.add( (pfs["ex"][row["name"]], a, pfs["ex"]["Person"]) )


# output_file = "output.ttl"
# temp = graph.serialize(format="turtle", encoding="utf-8", destination=output_file)