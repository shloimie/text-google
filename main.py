import time
import email_handling as eh
from web_handler import WebHandleing , check_type



from_dic = {}
list_users = {}
while True:
    print("refreshing")
    my_inbox = eh.get_inbox()
    # my_inbox = [{"from": "1" , "body":"myzmanim"},{"from": "2" , "body":"weather jerusalum"},{"from": "1" , "body":"1"},{"from": "3" , "body":"weather paris"}]
    #check if any new nessages if not wait
    if len(my_inbox) == 0:
        print("sleeping cuz empty")
        time.sleep(10)
        pass

    #if there is a new message
    else:
        print("starting to handle new message")
        # for every message
        for thing in my_inbox:
            fromw, body = thing["from"], thing["body"].strip()
            fromw = eh.strip(fromw)
            # check if sender already has a session open
            if body == "stop":
                break
            if fromw in from_dic:
                print(f"{fromw} is in list body {body}")
                # update time
                from_dic[fromw] = time.time()
                #confirm that it is a digit
                if not check_type(body):
                    #find session and send tabs
                    print("attemting to run secondary search now")
                    list_users[fromw].secondary_search(body)

            else:
                # add to list of setions and make new session
                from_dic[fromw] = time.time()
                print(f"running person {fromw} on body {body}")

                #confirm it not a number
                if check_type(body):
                    list_users[fromw] = WebHandleing(fromw)
                    list_users[fromw].intial_search(body)
                else:
                    print("number enter - no previous session for this user")
            time.sleep(1)

    # delete old users
    cur_time = time.time()
    to_del = []
    for thing in from_dic:
        if round(from_dic[thing] - cur_time) * -1 > 120:
            print(f"deleting {thing}")
            list_users[thing].close()
            list_users[thing].del_user()
            del list_users[thing]
            to_del.append(thing)
    for thing in to_del:
        del from_dic[thing]
    del to_del



