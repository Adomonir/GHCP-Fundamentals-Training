"""MyCorp‑Auth KB — MCP server (scaffold)

You’ll use Copilot Chat to fill each `pass` by accepting its suggestion.
Read the 💡 prompt above the cursor, hit Tab or Ctrl+Enter, review, then accept.
"""

# ============================================================
# STEP 1 · Imports
# ------------------------------------------------------------
# 💡 Prompt: "Import flask and the pathlib and re modules."
import flask
import pathlib
import re
import sys

# ============================================================
# STEP 2 · Flask app
# ------------------------------------------------------------
# 💡 Prompt: "Create a Flask app named `app`."
app = flask.Flask(__name__)


# ============================================================
# STEP 3 · Discover Markdown knowledge‑base files
# ------------------------------------------------------------
# 💡 Prompt:
# "Build a DOCS list containing all *.md files under
#  the 'mycorp-auth-docs' directory."
DOCS = list(pathlib.Path("mycorp-auth-docs").rglob("*.md"))

# ============================================================
# STEP 4 · Helper: search paragraphs for a query string
# ------------------------------------------------------------
# 💡 Prompt:
# "Define a function `search(query: str, k: int = 1)` that:
#    • iterates over DOCS
#    • splits each file on blank lines
#    • matches paragraphs containing the query (case‑insensitive)
#    • returns at most k dicts with keys 'file' and 'excerpt'
#    • if no matches, return {'error': 'no match'}."
def search(query: str, k: int = 1):
    results = []
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    for doc in DOCS:
        content = doc.read_text(encoding='utf-8')
        paragraphs = re.split(r'\n\s*\n', content)
        for para in paragraphs:
            if pattern.search(para):
                results.append({'file': str(doc), 'excerpt': para.strip()})
                if len(results) >= k:
                    return results

    if not results:
        return {'error': 'no match'}
    return results

# ============================================================
# STEP 5 · HTTP endpoint
# ------------------------------------------------------------
# 💡 Prompt:
# "Create a POST endpoint '/authdoc' that extracts the 'query'
#  field from the JSON body, calls `search`, and returns the result."
@app.post("/authdoc")
def authdoc():
    data = flask.request.get_json()
    query = data.get('query', '')
    result = search(query)
    return flask.jsonify(result)

# ============================================================
# STEP 6 · Run the server
# ------------------------------------------------------------
# 💡 Prompt:
# "Run the Flask app on port 8000 when executed directly."
if __name__ == "__main__":
    # Support a simple CLI test mode so we don't spin up the server when asked.
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        matches = search("token", k=10)
        if isinstance(matches, dict):
            print("No matches found for 'token'")
            sys.exit(1)
        print(f"Found {len(matches)} documents mentioning 'token'")
        sys.exit(0)

    app.run(port=8000)