import json
from langchain_ollama import ChatOllama

system_prompt = "You are a helpful software development assistant who produces JSON data. Your responses will only be the JSON without any explanations or other text. You will also not include any code tags in your response."

NUM_RES = 5

user_prompt = f"""You will create fake JSON data. Create {NUM_RES} results that are in an array. The JSON will be passed to a DJANGO app so thefollowing format must be used for the keys and values:
    
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    feedback_text = models.TextField()
    sentiment_score = models.FloatField()
    sentiment_label = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    
    The name field should containe a firstname and last initial. For example Matthew C.
    The email field should contain an email format. For example prefix@suffix.com.
    The feedback text field should contain a fake review which either suggests a positive, neutral or negative sentiment. For example 'I thought it was very good'.
    The sentiment_score field should be a floating point number between 1 and -1. and can contain up to 4 decimal places. For example 0.5563.
    The sentiment_label should be one of 'Positive', 'Neutral', or 'Negative'.
    The created_at DateTimeField should all be for the year 2025. For example, 2025-08-27T15:34:36.014299Z.


    Before returning the data to me, please ensure that the JSON objects are in an array and that there are no explanations, comments, other text or any code tags. Your response will be directly parsed in my application.
    """

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
]

def write_to_file(json_obj):
    with open("test.json", "w") as f:
        f.write(json_obj)

def chat(messages):
    chat = ChatOllama(model="llama3.2")
    print("Sending to model.")
    response = chat.invoke(messages)
    print("Response received.")
    write_to_file(response.content)
    print("Finished.")
    

chat(messages)