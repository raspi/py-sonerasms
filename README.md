Send SMS messages through Sonera's web page

CLI usage:

    python cli.py --createconfig
    $EDITOR ~/.sonerasms
    python cli.py --recipient 0401234567 --message "Hello from Python!"
    

Library usage:

    sms = SoneraSMS("myuser", "mypass")
    if sms.login():
        if sms.send("0401234567", "Hello from Python!"):
            print("Sent successfully!")
        else:
            print("Something went horribly wrong!")
        
    
Uses Requests - http://python-requests.org/
