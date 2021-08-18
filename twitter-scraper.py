import csv
from time import sleep

# selenium imports
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver

# counter import for getting top 20 most common words in tweets
from collections import Counter

# create loginData file and import twitter account passes from it
from loginData import email, pswd, u_name, path


def get_tweet_data(card):
    """Extract data from tweet data"""
    user = card.find_element_by_xpath('.//span').text # username who posted a tweet
    handle = card.find_element(By.XPATH, './/span[contains(text(), "@")]').text # twitter handle
    try:
        postdate = card.find_element(By.XPATH, './/time').get_attribute('datetime') # postdate
    except NoSuchElementException:
        return

    # tweet content
    comment = card.find_element(By.XPATH, './/div[2]/div[2]/div[1]').text
    response = card.find_element(By.XPATH, './/div[2]/div[2]/div[2]').text
    text = comment + response

    reply_count = replies = card.find_element(By.XPATH, ".//div[@data-testid='reply']").text
    retweets_count = card.find_element(By.XPATH, ".//div[@data-testid='retweet']").text
    likes_count = card.find_element(By.XPATH, ".//div[@data-testid='like']").text

    tweet = []
    if 'Musk' in user:
        tweet = [user, handle, postdate, text, reply_count, retweets_count, likes_count]
    return [tweet, text]


# webdriver startup
browser = webdriver.Chrome(executable_path=path)
driver = webdriver.Chrome(executable_path=path)
driver.maximize_window()

# navigate to twitter login page
driver.get('https://www.twitter.com/login')

sleep(1) # woah cowboy! my Internet is not as fast as you are!

# Log in 1st method
try:
    # username = #driver.find_element_by_xpath('//input[@name=]')
    username = driver.find_element_by_name("session[username_or_email]")
    username.send_keys(email)

    password = driver.find_element_by_name("session[password]")
    password.send_keys(pswd)

    password.send_keys(Keys.RETURN)
    sleep(2) # woah cowboy! my Internet is not as fast as you are!
except NoSuchElementException:
    print("Login difficulties - Twitter is blocking logging in. Let's Try another method.")

# Log in 2nd method
try:
    username = driver.find_element_by_name("session[username_or_email]")
    username.send_keys(u_name)

    password = driver.find_element_by_name("session[password]")
    password.send_keys(pswd)

    password.send_keys(Keys.RETURN)
except NoSuchElementException:
    print("Logging in successful with first method or unable to log in. Try again later")

sleep(2) # woah cowboy! my Internet is not as fast as you are!

# Navigating to Elon Musk twitter page
search_input = driver.find_element(By.XPATH, "//input[@aria-label='Search query']")
search_input.send_keys("@elonmusk")
search_input.send_keys(Keys.RETURN)
sleep(3) # woah cowboy! my Internet is not as fast as you are!

elon_card = driver.find_element(By.XPATH, "//div[@role='button' and @data-testid='UserCell']")
elon_card.click()
sleep(3)

# get tweets on the page
tweet_data = []
tweet_ids = set()
last_position = driver.execute_script("return window.pageYOffset")
scrolling = True
tweets_to_analisis = []

while scrolling:
    page_cards = driver.find_elements(By.XPATH, "//div[@data-testid='tweet']")
    for card in page_cards[-15:]:
        tweet = get_tweet_data(card)[0]
        if tweet:
            tweet_id = ''.join(tweet)
            tweets_to_analisis.append(get_tweet_data(card)[1])
            # print(tweet)
            # print(tweets_to_analisis)
            if tweet_id not in tweet_ids:
                tweet_ids.add(tweet_id)
                tweet_data.append(tweet)

    scroll_attempt = 0
    while True:
        # Scrolling on page pagination
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(1.5)
        current_position = driver.execute_script("return window.pageYOffset")
        if last_position == current_position:
            scroll_attempt += 1

            # end of scroll region
            if scroll_attempt >= 5:
                scrolling = False
                break
            else:
                sleep(2) # attempt to scroll again
        else:
            last_position = current_position
            break

print("Number of tweets scrapped: ", len(tweet_data))

# Saving the tweet data to csv
with open('polynote_tweets.csv', 'w', newline='', encoding='utf-8') as f:
    header = ['UserName', 'Handle', 'PostDate', 'Tweet Text', 'Reply Amount', 'Retweets Amount', 'Likes Amount']
    writer = csv.writer(f)
    writer.writerow(header)
    # for head in header:
    #     writer.w
    # writer.writerows(header)
    # for twt in tweet_data:
    writer.writerows(tweet_data)


# Get Top 20 most common words in tweets
print("=============================================================")
print("Number of tweets scrapped: ", len(tweet_data))
print("Analysing tweets.")
string_result = ' '.join(tweets_to_analisis)
string_result.split()
final_list = string_result.split()
print("=============================================================")
print("Top 25 Most Common Words in Elon's Tweets:")
c = Counter(final_list)
print(c.most_common(100))
