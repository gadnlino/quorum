# Quorum Coding Challenge - Solution details

## Table of Contents

- [Context](#context)
- [Solution](#solution)

## Context

In the challenge, we were given 4 csv files containing data about US Congress legislation bills, alongside its sponsors, voting results and which legislator voted in favor or against each bill. In the code solution, we had to provide views to these 2 user requests:

1) For every legislator available, how many bills did the legislator support (voted for the bill)? How many bills did the legislator oppose?
2) For every bill available, how many legislators supported the bill? How many legislators opposed the bill? Who was the primary sponsor of the bill?

In almost 8 hours, considering the implementation and the writeup, I was able to provide the solution described in the section below.

## Solution

My code solution consisted in two main parts:

1) A Flask web API
2) A SQLite database with the provided data

![](https://i.imgur.com/1gnDTMg.png)

The Flask framework fits perfectly for this scenario. It allowed me to develop the API quickly and, because of the small complexity of the project, the codebase maintained an organized and straightforward fashion, with easy maintainability. It uses a standard integration format that is REST, that can be easily integrated with other applications such as web frontends, mobile applications and other APIs and backend systems with ease. Finally, the OpenAPI/Swagger documentation format page allows users to interact with the app and validate the results in an easy and well known way.

![](https://i.imgur.com/OfckrEJ.png)

Regarding the SQLite database: I could have used another data manipulation framework for Python such as Pandas; Unfortunately these frameworks do not offer you a fashionable and easy(and quick!, since I do not need to load the entire data into memory) way to do data aggregations and other transformations needed in a data report for example. Therefore, I promptly loaded the .csv files in a SQLite database that, in addition to offering a standard, clearer and well known data manipulation language, gives me the benefit of extensibility and maintainability; If thinking about a real production scenario, one could simply change the database connection in the repository file to a real DB and the application would continue to function seamlessly, and for additional data in the report, such as new views and columns in the existing reports, the only thing needed is to adjust the existing queries and write new ones if needed.

![](https://i.imgur.com/VwwHqEs.png)

If the data input was to be in a different format, such as a text file, the best way to have it working was to build an adapter or a script to interpret this file and load the data into the SQLite database; No changes in the application core would be needed.