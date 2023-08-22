import threading
import time
import os

def ask():
    """
    Simple function where you ask him his name, if he answers
    you print message and exit
    """
    name = raw_input("Tell me your name, you have 5 seconds: ")
    exit_message = "Wohoho you did it..Your name is %s" % name
    exit(exit_message)

def exit(msg):
    """
    Exit function, prints something and then exits using OS
    Please note you cannot use sys.exit when threading..
    You need to use os._exit instead
    """
    print(msg)
    os._exit(1)

def close_if_time_pass(seconds):
    """
    Threading function, after N seconds print something and exit program
    """
    time.sleep(seconds)
    exit("Time passed, I still don't know your name..")

def main():
    # define close_if_time_pass as a threading function, 5 as an argument
    t = threading.Thread(target=close_if_time_pass,args=(5,))
    # start threading
    t.start()
    # ask him his name
    ask()

if __name__ == "__main__":
    main()