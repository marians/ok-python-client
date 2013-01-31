ok-python-client
================

Python Client für die Offenes Köln API

## Installation

    pip install okclient

## Quickstart

    import okclient
    
    oc = okclient.Client()

    # Suche nach Dokumente mit dem Begriff "haushalt"
    result = oc.documents(query="haushalt")
    for doc in result:
        print doc.date, doc.title
    
    # Dokument mit der Kennung "3323/2008" abholen,
    # mit Attachments und Thumbnails
    result = oc.documents("3323/2008", attachments=True,
                          thumbnails=True)
    print result[0].date, result[0].title
    print result[0].attachments[0].url
    print result[0].attachments[0].content

