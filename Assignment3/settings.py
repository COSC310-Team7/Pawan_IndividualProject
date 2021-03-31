import os


def joinpath(*args):
    return os.path.join(*args)


# DONE: Resolve paths
ROOT = os.path.dirname(__file__)
NEURAL_NET_AGENT_PATH = joinpath(ROOT, 'NeuralNet_Agent')
GOOGLE_API_PATH = joinpath(ROOT, 'Google_API')
CREDENTIALS = joinpath(ROOT, 'Credentials')
