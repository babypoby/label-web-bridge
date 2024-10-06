import os
import json
import asyncio
import re
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)

async def fetch_existing_ids():
    loop = asyncio.get_event_loop()
    existing_ids_response = await loop.run_in_executor(None, lambda: supabase.table("bridge").select("conversation_id").execute())
    return set(item['conversation_id'] for item in existing_ids_response.data)

async def insert_data(table, data):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: supabase.table(table).insert(data).execute())

def remove_text_in_parentheses(text):
    return re.sub(r'\([^)]*\)', '', text).strip()

async def main():
    existing_ids = await fetch_existing_ids()
    print(f"Existing IDs in bridge table: {len(existing_ids)}")

    entries_bridge = []
    entries_bridge_convo = []
    entries_bridge_response = []
    seen_conversation_ids = set()
    count = 0

    with open('test.jsonl', 'r') as file:
        for line in file:
            data = json.loads(line)
            qid = data['qid']
            scenario = data['scenario']
            conversation_id = f"{qid}_{scenario}"
            
            if conversation_id not in existing_ids and conversation_id not in seen_conversation_ids:
                count += 1
                entries_bridge.append({
                    "conversation_id": conversation_id,
                    "solution": data.get('ground_truth', '')  # Add the ground_truth as solution
                })
                
                conversation = data['conversation']
                parts = conversation.split("|EOM|")
                for i, part in enumerate(parts[:3]):  # Only consider the first three parts (0, 1, 2)
                    part = part.strip()
                    if part.startswith("Teacher:"):
                        user = "tutor"
                        text = remove_text_in_parentheses(part[8:].strip())
                    elif part.startswith("Student:"):
                        user = "student"
                        text = remove_text_in_parentheses(part[8:].strip())
                    else:
                        continue
                    
                    if i < 2:
                        entries_bridge_convo.append({
                            "conversation_id": conversation_id,
                            "id": i,
                            "user": user,
                            "text": text
                        })
                    else:  # i == 2
                        entries_bridge_response.append({
                            "conversation_id": conversation_id,
                            "id": i,
                            "user": user,
                            "text": text
                        })
                
                seen_conversation_ids.add(conversation_id)

    print(f"New unique conversation IDs to be inserted: {count}")

    if entries_bridge:
        try:
            response_bridge = await insert_data("bridge", entries_bridge)
            print(f"Inserted {len(entries_bridge)} new unique entries into bridge table.")
            
            response_bridge_convo = await insert_data("bridge_convo", entries_bridge_convo)
            print(f"Inserted {len(entries_bridge_convo)} new entries into bridge_convo table.")
            
            response_bridge_response = await insert_data("bridge_response", entries_bridge_response)
            print(f"Inserted {len(entries_bridge_response)} new entries into bridge_response table.")
            
            # Verification steps would go here, similar to the synchronous version
        except Exception as e:
            print(f"An error occurred: {str(e)}")
    else:
        print("No new unique entries to insert.")

if __name__ == "__main__":
    asyncio.run(main())

