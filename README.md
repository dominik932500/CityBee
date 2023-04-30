# CityBee
Get notified when new cars are added to CityBee car sharing fleet

# Installation
pip3 install -r requirements.txt

#Ansible installation
ansible-playbook playbook.yml -e hostname=localhost
Please change hostname that will match your inventory. If MySQL is not installed - this playbook will install it, setup an user with a new database and then import the latest dump.

