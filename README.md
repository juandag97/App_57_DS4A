# Readme
These are the instructions to install and execute the Data Analysis project inside a Linux server in the cloud instance.

## Installation
All the steps are based on a Linux server in the cloud with and a domain name or IP exposed to the internet.
Installation

### Step 1.
Be sure you have Python 3 installed

### Step 2.
Install NGINX. 
Follow the [documentation](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/) 

### Step 3.
Create a folder for your project
```
mkdir project
```
### Step 4.

Create a python3 environment inside your project folder
```
python3 -m venv /path/to/new/virtual/environment
```
Follow the [documentation](https://docs.python.org/3/library/venv.html)

```
source project/env/bin/activate
```
### Step 5.
Send the files from the repository to the project folder.

### Step 6.
Access to the python environment
```
source project/env/bin/activate
```
Execute the requirement folder and install all the dependencies

```
pip install -r requirements.txt
```
The requirement file is inside the folder.
This will install all the python libraries for the project, flask, and WSGI


## Configuration

### Step 1.
Let's configure Nginx.

Go to the Nginx configuration file
```
/etc/nginx/nginx.conf
```
Copy and paste the nginx.config file from the repository's folder config_files 

### Step 2.
Let's configure WSGI

Go to the folder
```
/etc/systemd/system
```
Create send the file `server_project.service` from the repository's folder `config_files`  to the server in the previous path. 

## Usage

### Step 1.
Restart the services Nginx and the service that execute the WSGI. Write the following commands

```
systemctl start nginx
```
```
systemctl start server_project.service
```
### Step 2.
Check the status from both services with these commands


```
systemctl status server_project.service
```

```
systemctl status nginx
```
The responses should be green with a 'running' label

In case to update the application just restart the services with these commands

```
systemctl restart server_project.service
```

```
systemctl restart nginx
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)