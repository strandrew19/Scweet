from . import utils
from time import sleep
import random
import json
from selenium.webdriver.common.by import By

def get_user_information(users, driver=None, headless=True, description=False):
    """ get user information if the "from_account" argument is specified """

    driver = utils.init_driver(headless=headless)

    users_info = {}

    #used to just grab user descriptions and no print outs
    if description:
        print('Grabbing Descriptions')
        for i, user in enumerate(users):

            log_user_page(user, driver)
            print(i, len(users) - 1)
            if user is not None:
                try:
                    desc = driver.find_element(By.XPATH,'//div[contains(@data-testid,"UserDescription")]').text
                except Exception as e:
                    desc = ""
                users_info[user] = [desc]
                if i == len(users) - 1:
                    driver.close()
                    return users_info
            else:
                print("You must specify the user")
                continue


    if not description:
        for i, user in enumerate(users):

            log_user_page(user, driver)
            print(i, len(users) - 1)
            if user is not None:
                try:
                    following = driver.find_element(By.XPATH,
                        '//a[contains(@href,"/following")]/span[1]/span[1]').text
                except Exception as e:
                    following = ""

                try:
                    followers = driver.find_element(By.XPATH,
                        '//a[contains(@href,"/followers")]/span[1]/span[1]').text
                except Exception as e:
                    followers = ""

                try:
                    element = driver.find_element(By.XPATH,'//div[contains(@data-testid,"UserProfileHeader_Items")]//a[1]')
                    website = element.get_attribute("href")
                except Exception as e:
                    website = ""

                try:
                    desc = driver.find_element(By.XPATH,'//div[contains(@data-testid,"UserDescription")]').text
                except Exception as e:
                    desc = ""
                try:
                    join_date = driver.find_element(By.XPATH,
                        '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[3]').text
                    birthday = driver.find_element(By.XPATH,
                        '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[2]').text
                    location = driver.find_element(By.XPATH,
                        '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
                except Exception as e:
                    try:
                        join_date = driver.find_element(By.XPATH,
                            '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[2]').text
                        span1 = driver.find_element(By.XPATH,
                            '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
                        if hasNumbers(span1):
                            birthday = span1
                            location = ""
                        else:
                            location = span1
                            birthday = ""
                    except Exception as e:
                        # print(e)
                        try:
                            join_date = driver.find_element(By.XPATH,
                                '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
                            birthday = ""
                            location = ""
                        except Exception as e:
                            # print(e)
                            join_date = ""
                            birthday = ""
                            location = ""
                print("--------------- " + user + " information : ---------------")
                print("Following : ", following)
                print("Followers : ", followers)
                print("Location : ", location)
                print("Join date : ", join_date)
                print("Birth date : ", birthday)
                print("Description : ", desc)
                print("Website : ", website)
                users_info[user] = [following, followers, join_date, birthday, location, website, desc]

                if i == len(users) - 1:
                    driver.close()
                    return users_info
            else:
                print("You must specify the user")
                continue


def log_user_page(user, driver, headless=True):
    sleep(random.uniform(1, 2))
    driver.get('https://twitter.com/' + user)
    sleep(random.uniform(1, 2))


def get_users_followers(users, env, verbose=1, headless=True, wait=2, limit=float('inf'), file_path=None, write_out=True):
    followers = utils.get_users_follow(users, headless, env, "followers", verbose, wait=wait, limit=limit)

    if write_out:
        if file_path == None:
            file_path = 'outputs/' + str(users[0]) + '_' + str(users[-1]) + '_' + 'followers.json'
        else:
            file_path = file_path + str(users[0]) + '_' + str(users[-1]) + '_' + 'followers.json'
        with open(file_path, 'w') as f:
            json.dump(followers, f)
            print(f"file saved in {file_path}")
        return followers
    if not write_out:
        return followers


def get_users_following(users, env, verbose=1, headless=True, wait=2, limit=float('inf'), file_path=None, write_out=True):
    following = utils.get_users_follow(users, headless, env, "following", verbose, wait=wait, limit=limit)

    if write_out:
        if file_path == None:
            file_path = 'outputs/' + str(users[0]) + '_' + str(users[-1]) + '_' + 'following.json'
        else:
            file_path = file_path + str(users[0]) + '_' + str(users[-1]) + '_' + 'following.json'
        with open(file_path, 'w') as f:
            json.dump(following, f)
            print(f"file saved in {file_path}")
        return following
    if not write_out:
        return following

def get_retweeters(users, tweets,  env, verbose=1, headless=True, wait=2, limit=float('inf'), file_path=None):
    retweeters = utils.get_retweets(users, tweets, headless, env, "followers", verbose, wait=wait, limit=limit)

    if file_path == None:
        file_path = 'outputs/' + str(users[0]) + '_' + str(tweets[users[0]]) + '.json'
    else:
        file_path = file_path + str(users[0]) + '_' + str(tweets[users[0]]) + '.json'
    with open(file_path, 'w') as f:
        json.dump(retweeters, f)
        print(f"file saved in {file_path}")
    return retweeters


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

