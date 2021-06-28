# A machine running ubuntu with python 3
FROM python:3  
# Our working directory in /usr/src/app
WORKDIR /usr/src/app
# Copy the 'requirements.txt' to the current working directory '.'
COPY requirements.txt .
# We tell to ubuntu machine to run pip3 which is included to install,
# after making sure there is no cache '--no-cache-dir'
# '-r' is recursive, the 'requirements.txt' file which is flask and flask restful
RUN pip3 install --no-cache-dir -r requirements.txt
# Now we copy the current files 'app.py' and 'requirements.txt',
# into the system into the working directory
# the first '.' is your code and the second '.' is whats going into the machine 
COPY . .
# Now we run python3 asmd.py
CMD [ "python3", "tokenApi.py" ]
# we now specify the requirements 'Flask' and 'flast_restful' in the txt file



