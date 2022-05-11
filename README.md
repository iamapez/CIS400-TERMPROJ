# CIS400-TERMPROJ

## Access Devlopment Environment
Access: http://44.197.133.174:8501


## TA or Professor use the following instruction to get this running 


## Setting up Project Environment locally
## Git instructions (harder)
Add an SSH key to your local machine. [Link](https://betterprogramming.pub/how-to-add-an-ssh-key-to-github-96d934d09d35)
Clone the Repo locally:
```
git clone https://github.com/iamapez/CIS400-TERMPROJ.git
```
## Local instructions
```
Download the CIS400-TERMPROJ-integration folder from the zipped deliverables
Navigate to the project environment and run:
cd CIS400-TERMPROJ-integration
pip install -r requirements.txt
```

```
## To get your local front end running
cd into your frontend directory using
cd frontend

and run the following in terminal to get running on local machine. Open the local host link that populates in terminal
```
streamlit run landingPage.py
```
Open the localhost and port that is provided to you in the terminal.

## Updating code on EC2 Instance
ssh into EC2 instance
```
ssh -i Downloads/sshkey.pem ec2-user@44.197.133.174
sudo yum update
cd CIS400-TERMPROJ-integration/
git pull
```

## Access AWS (WIP)

