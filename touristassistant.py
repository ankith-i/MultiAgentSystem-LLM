import streamlit as st
import openai

# Initialize and set up OpenAI API
def setup_openai():
    openai.api_key = ''

def classify_query(query, context):
    """ Classify the query using the context from previous interactions. """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"{context} Classify this query into one of the following categories: general, tour_location, dining_and_lodging, or info. If the query is about the hotels, restaurants, accommodation, stay, food, snacks and anything related to food, beverages and hospitality classify it into dining_and_lodging. If the query is related to any location, place, monument, historic and non-historic place and any building and any location or place and any random thing which don't qualify under food, beverages, hospitality, lodging places then classify it into info. If the query is associated with advice for planning and tour or a trip then classify it into tour_location. If the query is too general like for example if its like greetings, some general info about weather, some general info about time, something random and things which don't fall under dining_and_lodging, info, tour_location then classify it into general. Just return category names like general or info or dining_and_lodging or tour_location, don't return anything extra like don't even add verbose like the category of this quer is or anything else just give the name of category as efined that's it. \nQuery: '{query}'"}],
        max_tokens=50
    )
    return response.choices[0].message['content'].strip().lower()

def handle_query(agent_type, query, context):
    """ Directly handle the query by the specific agent using GPT with context. """
    agent_names = {
        "general": "General Agent",
        "tour_location": "Tour Planning Agent",
        "dining_and_lodging": "Dining and Lodging Agent",
        "info": "Information Agent"
    }
    detail_prompts = {
        "tour_location": "You are an agent specializing in tour locations. Given the user's query, details and context about previous convesations, provide a comprehensive suggestion.",
        "dining_and_lodging": "You are a dining and lodging agent. Given the user's preferences and context about previous convesations, suggest the best options for eating out and accommodations. Analyse the query properly and answer to it with a more standard and appealing way and answer about only resturants if the user asks about only food or eating or drinking or resturants or anything realted to it and don't answer about accomodation or stay. If the user asks about accomodiation or stay or anything realted to it then only answer about accomodation ans tay and don't answer about food, resturants, bevarages, snacks or anything realted to these topics. If and only if user asks about both dining and loddging then only answer about both.",
        "info": "You are an information desk agent. Provide detailed information based on the user's query and context about previous convesations, about a specific location or subject."
    }
    prompt_for_agent = detail_prompts.get(agent_type, "Respond helpfully to the user's query.")
    full_prompt = f"{prompt_for_agent}\n\nPrevious Context: {context}\n\nUser query: '{query}'"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": full_prompt}],
        max_tokens=3000
    )
    agent_name = agent_names.get(agent_type, "General Assistant")
    category = classify_query(user_input, context)
    print("Classified Category:", category)  # Debugging line to check classification
    return agent_name, response.choices[0].message['content'].strip()



# Streamlit title
st.title('Tourist Assistant Chatbot')

# Initialize Streamlit and OpenAI
setup_openai()

# Ensure history is initialized in the session state
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Input area at the bottom
with st.form("user_input_form"):
    user_input = st.text_input("Ask me anything about your next trip!", key="user_query")
    submit_button = st.form_submit_button("Submit")

if submit_button and user_input:
    context = " ".join([msg['content'] for msg in st.session_state.conversation])
    category = classify_query(user_input, context)
    agent_name, response = handle_query(category, user_input, context)
    # Prepend to conversation for immediate display
    st.session_state.conversation.insert(0, {"role": agent_name, "content": response})
    st.session_state.conversation.insert(0, {"role": "User", "content": user_input})

# Display the conversation in natural order
for message in st.session_state.conversation:
    st.text(f"{message['role']} says: {message['content']}")





