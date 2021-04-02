# Module imports
# Random module
import random
# Json module
import json
# Pickle module
import pickle
# Numpy Module
import numpy as np
# Natural language tool kit module
import nltk
# Natural language tool kit stem module
from nltk.stem import WordNetLemmatizer

# Tensorflow models module to load in the model we trained
from tensorflow.keras.models import load_model

# Autocorrect -> spell check
from autocorrect import Speller

from Pawan_IndividualProject.Assignment3 import settings

from Pawan_IndividualProject.Assignment3.NeuralNet_Agent.API import *

class Agent:
    """
        The class contains will contain the model that the chat bot will use to determine a response to user input.

        Attributes:
            lemmatizer (object): A wordnet lemmatizer object.
            intents (object): A JSON object containing all the structure of the neural net model.
            tags (list): A list containing all the response type tags from a pickle object.
            responses (list): A list containing all the responses from a pickle object.
            model (object): An object containing a trained model.

        Methods:
            deconstructSentence(): deconstructs sentences into their root words.
            spellCheck(): takes a sentence and corrects any spelling mistakes based on closest known word
            bagWords(): uses the deconstructed sentence to a series of words and maps it to a matching tag.
            predictResponse(): uses the chatbot model to return a response, with an associated probability.
            getResponse(): returns random bot response that has a greater probability than the minimum threshold.
            run(): runs the chatbot.
        """

    # Object constructor
    def __init__(self):
        # Create a lemmatizer object
        self.lemmatizer = WordNetLemmatizer()
        # read in intents.json file
        # TODO: Updated paths to use settings module instead
        path = settings.joinpath(settings.NEURAL_NET_AGENT_PATH, 'intents.json')
        with open(path) as file:
            self.intents = json.loads(file.read())
        # load in the tags, and responses from the pickle files and load the saved model
        path = settings.joinpath(settings.NEURAL_NET_AGENT_PATH, 'tags.pk1')
        with open(path, 'rb') as file:
            self.tags = pickle.load(file)
        path = settings.joinpath(settings.NEURAL_NET_AGENT_PATH, 'responses.pk1')
        with open(path, 'rb') as file:
            self.responses = pickle.load(file)

        path = settings.joinpath(settings.NEURAL_NET_AGENT_PATH, 'chatbotmodel.h5')
        self.model = load_model(path)
        self.check = Speller(lang='en')

    def spellCheck(self, sentence):
        """
        This method takes a sentence and corrects any spelling mistakes based on closest known word
        Parameters:
            sentence (str): a sentence of user input
        Returns:
            corrected (str): a spell corrected sentence
        """
        corrected = self.check(sentence)
        return corrected

    def deconstructSentence(self, sentence):
        """
        This is a methods takes sentence and deconstructs it into its words, and breaks
        each word into it's stem word.
        Parameters:
            sentence (str): a sentence from user input
        Returns:
            separatedWords (list): a list containing individual root words of a given sentence
        """
        separatedWords = nltk.word_tokenize(sentence.lower())
        # print(separatedWords)
        separatedWords = [self.lemmatizer.lemmatize(word) for word in separatedWords]
        # print(separatedWords)
        return separatedWords

    def bagWords(self, sentence):
        """
        This is a methods takes sentence and uses the deconstructSentence methods and creates a
        bag of words (the same length as the tags), that is, it constructs an array with zeros everywhere
        except where the tags matches a word from the sentence.
        Parameters:
            sentence (str): a sentence from user input
        Returns:
            bag (numpy array): an numpy array for the model
        """
        separatedWords = self.deconstructSentence(sentence)
        bag = [0] * len(self.tags)

        # each word in the list
        for word in separatedWords:
            # enumerate the list of tags
            for (i, key) in enumerate(self.tags):
                # print("This is the key:", key)
                # if a key matches a word, set the bag at the given index to 1
                if key == word:
                    bag[i] = 1
        return np.array(bag)

    def predictResponse(self, sentence):
        """
        This is a methods takes sentence and uses the bagWords methods and predicts the responses
        Parameters:
            sentence (str): a sentence from user input
        Returns:
            potentialResponses (list): a list with responses, and probability of that being the closest responses
        """
        bow = self.bagWords(sentence)
        predictionModel = self.model.predict(np.array([bow]))[0]
        # Specify the error threshold
        ERROR_THRESHOLD = 0.25
        predictedResponses = [[i, r] for i, r in enumerate(predictionModel) if r > ERROR_THRESHOLD]

        predictedResponses.sort(key=lambda x: x[1], reverse=True)
        potentialReponses = []
        for r in predictedResponses:
            potentialReponses.append({'intent': self.responses[r[0]], 'probability': str(r[1])})
        # print(potentialReponses)
        return potentialReponses

    def getResponse(self, userSentence):
        """
        This is a methods takes the user input, retrieves the tags from the JSON
        and checks if it matches the tags from intents list and chooses a random response
        (of the appropriate responses) to return to the user
        Parameters:
            userSentence (list): a sentence from user input
        Returns:
            idealResponse (list): a randomly selected response to the user input
        """
        tag = userSentence[0]['intent']
        intents = self.intents['intents']
        for group in intents:
            if group['tag'] == tag:
                idealResponse = random.choice(group['responses'])
                break
        return idealResponse

    def findShop(self, botResponse):
        api = googleApi()
        additionalHelpRequired = ["Try testing your display with a different device. "
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
        if botResponse in additionalHelpRequired:
            botResponse = "Would you like me to find some computer repair shops in your area? (Y/N)"
            print("Agent: " + botResponse)
            userInput = input("Enter text: ")
            if userInput.lower() in ["y", "yes"]:
                botResponse = "Please format your address in the following form: 1234 SomeStreet St SomeCity " \
                              "SomeProvince F6F 6F6 "
                print("Agent: " + botResponse)
                userAddress = input("Enter text: ")
                api.shopSearch(userAddress)
                print("Agent: Here are some computer shops in your area")
                api.searchResults()
            else:
                print("Agent: Is there anything else I can help you with?")
                return

    def run(self):
        """
        This methods receives user input, and uses the predictResponse methods to determine what the user's intention
        is, then uses the getResponse methods to determine an ideal response to return.
        """

        print("Welcome, we are here to help you with your computer issues. Please type \"Hello\" "
              "or the type of issue you are having, to begin.")

        while True:
            userInput = input("Enter text: ")
            correctedInput = self.spellCheck(userInput)
            # print(correctedInput)

            if correctedInput.lower() == 'quit':
                break
            intentions = self.predictResponse(correctedInput)
            botResponse = self.getResponse(intentions)
            print("Agent: " + botResponse)
            self.findShop(botResponse)


# run the chat bot
def main():
    chatBot = Agent()
    chatBot.run()


if __name__ == '__main__':
    main()
