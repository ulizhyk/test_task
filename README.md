# WingTel Coding Challenge 2

## Requirements
* Python 3.5+
* SQLite

## Starting the server
Everything is set up, including the database and some seed data. All you need to do is create the virtual environment with the dependencies and then execute `flask run`. Voila!

## Challenge
1. Add a versioning table for subscriptions and service codes so we can track what exact datetime a service code was added or removed from a subscription

2. Add code for the `monitor_usage_for_data_blocks` task in the `usages.py` tasks file. This should do the following:
    - Query any subscriptions with the data blocking service code applied
    - Determine when the subscription has data blocking applied and check if any usage has been added in the DataUsage table since that date (use the versioning table from the previous step to determine when data blocking was applied)
    - For any subscriptions that have accrued usage during the time it was data blocked, return those subscription ids

### NOTES:
- Only `active` subscriptions and subscriptions on a non-unlimited plan need to be checked in the monitoring task
