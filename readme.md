# ADS-B data cleaning

## Data Download:

The best source we've been able to find is the free samples at adsbexchange.com, located here:

https://history.adsbexchange.com/downloads/samples/

Just need any of those, pick the top smallest one (2016-07-01) for simplicity.

An explanation of the data fields can be found at:
https://www.adsbexchange.com/datafields/


## Code Organization and Tips
1. Please keep your R&D code contained to the ./code/exploratory/ directories. 
Once we have something working and producing final results, recreate a clean functions
in the ./code/final/ directory.
2. Use Python Docstrings at the top of each file, function, and class.
These comments can be auto-generated into more formal documentation later. 
See more here: https://www.python.org/dev/peps/pep-0257/
3. Place all your imports at the top of your files **not** anywhere in the middle. 
This makes your dependencies much easier to see at a quick glance.
4. Make your variable names descriptive. I usually use "camel case" where your variables
are formatted as: testVariable1, secondTestVar. The other typical format uses underscores: 
test_variable1, second_test_var.
Doesn't really matter between them but be consistent. 
5. Comments are good to describe your process, but over-commenting can quickly become
problematic. You'll often find yourself going back
over the same code again and again trying different things. If you write
too many comments, you're unlikely to completely change them every time 
and they just end up incorrect/not describing the final version of your method.
6. **ALWAYS open files and database connections using the Python _with_ command.**
When working with these big data sets not using this can very quickly cause problems for your computer or the servers.
 See example here:
https://www.geeksforgeeks.org/with-statement-in-python/
7. The PyCharm debugger is incredibly useful and you really can't work without it.
Learn how to use it.
8. The enumerate operation is another thing you should be familiar with and use 
frequently. Simultaneously tracks the value and location while iterating through
nearly any obejct.


## Steps to Get Started:
0. Download the git repo, and install git if you don't have it (to commit things back up)
1. Download the data somewhere local and extract it. The total data set will need about 11Gb of space.
If you don't have room for this then hopefully someone can get you some pre-combined flights
which should be significantly smaller.  
2. **Dont add any data to the git repo. Limited figures/final results may be acceptable if small.**
3.
4.
