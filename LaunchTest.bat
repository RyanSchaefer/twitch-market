@echo off
start "Server" python TwitchMarketTest.py
start "Databse" python TwitchMarketDatabase.py
timeout 2
start "Client1" python TwitchMarketClient.py