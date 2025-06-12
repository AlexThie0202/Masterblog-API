import json
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First API Post about Flask",
     "content": "This is the first post from the API, discussing Flask development."},
    {"id": 2, "title": "Second API Post - Python Basics", "content": "This post covers fundamental Python concepts."},
    {"id": 3, "title": "Third API Post: Advanced Flask Features",
     "content": "Exploring advanced features of the Flask framework."},
    {"id": 4, "title": "Database Integration with Flask",
     "content": "How to connect your Flask app to various databases."},
    {"id": 5, "title": "Frontend Frameworks for your Blog",
     "content": "A look at React, Vue, and Angular for client-side rendering."},
]


# Helper function to find a post by ID
def find_post_by_id(post_id):
    for post in POSTS:
        if post['id'] == post_id:
            return post
    return None


# Helper function to generate a new unique ID
def generate_new_id():
    if POSTS:
        return max(post['id'] for post in POSTS) + 1
    return 1


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Returns a list of all blog posts, with optional sorting."""

    # Hol die Sortier-Parameter
    sort_by = request.args.get('sort')  # Kann 'title' oder 'content' sein
    direction = request.args.get('direction')  # Kann 'asc' oder 'desc' sein

    # Validierung der Sortierfelder und Richtungen
    valid_sort_fields = ['title', 'content']
    valid_directions = ['asc', 'desc']

    # Erstelle eine Kopie der Liste, um die globale POSTS-Liste nicht direkt zu ändern
    # und um Sortierung zuzulassen, ohne den Originalzustand zu verlieren (für Debugging etc.)
    # In einer echten DB-Anwendung würde die Sortierung in der Datenbankabfrage stattfinden
    sorted_posts = list(POSTS)

    if sort_by:  # Nur sortieren, wenn 'sort' Parameter vorhanden ist
        if sort_by not in valid_sort_fields:
            return jsonify({"error": f"Invalid sort field. Must be one of: {', '.join(valid_sort_fields)}"}), 400

        if direction:  # Nur prüfen, wenn 'direction' Parameter vorhanden ist
            if direction not in valid_directions:
                return jsonify({"error": f"Invalid sort direction. Must be one of: {', '.join(valid_directions)}"}), 400
        else:
            # Wenn 'sort' vorhanden ist, aber 'direction' fehlt, default zu 'asc'
            direction = 'asc'

            # Sortierlogik anwenden
        # key=lambda post: post[sort_by] definiert, wonach sortiert werden soll (z.B. post['title'])
        # reverse=True für absteigende Sortierung
        sorted_posts.sort(key=lambda post: post[sort_by], reverse=(direction == 'desc'))

    return jsonify(sorted_posts)  # Gibt die (potenziell) sortierte Liste zurück


@app.route('/api/posts', methods=['POST'])
def add_post():
    """Adds a new blog post."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    title = data.get('title')
    content = data.get('content')

    missing_fields = []
    if not title:
        missing_fields.append('title')
    if not content:
        missing_fields.append('content')

    if missing_fields:
        return jsonify({
            "error": "Missing fields",
            "required_fields": missing_fields
        }), 400

    new_id = generate_new_id()
    new_post = {
        "id": new_id,
        "title": title,
        "content": content
    }
    POSTS.append(new_post)  # Fügt zum globalen POSTS hinzu, der von get_posts verwendet wird
    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Deletes a blog post by ID."""
    global POSTS

    post_index = -1
    for i, post in enumerate(POSTS):
        if post['id'] == post_id:
            post_index = i
            break

    if post_index == -1:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404

    del POSTS[post_index]
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Updates an existing blog post by ID."""
    global POSTS

    post_to_update = None
    for post in POSTS:
        if post['id'] == post_id:
            post_to_update = post
            break

    if post_to_update is None:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404

    data = request.get_json()
    if not data:
        return jsonify(post_to_update), 200

    if 'title' in data:
        post_to_update['title'] = data['title']
    if 'content' in data:
        post_to_update['content'] = data['content']

    return jsonify(post_to_update), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """Searches for blog posts by title or content based on query parameters."""
    search_title = request.args.get('title', '').lower()
    search_content = request.args.get('content', '').lower()

    matching_posts = []
    for post in POSTS:
        post_title_lower = post['title'].lower()
        post_content_lower = post['content'].lower()

        title_match = search_title and search_title in post_title_lower
        content_match = search_content and search_content in post_content_lower

        if (search_title and title_match) or \
                (search_content and content_match):
            matching_posts.append(post)

    return jsonify(matching_posts), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)