# fantasy-hoops-assistant

Project Goal: Use Python and Bash to connect to ESPN Fantasy Basketball League via API and assist a team in daily lineups and add/drop suggestions.

MVP: 
  - Connect to league with League ID
  - Load roster, each player's injury status, and play schedule for that day
  - Build that day's lineup- filling every role with the best available healthy player
  - Pull the top free agents and compare against weakest roster players
  - Suggest an add/drop only when the swap clears a minimum level
  - Print the results as a readable markdown file
  - Run on a schedule through Bash

Future Plans:
  - Test lineup builder and add/drop logic with fake player data
  - Final write up and presentation of project

Tech Stack:
  - Language: Python for main program and Bash to schedule the running of the program
  - Tools: espn_api, pandas, pytest from Python; and date, curl, jq from Bash
  - Storage: settings stores in .env, each run of the code stored in a .md markdown
  - External Source: pulling data from ESPN Fantasy via fantasy.espn.com (unofficial) API

How it works:
  - Bash/cron scheduler runs 'run_daily.sh' which calls 'src/main.py'
  - It fetches league data through the 'espn-api', scores every player, builds a lineup, and add/drop advice
  - Writes a report for each day

Scheduling with bash/cron:
  - cron: '0 9 * * * /bin/bash /home/<user>/fantasy-hoops-assistant/run_daily.sh >> /home/<user>/fantasy-hoops-assistant/logs/cron.log 2>&1'
  - only runs while WSL is running

Scheduling through Windows Task Scheduler (option instead of bash scheduler):
- Trigger: daily at 9:00 AM
- Program: wsl.exe
- Arguments: -e /home/<user>/fantasy-hoops-assistant/run_daily.sh
- Setting: run as soon as possible after a missed start
