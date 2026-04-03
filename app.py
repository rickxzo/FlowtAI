import os
from dotenv import load_dotenv
from flask_cors import CORS
import time
import requests

load_dotenv()
import random
import json
import re

from werkzeug.security import generate_password_hash, check_password_hash
import logging
logger = logging.getLogger(__name__)

import psycopg2
def connect_db():
    try:
        conn = psycopg2.connect(
            host="ep-blue-surf-adwk6v0m-pooler.c-2.us-east-1.aws.neon.tech",
            dbname="neondb",
            user="neondb_owner",
            password="npg_GVplZkyajw67",
            sslmode="require",
             
        )
        return conn
    except Exception as e:
        logger.error(f"Error connecting to database: {e}", exc_info=True)
        return 404
    
import resend
resend.api_key = os.getenv('RESEND_API_KEY')
def send_mail(mail, message, subject):
    try:
        params: resend.Emails.SendParams = {
        	"from": "Acme <onboarding@resend.dev>",
        	"to": [mail],
        	"subject": f"Flowt.AI - {subject}",
        	"html": message,
        }
        resend.Emails.send(params)
        return 1
    except Exception as e:
        logger.error("Error sending mail: ", e)
        return -1

logger.error("IMPORTS DONE")

def semantic_chunk(text):
    try:
        sections = text.split("[section]")
        return sections
    except Exception as e:
        logger.error(f"Error creating knowledge chunk: {e}")
        return f"Error creating knowledge chunk: {e}", 500

import threading

def post_process(user_id, agent_id, convo_id, reply, ipt, opt, user_input, input_cost, output_cost):
    cost = (input_cost/1000000 * ipt + output_cost/1000000 * opt) * 1.1

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        '''
        UPDATE agents
        SET spend = spend + %s,
            iptokens = iptokens + %s,
            optokens = optokens + %s
        WHERE id = %s
        ''', (cost, ipt, opt, agent_id)
    )
    cursor.execute(
        '''
        UPDATE users
        SET balance = balance - %s
        WHERE id = %s
        ''', (cost, user_id)
    )
    cursor.execute("INSERT INTO messages (convo_id, message) VALUES (%s, %s)", (convo_id, f"User: {user_input}"))
    cursor.execute(
        '''
        INSERT INTO messages (convo_id, message)
        VALUES (%s, %s)
        ''', (convo_id, f"You: {reply}")
    )
    conn.commit()
    cursor.close()
    conn.close()


from pinecone import Pinecone
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))  

import replicate
client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))

from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, START, END

def vector_search(prompt, index, namespace):
    try:
        index = pc.Index(host=index)
        search = index.search(
                namespace = namespace,
                query = {
                    "inputs": {"text": prompt},
                    "top_k": 5
                },
                fields = ["category", "chunk_text"],
                rerank = {
                    "model": "bge-reranker-v2-m3",
                    "top_n": 5,
                    "rank_fields": ["chunk_text"] 
                }
            )
        n = len(search['result']['hits'])
        vknowledge = [
            search['result']['hits'][i]['fields']['chunk_text'] for i in range(n) 
        ]
        return vknowledge
    except Exception as e:
        logger.error(f"Error conduction KB search: {e}")
        return f"Error conduction KB search: {e}", 500

def counttokens(model_name, prediction):
    def gpt_5(prediction):
        abc = prediction['logs'].split('\n')
        ip = int(abc[2][19:])
        op = int(abc[3][20:])
        return [ip, op]
    
    def deepseek_r1(prediction):
        abc = prediction['metrics']
        ip = int(abc['input_token_count'])
        op = int(abc['output_token_count'])
        return [ip, op]

    mn = model_name.split("/")[0]
    if mn=="openai":
        return gpt_5(prediction)
    
    elif mn in ['deepseek-ai', 'anthropic', "meta"]:
        return deepseek_r1(prediction)
    

    



class TextModel:
    def __init__(self, model_name, system_prompt):
        self.model_name = model_name
        self.system_prompt = system_prompt
    
    def gen(self, prompt):
        input = {
            "prompt": prompt,
            "system_prompt": self.system_prompt,
        }
        '''
        x = ''
        for event in replicate.stream(
            self.model_name,
            input=input
        ):
            x += str(event)
        return x 
        '''
        prediction = client.predictions.create(
            model=self.model_name,
            input=input
        ) 
        prediction.wait()
        iptokens, optokens = counttokens(self.model_name, prediction.dict())
        output = "".join(prediction.dict()["output"])
        if '4.5' in self.model_name:
            output = output[8:-4]
        reply = f"{output}sep001{iptokens}sep001{optokens}"
        return reply
        #return "".join(prediction.dict()["output"])
            

class ProcessState(TypedDict):
    index: str
    assistant: TextModel
    conversation: str
    knowledge: str
    response: str
    reply: str
    iptokens: int
    optokens: int
    namespace: str

def choose(state: ProcessState) -> str:
    conversation = state["conversation"]
    knowledge = state["knowledge"]
    response = state["response"]
    reply = state["reply"]
    prompt = f"""
    ### Conversation
    {conversation}

    ### Current Knowledge
    {knowledge}

    ### Available Actions
    vector
    """
    response = state["assistant"].gen(prompt).split('sep001')
    #print(response)
    reply = response[0]
    ip = int(response[1])
    op = int(response[2])


    #response = state['assistant'].gen(prompt)

    ipc = state["iptokens"] + ip
    opc = state["optokens"] + op
    return {
        "response": reply,
        "knowledge": knowledge,
        "reply": reply,
        "conversation": conversation,
        "iptokens": ipc,
        "optokens": opc
    }

def route(state: ProcessState) -> str:
    response = state["response"]
    #print(response)
    response = json.loads(response)
    return response["type"]

def go_vector(state: ProcessState):
    conversation = state["conversation"]
    knowledge = state["knowledge"]
    response = state["response"]
    reply = state["reply"]
    ipt = state['iptokens']
    opt = state['optokens']
    #print("GOVECTOR", state)
    response = json.loads(state["response"])
    info = vector_search(response["content"], state["index"], state['namespace'])
    knowledge = state["knowledge"]
    knowledge += f"-> VECTOR SEARCH :{response["content"]}' \nKNOWLEDGE :{info}"
    return {
        "response": response,
        "reply": reply,
        "conversation": conversation,
        "knowledge": knowledge,
        "iptokens": ipt,
        "optokens": opt
    }

def give_reply(state: ProcessState):
    conversation = state["conversation"]
    knowledge = state["knowledge"]
    response = state["response"]
    reply = state["reply"]
    ipt = state['iptokens']
    opt = state['optokens']
    #print("SENDREPLY", state)
    response = json.loads(state["response"])
    #print("RESPONSE ", response)
    reply = response["content"]
    #print("FINAL REPLY ", reply)
    return {
        "response": response,
        "conversation": conversation,
        "knowledge": knowledge,
        "reply": reply,
        "iptokens": ipt,
        "optokens": opt
    }

chat_graph = StateGraph(ProcessState)
chat_graph.add_node("choose", choose)
chat_graph.add_node("go_vector", go_vector)
chat_graph.add_node("give_reply", give_reply)

chat_graph.add_edge(START, "choose")
chat_graph.add_conditional_edges(
    "choose",
    route,
    {
        "answer": "give_reply",
        "vector": "go_vector"
    }
)
chat_graph.add_edge("go_vector", "choose")
chat_graph.add_edge("give_reply", END)

compiled_graph = chat_graph.compile()



from flask import Flask, Response, jsonify, request, session, render_template, redirect, url_for
app = Flask(__name__, template_folder='.', static_folder='front')
CORS(app,
     supports_credentials=True,
     origins=["https://flowtai.onrender.com"])
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
app.secret_key = os.getenv('SECRET_KEY')

import redis

r = redis.Redis(
    host='redis-18483.crce262.us-east-1-1.ec2.cloud.redislabs.com',
    port=18483,
    decode_responses=True,
    username="default",
    password=os.getenv("REDIS_PASS"),
)

from apscheduler.schedulers.background import BackgroundScheduler
def keepalive():
    URLS = [
    "https://flowtai.onrender.com",
    "https://flowtai-1.onrender.com"
    ]
    for url in URLS:
        try:
            response = requests.get(url, timeout=10)
            logger.error("keep alive.")
        except Exception as e:
            logger.error(f"{url} failed: {e}")
    

scheduler = BackgroundScheduler()
scheduler.add_job(func=keepalive, trigger="interval", seconds=90)
scheduler.start()

print("IMPORTS DONE")

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Origin'] = 'https://flowtai.onrender.com'
    return response

@app.route('/respond', methods=['POST', 'GET'])     
def respond():
    try:
        if 'userid' not in session or not session.get('verified', False):
            return "Unauthorized", 401
        agent_id = request.args.get('agent_id')
        user_input = request.args.get('input')
        convo_id = request.args.get('convo')
        convo_id = f"{agent_id}-{convo_id}"
        user_id = session['userid']
        conn = connect_db()
        if conn == 404:
            return "Database connection error", 500
        cursor = conn.cursor()
        cursor.execute(
            "SELECT balance FROM users WHERE id = %s", (session['userid'],)
        )
        balance = cursor.fetchone()[0]
        if balance < 0.05:
            return "Low balance"
        cursor.execute("SELECT model, namespace, prompt, active FROM Agents WHERE id = %s AND userid = %s", (agent_id, session['userid']))
        result = cursor.fetchone()
        if not result:
            cursor.close()
            conn.close()
            return "Agent not found", 404
        model_id, namespace, prompt, active = result
        if active == False:
            return "Agent is inactive"
        cursor.execute("SELECT name, input, output FROM models WHERE id = %s", (model_id,))
        res = cursor.fetchone()
        model_name = res[0]
        input_cost = float(res[1])
        output_cost = float(res[2])
        cursor.execute("SELECT message FROM messages WHERE convo_id = %s ORDER BY id DESC LIMIT 10", (convo_id,));
        convo = cursor.fetchall()
        cursor.close()
        conn.close()
        convo.reverse()
        logger.error(convo)
        conversation = "(Conversation start)\n"
        for i in convo:
            conversation += i[0] + "\n"
        conversation += f"User: {user_input}\nYou: "
        default_prompt = '''
        You are an intelligent assistant representing a company or service. Your primary responsibility is to answer user queries accurately using verified knowledge sources.

In many situations, the user may not provide enough context about the company, its services, products, policies, or internal information. When this happens, prioritize retrieving relevant information from vector search before answering.

Assume that a knowledge base may contain important details about the organization, its offerings, documentation, policies, FAQs, and other operational information. If the user's query could relate to such information, attempt to retrieve context using the available search tools.

Do not invent or assume details about the company. If relevant information cannot be found in available sources, respond honestly that the information is not available.

Your responses should remain helpful, concise, and focused on the user's request.

        '''
        system_prompt = f"""
You are an API agent that MUST return structured JSON.

Context:
{prompt if prompt is not None else default_prompt}

Your job is to decide whether you can answer directly or need to search the vector database.

You MUST return ONLY ONE valid JSON object.

VALID RESPONSE SCHEMA:

{{
  "type": "answer",
  "content": "string"
}}

OR

{{
  "type": "vector",
  "content": "search query"
}}

Rules:
- Output MUST be valid JSON.
- Output ONLY the JSON object.
- Do NOT include explanations.
- Do NOT include reasoning.
- Do NOT include markdown.
- Do NOT include text before or after JSON.
- Response MUST start with {{ and end with }}.
- Do NOT use "/" in the response.
- Do NOT wrap the JSON in ``` or ```json. IMPORTANT
- If the output contains ``` the response is INVALID.

Behavior Rules:
- If the question can be answered using the provided context → return type "answer".
- If additional knowledge is required → return type "vector".
- The "content" field must contain either the final answer OR the vector search query.

Vector Search Rules:
- The conversation history may include previous vector searches.
- Do NOT repeat previous vector search queries.
- Maximum 3 vector searches per conversation.
- Prefer answering with existing knowledge before searching.

If you cannot find the answer even after searching, return:

{{
  "type": "answer",
  "content": "I do not have enough information to answer this."
}}

Examples:

Example 1:
User: What services does the company provide?

Output:
{{
  "type": "vector",
  "content": "company services offered"
}}

Example 2:
User: Thank you!

Output:
{{
  "type": "answer",
  "content": "You're welcome. Let me know if you need anything else."
}}

IMPORTANT:
If the output is not valid JSON, it will be rejected by the system.

Return ONLY the JSON object.
"""
        
        Assistant = TextModel(model_name, system_prompt)
        
        index = f"https://flowt-{session['username']}-rz0q9xs.svc.aped-4627-b74a.pinecone.io"
        state = {
            "index": index,
            "assistant": Assistant,
            "conversation": conversation,
            "knowledge": "",
            "response": {},
            "reply": "",
            "iptokens": 0,
            "optokens": 0,
            "namespace": namespace
        }
        logger.error(state)
        def event_stream(user_id, convo_id, user_input):

            for event in compiled_graph.stream(state):

                if list(event.keys())[0] == "choose":
                    yield f"thinking...\n\n"
                
                elif list(event.keys())[0] == "go_vector":
                    yield f"searching docs...\n\n"
                
                elif list(event.keys())[0] == "give_reply":
                    reply = event['give_reply']['reply']
                    yield "data: "
                    for word in reply.split():
                        yield f"{word} "
                        time.sleep(0.1)
                    #yield f"data: {event['give_reply']['reply']}\n\n"
                    threading.Thread(
                        target=post_process,
                        args=(user_id, agent_id, convo_id, event['give_reply']['reply'], int(event['give_reply']['iptokens']), int(event['give_reply']['optokens']), user_input, input_cost, output_cost)
                    ).start()

                #yield f"data: {event.keys()}\n\n"

                #yield f"data: {json.dumps(event)}\n\n"

        return Response(event_stream(user_id, convo_id, user_input), mimetype="text/event-stream")
        
    except Exception as e:
        #print(f"Error during response generation: {e}")
        return f"Error during response generation: {e}", 500

@app.route('/signup', methods=['POST', 'GET'])        # CONVERT LINK -> FORM UPDATE
def signup():
    try:
        username = request.args.get('username')
        email = request.args.get('email')
        password = request.args.get('password')

        username_pattern = r'^[a-zA-Z0-9_]{3,20}$'
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        

        if not re.match(username_pattern, username):
            raise ValueError(f"Invalid characters detected in username")


        if not re.match(email_pattern, email):
            raise ValueError(f"Invalid characters detected in email")



        conn = connect_db()
        if conn == 404:
            return "Database connection error", 500
        agent_name = f"flowt-{username}"
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password, verified, pchost) VALUES (%s, %s, %s, %s, %s)", (username, email, generate_password_hash(password), True, agent_name))
        conn.commit()
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        userid = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        if not pc.has_index(agent_name):
            pc.create_index_for_model(
                name=agent_name,
                cloud="aws",
                region="us-east-1",
                embed={
                    "model":"llama-text-embed-v2",
                    "field_map":{"text": "chunk_text"}
                }
            )
        session['userid'] = userid
        session['verified'] = False
        session['username'] = username
        return "User created successfully", 200
    except Exception as e:
        #print(f"Error during signup: {e}")
        return f"Error during signup: {e}", 500
    
    
@app.route('/send-otp', methods=['POST', 'GET'])
def send_otp():
    try:
        email = request.args.get('email')
        otp = random.randint(100000, 999999)
        result = send_mail(email, f"Your OTP is: {otp}", "OTP for email verification")
        if result == 1:
            r.set(email, otp, ex=300)
            session['otp'] = otp
            return "OTP sent to email", 200
        else:
            return "Error sending OTP email", 500
    except Exception as e:
        #print(f"Error during OTP sending: {e}")
        return f"Error during OTP sending: {e}", 500

    

@app.route('/confirm-otp', methods=['POST', 'GET'])
def confirm_otp():
    try:
        user_otp = request.args.get('otp')
        email = request.args.get('email')
        print("otp is: ", r.get(email))
        if str(r.get(email)) == str(user_otp):
            return "Email verified successfully", 200
        else:
            return "Invalid OTP", 400
    except Exception as e:
        #print(f"Error during OTP confirmation: {e}")
        return f"Error during OTP confirmation: {e}", 500
    

@app.route('/login', methods=['POST', 'GET'])
def login():
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        conn = connect_db()
        if conn == 404:
            return "Database connection error", 500
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password, verified FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result and check_password_hash(result[2], password):
            session['userid'] = result[0]
            session['verified'] = result[3]
            session['username'] = result[1]
            cursor.close()
            conn.close()
            return "Login successful", 200
        else:
            cursor.close()
            conn.close()
            return "Invalid credentials", 400
    except Exception as e:
        #print(f"Error during login: {e}")
        return f"Error during login: {e}", 500

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200

@app.route('/logged-in', methods=['POST', 'GET'])
def logged_in():
    if 'userid' in session:
        return jsonify({"logged_in": True, "username": session.get('username', '')})
    else:
        return jsonify({"logged_in": False})


@app.route('/agents', methods=['POST', 'GET'])
def agents():
    try:
        if 'userid' not in session or not session.get('verified', False):
            return "Unauthorized", 401
        conn = connect_db()
        if conn == 404:
            return "Database connection error", 500
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT A.id, A.name, M.name, A.prompt, M.id, A.active, A.spend, A.iptokens, A.optokens
            FROM Agents A
            LEFT JOIN Models M ON A.model = M.id
            WHERE A.userid = %s
            ''',
            (session['userid'],)
        )
        agents = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"agents": [{"id": a[0], "name": a[1], "model": a[2], "prompt": a[3], "model_id": a[4], "active": a[5], 'spend': a[6], 'ipt': a[7], 'opt': a[8]} for a in agents]}, 200
    except Exception as e:
        #print(f"Error fetching agents: {e}")
        return f"Error fetching agents: {e}", 500

@app.route('/create-agent', methods=['POST', 'GET'])
def create_agent():
    try:
        if 'userid' not in session:
            return "Unauthorized - Login.", 401
        name = request.args.get('name').lower()
        model = request.args.get('model')
        prompt = request.args.get('prompt')
        conn = connect_db()
        if conn == 404:
            return "Database connection error", 500
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Agents WHERE userid = %s AND namespace = %s", (session['userid'], name))
        count = cursor.fetchone()[0]
        if count > 0:
            return "Agent with this name already exists", 400
        conn = connect_db()
        if conn == 404:
            return "Database connection error", 500
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Agents (userid, name, model, namespace, prompt, active) VALUES (%s, %s, %s, %s, %s, TRUE)", 
                       (session['userid'], name, model, name, prompt))
        conn.commit()
        cursor.close()
        conn.close()
        host = f"https://flowt-{session['username']}-rz0q9xs.svc.aped-4627-b74a.pinecone.io"
        index = pc.Index(host=host)
        index.upsert_records(
            name,
            [
                {
                "_id": f"{name}-{random.randint(1, 1000000)}",
                "chunk_text": "sample"
                } 
            ]
        )
        return "Agent created successfully", 200
    except Exception as e:
        #print(f"Error creating agent: {e}")
        return f"Error creating agent: {e}", 500

@app.route('/edit-agent', methods=['POST', 'GET'])    
def edit_agent():
    try:
        if 'userid' not in session or not session.get('verified', False):
            return "Unauthorized", 401
        agent_id = request.args.get('id')
        new_prompt = request.args.get('prompt')
        new_model = request.args.get('model')
        conn = connect_db()
        if conn == 404:
            return "Database connection error", 500
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Agents WHERE id = %s AND userid = %s", (agent_id, session['userid']))
        result = cursor.fetchone()
        if not result:
            cursor.close()
            conn.close()
            return "Agent not found", 404
        cursor.execute("UPDATE Agents SET prompt = %s, model = %s WHERE id = %s AND userid = %s", 
                       (new_prompt, new_model, agent_id, session['userid']))
        conn.commit()
        cursor.close()
        conn.close()
        return "Agent updated successfully", 200
    except Exception as e:
        #print(f"Error editing agent: {e}")
        return f"Error editing agent: {e}", 500
    
@app.route('/agent-kb', methods=['POST', 'GET'])      # OPTIMIZE (INDEX -> NAMESPACE)
def agent_kb():
    try:
        #if 'userid' not in session or not session.get('verified', False):
            #return "Unauthorized", 401
        agent_id = request.args.get('agent_id')
        file = request.files['file']
        if not file:
            return "No file uploaded", 400
        text = file.read().decode("utf-8")
        conn = connect_db()
        if conn == 404:
            return "Database connection error", 500
        cursor = conn.cursor()
        cursor.execute("SELECT namespace FROM Agents WHERE id = %s", (agent_id,))
        result = cursor.fetchone()
        if not result:
            cursor.close()
            conn.close()
            return "Agent not found", 404
        namespace = result[0]
        cursor.close()
        conn.close()
        #data = request.get_json()
        #text = data.get('text', [])
        chunks = semantic_chunk(text)
        #print(chunks)
        host = f"https://flowt-{session['username']}-rz0q9xs.svc.aped-4627-b74a.pinecone.io"
        #print(host)
        index = pc.Index(host=host)
        index.delete(delete_all=True, namespace=namespace)
        logger.error("Index deleted")
        index.upsert_records(
            namespace,
            [
                {
                "_id": f"{namespace}-{random.randint(1, 1000000)}",
                "chunk_text": "sample"
                } 
            ]
        )
        logger.error("SINGLE INSTANCE UPLOADED.")
        index.upsert_records(
            namespace,
            [
                {
                "_id": f"{namespace}-{random.randint(1, 1000000)}",
                "chunk_text": f"{chunk}"
                } for chunk in chunks
            ]
        )
        return {"knowledge_base": f"Knowledge base for agent with Pinecone index {namespace}"}, 200
    except Exception as e:
        #print(f"Error fetching agent knowledge base: {e}")
        return f"Error fetching agent knowledge base: {e}", 500

@app.route('/delete-agent', methods=['POST', 'GET'])   
def delete_agent():
    try:
        if 'userid' not in session or not session.get('verified', False):
            return "Unauthorized", 401
        agent_id = request.args.get('id')
        conn = connect_db()
        if conn == 404:
            return "Database connection error", 500
        cursor = conn.cursor()
        cursor.execute("SELECT namespace FROM Agents WHERE id = %s AND userid = %s", (agent_id, session['userid']))
        result = cursor.fetchone()
        if not result:
            cursor.close()
            conn.close()
            return "Agent not found", 404
        namespace = result[0]
        host = f"https://flowt-{session['username']}-rz0q9xs.svc.aped-4627-b74a.pinecone.io"
        index = pc.Index(host=host)
        index.delete(delete_all=True, namespace=namespace)
        cursor.execute("DELETE FROM Agents WHERE id = %s AND userid = %s", (agent_id, session['userid']))
        conn.commit()
        cursor.close()
        conn.close()
        return "Agent deleted successfully", 200
    except Exception as e:
        logger.error(f"Error deleting agent: {e}")
        return f"Error deleting agent: {e}", 500

@app.route('/add-credit', methods=['GET','POST'])     
def add_credit():
    try:
        amt = request.args.get('credit')
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET balance = %s WHERE id = %s", (amt, session['userid'])
        )
        return "Credit added"
    except Exception as e:
        return f"Error adding credit: {e}", 500

# ADMIN SECTION

@app.route('/admin-login', methods=['POST', 'GET'])
def admin_login():
    try:
        password = request.args.get('password')
        if password == os.getenv('ADMIN_PASS'):
            session['admin'] = True
            return "Admin login successful", 200
        else:
            return "Invalid admin password", 400
    except Exception as e:
        #print(f"Error during admin login: {e}")
        return f"Error during admin login: {e}", 500

@app.route('/admin-logout', methods=['POST', 'GET'])
def admin_logout():
    session.pop('admin', None)
    return "Admin logged out successfully", 200

@app.route('/show-models', methods=['POST', 'GET'])
def show_models():
    try:
        models = r.get("models")
        logger.error(models)
        if models is not None:
            models = json.loads(models)
            logger.error(models)
            return {"models": [{"id": m[0], 
                            "name": m[1], 
                            "description": m[2], 
                            "input": m[3], 
                            "output": m[4], 
                            "logo": m[5], 
                            "link": m[6]} 
                            for m in models]
                }, 200
        conn = connect_db()
        if conn == 404:
            return "Database connection error", 500
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM models")
        models = cursor.fetchall()
        cursor.close()
        conn.close()
        r.set('models', json.dumps(models), ex=900)
        return {"models": [{"id": m[0], 
                            "name": m[1], 
                            "description": m[2], 
                            "input": m[3], 
                            "output": m[4], 
                            "logo": m[5], 
                            "link": m[6]} 
                            for m in models]
                }, 200
    except Exception as e:
        logger.error(f"Error fetching models: {e}")
        return f"Error fetching models: {e}", 500

@app.route('/add-model', methods=['POST', 'GET'])
def add_model():
    try:
        if 'admin' not in session:
            return "Unauthorized", 401
        name = request.args.get('name')
        description = request.args.get('desc')
        input_desc = float(request.args.get('input'))
        output_desc = float(request.args.get('output'))
        link = request.args.get('link')
        logo = request.args.get('logo')
        conn = connect_db()
        if conn == 404:
            return "Database connection error", 500
        cursor = conn.cursor()
        cursor.execute("INSERT INTO models (name, descrip, input, output, logo, link) VALUES (%s, %s, %s, %s, %s, %s)", 
                       (name, description, input_desc, output_desc, logo, link))
        conn.commit()
        cursor.close()
        conn.close()
        r.delete('models')
        return "Model added successfully", 200
    except Exception as e:
        #print(f"Error adding model: {e}")
        return f"Error adding model: {e}", 500

@app.route('/delete-model', methods=['POST', 'GET'])
def delete_model():
    try:
        if 'admin' not in session:
            return "Unauthorized", 401
        model_id = request.args.get('id')
        conn = connect_db()
        if conn == 404:
            return "Database connection error", 500
        cursor = conn.cursor()
        cursor.execute("""
        SELECT model 
        FROM agents 
        WHERE model != %s
        GROUP BY model 
        ORDER BY COUNT(*) DESC 
        LIMIT 1
        """, (model_id,))
        
        result = cursor.fetchone()
        cursor.execute("SELECT DISTINCT(U.email) FROM users U JOIN agents A ON U.id = A.userid WHERE A.model = %s", (model_id,))
        emails = cursor.fetchall()
        for i in emails:
            send_mail(i[0], "Due to removal of a LLM model used by one or more of your AI agents, those agents are now supported by the most used LLM on our platform.", "LLM change for your agents.")
        cursor.execute(
            '''
            UPDATE agents SET model = %s
            WHERE model = %s
            ''', (result[0], model_id)
        )
        cursor.execute("DELETE FROM models WHERE id = %s", (model_id,))
        conn.commit()
        cursor.close()
        conn.close()
        r.delete("models")
        return "Model deleted successfully", 200
    except Exception as e:
        #print(f"Error deleting model: {e}")
        return f"Error deleting model: {e}", 500

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', debug=True)
