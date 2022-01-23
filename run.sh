source venv/bin/activate
curdir=${PWD##*/}
git pull
pip install -r requirements.txt

screen -X -S $curdir quit
screen -S $curdir python run.py