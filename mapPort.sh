read -p "Enter your username (name.surname): " username
read -p "Enter your password: " password

SSHPASS=$password sshpass -e ssh -tt -L *:5000:localhost:5000 -o StrictHostKeyChecking=no -p 34567 $username@200.14.84.235 'date; /bin/bash'
