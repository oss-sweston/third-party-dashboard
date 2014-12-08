third-party-dashboard
=====================
apt-get install libpq-dev libmysqlclient-dev
apt-get install mysql-server
apt-get install rabbitmq-server
pip install --upgrade "tox>=1.6,<1.7"
CREATE user 'dashboard'@'localhost' IDENTIFIED BY 'dashboard'; GRANT ALL PRIVILEGES ON thirdpartydashboard.* to 'dashboard'@'localhost'; FLUSH PRIVILEGES;
