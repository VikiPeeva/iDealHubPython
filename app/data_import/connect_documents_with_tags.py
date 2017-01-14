from app.database.neo4j_base_service import get_documents_from_database
from app.analyzers.similar_documents import similar_documents_to_document
from app.database.database import database


def connect_documents_with_tags():
    documents = get_documents_from_database()  # Take all documents from database

    counter = 0

    # For every document find five similar documents and add their titles as document tags
    for document in documents:
        similar_documents = similar_documents_to_document(document.title, 5)
        tags = []

        for similar in similar_documents:
            tags.append(similar["title"])

        # For every document create relationship in the database
        # between the document and the tags that we have initialized in the list

        database.open_connection()

        query = "MATCH (doc:Document)" \
                "WHERE ID(doc) = {doc_id} " \
                "WITH doc " \
                "MATCH "
        parameters = {"doc_id": document.id}
        index = 0
        for tag in tags:
            index += 1
            query += "(tag" + str(index) + ":Tag {value: {tag" + str(index) + "}})"
            parameters["tag" + str(index)] = tag
            if index < len(tags):
                query += ", "
            else:
                query += " "

        query += "CREATE "
        index = 0
        for tag in tags:
            index += 1
            query += "(doc)-[:TAG]->(tag" + str(index) + ")"
            if index < len(tags):
                query += ", "

        counter += 1
        print(counter)

        database.query(query, parameters)

    database.close_connection()