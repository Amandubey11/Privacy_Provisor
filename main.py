<<<<<<< HEAD
# main.py - PHASE 2: SQLite Database Integration
from fastapi import FastAPI
from pydantic import BaseModel
from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine
import google.generativeai as genai
import os
import sqlite3
import re
from dotenv import load_dotenv

# --- 1. CONFIGURATION & SECURITY ---
load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API_KEY")

if not GENAI_API_KEY:
    raise ValueError("API Key not found! Please check your .env file.")

genai.configure(api_key=GENAI_API_KEY)

def get_chat_model():
    model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    for name in model_names:
        try:
            return genai.GenerativeModel(name)
        except:
            continue
    return genai.GenerativeModel('gemini-1.5-flash')

model = get_chat_model()

# --- 2. THE UPGRADED VAULT (WITH SQLITE DATABASE) ---
class PrivacyVault:
    def __init__(self):
        print("Initializing Engine & Database...")
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
        self.entity_counters = {}

        # Connect to SQLite (This creates 'vault_memory.db' in your folder)
        self.conn = sqlite3.connect('vault_memory.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        # Create the database table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS token_map (
                token TEXT PRIMARY KEY,
                real_value TEXT
            )
        ''')
        self.conn.commit()

        # Custom Phone Rule
        phone_pattern = Pattern(name="ten_digit_mobile", regex=r"\b\d{10}\b", score=1.0)
        phone_recognizer = PatternRecognizer(supported_entity="PHONE_NUMBER", patterns=[phone_pattern])
        self.analyzer.registry.add_recognizer(phone_recognizer)

    def _generate_token(self, entity_type):
        if entity_type not in self.entity_counters:
            self.entity_counters[entity_type] = 0
        self.entity_counters[entity_type] += 1
        return f"<{entity_type}_{self.entity_counters[entity_type]}>"

    def anonymize(self, text):
        results = self.analyzer.analyze(text=text, language='en')
        
        # Filter Overlaps
        results.sort(key=lambda x: x.score, reverse=True)
        filtered_results = []
        keep_indices = []
        for res in results:
            is_overlap = False
            for kept_start, kept_end in keep_indices:
                if max(res.start, kept_start) < min(res.end, kept_end):
                    is_overlap = True
                    break
            if not is_overlap:
                filtered_results.append(res)
                keep_indices.append((res.start, res.end))
        
        filtered_results.sort(key=lambda x: x.start, reverse=True)
        
        anonymized_text_list = list(text)
        for result in filtered_results:
            original_value = text[result.start:result.end]
            entity_type = "PHONE_NUMBER" if result.entity_type in ["US_DRIVER_LICENSE", "UK_NHS"] else result.entity_type
                
            token = self._generate_token(entity_type)
            
            # --- DATABASE SAVE ---
            # Instead of a dictionary, we save the token to the hard drive
            self.cursor.execute('''
                INSERT OR REPLACE INTO token_map (token, real_value) 
                VALUES (?, ?)
            ''', (token, original_value))
            self.conn.commit()
            
            anonymized_text_list[result.start:result.end] = list(token)
            
        return "".join(anonymized_text_list)

    def de_anonymize(self, text):
        clean_text = text
        
        # --- DATABASE LOOKUP ---
        # 1. Use Regex to find all tokens in the AI's response (e.g., <EMAIL_ADDRESS_1>)
        tokens_in_text = re.findall(r'<[A-Z_]+_\d+>', text)
        
        # 2. Look up only those specific tokens in the database
        for token in set(tokens_in_text):
            self.cursor.execute('SELECT real_value FROM token_map WHERE token = ?', (token,))
            result = self.cursor.fetchone()
            
            if result:
                clean_text = clean_text.replace(token, result[0])
                
        return clean_text

app = FastAPI()
vault = PrivacyVault()

class UserPrompt(BaseModel):
    prompt: str

@app.post("/secure-chat")
async def secure_chat(user_input: UserPrompt):
    # 1. Anonymize
    sanitized_prompt = vault.anonymize(user_input.prompt)
    
    # 2. Call Real AI
    system_instruction = (
        "You are a helpful assistant. "
        "IMPORTANT: You will receive text with placeholders like <EMAIL_ADDRESS_1>. "
        "Please answer the user's question BUT PRESERVE these placeholders exactly as they are. "
        "Do not try to guess what they are."
    )
    
    try:
        response = model.generate_content(f"{system_instruction}\n\nUser Query: {sanitized_prompt}")
        real_llm_response = response.text
    except Exception as e:
        real_llm_response = f"AI Error: {str(e)}"
    
    # 3. De-anonymize
    final_response = vault.de_anonymize(real_llm_response)
    
    return {
        "original_prompt": user_input.prompt,
        "sanitized_sent_to_llm": sanitized_prompt,
        "raw_llm_response": real_llm_response,
        "final_response_to_user": final_response
=======
# main.py - PHASE 2: SQLite Database Integration
from fastapi import FastAPI
from pydantic import BaseModel
from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine
import google.generativeai as genai
import os
import sqlite3
import re
from dotenv import load_dotenv

# --- 1. CONFIGURATION & SECURITY ---
load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API_KEY")

if not GENAI_API_KEY:
    raise ValueError("API Key not found! Please check your .env file.")

genai.configure(api_key=GENAI_API_KEY)

def get_chat_model():
    model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    for name in model_names:
        try:
            return genai.GenerativeModel(name)
        except:
            continue
    return genai.GenerativeModel('gemini-1.5-flash')

model = get_chat_model()

# --- 2. THE UPGRADED VAULT (WITH SQLITE DATABASE) ---
class PrivacyVault:
    def __init__(self):
        print("Initializing Engine & Database...")
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
        self.entity_counters = {}

        # Connect to SQLite (This creates 'vault_memory.db' in your folder)
        self.conn = sqlite3.connect('vault_memory.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        # Create the database table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS token_map (
                token TEXT PRIMARY KEY,
                real_value TEXT
            )
        ''')
        self.conn.commit()

        # Custom Phone Rule
        phone_pattern = Pattern(name="ten_digit_mobile", regex=r"\b\d{10}\b", score=1.0)
        phone_recognizer = PatternRecognizer(supported_entity="PHONE_NUMBER", patterns=[phone_pattern])
        self.analyzer.registry.add_recognizer(phone_recognizer)

    def _generate_token(self, entity_type):
        if entity_type not in self.entity_counters:
            self.entity_counters[entity_type] = 0
        self.entity_counters[entity_type] += 1
        return f"<{entity_type}_{self.entity_counters[entity_type]}>"

    def anonymize(self, text):
        results = self.analyzer.analyze(text=text, language='en')
        
        # Filter Overlaps
        results.sort(key=lambda x: x.score, reverse=True)
        filtered_results = []
        keep_indices = []
        for res in results:
            is_overlap = False
            for kept_start, kept_end in keep_indices:
                if max(res.start, kept_start) < min(res.end, kept_end):
                    is_overlap = True
                    break
            if not is_overlap:
                filtered_results.append(res)
                keep_indices.append((res.start, res.end))
        
        filtered_results.sort(key=lambda x: x.start, reverse=True)
        
        anonymized_text_list = list(text)
        for result in filtered_results:
            original_value = text[result.start:result.end]
            entity_type = "PHONE_NUMBER" if result.entity_type in ["US_DRIVER_LICENSE", "UK_NHS"] else result.entity_type
                
            token = self._generate_token(entity_type)
            
            # --- DATABASE SAVE ---
            # Instead of a dictionary, we save the token to the hard drive
            self.cursor.execute('''
                INSERT OR REPLACE INTO token_map (token, real_value) 
                VALUES (?, ?)
            ''', (token, original_value))
            self.conn.commit()
            
            anonymized_text_list[result.start:result.end] = list(token)
            
        return "".join(anonymized_text_list)

    def de_anonymize(self, text):
        clean_text = text
        
        # --- DATABASE LOOKUP ---
        # 1. Use Regex to find all tokens in the AI's response (e.g., <EMAIL_ADDRESS_1>)
        tokens_in_text = re.findall(r'<[A-Z_]+_\d+>', text)
        
        # 2. Look up only those specific tokens in the database
        for token in set(tokens_in_text):
            self.cursor.execute('SELECT real_value FROM token_map WHERE token = ?', (token,))
            result = self.cursor.fetchone()
            
            if result:
                clean_text = clean_text.replace(token, result[0])
                
        return clean_text

app = FastAPI()
vault = PrivacyVault()

class UserPrompt(BaseModel):
    prompt: str

@app.post("/secure-chat")
async def secure_chat(user_input: UserPrompt):
    # 1. Anonymize
    sanitized_prompt = vault.anonymize(user_input.prompt)
    
    # 2. Call Real AI
    system_instruction = (
        "You are a helpful assistant. "
        "IMPORTANT: You will receive text with placeholders like <EMAIL_ADDRESS_1>. "
        "Please answer the user's question BUT PRESERVE these placeholders exactly as they are. "
        "Do not try to guess what they are."
    )
    
    try:
        response = model.generate_content(f"{system_instruction}\n\nUser Query: {sanitized_prompt}")
        real_llm_response = response.text
    except Exception as e:
        real_llm_response = f"AI Error: {str(e)}"
    
    # 3. De-anonymize
    final_response = vault.de_anonymize(real_llm_response)
    
    return {
        "original_prompt": user_input.prompt,
        "sanitized_sent_to_llm": sanitized_prompt,
        "raw_llm_response": real_llm_response,
        "final_response_to_user": final_response
>>>>>>> 9b195144be5d92762f53a2d94cb749a83a4b9079
    }