# Facebook Group Scrape
Code for collecting data on any public Facebook group.

## Quick Start: Doing a test run from docker

    docker pull mchirico/facebook-group-scrape
	
Once the image is downloaded, run it.

    docker run -it mchirico/facebook-group-scrape /bin/sh -c 'cd src && ./mainRun.sh'
	
	2016-05-28
	2016-06-04
	2016-06-11
	2016-06-18
	2016-06-25
    ...
	
The command above creates the file database.sqlite. You can copy this file out
after you get the container id from the "docker ps -a" command. Note below my
id was 11b4f36b58a0.

    docker ps -a
	
	CONTAINER ID        IMAGE                            COMMAND                  CREATED             
	11b4f36b58a0        mchirico/facebook-group-scrape   "/bin/sh -c 'cd src &"   About a minute ago  

    docker cp 11b4f36b58a0:/src/data/database.sqlite .




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
