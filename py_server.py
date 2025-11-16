from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib import request

class FlashcardHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        flashcard = json.loads(post_data)

        # Ensure decks exist for all tags
        self.ensure_decks_exist(flashcard["tags"])

        # Send the flashcard to each deck
        for tag in flashcard["tags"]:
            self.send_to_anki(flashcard, deck_name=tag.strip())

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Flashcard sent to all decks")

    def ensure_decks_exist(self, tags):
        existing_decks = self.get_existing_decks()
        for tag in tags:
            deck_name = tag.strip()
            if deck_name not in existing_decks:
                self.create_deck(deck_name)

    def get_existing_decks(self):
        payload = {
            "action": "deckNames",
            "version": 6
        }
        req = request.Request("http://127.0.0.1:8765", data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
        try:
            response = request.urlopen(req)
            result = json.loads(response.read())
            return result.get("result", [])
        except Exception as e:
            print("Error fetching deck names:", e)
            return []

    def create_deck(self, deck_name):
        payload = {
            "action": "createDeck",
            "version": 6,
            "params": {
                "deck": deck_name
            }
        }
        req = request.Request("http://127.0.0.1:8765", data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
        try:
            response = request.urlopen(req)
            print(f"Created deck: {deck_name}")
        except Exception as e:
            print(f"Error creating deck '{deck_name}':", e)

    def send_to_anki(self, card, deck_name):
        payload = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": deck_name,
                    "modelName": "Basic",
                    "fields": {
                        "Front": card["question"],
                        "Back": card["answer"]
                    },
                    "tags": card["tags"]
                }
            }
        }
        print(f"Sending card to deck: {deck_name}")
        req = request.Request("http://127.0.0.1:8765", data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
        try:
            response = request.urlopen(req)
            anki_codes  =json.loads(response.read())
            if anki_codes.get("error") != None and anki_codes.get("error") == "cannot create note because it is a duplicate":
                # print(f"Anki error for deck '{deck_name}':", anki_codes.get("error"))
                # print(payload)
                card['question'] = card['question'] + '(1)' 
                self.send_to_anki(card, deck_name)
        except Exception as e:
            print(f"Anki error for deck '{deck_name}':", e)

if __name__ == "__main__":
    server = HTTPServer(("localhost", 8080), FlashcardHandler)
    print("Server running on http://localhost:8080")
    server.serve_forever()