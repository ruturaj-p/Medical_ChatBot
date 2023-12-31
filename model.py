import httpcore
setattr(httpcore, 'SyncHTTPTransport', 'AsyncHTTPProxy')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import speech_recognition as sr
import langid
from pydub import AudioSegment
import langchain
import subprocess
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser
from openai import OpenAI
import openai
import os
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import HumanMessage
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from googletrans import Translator
from gtts import gTTS

#############################################################################################################
def get_language_code(language_name):
    # Dictionary mapping Indian languages to their Google language codes
    language_mapping = {
        "hindi": "hi",
        "bengali": "bn",
        "telugu": "te",
        "marathi": "mr",
        "tamil": "ta",
        "urdu": "ur",
        "gujarati": "gu",
        "kannada": "kn",
        "odia": "or",
        "punjabi": "pa",
        "malayalam": "ml",
        "assamese": "as",
        "maithili": "mai",
        "santali": "sat",
        "english": "en"
    }
    lowercase_language_name = language_name.lower()
    language_code = language_mapping.get(lowercase_language_name)
    if language_code is not None:
        return language_code
    else:
        return f"Language code not found for {language_name}"

def transcribe_audio(language_code, audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.record(source)
    language = language_code
    try:
        text = recognizer.recognize_google(audio, language=language)
        return text
    except sr.UnknownValueError:
        print("Google Web Speech API could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")

def transcribe_audio1(language_code, silence_timeout=5):
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("######### Listening .......  #######")
        # Adjust for ambient noise and record the audio
        recognizer.adjust_for_ambient_noise(source)

        try:
            # Listen for speech with dynamic input and automatic stopping
            audio = recognizer.listen(source, timeout=silence_timeout)

            # Transcribe the audio using Google Web Speech API
            text = recognizer.recognize_google(audio, language=language_code)
            return text

        except sr.UnknownValueError:
            print("Google Web Speech API could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")

def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

def text_to_audio(text, language, output_path, output_filename):
    tts = gTTS(text=text, lang=language, slow=False)
    output_file = os.path.join(output_path, output_filename)
    tts.save(output_file)

language_code = get_language_code("english")
##########################################################################################################
## Prompts for Conversation-GPT
## Very first promple (requires the description provided by patient)
Initial_prompt = PromptTemplate.from_template("""You are a normal consulting nurse/doctor. You will recieve some keywords or sentences described by the patient as input. You have to ask the patient two follow up question so as to acquire the information important to suggest him the type of doctor he needs.
No need to write the sentences like this: "I'm sorry to hear that you're experiencing trouble with your vision in your right eye.
Description = {Description_patient}""")

# Setting up conversation
conversation = ConversationChain(
    # llm=ChatOpenAI(openai_api_key="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"), #Ruturaj
    llm=ChatOpenAI(openai_api_key="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"),
    memory=ConversationBufferMemory()
)

## Final Promp to give results/suggestions.
final_text = PromptTemplate.from_template( """{Answer_patient}.
Based on the above coversation sugest patient the type of doctor he need to visit.
You may also give him some primary advices to relieve the patient before the proper counsultaion with doctor.
Just take care of one thing that I am going to use this conversation in my project where the app will fix the appoinment with the doctor itself.
Use this template to respond :
Sytoms :
Expected illness :
Primary Solutions :
I will connect you with [put the doctor type here] via esanjeevani app.
In primary solutions try to suggest some home made remedies and some safe medicines.
So instead of using pharses like "I will reccomend" use phrases like "I will fix find you (The type of doctor required for the patient).
And use the phrases like (Till the consulation with the doctor, you can,,,)"
""")

def first_response(answer):
    promtp_1 = Initial_prompt.format(Description_patient=answer)
    first = conversation.run(prompt_1)
    return first

def second_response(answer):
    second = conversation.run(answer)
    return second

def third_response(answer):
    final = conversation.run(final_text.format(Answer_patient=answer))
    return final

print("please press 'A' and describe your problem : \n")
var = input()
if var=="a":
    descr_patient = transcribe_audio1("en", silence_timeout=2)
print(descr_patient)
prompt_1 = Initial_prompt.format(Description_patient=descr_patient)
print("\n")
first = first_response(prompt_1)
print(first)
print("\n")
var = "b"

print("please press 'A' :" )
var = input()
if var=="a":
    answer_patient = transcribe_audio1("en", silence_timeout=2)
print(answer_patient)
second = second_response(answer_patient)
print(second)
print("\n")
var = "b"

print("please press 'A' :" )
var = input()
if var=="a":
    answer_patient = transcribe_audio1("en", silence_timeout=2)
print(answer_patient)
print("\n")
third = second_response(answer_patient)
print(third)
print("\n")
var = "b"

print("please press 'A' :" )
var = input()
if var=="a":
    Final = transcribe_audio1("en", silence_timeout=2)
print(Final)
print("\n")
final = final_text.format(Answer_patient=Final)
final = third_response(final)
print("\n")
var = "b"

# # Start conversation with initial patient input
# # first = conversation.run(prompt_1) 
# print(first)
# patient_answer1 = input("\nEnter your answer 1 : ")
# ## The first here here is to be spoken to the patient (it's the first question)
# # chat = chat + "\nBot : " + first
# ## Paste the answer of the patient here
# # patient_answer1 = " I am having bllurried vision and I am not having any pain and no itching as well "
# second = conversation.run(patient_answer1)
# print(second)
# patient_answer2 = input("\nEnter your answer2 : ")
# # third = conversation.run(patient_answer2)
# # print(third)
# # patient_answer3 = input("\nEnter your answer 3 : ")
# AI_report = conversation.run(final_text.format(Answer_patient=patient_answer2))
# print(AI_report)
# # chat = chat + "\nPatient :" + patient_answer1
# # patient_answer = patient_answer1
# # cond = chain_check(chat)
# # Loop to continue conversation
# while cond:
#   # Get model response
#   current = conversation.run(patient_answer)
#     # current is the next question ansked by the model
#   chat = chat +  "\nBot : " + current

#     #Point the answer of the paient here
#   patient_answer = input("please answer the question" + current)

#   chat = chat + "\nPatient :" + patient_answer
#     ## This loop continues till the model decides
#   cond = chain_check(chat)

# final_ans = final_text.format(Answer_patient=patient_answer)
# Final = conversation.run(final_ans)
# ## This is the final output by the model.

