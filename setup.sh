# Setup code overrides for GIC activity

sudo cp usr/bin/pwm.sh /usr/bin/
sudo chmod +x /usr/bin/pwm.sh

sudo cp etc/systemd/system/jetbot_pwm.service /etc/systemd/system/

sudo systemctl start jetbot_pwm.service
sudo systemctl enable jetbot_pwm.service

mv ~/jetbot/jetbot/robot.py robot_original.py
cp jetbot/jetbot/robot.py ~/jetbot/jetbot/
cp jetbot/jetbot/robot.py /usr/local/lib/python3.6/dist-packages/jetbot-0.4.3-py3.6.egg/jetbot

mkdir ~/jetbot/notebooks/gic
cp jetbot/notebooks/gic ~/jetbot/notebooks/gic
