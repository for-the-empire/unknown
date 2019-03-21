import http.server

####Init Kickstart Function Section####
####Used to get IP of Palo Alto before Flask API is Started####
#Modify simple server python class to read headers and not respond with root directory contents
class postHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        self.send_head()
				#adds the 'source ip' into a key called HOST-IP to for use when no XFF is detected
        updateHTTPHeaderDICT("HOST-IP", self.address_string())
        for header in self.headers:
						#GRABS ALL HEADERS sent to init API Server, stores them as key/value pairs in global 'headerDict' for later decision making
            self.send_header(header, self.headers[header])
            updateHTTPHeaderDICT(header, self.headers[header])
        self.end_headers()
				#Sends back a 200ok and no directory contents
        self.send_response(200, "")

#global variable for header dictionary created within modified class
def updateHTTPHeaderDICT(key, value):
    ##Updates the Header Value, should be with the IP of the XFF Header
    #NOTE: Should do some validation to make sure it is an IP
    global headerDICT
    headerDICT[key] = value


def initBasicHTTPValues():
    global headerDICT
    #set Basic-Auth-Token to False to maintain loop in getAPICallerIP so it doesn't prematurely exit on a ELB Healthcheck
		#This is going to be used in the future for a basic token authentication
    headerDICT = {"Authd": "False"}


def getHTTPHeaderDICT():
		#Returns global Dictionary of headers and values
    return headerDICT


def getSourceIP(dict):
    if dict['X-Forwarded-For'] != "" and len(dict["X-Forwarded-For"].split(", ")) == 1:
        #X-Forwarded For is the standard for AWS, AZURE, and GCP ELBs not configured in TCP mode
				#Check if there are more than 2 IPs in XFF Header, should only have 1 during init.
        return dict['X-Forwarded-For']
    else:
        #If a GCP NLB is used, it uses 'arp' and no header is present. Use Source-IP
        return dict['HOST-IP']


def getAPICallerIP(server_class=http.server.HTTPServer,
                   handler_class=postHandler):
    initBasicHTTPValues()
    serverAddress = ('', 80)
    httpd = server_class(serverAddress, handler_class)
    print('before while statement')
		##need to add a check for the Authd Token and maybe change it to Basic-Auth-Token header, but I am to tired to do a find and replace right now...
    while getHTTPHeaderDICT()["Authd"] == "False":
        print('in while statement')
        httpd.handle_request()
    return getHTTPHeaderDICT()
		#to use this in code: getSourceIP(getAPICallerIP())

