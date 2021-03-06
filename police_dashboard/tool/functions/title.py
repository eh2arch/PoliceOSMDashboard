import os
import pymongo
from os.path import isfile, join

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# All_handles={
# 	"blrcitypolice":["Bangalore City Police","BlrCityPolice","464946996873402"],
# 	"BangaloreTrafficPolice":["Bangalore Traffic Police","blrcitytraffic","147207215344994"],
# 	"GurgaonPolice":["Gurgaon Police","gurgaonpolice1","357011041078922"],
# 	"gnrpolice":["Gandhinagar Police","GnrPolice","182415085299685"],
# 	"hyderabadpolice":["Hyderabad City Police","hydcitypolice","326762537496491"],
# 	"HYDTP":["Hyderabad Traffic Police","HYDTraffic","103022096427538"],
# 	"SikkimPolice":["Sikkim Police","sikkimpolice","348545705193638"],
# 	"Chennai.Police":["Chennai City Police","chennaipolice_","457621584324537"],
# 	"chennaitrafficpolice":["Chennai Traffic Police","cctpolice","141144945912047"],
# 	"dcpnorth":["Delhi Police DCP North","DcpNorthDelhi","408718049271221"],
# 	"AhmedabadTrafficPolice":["Ahmedabad Traffic Police","AhdTraffic","125541044208873"],
# 	"keralatrafficpolice":["Kerela Traffic Police","keralatraffic","837606212949358"],
# 	"UpPolicePr":["UP Police PR","uppolicepr","127726260748187"],
# 	"rohtakrange":["Rohtak Police","RohtakPolice","294138767359123"],
# 	"PoliceCommissionerateFaridabad":["Faridabad Police","CPFbd","497268597013510"]
# }

def getAllHandles():
	client = pymongo.MongoClient()
	db = client.FBPoliceData
	page_info=db.page_names.find()
	All_handles={}
	for pi in page_info:
		j=db.page_fields.find_one({"page":pi["page"]})
		if j is None:
			continue
		if "id" in j.keys():
			All_handles[pi["page"]]=[pi["name"],pi["handle"],j["id"]]
	return All_handles

def getId(handle):
	handle=handle.encode('utf8')
	All_handles=getAllHandles()
	return All_handles[handle][2]

def getTitle(handle,platform):
	handle=handle.encode('utf8')
	All_handles=getAllHandles()
	return (All_handles[handle][0],All_handles[handle][1])

def getComparisons(handle,platform):
	handle=handle.encode('utf8')
	All_handles=getAllHandles()
	handles=All_handles
	# print All_handles.keys()
	output_handles={}
	for key in handles.keys():
		if key!=handle:
			output_handles[key]=handles[key];

	if platform=="twitter":
		return getTwitterTitles(handles)
	return sortHandles(output_handles)

def getKeywords(keyword):
	keywords=["worried","why","want","need","how can","where","fear","trouble","notice of","issue"]
	keywords.remove(keyword)
	return keywords

def getTwitterTitles(handles):
	output_handles={}
	for key in handles.keys():
		if handles[key][1]!="":
			output_handles[key]=handles[key];
	return sortHandles(output_handles)

def sortHandles(handles_dict):
	handles_list=[]
	for key in handles_dict.keys():
		datum={}
		datum["key"]=key
		datum["name"]=handles_dict[key][0]
		datum["tw_handle"]=handles_dict[key][1]
		datum["fb_id"]=handles_dict[key][2]
		handles_list.append(datum)

	sorted_handles_list = sorted(handles_list, key=lambda k: k['name'])

	return sorted_handles_list