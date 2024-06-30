# CAN_logs
Repo to host CAN logs and post processing scripts
## Adding new testing event logs:
1.Under "CAN_logs/logs" create a new folder for the testing event  
2.In this new folder create two folders "raw" and "parsed"  
3.Add all the new logs under the "raw" folder
## Processing logs
1.In a new terminal go to "CAN_logs/scripts"  
2.Run `python parse_tcu_data.py <pathToLog>` This will create a new file called myLog_parsed.txt  
3.Move this parsed log file to "CAN_logs/myTestingEvent/parsed"  
4.to graph the CAN signals Run `python parse_log.py -a <SignalName> graph <pathToLog>`
## Help
Message the #firmware channel for any questions

