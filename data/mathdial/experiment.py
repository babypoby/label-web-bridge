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
    existing_ids_response = await loop.run_in_executor(None, lambda: supabase.table("bridge_copy").select("conversation_id").execute())
    return set(item['conversation_id'] for item in existing_ids_response.data)

async def insert_data(table, data):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: supabase.table(table).insert(data).execute())

def remove_specific_parentheses(text):
    return re.sub(r'\s*\((focus|generic|probing)\)\s*', '', text).strip()


async def main():
    existing_ids = await fetch_existing_ids()
    print(f"Existing IDs in bridge table: {len(existing_ids)}")

    entries_bridge_copy = []
    entries_bridge_convo_copy = []
    entries_bridge_response_copy = []
    seen_conversation_ids = set()
    count = 0

    with open('train.jsonl', 'r') as file:
        for line in file:
            data = json.loads(line)
            qid = data['qid']
            scenario = data['scenario']
            conversation_id = f"{qid}_{scenario}"
            
            if conversation_id not in existing_ids and conversation_id not in seen_conversation_ids:
                count += 1
                entries_bridge_copy.append({
                    "conversation_id": conversation_id,
                    "solution": data.get('ground_truth', '')
                })
                
                conversation = data['conversation']
                parts = conversation.split("|EOM|")
                
                teacher_parts = []
                student_seen = False
                convo_id = 0
                
                for part in parts:
                    part = part.strip()
                    if part.startswith("Teacher:"):
                        user = "tutor"
                        text = remove_specific_parentheses(part[8:].strip())
                        if not student_seen:
                            teacher_parts.append({"user": user, "text": text})
                        else:
                            entries_bridge_response_copy.append({
                                "conversation_id": conversation_id,
                                "id": 0,
                                "user": user,
                                "text": text
                            })
                            break
                    elif part.startswith("Student:"):
                        user = "student"
                        text = remove_specific_parentheses(part[8:].strip())
                        student_seen = True
                        # Add all accumulated teacher parts to convo
                        for teacher_part in teacher_parts:
                            entries_bridge_convo_copy.append({
                                "conversation_id": conversation_id,
                                "id": convo_id,
                                "user": teacher_part["user"],
                                "text": teacher_part["text"]
                            })
                            convo_id += 1
                        teacher_parts = []
                        # Add student part to convo
                        entries_bridge_convo_copy.append({
                            "conversation_id": conversation_id,
                            "id": convo_id,
                            "user": user,
                            "text": text
                        })
                        convo_id += 1
                    else:
                        continue
                
                seen_conversation_ids.add(conversation_id)

    print(f"New unique conversation IDs to be inserted: {count}")

    if entries_bridge_copy:
        try:
            response_bridge_copy = await insert_data("bridge_copy", entries_bridge_copy)
            print(f"Inserted {len(entries_bridge_copy)} new unique entries into bridge_copy table.")
            
            response_bridge_convo_copy = await insert_data("bridge_convo_copy", entries_bridge_convo_copy)
            print(f"Inserted {len(entries_bridge_convo_copy)} new entries into bridge_convo_copy table.")
            
            response_bridge_response_copy = await insert_data("bridge_response_copy", entries_bridge_response_copy)
            print(f"Inserted {len(entries_bridge_response_copy)} new entries into bridge_response_copy table.")
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
    else:
        print("No new unique entries to insert.")


if __name__ == "__main__":
    asyncio.run(main())

