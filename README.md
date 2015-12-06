This app allow a user to manage a tournament using the swiss system

#Structure:
	* Configuration instructions
	* Operating instructions
	* File manifest
	* Changelog



##Installation instructions
	Before testing this app you have to make sure:
	1. python is installled
	2. prostgresql
	3. copy the github repository via the command line "git clone https://github.com/quentinbt/catalog.git"


##Operating instructions
	1. type the command line "psql -a -f tournament.sql"
	2. type the command line "python tournament_test.py"
	3. if you get the message "8. After one match, players with one win are paired. Success!  All tests pass!" everything is working fine.
		

##File manifest
	tournament/
	├── tournament.py
	├── tournament_test.py
	├── tournament.sql
	└── README.txt


##Changelog
	Check the commit history