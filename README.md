# CIS400-TERMPROJ

## Access Production Environment
Access: http://44.197.133.174:8501

## Setting up Project Environment locally
Add an SSH key to your local machine. [Link](https://betterprogramming.pub/how-to-add-an-ssh-key-to-github-96d934d09d35)
Clone the Repo locally:
```
git clone https://github.com/iamapez/CIS400-TERMPROJ.git
cd CIS400-TERMPROJ
pip install -r requirements.txt
```
## To get your local front end running
cd into your front end directory
```
streamlit run landingPage.py
```
Open the localhost and port that is provided to you in the terminal.
## Updating code on EC2 Instance
ssh into EC2 instance
```
ssh -i Downloads/sshkey.pem ec2-user@44.197.133.174
sudo yum update
cd CIS400-TERMPROJ/
git pull
```

## Access AWS (WIP)

