# Twitter Mini Project

- **[amonagha](https://github.com/ardenmonaghan)**, [Arden Monaghan](https://www.linkedin.com/in/arden-monaghan/)
- **[GaurangBhana](https://github.com/GaurangBhana)**, [Gaurang Bhana](https://www.linkedin.com/in/gaurang-bhana-42249a314/)
- **[havocflipper](https://github.com/havocflipper)**, [Rishabh Sharma](https://www.linkedin.com/in/rishabh-sharma-b5ab8522a/)
- **[osu](https://github.com/osu)**, [Hasan Khan](https://www.linkedin.com/in/pashto)  
# Group Work Breakdown

## Method of coordination
-  Discord group chat used for all communication, and we used discord calls several times to go over the mini project and used features, such as screensharing

## Break-down of the work items and file structure
```
assignment-3-twitter/
├── main.py - Hasan and Gaurang
├── exceptions.py - Hasan and Gaurang
├── db.py - Hasan and Gaurang
├── screen_stack.py - Gaurang and Rishabh
├── prj-sample.db - Provided in lab description, but updated by everyone
├── README.md - Hasan
├── designDoc.pdf - Arden, Gaurang, Hasan and Rishabh
├── .gitignore - Hasan
├── regexp_64bit.so - From sqlean added by Gaurang
├── regexp.dll - From sqlean added by Gaurang
├── regexp.so - From sqlean added by Gaurang
├── screens/ - Hasan
│   ├── __init__.py - Hasan
│   ├── screen.py - Hasan and Gaurang
│   ├── login_screen.py - Hasan and Gaurang
│   ├── signup_screen.py - Hasan and Gaurang
│   ├── main_menu_screen.py - Hasan and Gaurang
│   ├── feed_screen.py - Hasan and Gaurang
│   ├── search_tweets_screen.py - Hasan and Gaurang
│   ├── search_users_screen.py - Hasan and Gaurang
│   ├── user_profile_screen.py - Hasan and Gaurang
│   ├── user_tweets_screen.py - Hasan and Gaurang
│   ├── tweet_detail_screen.py - Hasan and Gaurang
│   ├── compose_tweet_screen.py - Arden, Hasan and Gaurang
│   ├── reply_tweet_screen.py - Hasan and Gaurang 
│   └── list_followers_screen.py - Hasan and Gaurang
```
Further work break down provided in designDoc.pdf 

## Initial Planning
- **October 18**  
  - Decided to meet up on **Wednesday, October 30** to further divide the work into specific portions.
  - We decided to vote on a language to use, so **python** was decided as the language to base the project on

## Development Timeline
### October 27
- **Hasan Khan**
  - Started laying the groundwork for the assignment, working from **11 PM to 3 AM**.
  - Created `twitter.py` and chose Python as the main language for this project.
  - Implemented initial login system and began using **Tkinter** for the graphical interface.

### October 27-28
- **Hasan Khan**
  - Spent **18 hours** working extensively on `twitter.py`, completing major functionalities:
    - **Features added**: Feed, Signup, Login, Search Users, Search Tweets, List Followers, Logout.
    - Created the base framework for **designDoc.pdf**.
  
- **Arden Monaghan & Hasan Khan**
  - Held a voice chat for **4 hours** (10 PM - 2 AM) to troubleshoot issues with:
    - **Search Tweets** logic, specifically parsing hashtags.
    - Collaborated on **Tkinter** implementation and other parts of the code, such as the login system.

### October 28
- **Arden Monaghan**
  - Created a **backup frontend template** using **PyQt** as an alternative to Tkinter.

- **Hasan Khan**
  - Accidentally used `git push --force`, wiping **37-40 commits**. However, files were saved locally, so no data was lost.

- **Gaurang Bhana**
  - Reviewed the code and performed bug fixes:
    - Added error handling to prevent the application from loading an empty database without schema.
    - Implemented **Update Button** functionality.
    - Fixed visual bugs in the interface.

### October 29
- **Hasan Khan & Rishabh Sharma**
  - Discussed switching to command-line prompts but decided to stay with Tkinter after confirming GUI compatibility with X server.

- **Gaurang Bhana**
  - Added additional functionality (currently redundant) for the **Exit Button UI** and future **Favorites List** features.
  - Code was pushed to a separate branch.

### October 30
- **Rishabh Sharma**
  - Wrote tests for registration and authentication.
    
### October 31
- **Gaurang Bhana**
- Documented the code:
  - Added **docstrings** for every class, function, and method.
  - Enhanced code readability by adding comments for specific sections.
- **Rishabh Sharma**
  - Wrote tests for user search, feed, profile and hashtags

### November 1
- Fixed all **SQL injection vulnerabilities** by replacing formatted strings with parameterized queries.
  
- **Rishabh Sharma**
  - Wrote tests to verify **SQL injection** mitigations.
    
### November 2
- **Hasan Khan**
  - Converted classes into separate Python files to improve **modularity** and **readability** of the codebase.
 
### November 6
- **Rishabh Sharma**
  - Wrote tests for follows, replies, tweet search and counters throughout the program
 
### November 10
- **Gaurang Bhana**
  - Worked extensively on cleaning up the code and breaking apart complex functions into multiple simple functions, where functionality is grouped based on which code logically fits with the other
  - Added the screen stack
  - Did a little Debugging
    
- **Rishabh Sharma**
  - Helped debug screens package (relative imports not functional)

### November 11
- **Gaurang Bhana**
  - Did even more cleanup of the code
  - Added some more minor functionality (previous button)
  - Extensively tested the code to make sure everything is working correctly

### November 12
- **Rishabh Sharma**
  - Wrote tests for name sort case and injections in follows table
### November 13
 - **Arden Monaghan**
   - Updated the designDoc to show the flow of data and different access points from the application.
   - Created a visual diagram to help represent this.

### November 14
 - **Hasan Khan**
   - Modified the code to adhere to the new clarifications annoucement, such as:
   - Implementing restriction to lone # case in compose tweet screen
   - Made sure keywords returned exact matches like if you search "he" then "hello" would not be shown
   - Updated tweet details screen to contain tweet type
 - **Gaurang Bhana**
   - Fixed a lot of queries where the data processing that could have been done in SQL is being done in python instead
   - Tested a lot of edge cases for searching and then also devised a regex solution to this

### November 15
- **Rishabh Sharma**
  - Added lone # case warning in reply screen
- **Gaurang Bhana**
  - Fixed a few bugs and tested edge cases


# Code execution guide
You will need to run this on the lab machine using full functionality (-X)
Download XQuartz or XMing
```
ssh -X <ccid>@ohaton.cs.ualberta.ca

git clone the repo

cd assignment-3-twitter

pip install tk

python3 main.py <your db file for example prj-sample.db>
```

# Names of anyone you have collaborated with (as much as it is allowed within the course policy) or a line saying that you did not collaborate with anyone else.  
We declare that we did not collaborate with anyone in this assignment

# External Tools:
 - User Guide Diagram created using [LucidChart](https://www.lucidchart.com).

# More detail of any AI tool used.
- Gaurang Bhana: I declare that I did not refer to any AI tool, but for a regex expression used inside of a query, I did search online and found results from these places: https://stackoverflow.com/questions/25483114/regex-to-find-whole-word-in-text-but-case-insensitive, 
- Hasan Khan: Used github copilot in vscode to make coding faster, also used chatgpt-4 to debug a small problem relating to hashtags when searching
