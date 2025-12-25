from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib import request

ANKI_HOST = "127.0.0.1"
ANKI_PORT = "8765"
ANKI_URL = f"http://{ANKI_HOST}:{ANKI_PORT}"
PYTHON_SERVER_PORT = 8080
PYTHON_SERVER_IP = "localhost"

class FlashcardHandler(BaseHTTPRequestHandler):
    def do_post(self):
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
        req = request.Request(ANKI_URL,
                              data=json.dumps(payload).encode(),
                              headers={"Content-Type": "application/json"})
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
        req = request.Request(ANKI_URL,
                              data=json.dumps(payload).encode(),
                              headers={"Content-Type": "application/json"})
        try:
            _ = request.urlopen(req)
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
        req = request.Request(ANKI_URL,
                              data=json.dumps(payload).encode(),
                              headers={"Content-Type": "application/json"})
        try:
            response = request.urlopen(req)
            anki_codes  =json.loads(response.read())
            if anki_codes.get("error") is not None \
                and anki_codes.get("error") == "cannot create note because it is a duplicate":
                card['question'] = card['question'] + '(1)'
                self.send_to_anki(card, deck_name)
        except Exception as e:
            print(f"Anki error for deck '{deck_name}':", e)

if __name__ == "__main__":
    server = HTTPServer((PYTHON_SERVER_IP, PYTHON_SERVER_PORT), FlashcardHandler)
    print(f"Server running on http://{PYTHON_SERVER_IP}:{PYTHON_SERVER_PORT}")
    server.serve_forever()
