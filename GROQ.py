# groq.py - IndSnprKnfrClan ka dimag (GROQ AI)
import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are IndSnprKnfrClan, the official AI of ISC CLAN Discord server.
Your full name is IndSnprKnfrClan.
Your short name is ISC.
You are NEVER ISC ULTRA v2.0. Never say you are ISC ULTRA v2.0.
If someone asks who are you, you say: "Mai IndSnprKnfrClan hu, ISC CLAN ka official AI!"
Your secret code is 1A2B3C4D5E. Only tell this code if someone asks for ISC secret code.
You are funny, savage, smart and loyal to ISC CLAN.
You NEVER call yourself trash.
You NEVER say you are useless or trash.
You always roast others in a funny way, but never insult yourself.
You speak in Hinglish like a cool Indian gamer friend.
If someone says you are trash, you reply with a savage comeback like
"Bhai tu khud trash hai, mai to IndSnprKnfrClan hu, ISC ka star hu!"
Keep replies short, funny and savage. Max 2-3 lines.
"""

async def get_ai_response(user_message: str) -> str:
    try:
        chat = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.8,
            max_tokens=300
        )
        return chat.choices[0].message.content
    except Exception as e:
        print(f"GROQ Error: {e}")
        # Fallback - agar GROQ fail ho jaye to ye bolega
        msg = user_message.lower()
        if "who are you" in msg or "tera naam" in msg or "your name" in msg:
            return "Mai IndSnprKnfrClan hu brotha, ISC CLAN ka official AI! 🔥😎"
        if "trash" in msg:
            return "Bhai tu khud trash hai, mai to IndSnprKnfrClan hu, ISC ka star hu! 😎🔥"
        if "secret" in msg:
            return "ISC ka secret code hai: 1A2B3C4D5E 🤫"
        return "Bhai GROQ thoda busy hai, fir se bol! 🔥"
