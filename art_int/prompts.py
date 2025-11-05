system_prompt = "You are a helpful software development assistant who produces JSON data. Your responses will only be the JSON without any explanations or other text. You will also not include any code tags in your response."

user_prompt = f"""You will create fake JSON data. Create 1 (one) JSON object. The JSON will be passed to a DJANGO app so thefollowing format must be used for the keys and values:
        
        name = models.CharField(max_length=100, blank=True, null=True)
        email = models.EmailField(blank=True, null=True)
        feedback_text = models.TextField()
        
        The name field should containe a firstname and last initial. For example Matthew C.
        The email field should contain an email format. For example prefix@suffix.com.
        The feedback text field should contain a fake review which either suggests a positive, neutral or negative sentiment. For example 'I thought it was very good'.
        
        Before returning the data to me, please ensure that there is 1 (one) JSON object and that there are no explanations, comments, other text or any code tags. Your response will be directly parsed in my application.
        """