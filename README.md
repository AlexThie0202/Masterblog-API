# Masterblog API - RESTful Blog System mit Flask

Dieses Projekt implementiert eine RESTful API für ein einfaches Blog-System mit Flask. Es ermöglicht die Verwaltung von Blog-Posts (CRUD-Operationen) und bietet zusätzliche Funktionen wie Suchen und Sortieren. Die Daten werden derzeit in einer hartkodierten Python-Liste gehalten (für Demonstrationszwecke), die bei jedem Neustart der Anwendung zurückgesetzt wird.

## Funktionen der API

* **POSTS abrufen (Liste):** `GET /api/posts`
    * Optionale Query-Parameter:
        * `sort`: Sortiert nach `'title'` oder `'content'`.
        * `direction`: Sortierrichtung `'asc'` (aufsteigend) oder `'desc'` (absteigend).
        * Beispiel: `/api/posts?sort=title&direction=desc`
* **Neuen POST hinzufügen:** `POST /api/posts`
    * Erwartet JSON im Body: `{"title": "...", "content": "..."}`
    * Gibt den neu erstellten Post mit generierter ID zurück (Status 201 Created).
* **POST löschen:** `DELETE /api/posts/<id>`
    * Löscht den Post mit der angegebenen ID.
    * Gibt Erfolgsmeldung zurück (Status 200 OK).
* **POST aktualisieren:** `PUT /api/posts/<id>`
    * Erwartet JSON im Body: `{"title": "...", "content": "..."}` (beide Felder optional).
    * Aktualisiert den Post mit der angegebenen ID.
    * Gibt den aktualisierten Post zurück (Status 200 OK).
* **POSTS suchen:** `GET /api/posts/search`
    * Optionale Query-Parameter:
        * `title`: Suchbegriff für den Titel.
        * `content`: Suchbegriff für den Inhalt.
    * Sucht Posts, deren Titel ODER Inhalt den Suchbegriff enthalten (case-insensitive).
    * Beispiel: `/api/posts/search?title=flask&content=python`

## Technologien

* **Backend:** Python 3, Flask, Flask-CORS
* **Datenhaltung:** In-memory Liste (für diese Übung)

## Einrichtung und Ausführung (Lokale Entwicklung)

Befolge diese Schritte, um das Projekt lokal auf Ihrem System einzurichten und auszuführen:

### 1. Repository klonen

```bash
git clone [https://github.com/DeinGitHubNutzername/Masterblog.git](https://github.com/DeinGitHubNutzername/Masterblog.git)
cd Masterblog
