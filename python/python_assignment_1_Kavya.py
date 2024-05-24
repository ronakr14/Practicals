# Take a dataframe and apply lambda operation on that
import pandas as pd
values= [['Rohan',455],['Elvish',250],['Deepak',495],
		['Soni',400],['Radhika',350],['Vansh',450]] 
df = pd.DataFrame(values,columns=['Name','Total_Marks'])
# Applying lambda function to find percentage of 'Total_Marks' column 
df = df.assign(Percentage = lambda x: (x['Total_Marks'] /500 * 100))
print(df)

# Q.2 To check whether two strings are anagram or not 
def check(s1, s2):
	# the sorted strings are checked 
	if(sorted(s1)== sorted(s2)):
		print("The strings are anagrams.") 
	else:
		print("The strings aren't anagrams.")		 		
s1 ="listen"
s2 ="silent"
check(s1, s2)

#Q3. Secondary Axis
 
import matplotlib.pyplot as plt
 
x = [1, 2, 3, 4, 5]
y1 = [10, 15, 20, 25, 30]
y2 = [100, 90, 80, 70, 60]
 
plt.plot(x, y1, label='Primary Axis', color='blue')
plt.xlabel('X-axis')
plt.ylabel('Primary Axis')
plt.legend(loc='upper left')
 
# Creating a secondary y-axis
plt.twinx()
plt.plot(x, y2, label='Secondary Axis', color='red')
plt.ylabel('Secondary Axis')
plt.legend(loc='upper right')
 
plt.title('Primary and Secondary Axis')
 
plt.show()

##Que4. Regex in python
 
import re
text = "Welcome to Nitor"
op = re.findall("o", text)
print(op)
op1 = re.search(r'\d+', text)
print(op1)

## Q.5 
#Types of Git Merges:
# 1) Normal Merge:
# - It creates new merge commit that combines the changes from both branches head branch and target branch.Git performs a three-way 
# comparison to identify any conflicts.If there are conflicts, then manually resolve them before merging.
 
# 2) Rebase Merge:
# - It replays the commits from the head branch on top of the target branch.Use this for feature branches that are up-to-date 
# with the target branch and don't require preserving the individual commits in the history.

# 3) Squash Merge:
# - It's similar to a normal merge, it combines changes from branches. Instead of creating a new merge commit, it condenses
# the commits from the head branch into a single new commit on the target branch. Use this when you want a simpler history.