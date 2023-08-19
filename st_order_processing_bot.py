import streamlit as st
from streamlit_chat import message as st_message
#from utils import get_initial_message, get_chatgpt_response, update_chat
import openai
import os
from dotenv import load_dotenv # read local .env file
load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')

global prompt
st.title("Pizza Order Processing Bot")

 

def get_initial_message(prompt):
   messages=[
            {"role": "system", "content": f"""I restrict you always remember You are not trained to answer questions like about Programming,Coding,Development,General Knowledge,Mathematics,Information about any country,city,place,person or History of any person, place, country, city, thing  or Softwares and educational information about any book,subject,document etc. Or any other types of questions which is not related to pizza ordering , an automated service to collect orders for a pizza restaurant. \  
    You first greet the customer, then collect the order, \
    and then ask if it's a pickup or delivery. \
    You wait to collect the entire order, then summarize it and check for a final \
    time if the customer wants to add anything else. \
    If it's a delivery, you ask for an address. \
    Finally, you collect the payment. \
    Make sure to clarify all options, extras, and sizes to uniquely \
    identify the item from the menu. \
    The menu includes: \ 
    - Pepperoni pizza: 12.95, 10.00, 7.00 \
    - Cheese pizza: 10.95, 9.25, 6.50 \
    - Eggplant pizza: 11.95, 9.75, 6.75 \
    - Fries: 4.50, 3.50 \
    - Greek salad: 7.25 \
    Toppings: \
    - Extra cheese: 2.00 \
    - Mushrooms: 1.50 \
    - Sausage: 3.00 \
    - Canadian bacon: 3.50 \
    - AI sauce: 1.50 \
    - Peppers: 1.00 \
    Drinks: \
    - Coke: 3.00, 2.00, 1.00 \
    - Sprite: 3.00, 2.00, 1.00 \
    - Bottled water: 5.00 \
    """},
    {"role": "user", "content": f""" analyze the following: {prompt} and return the answers of questions which is related to pizza ordering: {prompt}"""},
   ]
   return messages

def get_chatgpt_response(messages):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
    )
    return  response['choices'][0]['message']['content']

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages
 
prompt = st.text_input("Order Please 🍕: ", key="input") 

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
    
if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'messages' not in st.session_state:
    st.session_state['messages'] = get_initial_message(prompt)    
        

if prompt:
    with st.spinner("generating..."):
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", prompt)
        response = get_chatgpt_response(messages)
        messages = update_chat(messages, "assistant", response)
        st.session_state.past.append(prompt)
        st.session_state.generated.append(response)    
  
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        st_message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        st_message(st.session_state["generated"][i], key=str(i)) 


              

    #with st.expander("Show Messages"):
     #   st.write(st.session_state['messages'])
    


