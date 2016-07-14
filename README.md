# facebook-group-scrape
Code for collecting data on any public Facebook group.



## Step 0:  Just run mainRun.sh  It should have a working token
            and everything else. This way you can see if it works.

           ./mainRun.sh



## Step 1:  Obtain a Token

   You probably want to use an App toke, since it will stay valid
   for a few months.
   
   https://developers.facebook.com/tools/explorer
   
   a. Select an App in the drop down box. Or add a new App and select.
   
   b. Select 'Get App Token'
   
     You'll want to paste this token in the file tokenf.py. Or, you 
	 can use my token.


## Step 2:  Get Your GroupID

	a. The groupid goes in tokenf.py
	
	    FACEBOOK_GROUP='25160801076'
