Send SMS messages through Sonera's web page

    sms = SoneraSMS("myuser", "mypass")
    if sms.login():
        sms.send("0401234567", "Hello from Python!")
        
    
Uses Requests - http://python-requests.org/
