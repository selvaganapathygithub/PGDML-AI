from rasa_core.channels import HttpInputChannel
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_slack_connector import SlackInput


nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/restaurantnlu')
agent = Agent.load('./models/dialogue', interpreter = nlu_interpreter)

input_channel = SlackInput('xoxp-517680107157-516742350496-522632662466-be4114e354b729b0757bb695f2fc56de', #app verification token
							'xoxb-517680107157-524035418886-5pys6OKhn8MokpZjLrvv9fb2', # bot verification token
							'r6MshE0S2MsCd8ffoICJ2OXR', # slack verification token
							True)

agent.handle_channel(HttpInputChannel(5004, '/', input_channel))