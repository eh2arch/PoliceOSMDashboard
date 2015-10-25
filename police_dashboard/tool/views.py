import os,json
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from functions.json_parser import fileParser,getData
from functions.graphing import parseData,parseFBData,chartD3Line,chartD3LineVS,wordTree,parseText,wordCloud,getGraphData
from functions.title import getTitle,getComparisons,getKeywords

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def index(request):
    return HttpResponse("Hello, world. You're at the tool index.")

def dashboard(request,handle):
	template = loader.get_template('tool/basic.html')

	(title,tw_handle)=getTitle(handle,"")

	### for twitter
	filename = os.path.join(BASE_DIR, 'tool/data/tweets_'+tw_handle+'.json')
	data_tw = fileParser(filename)
	series = parseData(data_tw,filename)
	graph_data_tw=getGraphData(series,"twitter")

	### for facebook
	data_fb = getData(handle)
	series = parseFBData(data_fb)
	graph_data_fb=getGraphData(series,"facebook")
	
	d3graph_tw=chartD3Line(graph_data_tw,"tw",tw_handle)
	d3graph_fb=chartD3Line(graph_data_fb,"fb",handle)

	# print "GRAPH HERE"
	# print d3graph

	comp_list_tw=getComparisons(handle=handle,platform="twitter")
	comp_list_fb=getComparisons(handle=handle,platform="facebook")
	comp_div_twitter1=""
	comp_div_facebook1=""
	pick_div=""
	for key in comp_list_tw.keys():
		comp_div_twitter1=comp_div_twitter1+'<li><a class="compare-to-graph1-twitter" href="#">'+comp_list_tw[key][0]+'<div class="comp-fb-handle" style="display:none">'+key+'</div></a></li>'
	for key in comp_list_fb.keys():
		comp_div_facebook1=comp_div_facebook1+'<li><a class="compare-to-graph1-facebook" href="#">'+comp_list_fb[key][0]+'<div class="comp-fb-handle" style="display:none">'+key+'</div></a></li>'
		pick_div=pick_div+'<li><a class="pick-account" href="../'+key+'/">'+comp_list_fb[key][0]+'</a></li>'

	word="why"
	keyList=getKeywords(keyword=word)
	key_div_twitter1=""
	key_div_facebook1=""
	for key in keyList:
		key_div_twitter1=key_div_twitter1+'<li><a class="victimzn-key-twitter" href="#">'+key+'</a></li>'
		key_div_facebook1=key_div_facebook1+'<li><a class="victimzn-key-facebook" href="#">'+key+'</a></li>'

	text_array_tw=parseText(data_tw,"twitter")
	text_array_fb=parseText(data_fb,"facebook")
	tree_tw=wordTree(text_array=text_array_tw,name="wordtree_twitter",word=word)
	tree_fb=wordTree(text_array=text_array_fb,name="wordtree_facebook",word=word)

	if len(text_array_tw)>0:
		(cloud_tw,cloud_list_tw)=wordCloud(text_array=text_array_tw,name="wordcloud_twitter")
	else:
		cloud_tw=""
		cloud_list_tw=[]

	if len(text_array_fb)>0:
		(cloud_fb,cloud_list_fb)=wordCloud(text_array=text_array_fb,name="wordcloud_facebook")
	else:
		cloud_fb=""
		cloud_list_fb=[]

	context = RequestContext(request, {
	    'dashboard_name': title+" Dashboard",
	    'pick_account':pick_div,
	    'graph_tweets':d3graph_tw,
	    'graph_facebook':d3graph_fb,
	    'graph_tree_twitter':tree_tw,
	    'graph_tree_facebook':tree_fb,
	    'twitter_handle':handle,
	    'facebook_handle':handle,
	    'compare_to_graph1_twitter':comp_div_twitter1,
	    'compare_to_graph1_facebook':comp_div_facebook1,
	    'victimisation_twitter':key_div_twitter1,
	    'victimisation_facebook':key_div_facebook1,
	    'victim_current_key_twitter':word,
	    'victim_current_key_facebook':word,
	    'wordcloud_twitter':cloud_tw,
	    'wordcloud_twitter_list':cloud_list_tw,
	    'wordcloud_facebook':cloud_fb,
	    'wordcloud_facebook_list':cloud_list_fb
	})

	return HttpResponse(template.render(context))

def load_name(request):
    context = RequestContext(request)
    name=""
    if request.method == 'GET':
        name = request.GET['comp_handle_name']

    return HttpResponse("Comparing to "+name)

def graph_comp(request):
	context =RequestContext(request)
	handle=""
	platform=request.GET['platform']
	if request.method == 'GET':
		handle = request.GET['handle_name']
		comp_handle = request.GET['comp_handle_name']
			
		series1={}
		series2={}

		if platform=="twitter":
			(title,tw_handle)=getTitle(handle,"")
			filename1 = os.path.join(BASE_DIR, 'tool/data/tweets_'+tw_handle+'.json')
			data1 = fileParser(filename1)
			series1 = parseData(data1,filename1)
			
			(title,tw_comp_handle)=getTitle(comp_handle,"")
			filename2 = os.path.join(BASE_DIR, 'tool/data/tweets_'+tw_comp_handle+'.json')
			data2 = fileParser(filename2)
			series2 = parseData(data2,filename2)

			handle=tw_handle
			comp_handle=tw_comp_handle

			# print handle+" "+comp_handle
		else:
			data_fb = getData(handle)
			series1 = parseFBData(data_fb)

			data_fb_comp = getData(comp_handle)
			series2 = parseFBData(data_fb_comp)

			# print handle+" "+comp_handle

		graph_data1=getGraphData(series1,platform)
		graph_data2=getGraphData(series2,platform)
		
		d3graph=chartD3LineVS(graph_data1,graph_data2,platform,handle,comp_handle)
		# print d3graph
	return HttpResponse(d3graph)

def victimzn_tree(request):
	context =RequestContext(request)
	handle=""
	if request.method == 'GET':
		platform=request.GET['platform']
		handle = request.GET['handle_name']
		if platform=="twitter":
			(title,tw_handle)=getTitle(handle,"")
			filename = os.path.join(BASE_DIR, 'tool/data/tweets_'+tw_handle+'.json')
			data = fileParser(filename)
		else:
			data = getData(handle)
		word = request.GET['keyword']
		text_array=parseText(data,platform)
		tree=wordTree(text_array=text_array,name="wordtree_"+platform,word=word,kind="ajax")

	return HttpResponse(tree)

def word_cloud(request):
	context =RequestContext(request)
	handle=""
	if request.method == 'GET':
		platform=request.GET['platform']
		handle = request.GET['handle_name']
		if platform=="twitter":
			(title,tw_handle)=getTitle(handle,"")
			filename = os.path.join(BASE_DIR, 'tool/data/tweets_'+tw_handle+'.json')
			data = fileParser(filename1)
		else:
			data = getData(handle)

		word = request.GET['keyword']
		text_array=parseText(data,platform)
		(cloud,cloud_list)=wordCloud(text_array=text_array,name="wordcloud_"+platform,keyword=word)
		response_data={}
		response_data['cloud']=cloud
		response_data['cloud_list']=cloud_list

	return HttpResponse(json.dumps(response_data), content_type="application/json")