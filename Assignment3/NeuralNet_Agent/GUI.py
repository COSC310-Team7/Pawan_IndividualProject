# Import tkinter and agent.py
from tkinter import *
from Pawan_IndividualProject.Assignment3.NeuralNet_Agent.agent import *

# botname specified
bot_name = "Steven"

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"


class ChatApplication:

    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
        self.agent = Agent()
        self.case = 0
        self.noMoreOptions = ["Try testing your display with a different device. "
                              "Otherwise please bring your computer into the shop so we can better assist you.",
                              "Please bring your computer to the shop so we can better assist you.",
                              "Try to unplug it and replug it back in, if it still doesn't work then bring it to "
                              "our shop",
                              "We can look at your monitor at the shop and try to fix it",
                              "Try testing your display with a different device. "
                              "Otherwise please bring your computer into the shop so we can better assist you.",
                              "Make sure none of the wires are getting in the fans. "
                              "Clean the fans and the vents inside the case and that should fix your problem. "
                              "If the problem persists then you can bring your computer to our shop.",
                              "You can try running a security scan or clearing space on your hard drives. "
                              "Otherwise you can buy faster storage at our shop",
                              "If you bring it to the shop we may be able to fix it otherwise we can sell you a "
                              "mouse",
                              "For now you will not be able to use that usb slot. "
                              "If you bring your computer to the shop we can fix it.",
                              "Try checking what temperature your processor operates at. "
                              "Otherwise bring your computer to the shop and we'd be happy to take a look at it.",
                              "Try checking to see what processes are idly running in the background. "
                              "Try to close them. Otherwise bring your computer to the shop and we'd be happy to "
                              "take a "
                              "look at it.", "Try uninstalling the applications are reinstalling them. "
                                             "Otherwise bring your computer to the shop and we'd be happy to take "
                                             "a look at it."]

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("Chatbot")
        self.window.resizable(width=True, height=True)
        self.window.configure(width=600, height=550, bg=BG_COLOR)

        # head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text="Welcome", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        # tiny divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        # text widget
        self.text_widget = Text(self.window, width=30, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=0, pady=0)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(state=NORMAL)

        intro_msg = "Welcome, we are here to help you with your computer issues. Please type \"Hello\" or the type " \
                    "of issue you are having, to begin.\n\n"
        self.text_widget.insert(END, intro_msg)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar.configure(command=self.text_widget.yview)

        # bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        # message entry box
        self.msg_entry = Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        # send button
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

    # on enter pressed function defined
    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "You")
        # print(self.case)

        if self.case == 0:
            self._bot_response(msg)

        elif self.case == 1:
            self._need_help(msg)

        elif self.case == 2:
            api = googleApi()
            api.shopSearch(msg)
            botResponse = "Hear are some shops in your area:\n\n"
            path = settings.joinpath(settings.NEURAL_NET_AGENT_PATH, "placesSearch.json")
            with open(path) as jsonFile:
                searchedLocations = json.load(jsonFile)
            for shop in searchedLocations['results']:
                name = shop["name"]
                address = shop["formatted_address"]
                rating = shop["rating"]
                if rating == 5:
                    botResponse = botResponse + "---- " + str(name) + " ----\n"
                    botResponse = botResponse + "Address: " + str(address) + "\n"
                    botResponse = botResponse + "Rating: " + str(rating) + "\n"

            self._insert_message(botResponse, bot_name)
            botResponse = "Is there anything else I can assist you with?"
            self._insert_message(botResponse, bot_name)
            self.case = 0

    def _insert_message(self, msg, sender):
        if not msg:
            return  # if there is no text entered
        msg = self.agent.spellCheck(msg)
        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)
        self.text_widget.see(END)

    def _bot_response(self, userInput):
        intentions = self.agent.predictResponse(userInput)
        botResponse = self.agent.getResponse(intentions)

        if botResponse in self.noMoreOptions:
            botResponse = botResponse + " Would you like me to find computer shops near you? (Y/N)"
            self._insert_message(botResponse, bot_name)
            self.case = 1
        else:
            self._insert_message(botResponse, bot_name)

    def _need_help(self, userInput):
        if userInput.lower() in ["y", "yes"]:
            botResponse = "Please format your address in the following form: 1234 SomeStreet St SomeCity SomeProvince " \
                          "F6F 6F6"
            self._insert_message(botResponse, bot_name)
            self.case = 2
        else:
            botResponse = "Is there anything else I can help you with?"
            self._insert_message(botResponse, bot_name)
            self.case = 0


if __name__ == "__main__":
    app = ChatApplication()
    app.run()
