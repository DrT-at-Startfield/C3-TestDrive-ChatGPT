# AdventureGPTBE Class - a back end class to drive an adventure game
# using the chat completion capability of OpenAI's ChatGPT

import os
import time
import datetime
from dotenv import load_dotenv
import openai


class TestDriveGPT:
    """A Class to test out ChatGPT interactions."""

    def __init__(self):
        self.api_token = None
        self.base_prompt = """Pretend you are an all powerful genie who has been summoned. Respond to all questions
            and requests in an aloof and grandiose manor."""

    def load_api_key(self):
        load_dotenv()
        self.api_token = os.getenv("OPENAI_API_KEY")
        # Use the version below if you are using Replit's Secret tool
        #self.api_token = os.environ['OPENAI_API_KEY']
        openai.api_key = self.api_token

    def init_chat(self):
        self.load_api_key()
        if self.api_token is None:
            print('An OpenAI API Key has to be specified to use ChatGPT')
            raise 'Missing API Key'

        # now = datetime.datetime.now()
        # timestamp = now.strftime("%Y-%m%d-%H%M%S")
        # logfilename = "Log\chat_log_{0}.txt".format(timestamp)
        # os.makedirs(os.path.dirname(logfilename), exist_ok=True)
        # self.log_fp = open(logfilename, 'w')

    def chat_intro(self):
        """Explain what this interaction with ChatGPT is about"""
        print("Welcome to the great and powerful ChatGPT wizard. Make a request of me, and I'll see what I can do.\n")
        print("Do you want to hear a story? Are you seeking wisdom or your fortune?\n")

    def chat_loop(self):
        # Send base prompt to ChaptGPT and then enter a loop
        keepChatting = True
        request = ""
        last_result = ""
        while keepChatting:
            last_result = self.generate_the_next_response(request, last_result)
            request, keepChatting = self.make_request(request, keepChatting)


    def generate_the_next_response(self, request, last_result):
        print('The great wizard is preparing to address you ...')
        waitingForNextAction = True
        while waitingForNextAction:
            try:
                last_result = self.get_wisdom_from_chatbot(request, last_result)
                print(last_result)
                #self.log_fp.write(last_result + "\n")
                waitingForNextAction = False
            except openai.error.RateLimitError:
                self.pause_game()
        return last_result

    def make_request(self, request, keepChatting):
        needRequest = True
        while needRequest:
            answer = input('What is it that you seek? [q quits] ==> ')
            try:
                if answer == 'q':
                    print('You may leave my presence. Farewell mortal.')
                    # self.log_fp.close()
                    keepChatting = False
                    needRequest = False
                else:
                    request = answer
                    needRequest = False
                #if keepChatting:
                    #self.log_fp.write('Human requested {0}\n'.format(request))
            except ValueError:
                print("I didn't understand your answer. Try again.")
        return request, keepChatting

    def get_wisdom_from_chatbot(self, choice, last_result):
        the_message = self.build_message(choice, last_result)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=the_message
        )
        last_result = response.choices[0].message.content
        return last_result

    def build_message(self, request, last_result):
        message = [
            {"role": "system", "content": self.base_prompt}
        ]
        if len(last_result) > 0:
            message.append({"role": "assistant", "content": last_result})
        if len(request) == 0:
            message.append({"role": "user", "content": "Ask what it is that I seek."})
        else:
            message.append({"role": "user", "content": "{0}.".format(request)})
        return message

    def pause_game(self):
        print('Hit OpenAI rate limit. Stretch your legs for a bit!')
        print('Sleeping for 30 seconds ...')
        time.sleep(10)
        print('  20 seconds')
        time.sleep(10)
        print('  10 seconds')


if __name__ == '__main__':
    adventure = TestDriveGPT()
    adventure.init_chat()
    adventure.chat_intro()
    adventure.chat_loop()



