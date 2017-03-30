@echo off
start "Server" python TwitchMarket.py
start "Databse" python TwitchMarketDatabase.py
start "Client1" python TwitchMarketClient.py