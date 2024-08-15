
import ollama
import os
import time
import profileExtractor

os.system("cls")

custom_information = "You are a Reddit Profile Analyzer. I will give you the following information about a reddit account: username, total karma, date of creation of the account, list of subreddits the user has posted in, posts of the user, and mod status (if the user is a moderator or not). Your job is to return the following details of the account (based on the info I gave you) organized in bullet points: - Real name of the person (if found or based on assumptions of information in posts, if not, write 'NOT FOUND') - Gender (if found or based on assumptions of information in posts, if not, write 'NOT FOUND') - Occupation (if found or based on assumptions of information in posts, if not, write 'NOT FOUND') - Country (if found or based on assumptions of information in posts, if not, write 'NOT FOUND') - City (if found or based on assumptions of information in posts, if not, write 'NOT FOUND') - Overview description of the person (paragraph/paragraphs) - Psychological analysis (paragraph/paragraphs) (based on assumptions and information in posts) - General assumptions (paragraph/paragraphs) (based on assumptions and information in posts) - Brief conclusion (paragraph/paragraphs) (summary of the profile) If you cannot find some of the information nor have any assumptions based on the content, you will write 'NOT FOUND' in the corresponding not found information. The information should be presented directly without any introductory phrases like 'here is the info' or 'this is what I found'."

modelfile = f"""
from llama3
system {custom_information}
"""

# Start time of model creation
start_time = time.time()

print("\033[34mCreating model...\033[0m")

try:

    ollama.create(model="redditalan", modelfile=modelfile)

except Exception as e:

    print("\033[31mError creating model\033[0m")
    print(e)
    exit()

# End time of model creation
end_time = time.time()

print("\033[34mModel created in", end_time - start_time, "seconds\033[0m")
print("\033[32mModel ready to chat\033[0m")

username = input("\n Enter the username of the Reddit user (without u/): ")

#Extract information from the user
print("\033[34mExtracting information...\033[0m")
userdata = profileExtractor.getUserInfo(username)

print("\033[32mInformation extracted successfully\033[0m")
print("\033[34mFormatting information...\033[0m")
#Format the information extracted
userString = profileExtractor.infoFormatter(userdata[0], userdata[1], userdata[2], userdata[3], userdata[4], userdata[5])
print("\033[32mInformation formatted successfully)\033[0m")


print("\033[34mThe model is thinking...\033[0m")

#Time it takes to run the prompt
start_time2 = time.time()
#Chat with the model
response = ollama.chat(model="redditalan", messages=[{

    'role': 'user',
    'content': userString

}])
print(f"\033[34mModel took {time.time() - start_time2} seconds to answer \033[0m")

print("\033[32mModel has responded\033[0m")

#Print the response
print(f"\n[BOT] {response["message"]["content"]}")

#Save response["message"]["content"] in a txt file
with open(f"./profiles/{username}_profile.txt", "w") as file:
    file.write(response["message"]["content"])