from flask import Flask, render_template, request, make_response
import plivo
from app import app
import csv, os

auth_id = "MAMZRKNGYYNZQ1YJBHYT"
auth_token = "OGM0NzhiNjE5YzdjNWVjNDY0MDJhMzM0ZjY4MDYx"
 
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/call/', methods=['POST'])
def call():

    # Get the Phone numbers data
    if request.method == 'POST':

        # Receive the text to be played
        global textTobePlayed
        textTobePlayed = request.form['speaktext']

	# Save the csv file in a folder
	filefolder = app.config['UPLOAD_FOLDER']
    	file = request.files['datafile']
	filename = file.filename
	file.save(os.path.join(filefolder, filename))
	filepath = os.path.join(filefolder, filename)
	
	# Connect Plivo API
	p = plivo.RestAPI(auth_id, auth_token)   

        # Open the csv file and fire a call to each number
	with open(filepath, 'rb') as csvfile:
	    nosList = csv.reader(csvfile)
	    for no in nosList:
		dialNumber1 = no[0]
        
		# Make Calls
	        params = {
        	'from': '1800111108', # Caller Id
	        'to' : dialNumber1, # User Number to Call	
        	'answer_url' : 'http://afternoon-fortress-6063.herokuapp.com/answer_url/',
	        'answer_method' : 'POST',
        	}
	        response = p.make_call(params)
		print response
	
    	return render_template('home.html')
	
@app.route('/answer_url/', methods=['POST'])
def answer_url():

    r = plivo.Response()
    
    params = {'loop':1}
    r.addWait(length=1)
    r.addSpeak(textTobePlayed)
    
    response = make_response(r.to_xml())
    response.headers["Content-type"] = "text/xml"

    return response
