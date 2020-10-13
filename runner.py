
import omegaml as om

om = om.setup(username='devconnect', 
          apikey='2d4b51a02d0a9c91507cca882ee5e5f5188808fc')

 # your notebook
!if [ ! -d /app/pylib/user/myrepo ]; then git clone https://github.com/omegaml/apps /app/pylib/user/myrepo; fi
!if [ -d /app/pylib/user/myrepo ]; then cd /app/pylib/user/myrepo && git pull; fi

task = om.runtime.require('huge').job('main-nb').run() ## Sends message to celery with name of notebook, and desire to run

## As soon as celery receives the message, it will start running it.
## When finished, a message is sent back to temp storage in Rabbit, 
## persists for an hour or so stating the result

## Result of notebook execution is stored in the notebook created in 
## results folder

# task.get()  ## Celery looks in temp storage (based on task ID) and times out
